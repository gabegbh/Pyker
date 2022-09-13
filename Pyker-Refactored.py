import random
import sys
from time import time
from Card import Card, Deck, Hand
from Player import Player, Game
import curses


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

def main(w):
	players = None
	q = False
	while True:
		try:
			w.addstr(0,0,'Int > 1: How many players (including yourself)? "Q" - Quit')
			usr =  w.getkey()
			if usr.upper() == 'Q':
				return
			players = int(usr)
			assert(players >= 2 and players <= 5)
		except: 
			w.addstr('   Input Not Valid')
		else:
			w.addch(' ')
			w.addch(usr)
			w.addstr(' Players Added! ')
			w.refresh()
			break
	player_names = []
	for i in range(players):
		player_names.append(f'p{i}')
	g = Game(player_names, [100, 1])
	# g.preFlop()
#type the following commands: q (Quit),  f (someone folded), [val] [suit] [val] [suit] [val] [suit] i.e. 7 h 8 h 9 h (cards in the flop)f
	
	
	while True:
		try:
			hand = input('type your hand in format [val] [suit] [val] [suit]... i.e. k h 5 d (King of Hearts, 5 of Diamonds: Q - Quit, R - Random hand')
			if hand.upper() == 'Q':
				q = True
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
	if not q:
		hands = [g.p[0].hand.card1, g.p[0].hand.card2]
		for players in range(len(g.p) - 1):
			hands.extend([Card(0,0), Card(-1,0), Card(-1,0)])
		illustrate(hands)
		print(f'\nYour hand has a {int(((g.p[0].hand.odds / 100) ** (len(g.p) - 1)) * 100)}% chance of winning while averaging these hands.\n')
		g.p[0].hand.winRate(g.table, 50000, g.d, debug = True)
	while not q and len(g.table) < 3:
		try: 
			cmd = input('type the following commands: q (Quit),  f (someone folded), [val] [suit] [val] [suit] [val] [suit] i.e. 7 h 8 h 9 h (cards in the flop)')
			if cmd.upper() == 'Q':
				q = True
				break
			elif cmd.upper() == 'F':
				if len(g.p) > 2:
					g.p.pop()
					hands.pop()
					hands.pop()
					hands.pop()
					illustrate(hands)
					print(f'\nYour hand has a {int(((g.p[0].hand.odds / 100) ** (len(g.p) - 1)) * 100)}% chance of winning while averaging these hands.\n')
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
	if not q:
		illustrate(hands)
		illustrate(g.table)
		print(f"\nWith those results you win {int(((g.p[0].hand.winRate(g.table, 50000, g.d, debug = True) / 100) ** (len(g.p) - 1)) * 100)}% of the hands\n")

	while not q and len(g.table) < 4:
		try: 
			cmd = input('type the following commands: q (Quit),  f (someone folded), [val] [suit] i.e. A C (card in the turn)')
			if cmd.upper() == 'Q':
				q = True
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
	if not q:
		illustrate(hands)
		illustrate(g.table)
		print(f"\nWith those results you win {int(((g.p[0].hand.winRate(g.table, 50000, g.d, debug = True) / 100) ** (len(g.p) - 1)) * 100)}% of the hands\n")

	while not q and len(g.table) < 5:
		try: 
			cmd = input('type the following commands: q (Quit),  f (someone folded), [val] [suit] i.e. A C (card in the river)')
			if cmd.upper() == 'Q':
				q = True
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
	if not q:
		illustrate(hands)
		illustrate(g.table)
		print(f"\nYou win {int(((g.p[0].hand.winRate(g.table, 50000, g.d, debug = True) / 100) ** (len(g.p) - 1)) * 100)}% of hands with {g.p[0].hand.phrase}\n")

if __name__ == '__main__':
	#w = curses.initscr()
	curses.wrapper(main)
	# curses.noecho()
    # curses.cbreak()
    # w.addstr(1,0,'I am Gabe')
    # w.nodelay(0)