import sqlite3
import json
from graphqlclient import GraphQLClient

# establece la URL de la API de Rick and Morty
client = GraphQLClient('https://rickandmortyapi.com/graphql')

# Define la consulta GraphQL
query ='''
    query getAllCharacters($page: Int!) {
  characters(page: $page) {
    info {
      next
    }
    results {
      id
      name
      species
      gender
      status
      type
      image
      episode {
        id
      }
    }
  }
}
'''

def get_all_characters():
    all_characters = []
    page = 1
    # Bucle personajes paginacion
    while True:
        result = client.execute(query, {'page': page})
        response = json.loads(result)
        # Agrega los personajes y sus episodios
        for character in response['data']['characters']['results']:
            episode_ids = [str(episode['id']) for episode in character['episode']]
            episode_ids_str = ",".join(episode_ids)
            character_dict = {
                'id': character['id'],
                'name': character['name'],
                'species': character['species'],
                'gender': character['gender'],
                'status': character['status'],
                'type': character['type'],
                'image': character['image'],
                'episode_id': episode_ids_str
            }
            all_characters.append(character_dict)
        next_page = response['data']['characters']['info']['next']
        if next_page is None:
            break
        page += 1
    return all_characters
  
all_characters = get_all_characters()
conn = sqlite3.connect('C:/db/rick_and_morty.db')

conn.execute('DROP TABLE IF EXISTS characters')
conn.execute('CREATE TABLE characters (id INTEGER PRIMARY KEY, name TEXT, status TEXT, species TEXT, type TEXT, gender TEXT, image TEXT, episode_id TEXT)')

for character in all_characters:
    conn.execute(
        'INSERT INTO characters (id, name, status, species, type, gender, image, episode_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (character['id'], character['name'], character['status'], character['species'], character['type'], character['gender'], character['image'], character['episode_id'])
    )
conn.commit()
conn.close()
