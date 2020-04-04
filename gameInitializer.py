import json
import jwt
import random
import time

lines = list()

GRID_SIZE = 3
NUMBER_OF_WORDS = 2

class WordClasses:
	BLACK = "black"
	RED = "red"
	BLUE = "blue"
	NEUTRAL = "neutral"

class GameInitializer:
	def loadWords():
		global lines
		with open('words_english.txt', encoding='utf-8') as f:
			lines = [line.rstrip() for line in f]	
			random.shuffle(lines)

	def getNewGameData():
		game = dict()
		game['redBegins'] = GameInitializer.getRedBegins()

		wordData = GameInitializer.getWordGridLinear()
		masterData = GameInitializer.getMasterGridLinear(game)
		zippedData = [
			{'word': wordData[i], 'category': masterData[i], 'flipped': False, 'chosen': False}
			for i in range(len(wordData))
		]
		game['grid'] = GameInitializer.toGrid(list(zippedData))

		data = dict()
		data['identifier'] = GameInitializer.getGameIdentifier(game)
		data['game'] = game
		return data

	def getRedBegins():
		return random.random() > 0.5

	def getWordGridLinear():
		global lines
		if len(lines) < (GRID_SIZE * GRID_SIZE):
			GameInitializer.loadWords()
		linesToPlay = lines[:GRID_SIZE*GRID_SIZE]
		lines = lines[GRID_SIZE*GRID_SIZE+1:]
		return linesToPlay

	def getMasterGridLinear(redBegins):
		masterGrid = list()
		masterGrid.append(WordClasses.BLACK)

		for i in range(NUMBER_OF_WORDS + (1 if redBegins else 0)):
			masterGrid.append(WordClasses.RED)
		
		for i in range(NUMBER_OF_WORDS + (1 if not redBegins else 0)):
			masterGrid.append(WordClasses.BLUE)

		while len(masterGrid) < (GRID_SIZE * GRID_SIZE):
			masterGrid.append(WordClasses.NEUTRAL)

		random.shuffle(masterGrid)

		return masterGrid	

	def toGrid(data):
		gridData = list();

		for i in range(GRID_SIZE):
			gridData.append(list())
			for j in range(GRID_SIZE):
				gridData[i].append(data[i*GRID_SIZE + j])

		return gridData

	def getGameIdentifier(data):
		return jwt.encode(data, key=None, algorithm=None).decode()

	def loadGame(gameAsJwt):
		return jwt.decode(gameAsJwt, verify=False)