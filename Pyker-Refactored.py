import random
import sys
from time import time
from Card import Card, Deck, Hand
from Player import Player, Game


printNum = [0,0, 'Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten','Jack','Queen','King','Ace']
printSuit = ['Spades','Hearts','Clubs','Diamonds']
printRank = [0, "High card", "Two of a kind","Two pair", "Three of a kind","Straight", "Flush", "Full House", "Four of a kind", "Straight flush", "Royal flush"]
labels = [' ',' ','2','3','4','5','6','7','8','9','10','J','Q','K','A']
suit_labels = ['S', 'H', 'C', 'D']
pred = [0,0]
dealer = []
hand = []
deck = Deck()
n = 16
input_string = 'type the following commands: q (Quit),  f (someone folded), [val][suit][val][suit][val][suit] (cards in the flop)'

def illustrate(arr):
	blank = "        "
	for i in range(0, 5):
		line = ""
		for card in arr:
			num = card.num
			suit = card.suit
			rows = [".------.", "| " + labels[num] + "    |", "|  " + printSuit[suit][0:2] + "  |", "|    " + labels[num] + " |", "'------'"]
			if num == 10:
				rows[1] = "| " + labels[num] + "   |"
				rows[3] = "|   " + labels[num] + " |"
			if num > 0:
				line += rows[i]
			elif num == 0: 
				line += blank
			elif num < 0:
				rows = [".------.", "| ?    |", "|      |", "|    ? |", "'------'"]
				line += rows[i]
		print(line)


# def simHandOdds():
# 	for row in handOdds:
# 		print(row)
# 		print("Row")
# 	tmp = [0,0]
# 	for i in range(2,14):
# 		for j in range(0,3):
# 			tmp[0] = Card(i,j)
# 			for k in range(2,14):
# 				for l in range(0,3):
# 					tmp[1] = Card(k,l)
# 					if not tmp[0].equals(tmp[1]):
# 						handOdds[i][k][j==l] = Hand(tmp).winRate([], tmp, 5000)
# 	print(handOdds)


if __name__ == '__main__':
	players = None
	while True:
		try:
			players = input('Int > 1: How many players (including yourself)? "Q" - Quit')
			if players.upper() == 'Q':
				break
			players = int(players)
			assert(players >= 2)
		except: 
			print('Input Not Valid')
		else: break
	player_names = []
	for i in range(players):
		player_names.append(f'p{i}')
	g = Game(player_names, [100, 1])
	# g.preFlop()
	while True:
		try:
			hand = input('type your hand in format [val] [suit] [val] [suit]... i.e. k h 5 d (King of Hearts, 5 of Diamonds: Q - Quit, R - Random hand')
			if hand.upper() == 'Q':
				break
			elif hand.upper() == 'R':
				g.p[0].deal(g.d.deal(2))
			else:
				hand = hand.split(' ')
				card1 = Card(labels.index(hand[0].upper()), suit_labels.index(hand[1].upper()))
				card2 = Card(labels.index(hand[2].upper()), suit_labels.index(hand[3].upper()))
				g.p[0].hand = Hand([card1, card2])
				g.d.used.extend([card1, card2])
		except:
			print('Input Not Valid')
		else: break
	hands = [g.p[0].hand.card1, g.p[0].hand.card2]
	for players in range(len(g.p) - 1):
		hands.extend([Card(0,0), Card(-1,0), Card(-1,0)])
	illustrate(hands)
	print(f'\nYour hand has a {g.p[0].hand.odds}% chance of winning while averaging these hands.\n')
	g.p[0].hand.winRate(g.table, 10000, g.d, debug = True)

	while len(g.table) < 3:
		try: 
			cmd = input('type the following commands: q (Quit),  f (someone folded), [val] [suit] [val] [suit] [val] [suit] i.e. 7 h 8 h 9 h (cards in the flop)')
			if cmd.upper() == 'Q':
				break
			elif cmd.upper() == 'F':
				if len(g.p) > 2:
					g.p.pop()
					hands.pop()
					hands.pop()
					hands.pop()
					illustrate(hands)
				else:
					print("You're the last one standing! Congrats!")
					quit()
			elif cmd.upper() == 'R':
				g.table.extend(g.d.deal(3))
			else:
				cmd = cmd.split(' ')
				g.table.extend([Card(labels.index(cmd[0].upper()), suit_labels.index(cmd[1].upper())),
								Card(labels.index(cmd[2].upper()), suit_labels.index(cmd[3].upper())),
								Card(labels.index(cmd[4].upper()), suit_labels.index(cmd[5].upper()))])
				g.d.used.extend(g.table)
		except:
			print('Input Not Valid')
	illustrate(hands)
	illustrate(g.table)
	print(f"\nWith those results you win {g.p[0].hand.winRate(g.table, 10000, g.d, debug = True)}% of the hands\n")

	while len(g.table) < 4:
		try: 
			cmd = input('type the following commands: q (Quit),  f (someone folded), [val] [suit] i.e. A C (card in the turn)')
			if cmd.upper() == 'Q':
				break
			elif cmd.upper() == 'F':
				if len(g.p) > 2:
					g.p.pop()
					hands.pop()
					hands.pop()
					hands.pop()
					illustrate(hands)
				else:
					print("You're the last one standing! Congrats!")
					quit()
			elif cmd.upper() == 'R':
				g.table.extend(g.d.deal(1))
			else:
				cmd = cmd.split(' ')
				turn = Card(labels.index(cmd[0].upper()), suit_labels.index(cmd[1].upper()))
				g.table.append(turn)
				g.d.used.append(turn)
		except:
			print('Input Not Valid')
	illustrate(hands)
	illustrate(g.table)
	print(f"\nWith those results you win {g.p[0].hand.winRate(g.table, 10000, g.d, debug = True)}% of the hands\n")

	while len(g.table) < 5:
		try: 
			cmd = input('type the following commands: q (Quit),  f (someone folded), [val] [suit] i.e. A C (card in the river)')
			if cmd.upper() == 'Q':
				break
			elif cmd.upper() == 'F':
				if len(g.p) > 2:
					g.p.pop()
					hands.pop()
					hands.pop()
					hands.pop()
					illustrate(hands)
				else:
					print("You're the last one standing! Congrats!")
					quit()
			elif cmd.upper() == 'R':
				g.table.extend(g.d.deal(1))
			else:
				cmd = cmd.split(' ')
				turn = Card(labels.index(cmd[0].upper()), suit_labels.index(cmd[1].upper()))
				g.table.append(turn)
				g.d.used.append(turn)
		except:
			print('Input Not Valid')
	illustrate(hands)
	illustrate(g.table)
	print(f"\nYou win {g.p[0].hand.winRate(g.table, 10000, g.d, debug = True)}% of hands with {g.p[0].hand.phrase}\n")
	# g.flop()
	# illustrate(hands)
	# illustrate(g.table)
	# print("", g.p)
	# g.turn()
	# illustrate(hands)
	# illustrate(g.table)
	# print("", g.p)

	# g.river()
	# illustrate(hands)
	# illustrate(g.table)
	