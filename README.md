# cipherwords
A word guessing game written in python / flask.

# UI
## views
### start 
![start](/images/start.png)

### guessing view
![guessing view](/images/guess.png)

### explanation view
![explanation view](/images/explain.png)

### show game id
![show game id](/images/gameid.png)

### loading game state
![loading game state](/images/load.png)

# word lists

Currently included are word lists in english (words_english.txt) and german (words_german.txt).

To switch the list replace the loaded file in ```GameInitializer.loadWords()```

# requirements

Install requirements with pip

```
pip install -r requirements.txt
```

# running

```
python app.py
```

Default runs on port 8080. This can be changed in app.py