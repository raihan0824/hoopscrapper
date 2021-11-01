class hoopscrapper:


  class awards:

    def mvp(season):
      season = str(season)
      url = 'https://www.basketball-reference.com/awards/mvp.html'
      htmls = BeautifulSoup(urlopen(url), 'html.parser').findAll('table')
      df = pd.read_html(str(htmls[0]))[0] # read table
      df.columns = df.columns.droplevel(0)
      df = df[['Season','Player']]
      
      for i in range(len(df)):
        if df['Season'][i] == '1999-00':
          df['Season'][i] = '2000'
        else:
          df['Season'][i] = df['Season'][i][0:2] + df['Season'][i][5:7]
          mvp_lists = df.values.tolist()

      for data in mvp_lists:
        if season in data[0]:
          return data[1]

    def allstar(season):
      if season == 1999:
        print('No All Star game in 1999 season') # No all star game in 1999 season
      else:
        season = str(season)
        url = 'https://www.basketball-reference.com/allstar/'
        htmls = BeautifulSoup(urlopen(url),'html.parser').findAll('a', string=re.compile('(^[0-9]{4}$)'), href = re.compile('^/allstar/NBA') ) # open bball reference html with a tags,string contains year format, and href contains '/allstar
        seasons = []
        seasons_links = [] 

        for html in htmls:
          seasons.append(html.text) # get url titles (ex: 2017)
          seasons_links.append(html.get('href')) # get url extensions
        seasons_data = list(zip(seasons,seasons_links))
        
        for data in seasons_data:
          if season in data[0]:
            extension = data[1] # get extension for determined season

        url = 'https://www.basketball-reference.com' + extension
        # print('All Star URL:',url)

        name_html = BeautifulSoup(urlopen(url),'html.parser').findAll('a', string = re.compile('[a-z]'), href = re.compile('^/players/.+'), title= False) # get html that contains all star names
        names = [list(set(name.text for name in name_html))][0] # create all star name list and remove duplicates with set function
        
        return names 



  class get_data:

    def team_records(season):
      url = 'https://www.basketball-reference.com/leagues/NBA_{}.html'.format(season)
      htmls = BeautifulSoup(urlopen(url), 'html.parser').findAll('table', id = re.compile('advanced-team'))[0].findAll('a')
      # get team abbrevation
      team_name = []
      team_abrv = []
      for html in htmls:
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
      team_records = team_records.loc[:,['Team','W','L']]
      team_records.Team = team_records.Team.str.replace('*','')
      team_records

      team_names = [i[0] for i in team_abrv] # get list of team names
      team_abbrevation = [i[1] for i in team_abrv] # get list of team abbrevation
      for team,i in zip(team_records.Team,team_records.index.values): 
        if team in team_names:
          idx = (team_names.index(team))
          team_records.Team[i] = team_abbrevation[idx]
        else:
          pass
      return team_records

    def single(season,stats):
      # stats: per_game, totals, per_minute,per_poss,adj_shooting,advanced,play-by-play,shooting
      season = str((season)-1) + '-' + str(season)[2:5] # convert 20yy to 20xx-yy
      url = 'https://www.basketball-reference.com/leagues/'
      htmls = BeautifulSoup(urlopen(url),'html.parser').findAll('a',href=re.compile('/leagues')) # open bball reference html with a tags and href contains '/leagues
      seasons = []
      url_extensions = []  

      for html in htmls:
        url_extensions.append(html.get('href')) # get url extensions
        seasons.append(html.text) # get url titles (ex: 2016-17)
      seasons_links = ['https://www.basketball-reference.com' + extension for extension in url_extensions] # get url links
      seasons_data = list(zip(seasons,seasons_links)) # zip url titles and url links together

      for data in seasons_data:
        if season in data[0]:
          url = data[1] # get url for determined season
      print('Loading',season,'data')
      soup = BeautifulSoup(urlopen(url),'html.parser') # open html for determined url
      season_html = soup.findAll('a',href=re.compile(stats+'.html'))[0] # get html with a tags and contains determined stats
      season_url = season_html.get('href') # get url extension
      url = 'https://www.basketball-reference.com' + season_url
      soup = BeautifulSoup(urlopen(url),'html.parser') # get url link
      table_html = soup.findAll('table',id=re.compile(stats)) # open table in the page

      df = pd.read_html(str(table_html))[0] # read table

      # insert season column
      df.insert(0,'Season','') 
      if season == '1999-00':
        df['Season'] = '2000'
        season = '2000'
      else:
        df['Season'] = season[0:2] + season[5:7] # convert to the original season name
        season = season[0:2] + season[5:7]

      df = df.drop(df[df.Player == 'Player'].index) # drop the repetitive table names
      df = df.drop('Rk', 1) # drop Rk columns
      df.Player = df.Player.str.replace('*','') # remove asterisk on player's name

      # Convert non string values to float
      df = df.apply(pd.to_numeric, errors='coerce').fillna(df)

      # Adding all star column
      df['All_Star'] = 0
      if season == '1999':
        pass # No all star game in 1999 season
      else:
        all_star = hoopscrapper.awards.allstar(season)
        df.loc[df['Player'].isin(all_star), 'All_Star'] = 1  # change all star column to 1 if the player is in the all star list

      # Adding mvp column
      df['MVP'] = 0
      mvp = hoopscrapper.awards.mvp(season)
      df.loc[df['Player'] == mvp, 'MVP'] = 1 # change MVP column to 1 if the player is in the MVP of the season

      # Adding team records and nba total game in season (optional)
      team_records_list = hoopscrapper.get_data.team_records(season).values.tolist()
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
      df

      return df

    def multiple(start_year,end_year,stats):
      df = hoopscrapper.get_data.single(start_year,stats)
      while start_year < end_year:
        start_year = start_year + 1
        df = df.append(hoopscrapper.get_data.single(start_year,stats))
      return df


# hoopscrapper.get_data.single(2020,'per_game')
# start_time = datetime.now()
# hoopscrapper.get_data.multiple(2018,2021,'per_game')
# end_time = datetime.now()
# print('Duration: {}'.format(end_time - start_time))
