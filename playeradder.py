# This program keeps track of n players and their plus and minus scores per minute.
# Each game will be x minutes long and the program will calculate the average score per minute for each player.
# The user will input the number of total players initially and then keep track of that many players' scores.
# For every game, it has 5 players on each team and the user will specify the id of each player that is on each team (2 teams play eachother)
# keep track of how good the teammates are and the opponents are for each player and calculate
# the average plus minus of the teammates

# Creating a dictionary of players and the games id they participated in, along with which team they were on
# also store the player's average plus minus score
# along with their teammates' average plus minus score and their opponents' average plus minus score

import os
import pickle

players = {}

games = {}

gameIndex = 0

# add game function
def addGame():

    global gameIndex, games, players

    # Ask player for the id of each player on each team
    team1 = []
    team2 = []

    for i in range(5):
        satisfactory = False
        id = None
        while (not satisfactory):
            id = int(input("Enter the id of player {} on team 1: ".format(i+1)))
            if id in team1 or id in team2:
                print("Error: Player already on a team, try again!")
            else:
                satisfactory = True
        team1.append(id)
    for i in range(5):
        satisfactory = False
        id = None
        while (not satisfactory):
            id = int(input("Enter the id of player {} on team 2: ".format(i+1)))
            if id in team1 or id in team2:
                print("Error: Player already on a team, try again!")
            else:
                satisfactory = True
        team2.append(id)

    # ask for the score of team 1 (team2 score is automatically the opposite of team1 score)
    team1score = int(input("Enter the score of team 1: "))
    # setting the info at the game index
    game = games.get(gameIndex, {"team1": team1, "team2": team2, "team1score": team1score})
    games.update({gameIndex: game})

    # add the game to the players dictionary and the player's plus minus score
    for i in range(5):
        player = players.get(team1[i], {"gameIDs": [], "plusminus": 0.0, "teammates": [], "opponents": []})
        player["plusminus"] *= len(player["gameIDs"])
        player["plusminus"] += team1score
        player["plusminus"] /= len(player["gameIDs"])+1
        player["teammates"] = player["teammates"] + team1
        player["opponents"] = player["opponents"] + team2
        # remove the player's id from the teammates list
        player["teammates"] = [x for x in player["teammates"] if x != team1[i]]
        player["gameIDs"].append(gameIndex)

        Oppositeplayer = players.get(team2[i], {"gameIDs": [], "plusminus": 0.0, "teammates": [], "opponents": []})
        Oppositeplayer["plusminus"] *= len(Oppositeplayer["gameIDs"])
        Oppositeplayer["plusminus"] -= team1score
        Oppositeplayer["plusminus"] /= len(Oppositeplayer["gameIDs"])+1
        Oppositeplayer["teammates"] = Oppositeplayer["teammates"] + team2
        Oppositeplayer["opponents"] = Oppositeplayer["opponents"] + team1
        # remove the player's id from the teammates list
        Oppositeplayer["teammates"] = [x for x in Oppositeplayer["teammates"] if x != team2[i]]
        Oppositeplayer["gameIDs"].append(gameIndex)

        players.update({team1[i]: player})
        players.update({team2[i]: Oppositeplayer})

    # gmae is finished now so increment the gameIndex
    gameIndex += 1

# gets the average plus minus of a player's teammates
def getTeammatePlusMinus(playerID):
    player = players.get(playerID)
    teammates = player["teammates"]
    plusminus = 0.0
    for teammate in teammates:
        plusminus += players.get(teammate)["plusminus"]
    return plusminus / len(teammates)

# gets the average pus minus of a player's opponents
def getOpponentPlusMinus(playerID):
    player = players.get(playerID)
    opponents = player["opponents"]
    plusminus = 0.0
    for opponent in opponents:
        plusminus += players.get(opponent)["plusminus"]
    return plusminus / len(opponents)

def printRow(strings, width):
    print("|", end="")
    for string in strings:
        print("{:^{width}}".format(string, width=width), end=" |")
    print()

def read_or_new_pickle(path, default):
    if os.path.isfile(path):
        with open(path, "rb") as f:
            try:
                return pickle.load(f)
            except Exception: # so many things could go wrong, can't be more specific.
                pass
    with open(path, "wb") as f:
        pickle.dump(default, f)
    return default

def write_pickle(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f)

if __name__ == "__main__":

    # While loop to keep asking the user if they want to play a game at the end
    running = True

    # load the save file
    # get name of save file
    fileStr = input("Enter the name of the session file (excluding .data): ") + ".data"
    data = read_or_new_pickle(fileStr, {"players": {}, "games": {}, "gameIndex": 0})

    players = data["players"]
    games = data["games"]
    gameIndex = data["gameIndex"]

    while (running):
        addGame()
        # display results
        print("Players")
        printRow(["Player", "Plus Minus", "Teammate Plus Minus", "Opponent Plus Minus"], 20)
        for key in sorted(players.keys()):
            player = players.get(key)
            # print("Player " + str(key) + " has a plus minus of " + str(player["plusminus"]) + " and a teammate plus minus of " + str(getTeammatePlusMinus(key)) + " and an opponent plus minus of " + str(getOpponentPlusMinus(key)))
            printRow([str(key), str(player["plusminus"]), str(getTeammatePlusMinus(key)), str(getOpponentPlusMinus(key))], 20)

        # display games
        print("Games")
        printRow(["index", "Team 1 Score", "Team 1", "Team 2"], 20)
        for i in range(gameIndex):
            game = games.get(i)
            printRow([str(i), str(game["team1score"]), str(game["team1"]), str(game["team2"])], 20)

        # save the data
        data["players"] = players
        data["games"] = games
        data["gameIndex"] = gameIndex
        write_pickle(fileStr, data)

        # would you like to play another game?
        playAgain = input("Would you like to play another game? (y/n): ")
        running = "y" in playAgain.lower()


