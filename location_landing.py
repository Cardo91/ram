import sqlite3
import json
from graphqlclient import GraphQLClient

client = GraphQLClient('https://rickandmortyapi.com/graphql')

query = '''
    query getAllLocations($page: Int!) {
        locations(page: $page) {
            info {
                next
            }
            results {
                id
                name
                type
                dimension
                residents {
                    id
                }
            }
        }
    }
'''
def get_all_locations():
    all_locations = []
    page = 1
    while True:
        result = client.execute(query, {'page': page})
        response = json.loads(result)
        all_locations += response['data']['locations']['results']
        next_page = response['data']['locations']['info']['next']
        if next_page is None:
            break
        page += 1
    return all_locations

all_locations = get_all_locations()

conn = sqlite3.connect('C:\db/rick_and_morty.db')

conn.execute('DROP TABLE IF EXISTS location')
conn.execute('CREATE TABLE location (id INTEGER PRIMARY KEY, name TEXT, type TEXT, dimension TEXT)')
conn.execute('ALTER TABLE location ADD COLUMN residents TEXT')


for location in all_locations:
    residents_ids = [resident['id'] for resident in location['residents']]
    residents = ','.join(str(id) for id in residents_ids)
    conn.execute(f"""INSERT INTO location (id, name, type, dimension, residents) VALUES ({location['id']}, "{location['name']}", "{location['type'].replace("'", "''")}", "{location['dimension']}", "{residents}")""")

conn.commit()
conn.close()
