#importing requests and working on the script to 
import requests
import image_lib
import os

url_of_poke = 'https://pokeapi.co/api/v2/pokemon/'

def main():
    """
    The main function of the script. Currently it calls the download_pokemon_artwork function
    with a sample Pokemon name and directory path.
    """
    #poke_info = get_pokemon_info("Rockruff")
    #poke_info = get_pokemon_info(123)

    download_pokemon_artwork('dugtrio', r'C:\Users\Owner\Desktop\SEMESTER4\Scripting\COMP593-Lab10')   
    return

def get_pokemon_info(pokemon_name):
    """
    This function takes in a Pokemon name as input and returns a dictionary containing 
    information about the Pokemon from the PokeAPI.

    Args:
    pokemon_name (str): The name of the Pokemon to search for.

    Returns:
    dict: A dictionary containing information about the Pokemon, if the search is successful.
    None: If the search is unsuccessful.
    """
    pokemon_name = str(pokemon_name).strip().lower()

    url = url_of_poke + pokemon_name

    print ('\n',f'Searching for the Pokemon Ability with the name  {pokemon_name}..', '\n', end='')
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('\n','Congratulations, the data has been fetched successfully', '\n')
        return resp_msg.json()
    else:
        print('\n','Failure, No such data is available','\n')
        print('\n',f'Error Code : {resp_msg.status_code}, Reason For Error : {resp_msg.reason}', '\n')

   
def get_pokemon_name(offset = 0, limit = 100000):
    """
    This function gets a list of Pokemon names from the PokeAPI.

    Args:
    offset (int): The offset for the query string parameter.
    limit (int): The limit for the query string parameter.

    Returns:
    list: A list of Pokemon names, if the query is successful.
    None: If the query is unsuccessful.
    """
    query_str_params = {
        'offset' : offset,
        'limit' : limit

    }
    print (f'Getting list of pokemon name .....', end = '')
    resp_msg = requests.get(url_of_poke, params=query_str_params)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        pokemon_dict = resp_msg.json()
        pokemon_names_list = [p['name']for p in pokemon_dict['results']]
        return pokemon_names_list
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return

def download_pokemon_artwork(pokemon_name, save_dir ):
    """
    This function downloads the official artwork of a specified Pokemon from the PokeAPI.

    Args:
    pokemon_name (str): The name of the Pokemon to download artwork for.
    save_dir (str): The directory path to save the downloaded artwork.

    Returns:
    str: The path of the saved image file, if the download and save is successful.
    None: If either the download or save is unsuccessful.
    """
    #Get all info for the spevified Pokemon
    pokemon_info = get_pokemon_info(pokemon_name)

    if pokemon_info is None:
        return

    #extract the artwork URL from the info dictionry    
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']

    image_bytes = image_lib.download_image(artwork_url)
    if image_bytes is None:
    
        return

    file_ext = artwork_url.split('.')[-1]
    image_path = os.path.join(save_dir, f'{pokemon_name}.{file_ext}')
    if image_lib.save_image_file(image_bytes, image_path):
        return image_path
  
if __name__ == '__main__':
    main()
        