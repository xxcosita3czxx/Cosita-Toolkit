import os  # noqa: D100

import cosita_toolkit as costk


def test_gitapi_last_info_usr():
    costk.GithubApi.get_info_usr("xxcosita3czxx")
def test_osint():
    costk.OsintFramework.Universal.check_username("cosita3cz","Github")
def test_pokeapi():
    costk.PokeAPI.get_pokemon_raw(name="pikachu")
def test_main():
    os.system("python cosita_toolkit.py")  # noqa: S605, S607
