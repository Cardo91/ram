import sqlite3
import json
from graphqlclient import GraphQLClient

# Crea un cliente de GraphQL y establece la URL de la API de Rick and Morty
client = GraphQLClient('https://rickandmortyapi.com/graphql')

# Define la consulta GraphQL para obtener todas las ubicaciones
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

# Define una función para obtener todas las ubicaciones de la API utilizando la paginación
def get_all_locations():
    # Inicializa una lista vacía para almacenar las ubicaciones
    all_locations = []
    # Establece el número de página inicial
    page = 1
    # Bucle para obtener todas las ubicaciones de la API utilizando la paginación
    while True:
        # Envía la consulta GraphQL con el número de página actual
        result = client.execute(query, {'page': page})
        # Analiza la respuesta JSON en un diccionario de Python
        response = json.loads(result)
        # Agrega las ubicaciones de la página actual a la lista
        all_locations += response['data']['locations']['results']
        # Verifica si hay más páginas para obtener
        next_page = response['data']['locations']['info']['next']
        if next_page is None:
            break
        # Incrementa el número de página
        page += 1
    # Devuelve la lista de todas las ubicaciones
    return all_locations

# Llama a la función para obtener todas las ubicaciones de la API
all_locations = get_all_locations()

# Conecta a la base de datos SQLite
conn = sqlite3.connect('C:\db/rick_and_morty.db')

# Crea una tabla para los residentes de las ubicaciones
conn.execute('DROP TABLE IF EXISTS location_residents')
conn.execute('CREATE TABLE location_residents (location_id INTEGER, character_id INTEGER, character_name TEXT)')

# Recorre cada ubicación y agrega a la tabla "locations" en la base de datos
for location in all_locations:
    for resident in location['residents']:
        resident_id = resident['id']
        name = resident['name']
        conn.execute(f"""INSERT INTO location_residents (location_id, character_id, character_name) VALUES ({location['id']}, {resident_id}, '{name.replace("'", "''")}')""")

# Guarda los cambios y cierra la conexión a la base de datos
conn.commit()
conn.close()
