import cosita_toolkit as costk

def test_gitapi():
    costk.github_api.get_last_info_raw("xxcosita3czxx")
    costk.github_api.get_info_usr("xxcosita3czxx")