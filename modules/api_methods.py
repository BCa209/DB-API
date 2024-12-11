import requests

def obtener_datos(api_url):
    """
    Conecta con la API y retorna los datos en formato JSON.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        return response.json()      # Retorna los datos como diccionario
    except requests.RequestException as e:
        return {"error": str(e)}
