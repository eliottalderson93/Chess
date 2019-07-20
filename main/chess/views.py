from django.shortcuts import render, HttpResponse, redirect, render_to_response
import requests, json
from .models import Game,Board

def home(request):
	#IF NEWGAME
	request.session["current_game"] = True
	#print('neighbors of', theGame.get_board().get_Space_by_label("f7"), ":",theGame.get_board().get_Space_by_label("f7").get_neighbors())
	#print("Grid: ",theGame.get_board().get_grid())
	defaultBoard = Board()
	context = {"defaultBoard" : defaultBoard.get_grid()}
	myRender = render(request,"chess/home.html",context)
	#ELSE
	return myRender

def playerTurn(request):
	#alter the DB board and then get it from DB based on user input
	if request.method == 'POST':
		pass
	else:
		pass
	if False:
		context = { #these come from the database
				"Game" : None,
				"Board" : None,
				"P1" : None,
				"P2" : None,
				"Grid" : None
		}
	else: #default board
		theGame = Game()
		context = {
			"Game" : theGame,
			"Board" : theGame.get_board(),
			"P1" : theGame.get_p1(),
			"P2" : theGame.get_p2(),
			"Grid" : theGame.get_board().get_grid()
		}
	html = render(request,"chess/board.html",context)
	return HttpResponse(html)

def AITurn(request):
	html = ""
	#goes into database to perform machine learning TODO LATER
	#AI logic here
	#RECORD AI logic into DB
	#below: respond with updated board
	return HttpResponse(html)

def bad_request(request,*args,**argv):
	return redirect(reverse('home'))
