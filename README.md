For add-on description, please see [AnkiWeb page](https://ankiweb.net) (Which does not exist yet!)
# Development
## Setup
After cloning the project, run the following command to install [ankiaddonconfig](https://github.com/BlueGreenMagick/ankiaddonconfig/) as a git submodule.
```
git submodule update --init --recursive
```

## Tests & Formatting
This project uses [black] and [mypy](https://github.com/python/mypy).

```
black .
mypy .
pytest .
```

You will need to install the following python packages to run black, mypy and pytest: 
```
pip install aqt pyqt5-stubs mypy black
```

# Building ankiaddon file
After cloning the repo, go into the repo directory and run the following command to install the git submodule [ankiaddonconfig](https://github.com/BlueGreenMagick/ankiaddonconfig/)
```
git submodule update --init addon/ankiaddonconfig
```
After installing the git submodule, run the following command to create an `audiovisual_feedback.ankiaddon` file
```
cd addon ; zip -r ../audiovisual_feedback.ankiaddon * ; cd ../
```