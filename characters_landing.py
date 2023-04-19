import sqlite3
import json
from graphqlclient import GraphQLClient

# Crea un cliente de GraphQL y establece la URL de la API de Rick and Morty
client = GraphQLClient('https://rickandmortyapi.com/graphql')

# Define la consulta GraphQL para obtener todos los personajes
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
    # Inicializa una lista vacía para almacenar los personajes y sus episodios
    all_characters = []
    # Establece el número de página inicial
    page = 1
    # Bucle para obtener todos los personajes de la API utilizando la paginación
    while True:
        # Envía la consulta GraphQL con el número de página actual
        result = client.execute(query, {'page': page})
        # Analiza la respuesta JSON en un diccionario de Python
        response = json.loads(result)
        # Agrega los personajes y sus episodios de la página actual a la lista
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
        # Verifica si hay más páginas para obtener
        next_page = response['data']['characters']['info']['next']
        if next_page is None:
            break
        # Incrementa el número de página
        page += 1
    # Devuelve la lista de todos los personajes y sus episodios
    return all_characters

# Llama a la función para obtener todos los personajes de la API
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
