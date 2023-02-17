from nim import train, play

ai = train(200000)

for i in range(10):
    play(ai)