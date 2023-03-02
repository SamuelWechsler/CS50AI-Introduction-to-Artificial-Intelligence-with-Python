from nim import train, play
from datetime import datetime

t1 = datetime.now()
ai = train(1000)
t2 = datetime.now()

print("Training finished in ", t2 - t1)

ans = "yes"

while ans == "yes":
    play(ai, human_player=1)

    ans = input("Do you want to play again (yes / no): ")