from django.test import TestCase
from .models import Board, Player, Game
def test_board(print_board = False):
	test = Board()
	player1 = Player(1,test)
	player2 = Player(2,test)
	printarr = []
	for row in test.get_grid():
		printarr.append(row)
		for space in row:
			if space != None:			
				if space.piece != None:
					#print("[",space.get_x(),",",space.get_y(),"] : ",space.label()," : ",space.get_color()," : ",space.piece.get_name(),' : ',space.piece.get_color())
					pass
				# 	if space.piece.get_name() == "Queen":
				# 		print(space.piece.get_color(),":",space.piece.get_possible_moves())
	if(print_board):
		for flip in printarr:
		print(flip)
	return printarr
#test pieces
def print_test_piece_colors(printarr):
	test_str = ""
	for row in printarr:
		test_str += "["
		for ele in row:
			if ele == None:
				test_str += "None, "
			elif ele.piece != None:
				if ele.piece.get_color() == 1:
					test_str += "W|, "
				else: #black
					test_str += "B|, "
			else:
				test_str += "0|, "
		test_str += "]\n"
	print("\n")
	print(test_str)
#test spaces
def print_space(Board,x,y):
	print("\n")
	print(Board.get_Space(x,y).piece.get_name(),Board.get_Space(x,y).label(),"space color: ",Board.get_Space(x,y).get_color(),"piece color: ",Board.get_Space(x,y).piece.get_color())
def updateDebug():
	pass
	#the print statements are ordered beginning to end
	#print("Vectors for ",self.get_name()," at ",self.space.label(),": ",self._vectors.items(),"I exist: ",self.space.occupied)
	#print("-----------------GOING ",direction," FOR: ",magnitude,"-----------------------")
	#print("I HIT THE BOUNDARY")
	#print("IM AT: ",curSpace,"\nGOING TO THE ",direction," SPACE BEING ",myNeighbors[direction])
	#print("I HIT THE BOUNDARY")
	#print("It is ",myNeighbors[direction].occupied," that there is a piece here")
	#print("I HAVENT BEEN BLOCKED YET, SO")
	#print("THERE IS A PIECE HERE: ",blocker,"colors:",blocker.get_color(),self.get_color())
	#print("THIS PIECE IS MINE, I HAVE BEEN BLOCKED")
	#print("THIS PIECE IS THE ENEMIES, I HAVE BEEN BLOCKED")
	#print("THIS SPACE IS EMPTY")
	#print("MOVING FROM: ",curSpace," TO ", curSpace.get_neighbors()[direction])
	#print("MY FINAL POSSIBLE MOVES: ", self.get_possible_moves())







