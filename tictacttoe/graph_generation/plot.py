import matplotlib.pyplot as plt

player1_wins = 34  
player2_wins = 49  

players = ['Minimax with Alpa Beta', 'Q learning']
wins = [player1_wins, player2_wins]

# Create bar graph
plt.bar(players, wins, color=['blue', 'green'])
plt.xlabel('Players')
plt.ylabel('Wins')
plt.title('TIC-TAC-TOE Wins')
plt.show()
