from flask import Flask, flash, redirect, render_template, request, session, abort
import os
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

def getSpotifyTop10():
    countries = { 'United States':'us',
                  'United Kingdom':'gb',
                  'Argentina':'ar',
                  'Austria':'at',
                  'Australia':'au',
                  'Belgium':'be',
                  'Bulgaria':'bg',
                  'Bolivia':'bo',
                  'Brazil':'br',
                  'Canada':'ca',
                  'Switzerland':'ch',
                  'Chile':'cl',
                  'Colombia':'co',
                  'Costa Rica':'cr',
                  'Czech Republic':'cz',
                  'Germany':'de',
                  'Denmark':'dk',
                  'Dominican Republic':'do',
                  'Ecuador':'ec',
                  'Estonia':'ee',
                  'Spain':'es',
                  'Finland':'fi',
                  'France':'fr',
                  'Greece':'gr',
                  'Guatemala':'gt',
                  'Honduras':'hn',
                  'Hungary':'hu',
                  'Indonesia':'id',
                  'Ireland':'ie',
                  'Israel':'il',
                  'Iceland':'is',
                  'Italy':'it',
                  'Japan':'jp',
                  'Lithuania':'lt',
                  'Luxembourg':'lu',
                  'Latvia':'lv',
                  'Malta':'mt',
                  'Mexico':'mx',
                  'Malaysia':'my',
                  'Nicaragua':'ni',
                  'Netherlands':'nl',
                  'Norway':'no',
                  'New Zealand':'nz',
                  'Panama':'pa',
                  'Peru':'pe',
                  'Philippines':'ph',
                  'Poland':'pl',
                  'Portugal':'pt',
                  'Paraguay':'py',
                  'Romania':'ro',
                  'Sweeden':'se',
                  'Singapore':'sg',
                  'Slovakia':'sk',
                  'El Salvador':'sv',
                  'Thailand':'th',
                  'Turkey':'tr',
                  'Taiwan':'tw',
                  'Uruguay':'uy',
                  'Vietnam':'vn'
                  }

    top10 = {}
    for country in countries:
        target_url = 'https://spotifycharts.com/regional/' + countries.get(country) + '/daily/latest'

        # requesting html
        req = Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        page_html = urlopen(req).read()
        urlopen(req).close()
        page_soup = soup(page_html, 'html.parser')

        items = {}
        rows = page_soup.findAll('tr')  # table rows containing artists and stream count.
        for row in rows[1:51]:            # skip row[0] because it does not contain useful data.
            artist = row.find('span').find(text=True).replace('by ', '') # artist name.
            streams = int(row.find('td', {'class':'chart-table-streams'}).find(text=True).replace(',', '')) # song's stream count.
            # associate each artist with the sum of all their song's streams.
            if artist in items:
                items[artist] += streams
            else:
                items[artist] = streams
        # sort by total number of streams.
        top10_by_country = sorted(items, key=items.get, reverse=True)
        top10_by_country = top10_by_country[:10]  # top 10 artists are the first 10 keys of the sorted dict.
        top10[country] = top10_by_country # append to top10 list where the elements are the country
    return top10                          # and its corresponding top 10.


@app.route("/")
def index():
    top10 = getSpotifyTop10()
    return render_template('index.html', top10 = top10)

if __name__ == "__main__":
    app.run()
