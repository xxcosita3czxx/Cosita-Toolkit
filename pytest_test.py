import os
import cosita_toolkit as costk
def test_gitapi():
    costk.github_api.get_last_info_raw("xxcosita3czxx")
    costk.github_api.get_info_usr("xxcosita3czxx")
def test_osint():
    costk.osint_framework.universal.check_username("cosita3ct","Github")
def test_pokeapi():
    costk.PokeAPI.get_pokemon_raw("pikachu")
def test_main():
    try:
        os.system("python cosita_toolkit.py")
    except Exception as e:
        print (e)