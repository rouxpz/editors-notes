# -*- coding: utf-8 -*-

import os, csv, re
from pattern.en import parse
from PyDictionary import PyDictionary
from time import sleep
import sys

dictionary = PyDictionary()

constitution = []
amendmentWords = []
amendments = []
titles = []
amendmentDict = {}
statements = [[], [], [], [], []] #tweets, executive orders, press briefings
posList = ['NN', 'JJ']
exclude = ['i', 'is', 'be', 'am', 'are']
# keyWords = ['guns', 'fake', 'news', 'troops', 'uniform', 'illegal', 'undocumented', 'police']

punctuation = ['.', ',', '-', '!', '?', ';', ':', '"']

with open('amendments.txt', 'rb') as f:
	fullfile = f.read()
	am = fullfile.split('\n\n\n')
	for line in am:
		amendments.append(line)

cwd = os.getcwd()
# print len(amendments)

for a in amendments:
	atitle = a.split('\n')[0]
	# print atitle
	amendmentDict[atitle] = []
	amendmentWords.append([atitle])

def loadCSV(filename, type):
	with open(filename, 'rb') as f:
		reader = csv.reader(f, delimiter=";")
		if ".DS_Store" not in filename:
			# print filename
			for row in reader:
				if len(row) > 4:
					# print row[4]
					if row[4] not in statements[type]:
						statements[type].append(row[4])
				else:
					print row[0]

def loadTextFile(filename, type):
	with open(filename, "rb") as f:
		if ".DS_Store" not in filename:
			text = f.readlines()
			for t in text:
				# t = t.encode('utf-8')
				if t not in statements[type]:
					statements[type].append(t)

def adjustments(list):
	# try:
	multiple = 0
	for realL in list:
		sys.stdout.write("Searching word adjustments for phrase " + str(list.index(realL) + 1) + " of " + str(len(list)))
		sys.stdout.flush()
		sys.stdout.write('\r')

		l = realL.lower()
		l = l.strip()
		l = l.replace('(', '\(')
		l = l.replace(')', '\)')
		for p in punctuation:
			l = l.replace(p, '')

		for am in amendmentWords:
			atitle = am[0]
			for aw in am:
				if aw in l:
					awparsed = parse(aw).split('/')

					for pos in posList:
						if pos in awparsed[1] and multiple >= 4:
							if realL not in amendmentDict[atitle]:
								amendmentDict[atitle].append(realL)
						elif pos in awparsed[1] and multiple < 4:
							multiple += 1

		# print l


#collecting tweets
tweetFiles = os.listdir('../Trump Tweets/')
for t in tweetFiles:
	loadCSV('../Trump Tweets/' + t, 0) #tweets

#collecting EOs
orders = os.listdir('../EOs/')
for o in orders:
	loadTextFile('../EOs/' + o, 1)

# print len(statements[1])

#collecting memoranda
memoranda = os.listdir('../Memoranda/')
for m in memoranda:
	loadTextFile('../Memoranda/' + m, 2)

#collecting speeches
speeches = os.listdir('../Speeches/')
for s in speeches:
	loadTextFile('../Speeches/' + s, 3)

#collecting interviews
interviews = os.listdir('../Interviews/')
for iv in interviews:
	loadTextFile('../Interviews/' + iv, 4)

# print "Looking up synonyms"
# amendmentSynonyms()

for i in range(0, 1):
	with open(cwd + '/amendment' + str(i) + "synonyms.txt", "rb") as f:
		fullfile = f.read().split('\n')
		for line in fullfile:
		# for line in fullfile:
			amendmentWords[i].append(line)
		f.close()

print amendmentWords


#phraseMatch(statements[0], 3)
print "TWEETS"
print "----------"
adjustments(statements[0])
print "Tweets organized!"

print "EO"
print "----------"
adjustments(statements[1])
print "Executive Orders organized!"

print "MEMOS & PROCLAMATIONS"
print "----------"
adjustments(statements[2])
print "Memos & Proclamations organized!"

print "SPEECHES"
print "----------"
adjustments(statements[3])
print "Speeches organized!"

print "INTERVIEWS"
print "----------"
adjustments(statements[4])
print "Interviews organized!"

# print amendmentDict

for key in amendmentDict:
	print "Working on " + key
	cwd = os.getcwd()
	k = key.replace('/', '-')
	f = open(cwd + '/' + k + "-adjustedforsynonyms.txt", 'w')
	f.write(key + '\n\n')
	f.write('----------\n\n')
	for x in amendmentDict[key]:
		f.write(x + '\n')
	f.close()


#search through statements, tweets, emails, speeches and EOs
#export document with categories and the phrases that match
#manually go through and make edits (YUCK)
