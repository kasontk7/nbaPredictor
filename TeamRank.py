import requests
from bs4 import BeautifulSoup

class Matchup:
	home = ""
	away = ""
	spread = ""

class Pick:
	game = Matchup()
	projected = 0
	projection = ""
	value = 0
	home = 0

def getRanks():
	base_url = 'https://www.teamrankings.com/nba/ranking/last-5-games-by-other'
	r = requests.get(base_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	ranks = soup.find_all("td",{"class":"nowrap"})
	rates = soup.find_all("td",{"class":"text-right"})
	# for x in range(4):
	# 	del rates[0]
	
	teams = []
	ratings = []

	for thing in ranks:
			teams.append(thing["data-sort"])

	for x in range(30):
		idx = x * 4
		a = round(float(rates[idx]["data-sort"]) - 500,3)
		ratings.append(a)

	dictteams = {}
	
	for i in range(30):
		dictteams[teams[i]] = ratings[i]

	return (dictteams)

def getGames():
	base_url = 'https://www.docsports.com/nba-odds.html'
	r = requests.get(base_url)
	soup = BeautifulSoup(r.text, 'html.parser')
	teams = soup.find_all("td",{"class":"teams"})
	spreads = soup.find_all("td",{"class":"lines_c4"})

	for x in range(len(teams) // 2):
		del teams[0]
	for x in range(len(spreads) // 2):
		spreads.pop()
	t = []
	s = []

	for thing in teams:
		for br in thing.find_all("br"):
   			br.replace_with("\n")
		t.append(thing.text)

	for num in range(len(teams)):
		for br in spreads[num * 6].find_all("br"):
   			br.replace_with("\n")
		s.append(spreads[num * 6].text)

	slate = []

	for x in range(len(teams)):
		m = Matchup()
		a = t[x].split('\n')
		m.away = a[0]
		m.home = a[1]

		okc = "Okla City"
#
#        if m.away == "Oklahoma City":
#            m.away = okc
#        elif m.home == "Oklahoma City":
#            m.home = okc

		b = s[x].split('\n')
		c = b[2]

		while (not c.endswith('-') and not c.endswith('+')):
			c = c[:-1]
		c = c[:-1]
        print(c)
#        m.spread = float(c)
		slate.append(m)

	return slate

def printLines():
	a = getRanks()
	b = getGames()
	for x in a:
		print (x + ": " + str(a[x]) + "\n")
	for y in b:
		print (y.away + " @ " + y.home + ", " + str(y.spread) + "\n")

def algo():
	model = []
	rankings = getRanks()
	slate = getGames()
	for matchup in slate:
		if(rankings[matchup.home] > rankings[matchup.away]):
			projected = rankings[matchup.home]/2 - rankings[matchup.away]/2 + 3.2
			#matchup spread is typically negative here
			value = projected + matchup.spread
			if (value > 3):
				p = Pick()
				p.game = matchup
				p.home = 1
				p.projected = projected
				p.projection = p.game.home + " is projected to win by " + str(projected)
				p.value = value
				model.append(p)
			elif (value < -3):
				p = Pick()
				p.game = matchup
				p.home = 0
				p.projected = projected
				p.projection = p.game.home + " is projected to win by " + str(projected)
				p.value = abs(value)
				model.append(p)

		elif(rankings[matchup.away] > rankings[matchup.home]):
			projected = rankings[matchup.away]/2 - rankings[matchup.home]/2 - 3.2
			value = projected - matchup.spread
			if (value > 3):
				p = Pick()
				p.game = matchup
				p.home = 0
				p.projected = projected
				if (projected > 0):
					p.projection = p.game.home + " is projected to win by " + str(projected)
				else:
					p.projection = p.game.away + " is projected to win by " + str(abs(projected))
				p.value = value
				model.append(p)
			elif (value < -3):
				p = Pick()
				p.game = matchup
				p.home = 1
				p.projected = projected
				if (projected > 0):
					p.projection = p.game.home + " is projected to win by " + str(projected)
				else:
					p.projection = p.game.away + " is projected to win by " + str(abs(projected))
				p.value = abs(value)
				model.append(p)

	for a in model:
		print('\n')
		print(a.game.away + " @ " + a.game.home + ", " + str(a.game.spread))
		print(a.projection + ", Value: " + str(a.value))
		if (a.home):
			print("PICK: " + a.game.home + " " + str(a.game.spread))
		else:
			print("PICK: " + a.game.away + " " + str(a.game.spread*-1))
		print('\n')

algo()

# def spread(lst):

# 	for matchup in lst:


# 		string = matchup[0].split('@')

# 		BPI = getBPI()

# 		spread = matchup[1]
	
# 		away = string[0]
# 		home = string[1]
	
# 		line = (home + ' ' + spread)

# 		if home in BPI:
# 			if away in BPI:

# 				if (BPI[home] > BPI[away]):
# 					if ((BPI[home] - BPI[away]) >= 7.0):
# 						spread = (abs((BPI[home] - BPI[away]) + 2.5))
# 						spread = round(spread, 2)
# 						spread = (home + ' ' + '-' + str(spread))
# 					else:
# 						spread = (abs((BPI[home] - BPI[away]) * 1.25 + 3.0))
# 						spread = round(spread, 2)
# 						spread = (home + ' ' + '-' + str(spread))

# 				elif (BPI[away] > BPI[home]):
# 					if ((BPI[away] - BPI[home]) >= 7.0):
# 						spread = (abs((BPI[away] - BPI[home]) - 2.5))
# 						spread = round(spread, 2)
# 						spread = (home + ' ' + '+' + str(spread))
# 					else:
# 						spread = (abs((BPI[away] - BPI[home]) * 1.25 - 3.0))
# 						spread = round(spread, 2)
# 						spread = (home + ' ' + '+' + str(spread))
				

# 		newfile.write('{},{},{},{}\n'.format(away,home,line,spread))

# 		print (spread)


# lst = [ ('Chicago@Los Angeles Lakers', '-5.5')]
# 		#('Cleveland@Detroit', '+2.5'),
# 		#('Minnesota@Charlotte', '-2.5'),
# 		#('Indiana@Orlando', '-3.0'),
# 		#('Los Angeles Clippers@New York', '+1.0'),
# 		#('Portland@Memphis', '+2.0'),
# 		#('Washington@Milwaukee', '-4.5'),
# 		#('Oklahoma City@New Orleans', '+3.0'),
# 		#('Atlanta@San Antonio', '-9.5'),
# 		#('Boston@Dallas', '+6.5'),
# 		#('Denver@Sacramento', '+6.5')]

# print (spread(lst))
