from time import time
from Card import Card, Deck, Hand
import random

class Player:
    def __init__(self, name, hand, chips):
        self.name = name #string name of player
        self.hand = hand #Hand object assigned by Game
        self.chips = chips #Num of chips cur 1 inc
        self.status = False #playing this hand
        self.chipsIn = 0 #number of chips bet in one round - resets at next bet round

    def deal(self, hand): #redeal new cards to existing player
        self.hand = Hand(hand)

    def play(self, bigHand): #decide raise call or fold RANDOM NOW MUST CHANGE
        ret = ["Raise", "Call", "Raise", "Call","Call","Fold"]
        ch = random.choice(ret)
        if ch == "Call":
            print(self.name, ":", ch, " +", bigHand - self.chipsIn, "bigHand:", bigHand)
            return [ch, self.bet(bigHand - self.chipsIn)] #bigHand - chipsIn = delta to call amount
        elif ch == "Raise":
            print(self.name, ":", ch, " +", (bigHand - self.chipsIn) +2, "bigHand:", bigHand)
            return [ch, self.bet((bigHand - self.chipsIn) + 2)] #bigHand - chipsIn + 2= delta to raise by amount (2)
        else:
            print(self.name, ":", ch, " +", 0, "bigHand:", bigHand)
            return [ch, 0]
        
    def bet(self, amt): #update self variables and return how many chips were spent
        if amt > self.chips:
            max = self.chips
            self.chips = 0
            self.chipsIn += max
            return max #NEEDS WORK TO MOD THE PAYOUTS FOR ALL IN
        else:
            self.chips -= amt
            self.chipsIn += amt
            return amt
    


class Game:
    def __init__(self, players, stakes): #players - list of Player name strings only, stakes - [chips/player, little blind amount]
        self.d = Deck()
        self.lb = stakes[1]
        self.bb = stakes[1] * 2
        self.state = 0 #FUTURE CONTROL WHAT STAGE GAME IS ON
        self.p = [] 
        for n in players: #Create Player Objects from name strings
            self.p.append(Player(n, None, stakes[0]))
        self.numP = len(self.p) #convenient playercount var
        self.blindPlayer = 0 #first better each round. rotates each hand
        self.table = [] #Just the face up cards on the table (Card obj)
        self.call = 0 #amount of chips to call (BiggestBet)
        self.pot = 0 #total amount of chips for the payout
        self.folded =  [None] * len(self.p) #array to remove folded players from rotation while maintaining their state
    def preFlop(self):
        for p in self.p: #deal in all players 
            p.deal(self.d.deal(2))
            p.status = True
        self.bet(True) #start 1st betting round (True for blinds)
    def flop(self):
        self.table.extend(self.d.deal(3)) #Deal 3 cards on the table (Not True for blinds)
        self.bet()
    def turn(self):
        self.table.extend(self.d.deal(1))
        self.bet()
    def river(self):
        self.table.extend(self.d.deal(1))
        self.bet()
    def bet(self, blind = False): #loop that lets everyone raise call or fold (add blind bets for True)
        i = self.blindPlayer # player that starts the betting
        self.call = 0 #biggest bet on the table (must match to call)
        calls = 0 #number of calls or folds in a row to break the loop when no raises
        if blind: #force player 1 and 2 to put little and big blind bets (i%self.numP is looping player iterator)
            self.p[i%self.numP].bet(self.lb)
            print(self.p[i%self.numP].name, ": Little Blind +", self.lb)
            i+=1 #next player turn
            self.p[i%self.numP].bet(self.bb)
            print(self.p[i%self.numP].name, ": Big Blind +", self.bb)
            i+=1
            self.pot += self.lb * 3 #pot gets little blind plus big blind
            self.call = self.bb #biggestBet is big blind
        while calls < self.numP and self.numP > 1: #while there is a raise in a round and there are more than one player not folded
            tmp = self.p[i%self.numP].play(self.call) #returns ["action", chips added], (["Raise", 4])
            self.pot += tmp[1] #add bet to total pot
            if tmp[0] == "Raise":
                self.call = self.p[i%self.numP].chipsIn # new Biggest Hand
                calls = 0 #reset end of turn calls
            elif tmp[0] == "Call":
                calls+=1 #iterate end of turn calls
            if tmp[0] == "Fold":
                self.folded[i%self.numP] = self.p.pop(i%self.numP) #move plaer from active list to folded list
                i = i%self.numP #re-index the playyer rotation to accomodate for one less player
            else:
                i+=1
            self.numP = len(self.p) #refresh player num count
        for pl in self.p:
            pl.chipsIn = 0 #reset chips in per player