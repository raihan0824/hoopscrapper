import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import re
import string
from urllib.request import urlopen
import pandas as pd
pd.options.mode.chained_assignment = None 

class awards:

  def mvp(season):
    season = str(season)
    url = 'https://www.basketball-reference.com/awards/mvp.html'
    table_html = str(BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = 'mvp_NBA')[0])

    df = pd.read_html(table_html)[0]
    df.columns = df.columns.droplevel(0)
    df = df[['Season','Player']]
    df['Season'][0]

    for i in range(len(df)):
      df['Season'][i] = df['Season'][i][0:2] + df['Season'][i][5:7]

    mvp_lists = df.values.tolist()

    for data in mvp_lists:
      if season in data[0]:
        return data[1]

  def allstar(season):
    if season == 1999:
      print('No All Star game in 1999 season') # No all star game in 1999 season

    else:  
      url = f'https://www.basketball-reference.com/allstar/NBA_{season}.html'
      name_html = BeautifulSoup(urlopen(url),'html.parser').findAll('a', string = re.compile('[a-z]'), href = re.compile('^/players/.+'), title= False) 
      names = [names.text for names in name_html]
      names = list(set(names))

      return names


class get_data:

  def team_records(season):
    url = f'https://www.basketball-reference.com/leagues/NBA_{season}.html'
    table_html = BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = re.compile('advanced-team'))[0].findAll('a')
    table_html
    team_name = []
    team_abrv = []

    for html in table_html:
      abrv = html.get('href')
      pattern = re.compile(r'([A-Z]{3})')
      team_abrv.append(pattern.search(abrv).group())
      team_name.append(html.text)
    team_abrv = list(zip(team_name,team_abrv))

    table = BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = re.compile('advanced-team'))
    team_records = pd.read_html(str(table))[0]
    team_records = team_records.apply(pd.to_numeric, errors = 'coerce').fillna(team_records)
    team_records.columns = team_records.columns.droplevel(0)
    team_records = team_records.drop('Rk', 1) # drop Rk columns
    team_records = team_records.loc[:,['Team','W','L']] # only select team names and its winning and losing records
    team_records.Team = team_records.Team.str.replace('*','') # remove team names asterisk

    team_names = [i[0] for i in team_abrv] # get list of team names
    team_abbrevation = [i[1] for i in team_abrv] # get list of team abbrevation
    for team,i in zip(team_records.Team,team_records.index.values): # the mapping process
      if team in team_names:
        idx = (team_names.index(team))
        team_records.Team[i] = team_abbrevation[idx]
      else:
        pass

    return team_records

  def single(season,stats):
    print('Loading',season,'data...')
    url = f'https://www.basketball-reference.com/leagues/NBA_{season}_{stats}.html'
    table_html = BeautifulSoup(urlopen(url), 'html.parser').findAll('table')

    df = pd.read_html(str(table_html))[0]
    df = df.drop(df[df.Player == 'Player'].index) # drop row contains table header
    df = df.drop('Rk', 1) # drop Rk columns
    df.Player = df.Player.str.replace('*','') # remove asterisk on player's name
    df.insert(0,'Season',season) # insert season column
    df = df.apply(pd.to_numeric, errors='coerce').fillna(df) # convert non string values to numeric

    # OPTIONAL
    # If you want to put all-star and mvp column to the player stats data frame, open this hash. Note that it will slows the process.

    # Insert all-star column
    df['All_Star'] = 0
    if season == 1999:
      pass # No all star game in 1999 season
    else:
      all_star = awards.allstar(season)
      df.loc[df['Player'].isin(all_star), 'All_Star'] = 1  # change all star column to 1 if the player is in the all star list
    df[df.All_Star==1]

    # Insert MVP column
    df['MVP'] = 0
    mvp = awards.mvp(season)
    df.loc[df['Player'] == mvp, 'MVP'] = 1 
    df[df.MVP == 1]

    # Insert team records
    team_records_list = get_data.team_records(season).values.tolist()
    df['team_win'] = 0
    df['team_lose'] = 0
    teams = [i[0] for i in team_records_list] # get list of team names
    win = [i[1] for i in team_records_list] # get list of team winning records
    lose = [i[2] for i in team_records_list] # get list of team losing records

    for team,i in zip(df.Tm,(df.Tm.index.values)): # there's a missing index so the iteration is going through the index values
      if team in teams: 
        idx = (teams.index(team)) # get index in the team_records_list
        df.team_win[i]= win[idx] # add win records to df
        df.team_lose[i]= lose[idx] # add win records to df
      else:
        df.team_win[i] = 0
        df.team_lose[i] = 0

    return df


  def multiple(start_year,end_year,stats):
    df = get_data.single(start_year,stats)
    while start_year < end_year:
      start_year = start_year + 1
      df = df.append(get_data.single(start_year,stats))

    return df
