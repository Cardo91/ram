import pandas as pd
import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('C:/db/rick_and_morty.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS imdb
             (episode_name TEXT PRIMARY KEY, rating REAL, season INTEGER)''')

# Lista de capitulos a scrapear
seasons = [1, 2, 3, 4, 5, 6]

for season in seasons:
    url = f'https://www.imdb.com/title/tt2861424/episodes?season={season}'
    response = requests.get(url)
    
    # Chequeo de conexión
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        episode_name = []
        rating = []
        season_number = season
        
        episode_data = soup.findAll('div', attrs={'class': ['list_item odd', 'list_item even']})
        for store in episode_data:
            name = store.strong.a.text
            episode_name.append(name)
            ratings = store.find('span', class_ = 'ipl-rating-star__rating').text 
            rating.append(float(ratings))

        episode_df = pd.DataFrame({'episode_name': episode_name,'rating': rating})
        episode_df['season'] = season_number
        
        print(f'Season {season}:')
        print(episode_df)
        
        for i in range(len(episode_name)):
            c.execute("INSERT OR REPLACE INTO imdb VALUES (?, ?, ?)", (episode_name[i], rating[i], season_number))
        conn.commit()
        
conn.close()
