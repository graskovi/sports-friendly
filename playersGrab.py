import sys
import json
import requests

from bs4 import BeautifulSoup
from twill.commands import *

teamIdArray = ['buf', 'mia', 'ne', 'nyj', 'bal', 'cin', 'cle', 'pit',
               'hou', 'ind', 'jac', 'ten', 'den', 'kc', 'lac', 'oak',
               'dal', 'nyg', 'phi', 'was', 'chi', 'det', 'gb', 'min',
               'atl', 'car', 'no', 'tb', 'arz', 'lar', 'sea', 'sf']

# Grab player web page, grab the html, crab the divs from that html, and
# Grab the recent news about the player from that div.
def grabAllPlayers():
    playerList = [] # list of all players
    # For eah team, grab the roster
    for ID in teamIdArray:

        teamHTML = requests.get('http://www.rotoworld.com/teams/rosters/nfl/' + ID)
        htmlData = teamHTML.text

        # Grab the team name, may or may not be important
        divData = [div for div in BeautifulSoup(htmlData)("div")]
        for div in divData:
            divClass = div.get('class');
            if ( divClass ):
                if ( divClass[0] == 'teamname' ):
                    print (div.find_all('h1')[0].text)

        # Grab the roster table for each team, then look at each player
        # and grab their recent news
        tableData = [table for table in BeautifulSoup(htmlData)("table")]
        for table in tableData:
            tableClass = table.get('class');
            if ( tableClass ):
                if ( tableClass[0] == 'statstable' ):
                    for row in table.find_all('tr'):
                        for column in row.find_all('td'):
                            player = {}
                            if (column.a):
                                player['playerLink'] = column.a['href'].split('player')[1]
                                player['playerName'] = column.text
                                player['news'] = grabNewsForPlayer( player['playerLink'] )
                                playerList.append( player )
                                print ( player['playerName'] + " done" )
                                print ( player['playerLink'] )


def grabNewsForPlayer( playerLink ):
    playerNewsArray = []
    newsObject = {}
    # Grab player web page, grab the html, crab the divs from that html, and
    # Grab the recent news about the player from that div.
    playerHTML = requests.get('http://www.rotoworld.com/recent/' + playerLink)
    go( 'http://www.rotoworld.com/recent/' + playerLink )
    showforms()
    htmlData = playerHTML.text
    divData = [div for div in BeautifulSoup(htmlData)("div")]
    for div in divData:
        divClass = div.get('class');
        if (divClass):
            if ( "pb" == divClass[0] ):
                for child in div.find_all('div'):
                    childClass = child.get('class');
                    if ( childClass ):
                        if ( childClass[0] == 'report' ):
                            newsObject['report'] = child.text
                        if ( childClass[0] == 'impact' ):
                            newsObject['impact'] = child.text.lstrip().rstrip()
                        if ( childClass[0] == 'date' ):
                            newsObject['date'] = child.text
                            playerNewsArray.append( newsObject )
                            newsObject = {}

    return playerNewsArray

grabAllPlayers()
