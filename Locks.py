import requests
from bs4 import BeautifulSoup

dictteams = {}
valueadded = {}

class Team:
    name = ""
    offEff = 0.0
    defEff = 0.0
    pace = 0.0

class Matchup:
    home = ""
    away = ""
    spread = 0.0
    total = 0.0

class Result:
    m = Matchup()
    homeS = 0.0
    awayS = 0.0
    def picker(self):
        team = ""
        spr = ""
        if (self.awayS - self.homeS < self.m.spread):
            team = self.m.home
            spr = spreadDisplay(self.m.spread)
        else:
            team = self.m.away
            spr = spreadDisplay(self.m.spread * -1)
        
        print("Pick: " + team + "(" + spr + ") Value: " + str(round(abs(self.m.spread - (self.awayS - self.homeS)))))

    def totalPicker(self):
        direction = ""
        if (self.awayS + self.homeS > self.m.total):
            direction = "Over"
        else:
            direction = "Under"
        print("Pick: " + direction + " | Value: " + str(round(abs(self.m.total - (self.homeS + self.awayS)))))

def spreadDisplay(spread):
    word = ""
    if (float(spread) > 0.0):
        word = "+" + str(spread)
        return word
    else:
        return str(spread)

def getOff():
    base_url = 'http://www.espn.com/nba/hollinger/teamstats'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    teams = []
    offs = []
    
    for x in soup.find_all("td",{"align":"left"}):
        teams.append(x.text)
    
    for x in soup.find_all("td",{"class":"sortcell"}):
        offs.append(x.text)

    for x in range(30):
        idx = 3 + (x * 2)
        newteam = Team()
        newteam.name = teams[idx]
        newteam.offEff = float(offs[x])
        dictteams[teams[idx]] = newteam

    return

def getDef():
    base_url = 'http://www.espn.com/nba/hollinger/teamstats/_/sort/defensiveEff/order/false'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    teams = []
    defs = []
    
    for x in soup.find_all("td",{"align":"left"}):
        teams.append(x.text)
    
    for x in soup.find_all("td",{"class":"sortcell"}):
        defs.append(x.text)
    
    for x in range(30):
        idx = 3 + (x * 2)
        dictteams[teams[idx]].defEff = float(defs[x])
    
    return

def getPace():
    base_url = 'http://www.espn.com/nba/hollinger/teamstats/_/sort/paceFactor/order/true'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    teams = []
    paces = []
    
    for x in soup.find_all("td",{"align":"left"}):
        teams.append(x.text)

    for x in soup.find_all("td",{"class":"sortcell"}):
        paces.append(x.text)
    
    for x in range(30):
        idx = 3 + (x * 2)
        dictteams[teams[idx]].pace = float(paces[x])

    return

def getAverage():
    averages = []
    count = 0.0
    sumOff = 0.0
    sumPace = 0.0
    for key in dictteams:
        count += 1
        sumOff += dictteams[key].offEff
        sumPace += dictteams[key].pace
    averages.append(sumOff/count)
    averages.append(sumPace/count)
    return averages

def getVA():
    base_url = 'http://insider.espn.com/nba/hollinger/statistics/_/sort/VORP'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')

    players = []
    players2 = []
    vas = []
    

    for x in soup.find_all("td",{"align":"left"}):
        players.append(x.text)
    
    players.pop(0)
    players.pop(0)

    index = 0
    while index < len(players):
        players.pop(index)
        index += 1

    for x in players:
        name = x.split(", ")
        if (name[0] != "PLAYER"):
            players2.append(name[0])

    for x in soup.find_all("td",{"class":"sortcell"}):
        vas.append(x.text)

    for x in range(50):
        valueadded[players2[x]] = vas[x]

    return

def getVA2():
    base_url = 'http://insider.espn.com/nba/hollinger/statistics/_/sort/VORP/page/2'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    players = []
    players2 = []
    vas = []
    
    
    for x in soup.find_all("td",{"align":"left"}):
        players.append(x.text)

    players.pop(0)
    players.pop(0)

    index = 0
    while index < len(players):
        players.pop(index)
        index += 1

    for x in players:
        name = x.split(", ")
        if (name[0] != "PLAYER"):
            players2.append(name[0])
    
    for x in soup.find_all("td",{"class":"sortcell"}):
        vas.append(x.text)
    
    for x in range(50):
        valueadded[players2[x]] = vas[x]
    
    return

def getVA3():
    base_url = 'http://insider.espn.com/nba/hollinger/statistics/_/sort/VORP/page/3'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    players = []
    players2 = []
    vas = []
    
    
    for x in soup.find_all("td",{"align":"left"}):
        players.append(x.text)
    
    players.pop(0)
    players.pop(0)

    index = 0
    while index < len(players):
        players.pop(index)
        index += 1

    for x in players:
        name = x.split(", ")
        if (name[0] != "PLAYER"):
            players2.append(name[0])
    
    for x in soup.find_all("td",{"class":"sortcell"}):
        vas.append(x.text)
    
    for x in range(50):
        valueadded[players2[x]] = vas[x]
    
    return

def getAllStats():
    getOff()
    getDef()
    getPace()
    getVA()
    getVA2()
    getVA3()

def getNumGames():
    base_url = 'https://sports.yahoo.com/nba/scoreboard/'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    games = []
    for x in soup.find_all("span",{"data-tst":"first-name"}):
        games.append(x.text)

    return int(len(games)/2)


def getGames():
    base_url = 'http://stats.denverpost.com/odds/nba.aspx'
    r = requests.get(base_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    teams1 = []
    teams2 = []
    spreads1 = []
    spreads2 = []
    totals1 = []
    totals2 = []
    slate = []
    
#get all the teams
    for x in soup.find_all("td",{"align":"center"}):
        teams1.append(x.text)
    teams1.pop(0)
#enter number of games in range
    numGames = getNumGames()
    for x in range(numGames):
        idx = 1 + (x * 4)
        teams2.append(teams1[idx])
    
#    for x in teams2:
#        print(x)

#get all the spreads
    for x in soup.find_all("td",{"bgcolor":"#FFFFFF"}):
            spreads1.append(x.text)

#    for x in spreads1:
#        print(x)

    badwords = []
    badwords.append("Opening")
    badwords.append("5Dimes")
    badwords.append("Westgate")
    badwords.append("Wynn")
    badwords.append("Boyd")
    badwords.append("Covers.com")
    badwords.append("Best")
    badwords.append("Most")

    index = 0
    while index < len(spreads1):
        words = spreads1[index].split()
        if(words[0] == "OFF"):
            spreads1.pop(index)
            index += 1
        elif(words[0] in badwords):
            spreads1.pop(index)
            index -= 1
        index += 1

#    for x in range(len(spreads1)):
#        words = spreads1[idx].split()
#        if(words[0] == "OFF"):
#            x += 1
#        spreads2.append(words[0])

    for x in range(numGames):
        idx = x * 12
        words = spreads1[idx].split()
        spreads2.append(words[0])

#    for x in spreads1:
#        print(x)

#get all the totals
    for x in soup.find_all("td",{"class":"sdi-datacell"}):
        totals1.append(x.text)

#    for x in range(14):
#        totals1.pop(0)

    index = 0
    while index < len(totals1):
        words = totals1[index].split()
        if(words[0] in badwords):
            totals1.pop(index)
            index -= 1
        index += 1

    for x in range(numGames):
        idx = 3 + (x * 9)
        words = totals1[idx].split()
        totals2.append(words[0])

#    for x in totals1:
#        print(x)

    for x in range(numGames):
        if ("at" in teams2[x]):
            words = teams2[x].split("  at ")
        else:
            words = teams2[x].split("  vs ")
        m = Matchup()
        m.away = words[0].replace(".", "")
        m.home = words[1].replace(".", "")
        if (spreads2[x] == "OFF"):
            m.spread = spreads2[x]
            m.total = totals2[x]
        else:
            m.spread = float(spreads2[x])
            m.total = float(totals2[x])
        slate.append(m)

    return slate

def testScrape():
    slate = getGames()
    getAllStats()
    for key,value in dictteams.items():
        print(value.name, value.offEff, value.defEff, value.pace)
    for key, value in valueadded.items():
        print(key, value)
    for x in slate:
        print(x.away, x.home, x.spread, x.total)
    return

def algo():
    getAllStats()
    slate = getGames()
    averages = getAverage()
    calcs = []

    for x in slate:
        awayOff = dictteams[x.away].offEff - (0.014 * dictteams[x.away].offEff)
        awayDef = dictteams[x.away].defEff + (0.014 * dictteams[x.away].defEff)
        homeOff = dictteams[x.home].offEff + (0.014 * dictteams[x.home].offEff)
        homeDef = dictteams[x.home].defEff - (0.014 * dictteams[x.home].defEff)
        offAvg = averages[0]
        
        awayPace = dictteams[x.away].pace
        homePace = dictteams[x.home].pace
        paceAvg = averages[1]
        adjPace = awayPace * homePace / paceAvg
        
        awayScore = (awayOff * homeDef / offAvg) * (adjPace/100)
        homeScore = (homeOff * awayDef / offAvg) * (adjPace/100)

        r = Result()
        r.m = x
        r.homeS = homeScore
        r.awayS = awayScore
        calcs.append(r)
        
    print(" ")
    print("---------------------TODAY'S GAMES---------------------")
    print(" ")
    
    for x in calcs:
        if(x.m.spread == "OFF"):
            print(x.m.away + " @ " + x.m.home + " (Spread TBD)")
        else:
            print(x.m.away + " @ " + x.m.home + "(" + spreadDisplay(x.m.spread) + ")" + " - O/U " + str(x.m.total))
        print("Model predicts final score of " + str(int(x.awayS)) + " - " + str(int(x.homeS)))
#        print("Predicted Spread: " + x.m.home + "(" + spreadDisplay(round((x.awayS - x.homeS)*2)/2))
        print("Predicted Total: " + str(round((x.homeS + x.awayS)*2)/2))
        if(x.m.spread != "OFF"):
#            x.picker()
            x.totalPicker()
        print

    return

algo()






