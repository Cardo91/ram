import sqlite3
import json
from graphqlclient import GraphQLClient

# Crea un cliente de GraphQL y establece la URL de la API de Rick and Morty
client = GraphQLClient('https://rickandmortyapi.com/graphql')

# Define la consulta GraphQL para obtener todos los episodios
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

# Define una función para obtener todos los episodios de la API utilizando la paginación
def get_all_episodes():
    # Inicializa una lista vacía para almacenar los episodios
    all_episodes = []
    # Establece el número de página inicial
    page = 1
    # Bucle para obtener todos los episodios de la API utilizando la paginación
    while True:
        # Envía la consulta GraphQL con el número de página actual
        result = client.execute(query, {'page': page})
        # Analiza la respuesta JSON en un diccionario de Python
        response = json.loads(result)
        # Agrega los episodios de la página actual a la lista
        all_episodes += response['data']['episodes']['results']
        # Verifica si hay más páginas para obtener
        next_page = response['data']['episodes']['info']['next']
        if next_page is None:
            break
        # Incrementa el número de página
        page += 1
    # Devuelve la lista de todos los episodios
    return all_episodes

# Llama a la función para obtener todos los episodios de la API
all_episodes = get_all_episodes()

conn = sqlite3.connect('C:\db/rick_and_morty.db')

conn.execute('DROP TABLE IF EXISTS episodes')
conn.execute('CREATE TABLE episodes (id INTEGER PRIMARY KEY, name TEXT, air_date TEXT, episode TEXT)')

for episode in all_episodes:
    conn.execute(f"""INSERT INTO episodes (id, name, air_date, episode) VALUES ({episode['id']}, "{episode['name']}", "{episode['air_date'].replace("'", "''")}", "{episode['episode'].replace("'", "''")}")""")
    
conn.commit()
conn.close()
