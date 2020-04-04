import random
import time
import json
import base64

from enum import Enum

lines = list()

GRID_SIZE = 5
NUMBER_OF_CARDS = 8

class CardClasses:
	BLACK = 1
	RED = 2
	BLUE = 3
	EMPTY = 4

class GameInitializer:
	def loadWords():
		global lines
		with open('words_english.txt', encoding='utf-8') as f:
			lines = [line.rstrip() for line in f]	
			random.shuffle(lines)

	def getNewGameData():
		game = dict()
		game['gridSize'] = GRID_SIZE
		game['redBegins'] = GameInitializer.getRedBegins()
		game['redCards'] = NUMBER_OF_CARDS + (1 if game['redBegins'] else 0)
		game['blueCards'] = NUMBER_OF_CARDS + (1 if not game['redBegins'] else 0)

		wordData = GameInitializer.getWordGridLinear(game['gridSize'])
		masterData = GameInitializer.getMasterGridLinear(game)
		zippedData = [{'word': wordData[i], 'category': masterData[i], 'flipped': False, 'chosen': False} for i in range(len(wordData))]
		game['grid'] = GameInitializer.toGrid(list(zippedData), game['gridSize'])

		data = dict()
		data['identifier'] = GameInitializer.getGameIdentifier(game)
		data['game'] = game
		return data

	def getRedBegins():
		return random.random() > 0.5

	def getWordGridLinear(gridSize):
		global lines
		if len(lines) < (gridSize * gridSize):
			GameInitializer.loadWords()
		linesToPlay = lines[:gridSize*gridSize]
		lines = lines[gridSize*gridSize+1:]
		return linesToPlay

	def getMasterGridLinear(data):
		masterGrid = list()
		masterGrid.append(CardClasses.BLACK)

		for i in range(data['redCards']):
			masterGrid.append(CardClasses.RED)
		
		for i in range(data['blueCards']):
			masterGrid.append(CardClasses.BLUE)

		while len(masterGrid) < (data['gridSize']*data['gridSize']):
			masterGrid.append(CardClasses.EMPTY)

		random.shuffle(masterGrid)

		return masterGrid	

	def toGrid(data, gridSize):
		gridData = list();

		for i in range(gridSize):
			gridData.append(list())
			for j in range(gridSize):
				gridData[i].append(data[i*gridSize + j])

		return gridData

	def getGameIdentifier(data):
		return jwt.encode(data, key=None, algorithm=None).decode()

	def loadGame(gameAsJwt):
		return jwt.decode(gameAsJwt, verify=False)