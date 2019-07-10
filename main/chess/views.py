from django.shortcuts import render, HttpResponse, redirect, render_to_response
import requests, json
from models import Game
def home(request):
    context = {
        "Game" : Game(),
    }
    print(context["Game"])
    return render(request,"bokehGraphs/graphs.html", context)

new = Game()
