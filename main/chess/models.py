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
	def get_Space(self,x,y):
		return self.__grid[x][y]
	def get_Space_label(self,label):
		return 0
	def is_occupied(self,x,y):
		if not 1<=x<=8:
			return None
		if not 1<=y<=8:
			return None
		return self.__grid[x][y].occupied
	#TODO fix triple pipes and extra --- line
	def draw_grid(self):
		row_string = ""
		for y in range(20):
			for x in range(10):
				y_coord = int(y/2)
				add_to_rs = ''
				space_here = self.get_grid()[x][y_coord]

				if space_here == None:
					boundary_flag = False
				else:
					boundary_flag = True

				if y%2 == 0 and boundary_flag and not y == 0:
					add_to_rs = '--' #draw horiz borders between rows
					if x == 9:
						add_to_rs += '|'
				elif boundary_flag:
					#empty spaces (0) and pieces (P,Kn,B,R,Q,Ki) with vertical boundaries between
					#print("boundary: ",space_here, ":",type(space_here),":",space_here == None,":",boundary_flag,":",space_here.piece == None)
					if space_here.piece == None:
						add_to_rs = '0|'
						if x == 9:
							add_to_rs += '|'
					else:
						add_to_rs = space_here.piece.get_name()[0] + space_here.piece.get_name()[1]
						if add_to_rs[0] != 'K':
							add_to_rs = add_to_rs[0] #Ki = King, Kn = Knight, Q = Queen, B = Bishop, P = Pawn, R = Rook
						add_to_rs += '|'			
				else: #draw boundaries
					if y == 0:
						add_to_rs = '=='
					elif y == 19:
						add_to_rs = '=='
					if x == 0 and not y == 19:
						add_to_rs = '||'
					elif x == 9 and not y == 19:
						add_to_rs = '|'
				row_string += add_to_rs
			row_string += "\n"
		print(row_string)

class Space:
	def __init__(self,x,y):
		self.__x = x
		self.__y = y
		self.__number = y #labels for the space
		self.__letter = ['a','b','c','d','e','f','g','h'][((self.__x-1)%8)]
		self.occupied = False #is a piece here?
		self.piece = None #names the Piece object occupying it
		self.__color = self.colorize(self.__x,self.__y) #0 means black, 1 means white
	def __repr__(self):
		if self.piece == None:
			return "0|"
		else:
			return self.piece.__repr__()
	def colorize(self,x,y):
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
	def get_x(self):
		return self.__x
	def get_y(self):
		return self.__y
	def label(self):
		output = "" + self.__letter + str(self.__number)
		return output
	def get_color(self):
		return self.__color

class Piece:
	def __init__(self,x,y,Board):
		self._color = None #white:1 or black:0
		self._name = "Default"
		self.__possible_moves = [[None,None]] #array of possible moves for this piece unaltered by board boundaries, x,y coordinates
		self._possible_attacks = self.__possible_moves #this is unaltered except for pawns
		self.starting_position = True #necessary for pawn first move
		self._isKing = False
		self._isPawn = False
		self.space = Board.get_Space(x,y) #names the space object that this piece occupies
		Board.get_Space(x,y).piece = self #establishes a linked-list type structure of pieces and spaces
		Board.get_Space(x,y).occupied = True
	def __repr__(self):
		if self._name[0] != 'K':
			return self._name[0] + '|'
		else:
			return self._name[0] + self._name[1] + '|'
	def set_color(self,color):
		self._color = color
	def get_color(self):
		return self._color
	def get_name(self):
		return self._name
	def set_name(self,name):
		self._name = name
	def get_possible_moves(self,Board):
		output = self.update_possible_moves(Board)
		return output
	def update_possible_moves(self,Board):
		#out of bounds
		for i,move in enumerate(self.__possible_moves):
			if not 1 <= move[0] <= 8:
				del self._possible_moves[i]
			if not 1 <= move[1] <= 8:
				del self._possible_moves[i]
		#blocking
		if self._name == "Knight":
			#knights cant be blocked along their attack line
			pass
		else:
			pass
		return self.__possible_moves

	def move(self,Board):
		moves = []
		#for space in self.get_possible_moves(): #space is an [x,y]
			#if space

class Pawn(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = [[self.space.get_x(),self.space.get_y()+2],[self.space.get_x(),self.space.get_y()+1]]
		self._possible_attacks = [[self.space.get_x()+1,self.space.get_y()+1],[self.space.get_x()-1,self.space.get_y()+1]]
		self.set_name("Pawn")
		self.isPawn = True #for promotion

class King(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = [[self.space.get_x()+1,self.space.get_y()+1],[self.space.get_x()+1,self.space.get_y()],[self.space.get_x()+1,self.space.get_y()-1],[self.space.get_x(),self.space.get_y()-1],[self.space.get_x()-1,self.space.get_y()-1],[self.space.get_x()-1,self.space.get_y()],[self.space.get_x()-1,self.space.get_y()+1],[self.space.get_x(),self.space.get_y()+1]]
		self.set_name("King")
		self._isKing = True

class Queen(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = []
		for i in range(8):
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()])
			self.__possible_moves.append([self.space.get_x(),self.space.get_y()-i])
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()+i])
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()-i])
			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()-i])
			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()])
			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()+i])
			self.__possible_moves.append([self.space.get_x(),self.space.get_y()+i])
		self.set_name("Queen")

class Bishop(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = []
		for i in range(8):
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()+i])
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()-i])
			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()-i])
			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()+i])
		self.set_name("Bishop")

class Knight(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = [self.space.get_x()+1,self.space.get_y()+2],[self.space.get_x()-1,self.space.get_y()+2],[self.space.get_x()+1,self.space.get_y()-2],[self.space.get_x()-1,self.space.get_y()-2],[self.space.get_x()+2,self.space.get_y()+1],[self.space.get_x()+2,self.space.get_y()-1],[self.space.get_x()-2,self.space.get_y()+1],[self.space.get_x()-2,self.space.get_y()-1]
		self.set_name("Knight")

class Rook(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = []
		for i in range(8):
			self.__possible_moves.append([self.space.get_x(),self.space.get_y()+i])
			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()])
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()])
			self.__possible_moves.append([self.space.get_x(),self.space.get_y()-i])
		self.set_name("Rook")

class Player:
	def __init__(self,color,Board):
		self.current_pieces = []
		self.captured_pieces = [] #other player's pieces
		if color%2 == 1:#white
			self.__color = 1
			for i in range(8):
				newPawn = Pawn(i+1,2,Board)
				newPawn.set_color(self.__color)
				self.current_pieces.append(newPawn)
				if i == 0 or i == 7:
					newRook = Rook(i+1,1,Board)
					newRook.set_color(self.__color)
					self.current_pieces.append(newRook)
				elif i == 1 or i == 6:
					newKnight = Knight(i+1,1,Board)
					newKnight.set_color(self.__color)
					self.current_pieces.append(newKnight)
				elif i == 2 or i == 5:
					newBishop = Bishop(i+1,1,Board)
					newBishop.set_color(self.__color)
					self.current_pieces.append(newBishop)
				elif i == 3:
					newQueen = Queen(i+1,1,Board)
					newQueen.set_color(self.__color)
					self.current_pieces.append(newQueen)
				else: #i == 4
					newKing = King(i+1,1,Board)
					newKing.set_color(self.__color)
					self.current_pieces.append(newKing)
		else: #black
			self.__color = 0
			for i in range(8):
				newPawn = Pawn(i+1,7,Board)
				newPawn.set_color(self.__color)
				self.current_pieces.append(newPawn)
				if i == 0 or i == 7:
					newRook = Rook(i+1,8,Board)
					newRook.set_color(self.__color)
					self.current_pieces.append(newRook)
				elif i == 1 or i == 6:
					newKnight = Knight(i+1,8,Board)
					newKnight.set_color(self.__color)
					self.current_pieces.append(newKnight)
				elif i == 2 or i == 5:
					newBishop = Bishop(i+1,8,Board)
					newBishop.set_color(self.__color)
					self.current_pieces.append(newBishop)
				elif i == 4:
					newQueen = Queen(i+1,8,Board)
					newQueen.set_color(self.__color)
					self.current_pieces.append(newQueen)
				else: #i == 3
					newKing = King(i+1,8,Board)
					newKing.set_color(self.__color)
					self.current_pieces.append(newKing)
	def get_color(self):
		return self.__color
			
	#TODO add capture method, transfer pieces between arrays
class Game:
	def __init__(self):
		self.__board = Board()
		self._player_one = Player(1,self.__board) #white
		self._player_two = Player(2,self.__board) #black

test = Board()
player1 = Player(1,test)
player2 = Player(2,test)
for row in test.get_grid():
	#print(row)
	for space in row:
		if space != None:
			if space.piece != None:
				print("[",space.get_x(),",",space.get_y(),"] : ",space.label()," : ",space.get_color()," : ",space.piece.get_name(),' : ',space.piece.get_color())
			# 	if space.piece.get_name() == "Queen":
			# 		print(space.piece.get_color(),":",space.piece.get_possible_moves())
