import sqlite3
import json
from graphqlclient import GraphQLClient

client = GraphQLClient('https://rickandmortyapi.com/graphql')

query ='''
    query getAllEpisodes($page: Int!) {
        episodes(page: $page) {
            info {
                next
            }
            results {
                id
                name
                air_date
                episode
            }
        }
    }
'''

def get_all_episodes():
    all_episodes = []
    page = 1
    while True:
        result = client.execute(query, {'page': page})
        response = json.loads(result)
        all_episodes += response['data']['episodes']['results']
        next_page = response['data']['episodes']['info']['next']
        if next_page is None:
            break
        page += 1
    return all_episodes

all_episodes = get_all_episodes()

conn = sqlite3.connect('C:\db/rick_and_morty.db')

conn.execute('DROP TABLE IF EXISTS episodes')
conn.execute('CREATE TABLE episodes (id INTEGER PRIMARY KEY, name TEXT, air_date TEXT, episode TEXT)')

for episode in all_episodes:
    conn.execute(f"""INSERT INTO episodes (id, name, air_date, episode) VALUES ({episode['id']}, "{episode['name']}", "{episode['air_date'].replace("'", "''")}", "{episode['episode'].replace("'", "''")}")""")
    
conn.commit()
conn.close()
