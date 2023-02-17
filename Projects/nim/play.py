from nim import train, play

ai = train()

ans = "yes"

while ans == "yes":
    play(ai, human_player=1)

    ans = input("Do you want to play again (yes / no): ")