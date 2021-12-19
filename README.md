# Hoopscrapper
Hoopscrapper is a Python package to scrape data from https://www.basketball-reference.com/. Its main goal is to automate NBA data collection. With hoopscrapper, you can get NBA player statistics and team records from any year without downloading anything. For the details of the process, read my [article](https://medium.com/@mraihanafiandi/scraping-basketball-reference-data-using-python-f321c3f2903e) on Medium.
## Installation
Use the package manager pip to install hoopscrapper like below.

```bash
!pip install git+https://github.com/raihan0824/hoopscrapper
```

## Usage
Features:
- hoopscrapper.awards.mvp(season) --> Generate the name of NBA MVP in the determined season
- hoopscrapper.awards.allstar(season) --> Generate the list of NBA All-Star players in the determined season
- hoopscrapper.get_data.team_records(season) --> Generate the winning and losing records of NBA team in the determined season
- hoopscrapper.get_data.single(season,stats) --> Generate NBA players' stats in the determined season. Argument stats are:
  - per_game
  - per_minute
  - per_poss
  - totals
  - advanced
  - shooting
  - adj_shooting
  - play-by-play
- hoopscrapper.get_data.multiple(start_year,end_year,stats) --> Generate NBA players' stats in multiple season.

#### Demo of some of the features
```python
from hoopscrapper import hoopscrapper

mvp_2020 = hoopscrapper.awards.mvp(2020)
print(mvp_2020) # print the name of NBA MVP in 2020 season

player_stats_2020 = hoopscrapper.awards.single(2020,'per_game')
print(player_stats_2020) # print the dataframe contains NBA player per game statistics in 2020 season

player_stats_1980_2020 = hoopscrapper.awards.multiple(1980,2020,'per_game')
print(player_stats_1980_2020) # print the dataframe contains NBA player per game statistics from 1980 to 2020 season
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
