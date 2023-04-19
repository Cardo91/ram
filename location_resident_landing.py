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
                    name
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


conn.execute('DROP TABLE IF EXISTS location_residents')
conn.execute('CREATE TABLE location_residents (location_id INTEGER, character_id INTEGER, character_name TEXT)')

for location in all_locations:
    for resident in location['residents']:
        resident_id = resident['id']
        name = resident['name']
        conn.execute(f"""INSERT INTO location_residents (location_id, character_id, character_name) VALUES ({location['id']}, {resident_id}, '{name.replace("'", "''")}')""")

conn.commit()
conn.close()
