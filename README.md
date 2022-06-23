# Texas Hold'em Helper
Real-time Texas Hold'em winning odds calculator.

## Concept
Beginning as a simple script to determine the best poker hand out of a set of 7 cards, I added functionality on top to follow a real game of Texas Hold'em or simulate a fake one providing statistics along the way. 

## Functionality
As each hand of poker progresses, the program runs 10,000 hands randomizing the opponents' cards as well as the yet to be revealed table cards. During each of these simulations, it records your best hand and the winning hand. Once all 10,000 collect data, it returns a list of all poker hands and the odds of you drawing that hand along with the percent of all hands that you'd win. Each time a new card is drawn or a player has folded, it will reevaluate your odds of winning and your potential hands.

## Future Plans
As it stands, the basic CLI design is less than optimal to use intuitively. A GUI that is simple and intuitive will be added moving forward, along with many more statistics that couldn't fit well in a CLI without being cluttered. 

## Demo
For this demo we will play a hand while randomizing our hand and the table against 3 players.
1. Our random hand where we win a pretty high 67% of rounds with pocket 8's.
![image](https://user-images.githubusercontent.com/24580466/173734948-5d53f48c-dfaa-4c17-a7d8-562c3b42682d.png)
2. The random flop was not kind to us, our hand has less favorable percentages with no pairs made.
![image](https://user-images.githubusercontent.com/24580466/173734991-cda96883-86af-40e6-bc51-398ce013bb24.png)
3. The turn comes and again our share of the winning hands drops and our possible hands now shrinks to 3 ranks.
![image](https://user-images.githubusercontent.com/24580466/173735046-e4f17143-00d7-48ac-854e-198785a0ec61.png)
4. With the table pair on the river, we make two pair now our only possible hand, and win 72% of rounds with our Queen high kicker.
![image](https://user-images.githubusercontent.com/24580466/173735085-c825b2ea-da3e-4e4d-b307-4c9e3eda495f.png)
