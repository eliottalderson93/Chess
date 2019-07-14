from django.shortcuts import render, HttpResponse, redirect, render_to_response
import requests, json
from .models import Game

def home(request):
	the_session = dict(request.session)
	for key, val in dict(request.session):
		print("session:",key,":",val)
	print("var session",the_session)
	print(not request.session)
	if request.session.get('current_game') == None:
		#you just lost
		theGame = Game()
		request.session["current_game"] = True
		request.session["Game"] = theGame
		request.session["Board"] = theGame.get_board()
		request.session["P1"] = theGame.get_p1()
		request.session["P2"] = theGame.get_p2()
		request.session["Grid"] = theGame.get_board().get_grid()
		context = {
			"Game" : theGame,
			"Board" : theGame.get_board(),
			"P1" : theGame.get_p1(),
			"P2" : theGame.get_p2(),
			"Grid" : theGame.get_board().get_grid()
		}
		myRender = render(request,"chess/home.html", context)
	else:
		#there is a game in session
		context = {
			"Game" : request.session["Game"],
			"Board" : request.session["Board"],
			"P1" : request.session["P1"],
			"P2" : request.session["P2"],
			"Grid" : request.session["Grid"]
		}
		print(theGame)
		myRender = render(request,"chess/home.html", context)
	return myRender

# def white_square(request):
# 	myRender = 

def bad_request(request,*args,**argv):
	return redirect(reverse('home'))
