from MakePrediction import makePredictions
from Persistent import dto
from Persistent.repository import Repository
import platform
import pandas
import os

currentDirectory = os.getcwd()

slashDirection = "\\"
if platform.system() == "Darwin":
    slashDirection = "//"

rounds_to_predict = 23


def resultForGame(_date, home_team_name, away_team_name, league):
    filePath = currentDirectory + '{}Persistent{}Data{}{} stats{}Final{}{}-19-20-Final.csv'.format(slashDirection,
                                                                                                   slashDirection,
                                                                                                   slashDirection,
                                                                                                   league,
                                                                                                   slashDirection,
                                                                                                   slashDirection,
                                                                                                   league)
    tableToRead = pandas.read_csv(filePath, parse_dates=True)
    date = _date.replace('-', '/')
    date = date.split('/')
    date = str(date[2]) + "/" + str(date[1]) + "/" + str(date[0])

    for index, row in tableToRead.iterrows():
        if row[1] == date:
            if row[2] == home_team_name:
                if row[3] == away_team_name:
                    return row[13]
    return -1


def MakePredictionsAndMoveTheGamesFromUpToMainTable(rounds_to_predict):
    for _round in range(rounds_to_predict):
        _round = _round + 1
        gamesToMainTable = makePredictions(_round)
        for ind in gamesToMainTable.index:

            leagueName = gamesToMainTable['league'][ind]
            _date = gamesToMainTable['date'][ind]
            gameCounter = int(gamesToMainTable['round'][ind])

            _home_team_name = gamesToMainTable['home_team_name'][ind]
            _away_team_name = gamesToMainTable['away_team_name'][ind]

            _home_team_rank = int(gamesToMainTable['home_team_rank'][ind])
            _away_team_rank = int(gamesToMainTable['away_team_rank'][ind])

            _home_team_scored = gamesToMainTable['home_team_scored'][ind]
            _away_team_scored = gamesToMainTable['away_team_scored'][ind]

            _home_team_received = gamesToMainTable['home_team_received'][ind]
            _away_team_received = gamesToMainTable['away_team_received'][ind]

            _home_att = int(gamesToMainTable['home_att'][ind])
            _away_att = int(gamesToMainTable['away_att'][ind])

            _home_def = int(gamesToMainTable['home_def'][ind])
            _away_def = int(gamesToMainTable['away_def'][ind])

            _home_mid = int(gamesToMainTable['home_mid'][ind])
            _away_mid = int(gamesToMainTable['away_mid'][ind])

            _home_odds_n = gamesToMainTable['home_odds_n'][ind]
            _draw_odds_n = gamesToMainTable['draw_odds_n'][ind]
            _away_odds_n = gamesToMainTable['away_odds_n'][ind]

            _home_odds_nn = gamesToMainTable['home_odds_nn'][ind]
            _draw_odds_nn = gamesToMainTable['draw_odds_nn'][ind]
            _away_odds_nn = gamesToMainTable['away_odds_nn'][ind]

            _result = resultForGame(_date, _home_team_name, _away_team_name, leagueName)

            if _result == -1:
                print("Cant find")

            gameToAdd = dto.match(leagueName, _date, gameCounter, _home_team_name, _away_team_name,
                                  _home_team_rank, _away_team_rank, _home_team_scored, _away_team_scored,
                                  _home_team_received, _away_team_received, _home_att, _away_att, _home_def,
                                  _away_def,
                                  _home_mid, _away_mid, _home_odds_n, _draw_odds_n, _away_odds_n, _result,
                                  _home_odds_nn, _draw_odds_nn, _away_odds_nn)
            repo = Repository()
            repo.upcoming_games.delete(_date, _home_team_name, _away_team_name)
            repo.main_table.insert(gameToAdd)


def addResultColumnToExcels(rounds_to_predict):
    for prediction in range(rounds_to_predict):
        prediction = prediction + 1
        path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                              prediction)
        tableToRead = pandas.read_csv(path, parse_dates=True)
        tableToRead['Result'] = 0
        for index, row in tableToRead.iterrows():
            gameResult = resultForGame(row[1], row[2], row[3], row[0])
            tableToRead['Result'][index] = str(gameResult)
        tableToRead.to_csv(
            str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                                prediction))


def maxPrediction(list):
    return max(list)


def indexOfMaxPrediction(list):
    x = list.index(max(list))
    if x == 0:
        return '1'
    if x == 1:
        return '2'
    return 'X'


def nnOds(list):
    x = list.index(max(list))
    if x == 0:
        return 5
    if x == 1:
        return 7
    return 6


def AW(Excpected, Acutal):
    if (Excpected == Acutal):
        return 'True'
    return 'False'


def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup


def Sort_Tuple_Doubles(tup):
    return (sorted(tup, key=lambda x: x[5]))


def Sort_Tuple_Triples(tup):
    return (sorted(tup, key=lambda x: x[6]))


def byProbabilityOnly(rounds_to_predict):
    for prediction in range(rounds_to_predict):
        prediction = prediction + 1
        path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                              prediction)
        tableToRead = pandas.read_csv(path, parse_dates=True)

        tableToRead['----------------------------'] = ''
        tableToRead['Max Probability'] = ''
        tableToRead['Module Prediction'] = ''
        tableToRead['Winner Prediction'] = ''
        tableToRead['Win'] = ''
        tableToRead['Expectancy of variance'] = ''

        listOfGames = []
        TrueCounter = 0
        totalGames = 0
        for index, row in tableToRead.iterrows():
            # By module - 0 < x < 1
            maxP = maxPrediction([float(row[8]), float(row[9]), float(row[10])])
            tableToRead['Max Probability'][index] = maxP
            pair = (index, maxP)
            listOfGames.append(pair)
            # By Max Prob - 1 X 2
            mPred = indexOfMaxPrediction([float(row[8]), float(row[9]), float(row[10])])
            tableToRead['Module Prediction'][index] = mPred
            # By Module Prob - x > 0
            WP = row[int(nnOds([float(row[8]), float(row[9]), float(row[10])]))]
            tableToRead['Winner Prediction'][index] = WP
            # By module - TRUE FALSE
            aw = AW(row[11], indexOfMaxPrediction([float(row[8]), float(row[9]), float(row[10])]))
            if aw == 'True':
                TrueCounter = TrueCounter + 1
            tableToRead['Win'][index] = aw
            # ΩΘ-1
            FinalP = float(WP * maxP) - 1
            tableToRead['Expectancy of variance'][index] = FinalP

            totalGames = index + 1

        sortedTuples = Sort_Tuple(listOfGames)
        sortedTuples.reverse()

        tableToRead['--------------------------'] = ''
        index = 0
        total_stake = 0
        total_prize = 0
        tableToRead['Serial Number'] = ''
        tableToRead['Probability'] = ''
        tableToRead['W Prediction'] = ''
        tableToRead['Odds'] = ''
        tableToRead['Bet'] = ''
        tableToRead['Prize'] = ''
        for pair in sortedTuples:
            tableToRead['Serial Number'][index] = pair[0]
            tableToRead['Probability'][index] = pair[1]
            tableToRead['W Prediction'][index] = tableToRead['Module Prediction'][pair[0]]
            tableToRead['Odds'][index] = tableToRead['Winner Prediction'][pair[0]]
            tableToRead['Bet'][index] = 10
            total_stake = total_stake + tableToRead['Bet'][index]
            if (tableToRead['Win'][pair[0]] == 'True'):
                tableToRead['Prize'][index] = tableToRead['Bet'][index] * tableToRead['Odds'][index]
                total_prize = total_prize + tableToRead['Prize'][index]
            else:
                tableToRead['Prize'][index] = 0

            index = index + 1

        tableToRead['-------------------------'] = ''

        tableToRead.loc[5, '__'] = "Winning rate"
        tableToRead.loc[5, '_'] = float(TrueCounter / totalGames)

        tableToRead.loc[6, '__'] = "Total bet"
        tableToRead.loc[6, '_'] = int(total_stake)

        tableToRead.loc[7, '__'] = "Total prize"
        tableToRead.loc[7, '_'] = int(total_prize)

        tableToRead.loc[8, '__'] = "Prize rate"
        tableToRead.loc[8, '_'] = float(total_prize / total_stake)

        TSTACK_06 = 0
        TEARINING_06 = 0
        ToalGames_06 = 0
        TotalWins_06 = 0

        TSTACK_065 = 0
        TEARINING_065 = 0
        ToalGames_065 = 0
        TotalWins_065 = 0

        TSTACK_07 = 0
        TEARINING_07 = 0
        ToalGames_07 = 0
        TotalWins_07 = 0

        TSTACK_075 = 0
        TEARINING_075 = 0
        ToalGames_075 = 0
        TotalWins_075 = 0

        TSTACK_08 = 0
        TEARINING_08 = 0
        ToalGames_08 = 0
        TotalWins_08 = 0

        for index, row in tableToRead.iterrows():

            if row[14] > 0.6:
                TSTACK_06 = TSTACK_06 + 10
                ToalGames_06 = ToalGames_06 + 1
                if row[17]:
                    TotalWins_06 = TotalWins_06 + 1
                    TEARINING_06 = TEARINING_06 + 10 * row[23]

            if row[14] > 0.65:
                TSTACK_065 = TSTACK_065 + 10
                ToalGames_065 = ToalGames_065 + 1
                if row[17]:
                    TotalWins_065 = TotalWins_065 + 1
                    TEARINING_065 = TEARINING_065 + 10 * row[23]

            if row[14] > 0.7:
                TSTACK_07 = TSTACK_07 + 10
                ToalGames_07 = ToalGames_07 + 1
                if row[17]:
                    TotalWins_07 = TotalWins_07 + 1
                    TEARINING_07 = TEARINING_07 + 10 * row[23]

            if row[14] > 0.75:
                TSTACK_075 = TSTACK_075 + 10
                ToalGames_075 = ToalGames_075 + 1
                if row[17]:
                    TotalWins_075 = TotalWins_075 + 1
                    TEARINING_075 = TEARINING_075 + 10 * row[23]

            if row[14] > 0.8:
                test1 = row[17]
                TSTACK_08 = TSTACK_08 + 10
                ToalGames_08 = ToalGames_08 + 1
                if row[17]:
                    TotalWins_08 = TotalWins_08 + 1
                    TEARINING_08 = TEARINING_08 + 10 * row[23]

        totalPre06 = TEARINING_06 / TSTACK_06
        totalPre065 = TEARINING_065 / TSTACK_065
        totalPre07 = TEARINING_07 / TSTACK_07
        totalPre075 = TEARINING_075 / TSTACK_075
        totalPre08 = TEARINING_08 / TSTACK_08

        tableToRead.loc[10, '__'] = "Prize rate >0.6 is"
        tableToRead.loc[10, '_'] = totalPre06

        tableToRead.loc[11, '__'] = "Win rate >0.6 is"
        tableToRead.loc[11, '_'] = str(float(TotalWins_06 / ToalGames_06) * 100) + "%"

        tableToRead.loc[12, '__'] = "Prize rate >0.65 is"
        tableToRead.loc[12, '_'] = totalPre065

        tableToRead.loc[13, '__'] = "Win rate >0.65 is"
        tableToRead.loc[13, '_'] = str(float(TotalWins_065 / ToalGames_065) * 100) + "%"

        tableToRead.loc[14, '__'] = "Prize rate >0.7 is"
        tableToRead.loc[14, '_'] = totalPre07

        tableToRead.loc[15, '__'] = "Win rate >0.7 is"
        tableToRead.loc[15, '_'] = str(float(TotalWins_07 / ToalGames_07) * 100) + "%"

        tableToRead.loc[16, '__'] = "Prize rate >0.75 is"
        tableToRead.loc[16, '_'] = totalPre075

        tableToRead.loc[17, '__'] = "Win rate >0.75 is"
        tableToRead.loc[17, '_'] = str(float(TotalWins_075 / ToalGames_075) * 100) + "%"

        tableToRead.loc[18, '__'] = "Prize rate >0.8 is"
        tableToRead.loc[18, '_'] = totalPre08

        tableToRead.loc[19, '__'] = "Win rate >0.8 is"
        tableToRead.loc[19, '_'] = str(float(TotalWins_08 / ToalGames_08) * 100) + "%"

        tableToRead['----------------------------'] = ''

        tableToRead.to_csv(
            str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                                prediction))


def byEVsingle(rounds_to_predict):
    for prediction in range(rounds_to_predict):

        prediction = prediction + 1
        path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                              prediction)
        tableToRead = pandas.read_csv(path, parse_dates=True)
        listOfGames = []
        for index, row in tableToRead.iterrows():
            Omega = tableToRead['Expectancy of variance'][index]
            pair = (index, Omega)
            listOfGames.append(pair)

        sortedTuples = Sort_Tuple(listOfGames)
        sortedTuples.reverse()
        tableToRead['------> Single - by expectancy of variance'] = ''
        index = 0
        tableToRead['Serial Number EV'] = ''
        tableToRead['Expectancy of variance'] = ''
        tableToRead['Module Prediction EV'] = ''
        tableToRead['Win EV'] = ''
        tableToRead['Odds EV'] = ''
        tableToRead['Bet EV'] = ''
        tableToRead['Prize EV'] = ''
        tableToRead['------> Result single EV'] = ''
        tableToRead['Win Rate By E*V games'] = ''
        tableToRead['Win Rate By E*V games Result'] = ''
        gameTrueCounter = 0
        listOfTuples = []
        for pair in sortedTuples:
            gameTuple = ()
            tableToRead['Serial Number EV'][index] = pair[0]
            tableToRead['Expectancy of variance'][index] = pair[1]
            tableToRead['Module Prediction EV'][index] = tableToRead['Module Prediction'][pair[0]]
            tableToRead['Odds EV'][index] = tableToRead['Winner Prediction'][pair[0]]
            tableToRead['Win EV'][index] = tableToRead['Win'][pair[0]]
            tableToRead['Bet EV'][index] = 10
            if tableToRead['Win'][pair[0]] == 1:
                gameTrueCounter = gameTrueCounter + 1
                if index < 20:
                    if index == 0:
                        prizeCounter = 10 * tableToRead['Odds EV'][index]
                        gameTrueCounter = 1
                    else:
                        prizeCounter = listOfTuples[index - 1][1] + 10 * tableToRead['Odds EV'][index]
                        gameTrueCounter = listOfTuples[index - 1][0] + 1
                    gameTuple = (gameTrueCounter, prizeCounter)
                tableToRead['Prize EV'][index] = tableToRead['Bet EV'][index] * tableToRead['Odds EV'][index]
            else:
                if index < 20:
                    if index == 0:
                        gameTuple = (0, 0)
                    else:
                        gameTuple = (listOfTuples[index - 1][0], listOfTuples[index - 1][1])
                tableToRead['Prize EV'][index] = 0
            listOfTuples.append(gameTuple)
            index = index + 1

        excelIndex = 2
        gamesIndexx = 1
        for tuple in listOfTuples:
            if gamesIndexx <= 20:
                # Win Rate
                tableToRead.loc[excelIndex, 'Win Rate By E*V games'] = "Best {} games win rate".format(gamesIndexx)
                tableToRead.loc[excelIndex, 'Win Rate By E*V games Result'] = str(
                    float(tuple[0] / gamesIndexx) * 100) + "%"
                # Prize Win Rate
                tableToRead.loc[excelIndex + 1, 'Win Rate By E*V games'] = "Prize rate for {} games is".format(
                    gamesIndexx)
                tableToRead.loc[excelIndex + 1, 'Win Rate By E*V games Result'] = float(tuple[1] / (gamesIndexx * 10))

                # Prize Win Rate
                tableToRead.loc[excelIndex + 2, 'Win Rate By E*V games'] = "----------------------------"
                tableToRead.loc[
                    excelIndex + 2, 'Win Rate By E*V games Result'] = "---------------------------------------"

                gamesIndexx = gamesIndexx + 1
                excelIndex = excelIndex + 3

        tableToRead.to_csv(
            str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                                prediction),
            index=False)


def byEVdoubles(rounds_to_predict):
    for prediction in range(rounds_to_predict):

        prediction = prediction + 1
        path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                              prediction)
        tableToRead = pandas.read_csv(path, parse_dates=True)

        tableToRead['------> Double - by expectancy of variance'] = ''
        listOfDoubles = []
        for index_1, row_1 in tableToRead.iterrows():
            for index_2, row_2 in tableToRead.iterrows():
                if index_1 > index_2:
                    probabiltyGame1 = tableToRead['Max Probability'][index_1]
                    probabiltyGame2 = tableToRead['Max Probability'][index_2]

                    probabilty = probabiltyGame1 * probabiltyGame2
                    odds = tableToRead['Winner Prediction'][index_1] * tableToRead['Winner Prediction'][index_2]
                    isWin = 'False'
                    if tableToRead['Win'][index_1] == 1:
                        if tableToRead['Win'][index_2] == 1:
                            isWin = 'True'
                    ExpectancyOfVariance = probabilty * odds - 1
                    touple = (index_2, index_1, probabilty, odds, isWin, ExpectancyOfVariance)
                    listOfDoubles.append(touple)

        tableToRead['Serial Number Game1'] = ''
        tableToRead['Serial Number Game2'] = ''
        tableToRead['Probability Double'] = ''
        tableToRead['Odds Double'] = ''
        tableToRead['Win Double'] = ''
        tableToRead['Expectancy of variance Double'] = ''
        tableToRead['------> Result double EV'] = ''
        tableToRead['Win Rate by E*V double'] = ''
        tableToRead['Win Rate by E*V double result'] = ''

        sortedT = Sort_Tuple_Doubles(listOfDoubles)
        sortedT.reverse()
        doubleIndex = 0
        listOfTuplesWithRepitions = []
        for game in range(10):
            doubleIndex = doubleIndex + 1
            tableToRead['Serial Number Game1'][doubleIndex] = sortedT[game][0]
            tableToRead['Serial Number Game2'][doubleIndex] = sortedT[game][1]
            tableToRead['Probability Double'][doubleIndex] = sortedT[game][2]
            tableToRead['Odds Double'][doubleIndex] = sortedT[game][3]
            tableToRead['Win Double'][doubleIndex] = sortedT[game][4]
            tableToRead['Expectancy of variance Double'][doubleIndex] = sortedT[game][5]

            # tuplesDouble
            if game < 5:
                tupleDoublesWithRep = ()
                if sortedT[game][4] == 'True':
                    odds = sortedT[game][3]
                    if game == 0:
                        tupleDoublesWithRep = (1, 20 * odds)
                    else:
                        tupleDoublesWithRep = (listOfTuplesWithRepitions[game - 1][0] + 1,
                                               listOfTuplesWithRepitions[game - 1][1] + 20 * odds)
                else:
                    if game == 0:
                        tupleDoublesWithRep = (0, 0)
                    else:
                        tupleDoublesWithRep = (
                        listOfTuplesWithRepitions[game - 1][0], listOfTuplesWithRepitions[game - 1][1])
                listOfTuplesWithRepitions.append(tupleDoublesWithRep)
        doubleIndex = doubleIndex + 2

        # region dif doubles
        listOfTuplesWithoutRepitions = []
        difCounter = 0
        CounterIndex = 0
        listOfSn = []
        while (difCounter < 10):
            sn1 = sortedT[CounterIndex][0]
            sn2 = sortedT[CounterIndex][1]
            if sn1 not in listOfSn and sn2 not in listOfSn:
                listOfSn.append(sn1)
                listOfSn.append(sn2)
                tableToRead['Serial Number Game1'][doubleIndex] = sortedT[CounterIndex][0]
                tableToRead['Serial Number Game2'][doubleIndex] = sortedT[CounterIndex][1]
                tableToRead['Probability Double'][doubleIndex] = sortedT[CounterIndex][2]
                tableToRead['Odds Double'][doubleIndex] = sortedT[CounterIndex][3]
                tableToRead['Win Double'][doubleIndex] = sortedT[CounterIndex][4]
                tableToRead['Expectancy of variance Double'][doubleIndex] = sortedT[CounterIndex][5]

                toCheck = sortedT[CounterIndex]
                # tuplesDouble
                if difCounter < 5:
                    testF = sortedT[CounterIndex][4]
                    tupleDoublesWithRep = ()
                    odds = sortedT[CounterIndex][3]
                    lastRoundGames = 0
                    lastRoundWins = 0
                    if difCounter != 0:
                        lastRoundGames = listOfTuplesWithoutRepitions[difCounter - 1][0]
                        lastRoundWins = listOfTuplesWithoutRepitions[difCounter - 1][1]

                    if sortedT[CounterIndex][4] == 'True':
                        if difCounter == 0:
                            tupleDoublesWithRep = (1, 20 * odds)
                        else:
                            tupleDoublesWithRep = (lastRoundGames + 1,
                                                   lastRoundWins + odds * 20)
                    else:
                        if difCounter == 0:
                            tupleDoublesWithRep = (0, 0)
                        else:
                            tupleDoublesWithRep = (lastRoundGames,
                                                   lastRoundWins)
                    listOfTuplesWithoutRepitions.append(tupleDoublesWithRep)

                doubleIndex = doubleIndex + 1
                difCounter = difCounter + 1
            CounterIndex = CounterIndex + 1

        excelDoubleIndex = 1
        gamesCounter = 1
        for tuple in listOfTuplesWithRepitions:
            if gamesCounter <= 5:
                # Win rate
                tableToRead.loc[excelDoubleIndex, 'Win Rate by E*V double'] = "Best {} Double games win rate".format(
                    gamesCounter)
                tableToRead.loc[excelDoubleIndex, 'Win Rate by E*V double result'] = str(
                    float(tuple[0] / gamesCounter) * 100) + "%"
                # Prize Win Rate
                tableToRead.loc[
                    excelDoubleIndex + 1, 'Win Rate by E*V double'] = "Prize rate for {} Double games is".format(
                    gamesCounter)
                tableToRead.loc[excelDoubleIndex + 1, 'Win Rate by E*V double result'] = float(
                    tuple[1] / (gamesCounter * 20))
                gamesCounter = gamesCounter + 1
                excelDoubleIndex = excelDoubleIndex + 2

        excelDoubleIndex = excelDoubleIndex + 1
        gamesCounter = 1
        for tuple in listOfTuplesWithoutRepitions:
            if gamesCounter <= 5:
                # Win rate
                tableToRead.loc[excelDoubleIndex, 'Win Rate by E*V double'] = "Best {} Double games win rate".format(
                    gamesCounter)
                tableToRead.loc[excelDoubleIndex, 'Win Rate by E*V double result'] = str(
                    float(tuple[0] / gamesCounter) * 100) + "%"
                # Prize Win Rate
                tableToRead.loc[
                    excelDoubleIndex + 1, 'Win Rate by E*V double'] = "Prize rate for {} Double games is".format(
                    gamesCounter)

                tableToRead.loc[excelDoubleIndex + 1, 'Win Rate by E*V double result'] = float(
                    tuple[1] / (gamesCounter * 20))

                gamesCounter = gamesCounter + 1
                excelDoubleIndex = excelDoubleIndex + 2

        tableToRead.to_csv(
            str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                                prediction),
            index=False)


def byEVtripples(rounds_to_predict):
    for prediction in range(rounds_to_predict):

        prediction = prediction + 1
        path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                              prediction)
        tableToRead = pandas.read_csv(path, parse_dates=True)

        tableToRead['------> Triple - by expectancy of variance'] = ''
        listOfDoubles = []
        for index_1, row_1 in tableToRead.iterrows():
            for index_2, row_2 in tableToRead.iterrows():
                for index_3, row_3 in tableToRead.iterrows():
                    if index_1 > index_2:
                        if index_2 > index_3:
                            probabiltyGame1 = tableToRead['Max Probability'][index_1]
                            probabiltyGame2 = tableToRead['Max Probability'][index_2]
                            probabiltyGame3 = tableToRead['Max Probability'][index_3]

                            probabilty = probabiltyGame1 * probabiltyGame2 * probabiltyGame3
                            odds = tableToRead['Winner Prediction'][index_1] * tableToRead['Winner Prediction'][
                                index_2] * tableToRead['Winner Prediction'][index_3]
                            isWin = 'False'
                            if tableToRead['Win'][index_1] == 1:
                                if tableToRead['Win'][index_2] == 1:
                                    if tableToRead['Win'][index_3] == 1:
                                        isWin = 'True'
                            ExpectancyOfVariance = probabilty * odds - 1
                            touple = (index_3, index_2, index_1, probabilty, odds, isWin, ExpectancyOfVariance)
                            listOfDoubles.append(touple)

        tableToRead['Triple Serial Number Game1'] = ''
        tableToRead['Triple Serial Number Game2'] = ''
        tableToRead['Triple Serial Number Game3'] = ''
        tableToRead['Triple Probability Double'] = ''
        tableToRead['Triple Odds Double'] = ''
        tableToRead['Triple Win Double'] = ''
        tableToRead['Triple Expectancy of variance Double'] = ''
        tableToRead['------> Result triple EV'] = ''
        tableToRead['Triple Win Rate by E*V'] = ''
        tableToRead['Triple Win Rate by E*V result'] = ''

        sortedT = Sort_Tuple_Triples(listOfDoubles)
        sortedT.reverse()
        doubleIndex = 0
        listOfTuplesWithRepitions = []
        for game in range(10):
            doubleIndex = doubleIndex + 1
            tableToRead['Triple Serial Number Game1'][doubleIndex] = sortedT[game][0]
            tableToRead['Triple Serial Number Game2'][doubleIndex] = sortedT[game][1]
            tableToRead['Triple Serial Number Game3'][doubleIndex] = sortedT[game][2]
            tableToRead['Triple Probability Double'][doubleIndex] = sortedT[game][3]
            tableToRead['Triple Odds Double'][doubleIndex] = sortedT[game][4]
            tableToRead['Triple Win Double'][doubleIndex] = sortedT[game][5]
            tableToRead['Triple Expectancy of variance Double'][doubleIndex] = sortedT[game][6]

            # tuplesDouble
            if game < 5:
                tupleDoublesWithRep = ()
                if sortedT[game][5] == 'True':
                    odds = sortedT[game][4]
                    if game == 0:
                        tupleDoublesWithRep = (1, 30 * odds)
                    else:
                        tupleDoublesWithRep = (listOfTuplesWithRepitions[game - 1][0] + 1,
                                               listOfTuplesWithRepitions[game - 1][1] + 30 * odds)
                else:
                    if game == 0:
                        tupleDoublesWithRep = (0, 0)
                    else:
                        tupleDoublesWithRep = (
                            listOfTuplesWithRepitions[game - 1][0], listOfTuplesWithRepitions[game - 1][1])
                listOfTuplesWithRepitions.append(tupleDoublesWithRep)
        doubleIndex = doubleIndex + 2

        # region dif doubles
        listOfTuplesWithoutRepitions = []
        difCounter = 0
        CounterIndex = 0
        listOfSn = []
        while (difCounter < 10):
            sn1 = sortedT[CounterIndex][0]
            sn2 = sortedT[CounterIndex][1]
            sn3 = sortedT[CounterIndex][2]
            if sn1 not in listOfSn and sn2 not in listOfSn and sn3 not in listOfSn:
                listOfSn.append(sn1)
                listOfSn.append(sn2)
                listOfSn.append(sn3)
                tableToRead['Triple Serial Number Game1'][doubleIndex] = sortedT[CounterIndex][0]
                tableToRead['Triple Serial Number Game2'][doubleIndex] = sortedT[CounterIndex][1]
                tableToRead['Triple Serial Number Game3'][doubleIndex] = sortedT[CounterIndex][2]
                tableToRead['Triple Probability Double'][doubleIndex] = sortedT[CounterIndex][3]
                tableToRead['Triple Odds Double'][doubleIndex] = sortedT[CounterIndex][4]
                tableToRead['Triple Win Double'][doubleIndex] = sortedT[CounterIndex][5]
                tableToRead['Triple Expectancy of variance Double'][doubleIndex] = sortedT[CounterIndex][6]

                toCheck = sortedT[CounterIndex]
                # tuplesDouble
                if difCounter < 5:
                    testF = sortedT[CounterIndex][5]
                    tupleDoublesWithRep = ()
                    odds = sortedT[CounterIndex][4]
                    lastRoundGames = 0
                    lastRoundWins = 0
                    if difCounter != 0:
                        lastRoundGames = listOfTuplesWithoutRepitions[difCounter - 1][0]
                        lastRoundWins = listOfTuplesWithoutRepitions[difCounter - 1][1]

                    if sortedT[CounterIndex][5] == 'True':
                        if difCounter == 0:
                            tupleDoublesWithRep = (1, 30 * odds)
                        else:
                            tupleDoublesWithRep = (lastRoundGames + 1,
                                                   lastRoundWins + odds * 30)
                    else:
                        if difCounter == 0:
                            tupleDoublesWithRep = (0, 0)
                        else:
                            tupleDoublesWithRep = (lastRoundGames,
                                                   lastRoundWins)
                    listOfTuplesWithoutRepitions.append(tupleDoublesWithRep)

                doubleIndex = doubleIndex + 1
                difCounter = difCounter + 1
            CounterIndex = CounterIndex + 1

        excelDoubleIndex = 1
        gamesCounter = 1
        for tuple in listOfTuplesWithRepitions:
            if gamesCounter <= 5:
                # Win rate
                tableToRead.loc[excelDoubleIndex, 'Triple Win Rate by E*V'] = "Best {} Double games win rate".format(
                    gamesCounter)
                tableToRead.loc[excelDoubleIndex, 'Triple Win Rate by E*V result'] = str(
                    float(tuple[0] / gamesCounter) * 100) + "%"
                # Prize Win Rate
                tableToRead.loc[
                    excelDoubleIndex + 1, 'Triple Win Rate by E*V'] = "Prize rate for {} Double games is".format(
                    gamesCounter)
                tableToRead.loc[excelDoubleIndex + 1, 'Triple Win Rate by E*V result'] = float(
                    tuple[1] / (gamesCounter * 30))
                gamesCounter = gamesCounter + 1
                excelDoubleIndex = excelDoubleIndex + 2

        excelDoubleIndex = excelDoubleIndex + 1
        gamesCounter = 1
        for tuple in listOfTuplesWithoutRepitions:
            if gamesCounter <= 5:
                # Win rate
                tableToRead.loc[excelDoubleIndex, 'Triple Win Rate by E*V'] = "Best {} Double games win rate".format(
                    gamesCounter)
                tableToRead.loc[excelDoubleIndex, 'Triple Win Rate by E*V result'] = str(
                    float(tuple[0] / gamesCounter) * 100) + "%"
                # Prize Win Rate
                tableToRead.loc[
                    excelDoubleIndex + 1, 'Triple Win Rate by E*V'] = "Prize rate for {} Double games is".format(
                    gamesCounter)

                tableToRead.loc[excelDoubleIndex + 1, 'Triple Win Rate by E*V result'] = float(
                    tuple[1] / (gamesCounter * 30))

                gamesCounter = gamesCounter + 1
                excelDoubleIndex = excelDoubleIndex + 2

        tableToRead.to_csv(
            str(currentDirectory) + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                                prediction),
            index=False)


def winRateToAllSeason(rounds_to_predict):
    finalTable = []
    df = pandas.DataFrame(finalTable)
    for prediction in range(rounds_to_predict):
        prediction = prediction + 1
        path = currentDirectory + '{}outputs{}predictions-Week-{}.csv'.format(slashDirection, slashDirection,
                                                                              prediction)
        tableToRead = pandas.read_csv(path, parse_dates=True)

        single = tableToRead.iloc[:, 27:29].copy()
        double = tableToRead.iloc[:, 37:39].copy()
        triple = tableToRead.iloc[:, 48:50].copy()

        df["Week {} Single {}---->".format(prediction, prediction)] = ""
        df = pandas.concat([df, single], axis=1, sort=False)
        df["Double {} ------------>".format(prediction)] = ""
        df = pandas.concat([df, double], axis=1, sort=False)
        df["Triple {} ------------>".format(prediction)] = ""
        df = pandas.concat([df, triple], axis=1, sort=False)

    df.to_csv(currentDirectory + '{}outputs{}Avg.csv'.format(slashDirection, slashDirection), index=False)


if __name__ == '__main__':
    # byEVsingle(23)
    # byEVdoubles(23)
    # byEVtripples(23)
    winRateToAllSeason(23)
