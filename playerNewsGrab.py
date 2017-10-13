import sys
import json
import requests

from bs4 import BeautifulSoup

playerNewsArray = []
newsObject = {}

# Grab player web page
print "Remember to include the http portions of the webpage URL"
playerURL = raw_input("Type or copy/paste rotoworld URL of player here: ")
# Deprecated URL of player due to hardcoding, bad practice, keeping comment as note of acceptable URL
#playerHTML = requests.get('http://www.rotoworld.com/recent/nfl/11292/thomas-duarte')
playerHTML = requests.get(playerURL)

# Grab text from player if URL from user was valid
htmlData = playerHTML.text

# Grab the HTML div sections from the webpage
divData = [div for div in BeautifulSoup(htmlData)("div")]

# Collect recent news about the player from each div
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

# Iterate through player statistics and print relevant info
for news in playerNewsArray:
    print "Report:" + news['report']
    print "Impact:\n" + news['impact']
    print "Date:\n" + news['date'] + "\n\n"
