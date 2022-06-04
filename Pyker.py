import random
import collections

table = []
printNum = [0,0, 'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
printSuit = ['Spades','Hearts','Clubs','Diamonds']
sortNums = []
sortSuits = []

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


def populateTable():
	x = Card(random.randint(2,14), random.randint(0,3))
	unique = True
	for i in table:
		if i.equals(x):
			unique = False
	if unique:
		table.append(x)

def sortTable():
	table.sort(key=lambda Card: Card.num, reverse = True)
	for card in table:
		sortNums.append(card.toTuple()[0])
		sortSuits.append(card.toTuple())
	sortSuits.sort(key=lambda i: i[1])



def findBestHand():
	#Best of-a-kind
	nums = sorted(list(collections.Counter(sortNums).items()), key=lambda i: i[1], reverse=True)
	print(nums)
	high = nums[0]
	low = None
	print(nums)
	if high[1] == 1:
		print(printNum[high[0]], "High")
	elif high[1] == 2:
		if nums[1][1] == 2:
			print("Two Pair", printNum[high[0]]+'s',"and", printNum[nums[1][0]]+'s,', printNum[table[0].num], "High")
		else:
			print("Pair of", printNum[high[0]]+'s,', printNum[table[0].num], "High")
	elif high[1] == 3:
		if nums[1][1] >= 2:
			print("Full House", printNum[high[0]]+'s', "Over", printNum[nums[1][0]]+'s,')
		else:
			print("Three", printNum[high[0]]+'s,', printNum[table[0].num], "High")
	else:
		print("Four", printNum[high[0]]+'s,', printNum[table[0].num], "High")
		
	#best Flush
	checkSuits()
	#best Strait
def checkSuits():
	sortedTable = sorted(table, key=lambda card: card.suit)
	curSuit = sortedTable[0].suit
	for c in sortedTable:
		print(c.num, c.suit)
	i = 0
	count = 0
	while i < len(sortedTable):
		while i < len(sortedTable) and sortedTable[i].suit == curSuit:
			i += 1
			count += 1
		if count >= 5:
			print(printSuit[curSuit],"Flush,",printNum[sortedTable[i-count].num], "High")
			break
		if i < len(sortedTable):
			curSuit = sortedTable[i].suit
			count = 0


if __name__ == '__main__':
	while len(table) < 7:
		populateTable()
	sortTable()
	for i in table:
		i.print()
	findBestHand()
