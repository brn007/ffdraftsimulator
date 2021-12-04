import pandas as pd

rankings_list = ['rankings2020.csv', 'rankings2019.csv',
                 'rankings2018.csv', 'rankings2017.csv']
points_list = ['points2020.csv', 'points2019.csv',
               'points2018.csv', 'points2017.csv']

team_positions = {
    'QB': 1,
    'RB': 2,
    'WR': 2,
    'RB/WR': 1,
    'TE': 1,
    'K': 1,
    'DST': 1
}

for j in range(len(rankings_list)):
    rankings_csv = 'rankings/' + rankings_list[j]
    points_csv = 'points/' + points_list[j]

    df_rankings = pd.read_csv(rankings_csv)
    df_points = pd.read_csv(points_csv)
    df_combined = pd.merge(df_rankings, df_points,
                           on='NAME', how='left').fillna('NA')

    team_comp = [dict(team_positions) for i in range(12)]
    teams = [[] for i in range(12)]

    # 0 = name, 1 = position, 2 = ranking, 3 = points
    df_list = df_combined.values.tolist()
    for round in range(9):
        if round % 2 == 0:
            for team in range(12):
                for i in range(len(df_list)):
                    position = df_list[i][1]
                    position_count = team_comp[team][position]
                    if position_count > 0:
                        team_comp[team][position] -= 1
                        teams[team].append(
                            (df_list[i][0], df_list[i][1], df_list[i][3]))
                        df_list.pop(i)
                        break
                    elif (position == 'RB' or position == 'WR') \
                            and team_comp[team]['RB/WR'] > 0:
                        team_comp[team]['RB/WR'] -= 1
                        teams[team].append(
                            (df_list[i][0], df_list[i][1], df_list[i][3]))
                        df_list.pop(i)
                        break
        else:
            for team in range(11, -1, -1):
                for i in range(len(df_list)):
                    position = df_list[i][1]
                    position_count = team_comp[team][position]
                    if position_count > 0:
                        team_comp[team][position] -= 1
                        teams[team].append(
                            (df_list[i][0], df_list[i][1], df_list[i][3]))
                        df_list.pop(i)
                        break
                    elif (position == 'RB' or position == 'WR') \
                            and team_comp[team]['RB/WR'] > 0:
                        team_comp[team]['RB/WR'] -= 1
                        teams[team].append(
                            (df_list[i][0], df_list[i][1], df_list[i][3]))
                        df_list.pop(i)
                        break
    for team in range(12):
        for pos in team_comp[team]:
            while team_comp[team][pos] > 0:
                team_comp[team][pos] -= 1
                teams[team].append(('NA', pos, 'NA'))
    for team in range(12):
        pd.DataFrame(data=teams[team], columns=['NAME', 'POSITION', 'POINTS']).to_csv(
            str(2020 - j) + '/team' + str(team+1) + '.csv', index=False)
