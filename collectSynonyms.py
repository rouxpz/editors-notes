import os, csv, re
from pattern.en import parse
from PyDictionary import PyDictionary
from time import sleep
import sys

synonyms = []
amendmentWords = []
amendments = []
titles = []
punctuation = ['.', ',', '!', '?', ';', ':', '"']
posList = ['NN', 'JJ']
exclude = ['i', 'is', 'be', 'am', 'are']

dictionary = PyDictionary()

with open('amendments.txt', 'rb') as f:
	fullfile = f.read()
	am = fullfile.split('\n\n\n')
	for line in am:
		amendments.append(line)

print len(amendments)

cwd = os.getcwd()

for a in amendments:
	aText = a.split('\n')[1]
	titles.append(a.split('\n')[0])
	aText = aText.lower().replace('offence', 'offense').replace('defence', 'defense')
	for p in punctuation:
		aText = aText.replace(p, '')
	aText = aText.split(' ')

	# print aText
	# print len(aText)
	amendmentWords.append(aText)

	# aindex = len(amendmentWords) - 1
	# print aindex
print len(amendmentWords)

for w in amendmentWords:
	synonyms.append([])
	# print len(w)
	aindex = amendmentWords.index(w)
	print "Now processing synonyms for Amendment " + str(aindex + 1)
	for at in w:
		atparsed = parse(at).split('/')
		for pos in posList:
			if pos in atparsed[1]:
				syns = dictionary.synonym(at)
				print str(len(syns)) + " synonyms for " + at
				if syns != None:
					# print syns
					for s in syns:
						if s not in synonyms[aindex]:
							# print "new word: " + s
							synonyms[aindex].append(s)
					
						if ' ' not in s:
							sparsed = parse(s).split('/')
							for pos2 in posList:
								if pos in atparsed[1]:
								# print s
									syns2 = dictionary.synonym(s)

									if syns2 != None:

										for y in syns2:
											if y not in synonyms[aindex]:
												synonyms[aindex].append(y)

	print "SYNONYM LENGTH: " + str(len(synonyms[aindex]))
	# print len(synonyms)
	# print amendmentWords.index(w)

for i in range(0, len(amendmentWords)):
	for j in range(0, len(synonyms[i])):
		if synonyms[i][j].encode('utf-8') not in amendmentWords[i]:
			amendmentWords[i].append(synonyms[i][j])

	print "TOTAL LENGTH OF AMENDMENT " + str(i + 1) + "WORDS: " + str(len(amendmentWords[i]))

	with open(cwd + '/amendment' + str(i) + 'synonyms.txt', 'w+') as f:
		f.write("AMENDMENT " + str(i) + '\n')

		for m in amendmentWords[i]:
			try:
				f.write(m.encode('utf-8'))
				f.write('\n')
			except:
				print "unicode error, moving on"

		f.close()