<h1 align="center">Tribescheat</h1>


This is a cheat made for the game Tribes of Midgard. This tool uses the [Tribes of Midgard API](https://api.tribesofmidgard.com/) to create a world and afterwards it saves the world with desired properties like the amount of slain bosses, the golden horns gained and the amount of experience gained.
<br><br>
To achieve that it needs the auth-token for the game, you can either try to extract it yourself or you can have the game open and start the tool to automatically extract the auth-token from the game memory.
## To run the tool
I recommend using [poetry](https://python-poetry.org/) to use this project, although you can use any package manager.

### Using poetry
##### First install the dependencies:
```bash
poetry install
```

##### Then you can run the tool:
```bash
poetry run python main.py
```

### Not using poetry but using pip
##### First install the dependencies:
```bash
pip install -r requirements.txt
```

##### Then you can run the tool:
```bash
python main.py
```

### Video demo
[![Watch the video](https://user-images.githubusercontent.com/79755465/193370189-275f4938-5953-4fcc-afb4-70338ebb15ae.png)](https://www.youtube.com/watch?v=57BhOAT6_6w)

#### For pyinstaller
To create an exe file from the source code, you can use pyinstaller with the following command (you also need to install pyinstaller for that)
```
pyinstaller --icon=resources/icon.ico --onefile main.py
```

<br><br>
Have fun :p
