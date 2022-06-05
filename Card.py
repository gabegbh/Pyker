import numpy as np
import random
from time import time

printNum = [0,0, 'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
printSuit = ['Spades','Hearts','Clubs','Diamonds']
printRank = [0, "High card", "Two of a kind","Two pair", "Three of a kind","Straight", "Flush", "Full House", "Four of a kind", "Straight flush", "Royal flush"]


class Card:
	def __init__(self, num, suit):
		self.num = num
		self.suit = suit

	def equals(self, card):
		return self.num == card.num and self.suit == card.suit

	def print(self):
		print(printNum[self.num], "of", printSuit[self.suit])
	def toTuple(self):
		return[self.num,self.suit]

class Deck:
	def __init__(self):
		self.size = 52
		self.used = []
		self.tmp = []
	def deal(self, num, perm = True):
		#rand = np.random.default_rng()
		ret = []
		j = 0
		while j < num:
			#x = Card(rand.integers(low=2, high=14, size = 1, endpoint = True)[0], rand.integers(low=0, high=3, size = 1, endpoint = True)[0])
			x = Card(random.randint(2,14), random.randint(0,3))
			unique = True
			for i in self.used + self.tmp:
				if i.equals(x):
					unique = False
			if unique:
				if perm:
					self.size -= 1
					self.used.append(x)
				else:
					self.tmp.append(x)
				j+=1
				ret.append(x)
		# ret = Hand(ret)
		return ret
	def getSize(self):
		return self.size
	def purge(self):
		self.tmp = []
	def reset(self):
		self.size = 52
		self.used = []


#Pre-Flop hand odds [2-A] x [2-A] x [Not-Suited, Suited]
handOdds = [[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
			[[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
			[[0, 0], [0, 0], [53, 0], [29, 32], [31, 34], [28, 34], [30, 35], [31, 34], [31, 36], [32, 38], [33, 36], [37, 38], [36, 37], [36, 41], [39, 44]],
			[[0, 0], [0, 0], [30, 33], [55, 0], [30, 34], [31, 36], [33, 36], [32, 38], [30, 36], [32, 36], [31, 38], [33, 40], [34, 41], [37, 41], [43, 45]],
			[[0, 0], [0, 0], [29, 35], [32, 36], [56, 0], [31, 36], [34, 38], [33, 37], [34, 38], [32, 36], [33, 38], [34, 37], [35, 40], [39, 39], [38, 45]],
			[[0, 0], [0, 0], [31, 34], [32, 34], [32, 38], [57, 0], [36, 41], [36, 38], [34, 38], [35, 35], [34, 43], [36, 38], [34, 43], [37, 43], [42, 46]],
			[[0, 0], [0, 0], [31, 36], [29, 38], [36, 38], [37, 37], [62, 0], [37, 40], [37, 38], [37, 42], [37, 41], [37, 41], [37, 39], [41, 44], [43, 46]],
			[[0, 0], [0, 0], [30, 36], [32, 39], [33, 39], [33, 42], [39, 41], [62, 0], [36, 41], [38, 43], [39, 42], [37, 41], [42, 41], [39, 41], [45, 46]],
			[[0, 0], [0, 0], [30, 35], [32, 34], [36, 36], [36, 38], [34, 42], [37, 44], [67, 0], [38, 44], [39, 47], [40, 44], [39, 43], [39, 46], [41, 49]],
			[[0, 0], [0, 0], [31, 36], [34, 39], [36, 35], [33, 37], [36, 41], [40, 41], [41, 41], [65, 0], [38, 45], [40, 46], [41, 42], [44, 47], [43, 48]],
			[[0, 0], [0, 0], [30, 36], [33, 37], [34, 39], [31, 40], [35, 39], [39, 42], [42, 42], [39, 46], [69, 0], [44, 46], [42, 47], [43, 50], [45, 50]],
			[[0, 0], [0, 0], [32, 37], [30, 39], [36, 39], [34, 37], [36, 40], [37, 42], [37, 43], [41, 46], [46, 50], [74, 0], [42, 46], [45, 49], [47, 51]],
			[[0, 0], [0, 0], [36, 37], [38, 39], [38, 41], [33, 39], [36, 39], [38, 43], [40, 44], [41, 45], [40, 44], [42, 45], [77, 0], [45, 50], [46, 51]],
			[[0, 0], [0, 0], [38, 40], [37, 40], [36, 39], [37, 44], [40, 42], [43, 43], [42, 44], [42, 45], [46, 44], [44, 49], [42, 48], [80, 0], [46, 49]],
			[[0, 0], [0, 0], [39, 46], [38, 44], [42, 44], [41, 45], [43, 47], [43, 48], [41, 49], [44, 48], [48, 48], [45, 50], [48, 51], [50, 51], [82, 0]]]

class Hand:
	def __init__(self, cards):
		self.card1 = cards[0]
		self.card2 = cards[1]
		self.odds = handOdds[cards[0].num][cards[1].num][cards[0].suit == cards[1].suit]
		self.rank = 0
		self.pred = 0
		self.phrase = 0
		self.winPerc = 0

	def toList(self):
		return [self.card1, self.card2]

	def rankHand(self, dlr, debug = False):
		com = dlr + self.toList()
		table = sorted(com, key=lambda Card: Card.num, reverse=True)
		num = []
		suit = []
		for card in table:
			unique = True
			for entry in num:
				if card.num == entry[0]:
					entry.append(card.suit)
					unique = False
			if unique: num.append(card.toTuple())
			unique = True
			for entry in suit:
				if card.suit == entry[0]:
					entry.append(card.num)	
					unique = False
					break
			if unique: suit.append([card.suit, card.num])
		num.sort(key=lambda i: len(i), reverse=True)
		suit.sort(key=lambda i: len(i), reverse=True)
		sorts = [num, suit]
		
		#Best of-a-kind
		rank = [0, 0, 0]
		phrase = "null"
		num = sorts[0]
		suit = sorts[1]
		a = len(num[0]) - 1
		b = len(num[1]) - 1 if len(num) > 1 else 0
		if a == 1:
			phrase = printNum[num[0][0]] + " High"
			pred = [(len(table)*3*100) / (52-len(table)), 2]
			rank = [1, num[0][0], num[0][0]]
		elif a == 2:
			if b == 2:
				phrase = "Two Pair "+ printNum[num[0][0]]+"s and " + printNum[num[1][0]]+'s, ' + printNum[table[0].num] + " High"
				pred = [(4*100) / (52 - len(table)), 7]
				rank = [3, num[0][0], table[0].num]
			else:
				phrase = "Pair of " + printNum[num[0][0]]+'s, ' + printNum[table[0].num] + " High"
				#phrase = "Pair of", printNum[num[0][0]]+'s,', printNum[table[0].num], "High"
				pred = [(2*100) / (52 - len(table)), 4]
				rank = [2, num[0][0], table[0].num]
		elif a == 3:
			if b >= 2:
				phrase = "Full House " + printNum[num[0][0]]+"s Over " + printNum[num[1][0]]+'s'
				pred = [(1*100) / (52 - len(table)), 8]
				rank = [7,num[0][0], num[1][0]]
			else:
				phrase = "Three " + printNum[num[0][0]]+'s, ' + printNum[table[0].num] + " High"
				pred = [(1*100) / (52 - len(table)), 8]
				rank = [4, num[0][0], table[0].num]
		else:
			phrase = "Four " + printNum[num[0][0]]+'s, ' + printNum[table[0].num] + " High"
			pred = [100,8]
			rank = [8, num[0][0], table[0].num]
	#Find Flush
		flush = False
		if len(suit[0]) >= 6:
			flushSort = sorted(suit[0][1:], reverse=True)
			if len(flushSort) >= 5:
				for i in range(len(flushSort) - 4):
					if flushSort[i] - flushSort[i+4] == 4:
						phrase = "Straight flush " + printNum[flushSort[i+4]] + " to " + printNum[flushSort[i]] + " of " + printSuit[suit[0][0]]
						if rank[0] < 9: rank = [9, flushSort[i], flushSort[i]]
			flushEnds = [flushSort[0], flushSort[4]]
			phrase = "Flush of " + printSuit[suit[0][0]] + ", " + printNum[flushEnds[0]] + " High"
			if rank[0]  < 6: rank = [6, flushEnds[0], flushEnds[0]]
			flush = True
		elif len(suit[0]) == 5:
			if pred[1] < 6: pred = [(9 * 100) / (52 - len(table)), 6]
	#Find Straights
		i = 0
		if len(num) >= 5:
			st = sorted(num, key=lambda i: i[0], reverse=True)
			while i + 4 < len(st):
				if st[i][0] - st[i+4][0] == 4:
					straightEnds = [st[i][0], st[i+4][0]]
					if flush:
						if flushEnds == straightEnds:
							if flushEnds[0] == 14:
								phrase = "Royal flush " + printNum[st[i+4][0]] + " to " + printNum[st[i][0]] + " of " + printSuit[suit[0][0]]
								rank = [10, 14, 14]
							else:
								phrase = "Straight flush " + printNum[st[i+4][0]] + " to " + printNum[st[i][0]] + " of " + printSuit[suit[0][0]]
								if rank[0] < 9: rank = [9, st[i][0], st[i][0]]
					else:
						phrase = "Straight " + printNum[st[i+4][0]] + " to " + printNum[st[i][0]]
						if rank[0] < 5: rank = [5, st[i][0], st[i][0]]
					break
				i += 1
		i = 0
		if 6 >= len(num) >= 4 and not rank[0] in [5,9,10]:
			st = sorted(num, key=lambda i: i[0], reverse=True)
			while (i + 3) < len(st):
				if st[i][0] - st[i+3][0] == 3:
					if pred[1] < 5: pred = [(8*100) / (52 - len(table)), 5]
				elif st[i][0] - st[i+3][0] == 4:
					if pred[1] < 5: pred = [(4*100) / (52 - len(table)), 5]
				i += 1
		if debug:
			print(phrase)
			print("Prediction: ", round(pred[0], 1), "%", printRank[pred[1]])
		self.rank = rank
		self.pred = [round(pred[0], 1), printRank[pred[1]]]
		self.phrase = phrase
	
	def winRate(self, dlr, reps, deck, debug = False):
		i = 0
		tmpCards = []
		wins = 0
		if debug: 
			odds = ["Odds",0,0,0,0,0,0,0,0,0,0]
			start = time() * 1000
		empty = 5-len(dlr)
		while i < reps:
			tmpHnd = Hand(deck.deal(2, False))
			tmpCards = deck.deal(empty, False)
			self.rankHand(tmpCards + dlr)
			actual = self.rank
			tmpHnd.rankHand(tmpCards + dlr)
			sim = tmpHnd.rank
			#if len(dlr) == 5:
			odds[actual[0]] += 100/reps
			if sim[0] < actual[0]:
				wins += 1
			elif sim[0] == actual[0]:
				if sim[1] < actual[1]:
					wins += 1
			i+=1
			deck.purge()
		if debug:
			# print(wins, " / ", reps)
			# end = time() * 1000
			# print(end - start)
			print('Your hand leads to')
			for i in range(1,11):
				if odds[i] > 0:
					print(round(odds[i], 1), "%", printRank[i])
		return round(wins * 100 / reps)
