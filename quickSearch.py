import os, csv, re
from pattern.en import parse
from PyDictionary import PyDictionary
from time import sleep
import sys

statements = []
containsTerm = []

searchTerm = raw_input("Search Term: ")

def loadCSV(filename):
	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter=";")
		if ".DS_Store" not in filename:
			# print filename
			for row in reader:
				if len(row) > 4:
					# print row[4]
					if row[4] not in statements:
						statements.append(row[4])
				else:
					print row[0]

def loadTextFile(filename):
	with open(filename, "rb") as f:
		if ".DS_Store" not in filename:
			text = f.readlines()
			for t in text:
				# t = t.encode('utf-8')
				if t not in statements:
					statements.append(t)

tweetFiles = os.listdir('../Trump Tweets/')
for t in tweetFiles:
	print t
	loadCSV('../Trump Tweets/' + t) #tweets

#collecting interviews
# interviews = os.listdir('../Interviews/')
# for iv in interviews:
# 	print iv
# 	loadTextFile('../Interviews/' + iv)

# speeches = os.listdir('../Speeches/')
# for s in speeches:
# 	loadTextFile('../Speeches/' + s)

for s in statements:
	slower = s.lower()
	if searchTerm in slower and s not in containsTerm:
		containsTerm.append(s)

for c in containsTerm:
	print c
