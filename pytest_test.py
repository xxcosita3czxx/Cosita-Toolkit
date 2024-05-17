import os
import cosita_toolkit as costk

def test_gitapi_last_info_raw():
    costk.github_api.get_last_info_raw("xxcosita3czxx")
def test_gitapi_last_info_raw():
    costk.github_api.get_info_usr("xxcosita3czxx")
def test_osint():
    costk.osint_framework.universal.check_username("cosita3cz","Github")
def test_pokeapi():
    costk.PokeAPI.get_pokemon_raw("pikachu")
def test_main():
    os.system("python cosita_toolkit.py")
