import sys
import json
import requests

from bs4 import BeautifulSoup

playerNewsArray = []
newsObject = {}
# Grab player web page, grab the html, crab the divs from that html, and
# Grab the recent news about the player from that div.
playerHTML = requests.get('http://www.rotoworld.com/recent/nfl/11292/thomas-duarte')
htmlData = playerHTML.text
divData = [div for div in BeautifulSoup(htmlData)("div")]
for div in divData:
    divClass = div.get('class');
    if ( divClass ):
        if ( divClass[0] == 'report' ):
            newsObject['report'] = div.text
        if ( divClass[0] == 'impact' ):
            newsObject['impact'] = div.text.lstrip()
        if ( divClass[0] == 'date' ):
            newsObject['date'] = div.text
            playerNewsArray.append( newsObject )
            newsObject = {}

for news in playerNewsArray:
    print "Report:" + news['report']
    print "Impact:\n" + news['impact']
    print "Date:\n" + news['date'] + "\n\n"
