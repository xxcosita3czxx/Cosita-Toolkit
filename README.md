
# Cosita's ToolKit

![GitHub](https://img.shields.io/github/license/xxcosita3czxx/Cosita-ToolKit?color=blue&label=License&logo=github&style=for-the-badge)
![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/xxcosita3czxx/Cosita-ToolKit/python-package.yml?label=Tests&logo=github-actions&style=for-the-badge)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/xxcosita3czxx/Cosita-Toolkit/ruff.yml?style=for-the-badge&label=Ruff%20Tests)


ToolKit for some projects and api's i made, because it makes my life easier and your it can make too!

## Features

- Osint Api's
- windows Memory address editor and pid finder
- Auto updating, cuz PyPi is cursed for sm rsn
- other things i need in mah projects :)


## How To use:

To use this module, there is no PyPi so you wont need pip

Instead i have legacy method, aka "importing local module"

that means you can just put 'cosita-toolkit.py' to your dirrectory and
import it like this:
```python
import path.to.your.dir.cosita-toolkit
```

sounds easy right?

Also dont worry about license, i have it included inside code, just dont edit it and you will be good.
## Usage/Examples

Modifing Memory address of pid 9999:
```python
import cosita-toolkit as ctkit

ctkit.MemMod.modify(9999,0x03D55E, 37)
```

Getting last info about person on github and storing it inside json file:
```python
import cosita-toolkit as ctkit

ctkit.GithubApi.get_last_info_raw("xxcosita3czxx", "tmp/res/github_api/", "last-info")
# no need to put .json onto the name of file save to
```

[Documentation](https://github.com/xxcosita3czxx/Cosita-Toolkit/wiki/Documentation)
## Feedback

If you have any feedback, please reach out to me on Issue Page or my discord: @cosita3cz


## Support

For support, make Issue on Issue page


## Installation

There is no way to install this module yet
