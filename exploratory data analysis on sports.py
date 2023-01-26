#!/usr/bin/env python
# coding: utf-8

# ![sparks.jpg](attachment:sparks.jpg)

# # Author - Pagare Maithili
# ## The Sparks Foundation - Data Science and Business Analysis
# ### Task 5 - Exploratory Data Analysis - Sports
# 
# ### Problems
#     1.As a sports analysts, find out the most successful teams, players and factors contributing win or loss of a team.
#     2.Suggest teams or players a company should endorse for its products.
# 
# ### Data Insights
#     1.2011, 2012, and 2013 has highest number of matches
#     2.Mumbai Indians is the top IPL team and Chennai Superkings second.
#     3.Bowl First team have more chance of winning.
#     4.Winning toss team choose to feild first.
#     5.In finals Field first have more chance of winning
#     6.In finals toss winning choose field first.
#     7.CH gayle and AB de villers are the top IPL players
#     8.Shikar Dhawan hit most Four in IPL
#     9.CH gayle hit most Six in IPL
#     10.Virat Kholi hit maximum runs in IPL
#     11.Sk Raina played maximum matchs
#     12.Caught Out is most common type of out in IPL
#     13.SL Malinga take maximum wickets
#     
# ### Dataset: https://bit.ly/34SRn3b
#     
# #### IMPORTING LIBRARIES:

# In[1]:


import os 
import csv
import pandas as pd
import numpy  as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# #### Data Uploading 

# In[2]:


file_del = r"F:\internship 1\Indian Premier League\deliveries.csv"
file_mat = r"F:\internship 1\Indian Premier League\matches.csv"

data_del = pd.read_csv(file_del)
data_mat = pd.read_csv(file_mat)


# In[3]:


data_del.head()


# In[4]:


data_mat.head()


# #### Null Values

# In[5]:


null_del = data_del.isnull()
sum_del = null_del.sum()
sum_del


# In[6]:


null_mat = data_mat.isnull()
sum_mat = null_mat.sum()
sum_mat


# In[7]:


data_season = data_mat[['id','season','winner']]

data_complete = data_del.merge(data_season, how ='inner', left_on = 'match_id',right_on = 'id')


# In[8]:


data_mat.columns.values


# In[9]:


data_mat = data_mat.drop(columns = ['umpire3'], axis = 1)

data_mat.head()


# In[10]:


winner_season = data_mat.groupby('season')['winner'].value_counts()

winner_season


# ## Counts Number of Matches per Season 

# In[11]:


plt.figure(figsize = (18,9))
sns.countplot(x = 'season', data = data_mat)


# ## Maximum Winnings
# 

# In[34]:


plt.figure(figsize = (18,9))
sns.countplot(x = 'winner', data = data_mat)


# ## Winning on the bases of First Bat or First Bowl

# In[13]:


data_mat['win_by'] = np.where(data_mat['win_by_runs']> 0,'Bat first', 'Bowl first')


# In[14]:


win = data_mat.win_by.value_counts()
x = win.values
labels = win.index

plt.pie(x , labels = labels, autopct = '%1.1f%%')


# In[15]:


plt.figure(figsize = (18,9))
sns.countplot(x="season", hue ="win_by",data=data_mat)


# ## Winning on the bases of Toss Decision
# 

# In[16]:


toss = data_mat.toss_decision.value_counts()
x = toss.values
labels = toss.index

plt.pie(x, labels = labels, autopct = '%1.1f%%')


# In[17]:


plt.figure(figsize = (18,9))
sns.countplot(x='season', hue = 'toss_decision', data = data_mat).set_title('Winning by  Toss Decision')


# ## Season wise Winners
#  

# In[18]:


final_winner = data_mat.drop_duplicates(subset = ['season'], keep = 'last')
final_winner[['season', 'winner']].reset_index(drop = True).sort_values('season')


# In[36]:


plt.figure(figsize = (16,8))
x = data_mat.player_of_match.value_counts()[:10].index
y = data_mat.player_of_match.value_counts()[:10]
sns.barplot(x,y).set_title('Top Players in the IPL')


# ## City wise Winning
# 

# In[19]:


final_winner.groupby(['city','winner']).size()


# ## Season's won by Teams
# 

# In[20]:


final_winner['winner'].value_counts()


# In[21]:


final_winner[['toss_winner', 'toss_decision', 'winner']].reset_index(drop = True)


# ## Man of the Match
# 

# In[22]:


final_winner[['winner','player_of_match']].reset_index(drop = True)


# ## Counting Numbers of Fours and Sixs Team wise and Player Wise

# In[23]:


# Counting fours team wise
four_data = data_complete[data_complete['batsman_runs'] == 4]
four_data.groupby('batting_team')['batsman_runs'].agg([('runs by fours','sum'),('four', 'count')])


# In[24]:


# Counting four Player wise

x = four_data.groupby('batsman')['batsman_runs'].agg([('four','count')]).reset_index().sort_values('four', ascending = 0)
x.iloc[:10,:].plot('batsman','four', kind = 'bar')
plt.title('Number of fours hit by players')


# In[25]:


x = four_data.groupby('season')['batsman_runs'].agg([('four','count')]).reset_index().plot('season', 'four', kind = 'bar')
plt.title('Number of fours hit in seasons')


# In[26]:


# Counting Sixes hit by teams

six_data = data_complete[data_complete['batsman_runs'] == 6]
six_data.groupby('batting_team')['batsman_runs'].agg([('run by six', 'sum'), ('sixes','count')])


# In[27]:


# Counting six hit by players

x = six_data.groupby('batsman')['batsman_runs'].agg([('six', 'count')]).reset_index().sort_values('six', ascending = 0)
x.iloc[:10,:].plot('batsman','six', kind = 'bar')
plt.title('Number of six hit by players')


# In[28]:


# Counting six hit by in seasons

x = six_data.groupby('season')['batsman_runs'].agg([('six','count')]).reset_index().plot('season','six', kind = 'bar')
plt.title('Number of six hit is each season')


# ## Top 10 leading run scorer in IPL
#  

# In[29]:


batsman_score = data_del.groupby('batsman')['batsman_runs'].agg(['sum']).reset_index().sort_values('sum',ascending = False).reset_index(drop = True)
batsman_score = batsman_score.rename(columns = {'sum': 'batsman_runs'})
print('Top 10 Leading Run  Scores in IPL')
batsman_score.iloc[:10,:]


# In[30]:


no_match = data_del[['match_id','player_dismissed']]
no_match = no_match.groupby('player_dismissed')['match_id'].count().reset_index().sort_values(by = 'match_id',ascending = False).reset_index(drop = True)

no_match.columns = ['batsman','No_of_Matches']
no_match.head()


# In[31]:


batsman_score = data_del.groupby('batsman')['batsman_runs'].agg(['sum']).reset_index().sort_values('sum',ascending = False).reset_index(drop = True)
batsman_score = batsman_score.rename(columns = {'sum': 'batsman_runs'})
print('Top 10 Leading Run  Scores in IPL')
batsman_score.iloc[:10,:]


# In[32]:


no_match = data_del[['match_id','player_dismissed']]
no_match = no_match.groupby('player_dismissed')['match_id'].count().reset_index().sort_values(by = 'match_id',ascending = False).reset_index(drop = True)

no_match.columns = ['batsman','No_of_Matches']
no_match.head()


# ## Most wicket taking by bowlers
# 

# In[33]:


wicket_data = data_del.dropna(subset = ['dismissal_kind'])
wicket_data = wicket_data[~wicket_data['dismissal_kind'].isin(['run_out','retired hurt','obstructing the field'])]

wicket_data.groupby('bowler')['dismissal_kind'].agg(['count']).reset_index().sort_values('count', ascending = False).reset_index(drop = True).iloc[:10,:]


# ## THANK YOU
