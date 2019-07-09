from django.db import models

class Board:
	def __init__(self):
		self.__grid = []
		for i in range(10):
			row = []
			for k in range(10):
				if i == 0 or i == 9:
					new_space = None
				elif k == 0 or k == 9:
					new_space = None
				else:
					new_space = Space(i,k)	
				row.append(new_space)
			self.__grid.append(row)
	def get_grid(self):
		return self.__grid

class Space:
	letter_arr = ['a','b','c','d','e','f','g','h']
	def __init__(self,x,y):
		self.__x = x
		self.__y = y
		self.__number = y #labels for the space
		self.__letter = letter_arr[(self.x%8)]
		self.occupied = None #True or False
		self.piece = None #names the Piece object occupying it
		self.__color = colorize(self.x,self.y) #0 means black, 1 means white
	def colorize(x,y):
		if x%2 == 0:
			if y%2 == 0:
				return 0
			else:
				return 1
		else:
			if y%2 == 0:
				return 1
			else:
				return 0
	def get_x():
		return self.__x
	def get_y():
		return self.__y
	def label():
		output = self.__letter + string(self.__number)
		return output
	def get_color():
		return self.__color

class Piece:
	def __init__(self,x,y):
		self._color = None #white:1 or black:0
		self._name = ""
		self._possible_moves = [[None,None]] #array of possible moves for this piece, x,y coordinates
		self._possible_attacks = self.possible_moves #this is unaltered except for pawns
		self.starting_position = True #necessary for pawn first move
		self._isKing = False
		self._isPawn = False
		self.space = [x,y] #names the space that this piece occupies
	def set_color(self,color):
		self._color = color
	def get_color(self,color):
		return self._color
	def get_name(self):
		return self._name
	def set_name(self,name):
		self._name = name
	def get_possible_moves(self):
		return self._possible_moves


class Pawn(Piece):
	def __init__(self,x,y):
		Piece.__init__(self,x,y)
		self._possible_moves = [[self.x,self.y+2],[self.x,self.y+1]]
		self._possible_attacks = [[self.x+1,self.y+1],[self.x-1,self.y+1]]
		self.set_name("Pawn")
		self.isPawn = True #for promotion

class King(Piece):
	def __init__(self,x,y):
		Piece.__init__(self,x,y)
		self._possible_moves = [[self.x+1,self.y+1],[self.x+1,self.y],[self.x+1,self.y-1],[self.x,self.y-1],[self.x-1,self.y-1],[self.x-1,self.y],[self.x-1,self.y+1],[self.x,self.y+1]]
		self.set_name("King")
		self._isKing = True

class Queen(Piece):
	def __init__(self,x,y):
		Piece.__init__(self,x,y)
		self._possible_moves = []
		for i in range(8):
			self._possible_moves.append([self.x+i,self.y])
			self._possible_moves.append([self.x,self.y-i])
			self._possible_moves.append([self.x+i,self.y+i])
			self._possible_moves.append([self.x+i,self.y-i])
			self._possible_moves.append([self.x-i,self.y-i])
			self._possible_moves.append([self.x-i,self.y])
			self._possible_moves.append([self.x-i,self.y+i])
			self._possible_moves.append([self.x,self.y+i])
		self.set_name("Queen")

class Bishop(Piece):
	def __init__(self,x,y):
		Piece.__init__(self,x,y)
		self._possible_moves = []
		for i in range(8):
			self._possible_moves.append([self.x+i,self.y+i])
			self._possible_moves.append([self.x+i,self.y-i])
			self._possible_moves.append([self.x-i,self.y-i])
			self._possible_moves.append([self.x-i,self.y+i])
		self.set_name("Bishop")

class Knight(Piece):
	def __init__(self,x,y):
		Piece.__init__(self,x,y)
		self._possible_moves = [self.x+1,self.y+2],[self.x-1,self.y+2],[self.x+1,self.y-2],[self.x-1,self.y-2],[self.x+2,self.y+1],[self.x+2,self.y-1],[self.x-2,self.y+1],[self.x-2,self.y-1]
		self.set_name("Knight")

class Rook(Piece):
	Piece.__init__(self,x,y)
	self._possible_moves = []
	for i in range(8):
		self._possible_moves.append([self.x,self.y+i])
		self._possible_moves.append([self.x-i,self.y])
		self._possible_moves.append([self.x+i,self.y])
		self._possible_moves.append([self.x,self.y-i])
	self.set_name("Rook")

class Player:
	def __init__(self,color):
		self.current_pieces = []
		self.captured_pieces = [] #other player's pieces
		if color%2 == 1:#white
			self.first_move = True
			self.color = 1
			for i in range(8):
				newPawn = Pawn(i+1,2)
				newPawn.set_color(self.color)
				current_pieces.append(newPawn)
				if i == 0 or i == 7:
					newRook = Rook(i+1,1)
					newRook.set_color(self.color)
					current_pieces.append(newRook)
				elif i == 1 or i == 6:
					newKnight = Knight(i+1,1)
					newKnight.set_color(self.color)
					current_pieces.append(newKnight)
				elif i == 2 or i == 5:
					newBishop = Bishop(i+1,1)
					newBishop.set_color(self.color)
					current_pieces.append(newBishop)
				elif i == 3:
					newQueen = Queen(i+1,1)
					newQueen.set_color(self.color)
					current_pieces.append(newQueen)
				else: #i == 4
					newKing = King(i+1,1)
					newKing.set_color(self.color)
					current_pieces.append(newKing)
		else: #black
			self.first_move = False
			self.color = 0
			for i in range(8):
				newPawn = Pawn(i+1,7)
				newPawn.set_color(self.color)
				current_pieces.append(newPawn)
				if i == 0 or i == 7:
					newRook = Rook(i+1,8)
					newRook.set_color(self.color)
					current_pieces.append(newRook)
				elif i == 1 or i == 6:
					newKnight = Knight(i+1,8)
					newKnight.set_color(self.color)
					current_pieces.append(newKnight)
				elif i == 2 or i == 5:
					newBishop = Bishop(i+1,8)
					newBishop.set_color(self.color)
					current_pieces.append(newBishop)
				elif i == 3:
					newQueen = Queen(i+1,8)
					newQueen.set_color(self.color)
					current_pieces.append(newQueen)
				else: #i == 4
					newKing = King(i+1,8)
					newKing.set_color(self.color)
					current_pieces.append(newKing)
	#TODO add capture method, transfer pieces between arrays
class Game:
	def __init__(self):
		self.__board = Board()
		self._player_one = Player(1) #white
		self._player_two = Player(2) #black