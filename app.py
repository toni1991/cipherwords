import logging
import os

from flask import current_app
from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask_cors import CORS

from gameInitializer import GameInitializer
from gameInitializer import WordClasses

modules = {}
application = Flask(__name__)
application.logger.setLevel(logging.DEBUG)

CORS(application)

@application.errorhandler(404)
def notFound(error):
	return {'message': '404: Not found.'}, 404

@application.route('/')
def start():
	return render_template('start.html')

@application.route('/explain')
def getExplain():
	return render_template('base.html', gameData=getGame(), identifier=getIdentifier(), explain=True)

@application.route('/guess')
def getGuess():
	return render_template('base.html', gameData=getGame(), identifier=getIdentifier(), explain=False)

@application.route('/flip/<int:x>/<int:y>')
def flip(x, y):
	getCurrentGameGrid()[x][y]['flipped'] = not getCurrentGameGrid()[x][y]['flipped']
	return redirect(url_for('getExplain')) # Return explain, as only explain can flip the words!

@application.route('/choose/<int:x>/<int:y>')
def choose(x, y):
	getCurrentGameGrid()[x][y]['chosen'] = not getCurrentGameGrid()[x][y]['chosen']
	unchooseAllBut(getCurrentGameGrid()[x][y])
	
	return redirect(url_for('getGuess')) # Return guess, as only guess view can choose the words!

@application.route('/initGame')
def initGame():
	current_app.currentGame = GameInitializer.getNewGameData();
	return start()

@application.route('/getGame')
def getGame():
	if not hasattr(current_app, 'currentGame'):
		return initGame()
	setWordsCount()
	return current_app.currentGame['game']


@application.route('/load')
def loadGame():
	id = request.args.get('identifier')
	if id:
		data = GameInitializer.loadGame(id)
		if data:
			current_app.currentGame['game'] = data 

	return start() # Return start, as only start view can load a game!

@application.before_first_request
def init():
	initGame()

def calculateIdentifier():
	current_app.currentGame['identifier'] = GameInitializer.getGameIdentifier(current_app.currentGame['game'])

def getExplainRedirect():
	return redirect(url_for('getExplain'))

def unchooseAllBut(exclude):
	for row in getCurrentGameGrid():
		for cell in row:
			if exclude != cell:
 				cell['chosen'] = False

def getIdentifier():
	calculateIdentifier()
	return current_app.currentGame['identifier']

def getCurrentGameGrid():
	return current_app.currentGame['game']['grid']

def setWordsCount():
	data = current_app.currentGame['game']
	def wordsCountInner(dataName, color):
		data[dataName] = 0
		for row in data["grid"]:
			for cell in row:
				if cell['category'] == color and not cell['flipped']:
					data[dataName] += 1 

	wordsCountInner("blueWords", WordClasses.BLUE)
	wordsCountInner("redWords", WordClasses.RED)

if __name__ == '__main__':
	application.run(host='0.0.0.0', port=8080, debug=True)