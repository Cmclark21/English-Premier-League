#!/usr/bin/env python
# coding: utf-8

# ## Project Coding

# ### Importing Pandas and our data

# In[ ]:


import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('results.csv')


# ### Checking how our data looks like.

# In[ ]:


df.head()


# ### Creating a list of all the teams that have ever played in the premier league in the past 12 years

# In[ ]:


home_team_list = []
for team in df.home_team:
    if team not in home_team_list:
        home_team_list.append(team)
    else:continue
print(home_team_list)
print(len(home_team_list))


# ### Creating a table of Arsenal wins against Chelsea and counting the number of wins

# In[ ]:


team_1_home_win = df.loc[(df['result'] == 'H') & (df['home_team'] == 'Arsenal') & (df['away_team'] == 'Chelsea')]
team_1_away_win = df.loc[(df['result'] == 'A') & (df['home_team'] == 'Chelsea') & (df['away_team'] == 'Arsenal')]
team_1_total = pd.merge(team_1_home_win, team_1_away_win, how = 'outer')

print(team_1_total['result'].count())

team_1_total


# ### Creating a table of Chelsea wins against Arsenal and counting the number of wins
# 

# In[ ]:


team_2_home_win = df.loc[(df['result'] == 'H') & (df['home_team'] == 'Chelsea') & (df['away_team'] == 'Arsenal')]
team_2_away_win = df.loc[(df['result'] == 'A') & (df['home_team'] == 'Arsenal') & (df['away_team'] == 'Chelsea')]
team_2_total = pd.merge(team_2_home_win, team_2_away_win, how = 'outer')

print(team_2_total['result'].count())

team_2_total


# ### Data frame showing all the draws between the two teams

# In[ ]:



home_draws = df.loc[(df['result'] == 'D') & (df['home_team'] == 'Arsenal') & (df['away_team'] == 'Chelsea')]
away_draws = df.loc[(df['result'] == 'D') & (df['home_team'] == 'Chelsea') & (df['away_team'] == 'Arsenal')]
total_draws = pd.merge(home_draws, away_draws, how = 'outer')
print(total_draws['result'].count())

total_draws


# ### Dataframe showing all the games between the two teams

# In[ ]:


total_wins = pd.merge(team_1_total,team_2_total ,how="outer")
total_games = pd.merge(total_wins, total_draws, how='outer')
print(total_games['result'].count())

total_games.sort_values('season')


# ### Adding a new column

# In[ ]:



df.loc[df.result == 'H', 'winning_team'] = df.home_team
df.loc[df.result == 'A', 'winning_team'] = df.away_team
df.loc[df.result == 'D', 'winning_team'] = 'Draw'
df.head(20)


# ### Plotting a line graph with years on x-axis and wins on y-axis

# In[ ]:


def team_win_over_time(team):
    df_w = df.loc[df['winning_team'] == team]
    
    total_wins_per_season = {}
    
    for year in df_w['season']:
        if year not in total_wins_per_season:
            total_wins_per_season[year] = 1
        else:
            total_wins_per_season[year] += 1
    
    df_w2 = pd.DataFrame.from_dict(total_wins_per_season, orient='index', columns= ['%s wins per season'%team])
                                                                                    
    df_w2.plot.line()
    plt.title(team + ' wins by season')
    plt.xlabel('Seasons')
    plt.ylabel('Wins')

    


# In[ ]:


team1= 'Arsenal'
team2= 'Manchester United'
team_win_over_time(team1)
team_win_over_time(team2)


# ### Visulaization comparing the goal scoring against time for the two teams 

# In[ ]:


total_games = total_games.sort_values('season')
total_games.plot(kind='bar', x='season')
plt.title("Number of goals for the winning Team throughout all seasons")
plt.xlabel("Seasons")
plt.ylabel("Number of goals")
plt.legend(["Arsenal", "Chelsea"])


# ### Creating a function that can do everything above for teams of choice

# In[ ]:


def predictor(first_team,second_team):
    df1 = df.loc[(df['result'] == 'H') & (df['home_team'] == first_team) & (df['away_team'] == second_team)]
    df2 = df.loc[(df['result'] == 'A') & (df['home_team'] == second_team) & (df['away_team'] == first_team)]
    team_1_win = pd.merge(df2, df1, how = 'outer')
    team_1_wins = team_1_win['result'].count()

    df3 = df.loc[(df['result'] == 'H') & (df['home_team'] == second_team) & (df['away_team'] == first_team)]
    df4 = df.loc[(df['result'] == 'A') & (df['home_team'] == first_team) & (df['away_team'] == second_team)]
    team_2_win = pd.merge(df3, df4, how = 'outer')
    team_2_wins = team_2_win['result'].count()
 

    df5 = df.loc[(df['result'] == 'D') & (df['home_team'] == first_team) & (df['away_team'] == second_team)]
    df6 = df.loc[(df['result'] == 'D') & (df['home_team'] == second_team) & (df['away_team'] == first_team)]
    team_draws = pd.merge(df5, df6, how = 'outer')
    team_draw = team_draws['result'].count()
    

    total_wins = pd.merge(team_1_win,team_2_win ,how="outer")
    total_games = pd.merge(total_wins, team_draws, how='outer')
    total_game = total_games['result'].count()
    if total_game == 0:
        print("There is no past record for these 2 teams playing in the past 12 years.")
    else:
        print (" ")
        print(first_team, " has won ", str(team_1_wins), " times out of the " ,str(total_game)," games it has played against", second_team,' in the past 12 years ')
        print (" ")
        print(second_team, " has won ", str(team_2_wins), " times out of the",str(total_game)," games it has played against", first_team, "in the past 12 years ")
        print (" ")
        print('They have drawed ',team_draw, " times in the past 12 years")
        print (" ")
    
    
    total_wins = total_games.sort_values('season')
    total_wins.plot(kind='bar', x='season')
    plt.title("Number of goals for " + second_team + " and " + first_team + " throughout all seasons")
    plt.xlabel("Seasons")
    plt.ylabel("Number of goals")
    plt.legend([first_team, second_team])
    
    if team_1_wins > team_2_wins:
        print("Based on the results, if these two teams play agaisnt each other again", first_team, "is more likely to win")
        
    elif team_2_wins > team_1_wins:
        print("Based on the results, if these two teams play agaisnt each other again", second_team, "is more likely to win")

    
   


# ### Calling Function

# In[ ]:


first_team = input("Enter the first team name: ")
if first_team not in home_team_list:
    print('This team is not in Premier League, try another team:')

second_team = input("Enter the second team name: ")
if second_team not in home_team_list:
    print('This team is not in Premier League, try another team:')

predictor(first_team, second_team)
team_win_over_time(first_team)
team_win_over_time(second_team)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




