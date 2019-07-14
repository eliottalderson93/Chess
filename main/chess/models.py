from django.db import models
from django.contrib.postgres.fields import ArrayField
#models are on the bottom, the normal classes are for drawing the chess board and pieces
#as well as calculating the next move on the server side
#the models are for giving permanence to the chess board

#server objects that are exposed on the client to build the DOM and give logic to the game
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
		self.__init_neighbors()
		self._positions = self.positions()
		print(self)

	def __init_neighbors(self):
		for i, row in enumerate(self.__grid): #rows = north/south south++
			for k, space in enumerate(row): #cols = east/west east++
				if space != None:
					space._set_neighbors(self.__grid[i-1][k],self.__grid[i-1][k+1],self.__grid[i][k+1],self.__grid[i+1][k+1],self.__grid[i+1][k],self.__grid[i+1][k-1],self.__grid[i][k-1],self.__grid[i-1][k-1]) #N,NE,E,SE,S,SW,W,NW

	def __repr__(self):
		begin = "____________________\n"
		endstr = ""
		for i in range(1,9):
			row = ""
			row += '|'
			for k in range(10):
				if self.__grid[i][k] != None:
					row += self.__grid[i][k].__repr__()
			row += '|\n'
			endstr += row

		end = "____________________\n"
		return begin + endstr + end

	def get_grid(self):
		return self.__grid

	def get_Space(self,x,y):
		return self.__grid[y][x]

	def get_Space_label(self,label):
		return 0

	def is_occupied(self,x,y):
		if not 1<=x<=8:
			return None
		if not 1<=y<=8:
			return None
		return self.__grid[y][x].occupied

	def get_positions(Self):
		return self._positions

	def positions(self): #returns a dictionary with the positions of all pieces : used for permanence
		b_pawn_list = []
		b_knight_list = []
		b_bishop_list = []
		b_rook_list = []
		b_queen_list = []
		b_King = ""

		w_pawn_list = []
		w_knight_list = []
		w_bishop_list = []
		w_rook_list = []
		w_queen_list = []
		w_King = ""
		for row in self.__grid: #iterate through the board and find the space-labels of where all the pieces are
			for space in row:
				if space != None:
					if space.piece != None:
						if space.piece.get_color() == 0:
							if space.piece._isPawn:
								b_pawn_list.append(space.label())
							elif space.piece._isKing:
								b_King = space.label()
							elif space.piece.get_name() == "Bishop":
								b_bishop_list.append(space.label())
							elif space.piece._name == "Knight":
								b_knight_list.append(space.label())
							elif space.piece.get_name() == "Rook":
								b_rook_list.append(space.label())
							elif space.piece.get_name() == "Queen":
								b_queen_list.append(space.label())
						elif space.piece.get_color() == 1:
							if space.piece._isPawn:
								w_pawn_list.append(space.label())
							elif space.piece._isKing:
								w_King = space.label()
							elif space.piece.get_name() == "Bishop":
								w_bishop_list.append(space.label())
							elif space.piece.get_name() == "Knight":
								w_knight_list.append(space.label())
							elif space.piece.get_name() == "Rook":
								w_rook_list.append(space.label())
							elif space.piece.get_name() == "Queen":
								w_queen_list.append(space.label())
		positions = {
			"Black" : {
				"pawns" : b_pawn_list,
				"knights" : b_knight_list,
				"bishops" : b_bishop_list,
				"rooks" : b_rook_list,
				"queens" : b_queen_list,
				"king" : b_King
			},
			"White" : {
				"pawns" : w_pawn_list,
				"knights" : w_knight_list,
				"bishops" : w_bishop_list,
				"rooks" : w_rook_list,
				"queens" : w_queen_list,
				"king" : w_King				
			}
		}
		self._positions = positions
		return self._positions


class Space:
	def __init__(self,x,y):
		self.__x = x
		self.__y = y
		self.__number = [8,7,6,5,4,3,2,1][x-1] #labels for the space
		self.__letter = ['a','b','c','d','e','f','g','h'][((self.__y-1)%8)]
		self.occupied = False #is a piece here?
		self.piece = None #names the Piece object occupying it
		self.__color = self.colorize(self.__x,self.__y) #0 means black, 1 means white
		self.__neighbors = {"north" : None,"north-east": None,"east":None,"south-east":None,"south" : None,"south-west":None,"west":None,"north-west":None}
		self.isThreatened = 0

	def __repr__(self):
		if self.piece == None:
			return "0|"
		else:
			return self.piece.__repr__()
		#return self.label() + '|' + str(self.get_color()) + '|'

	def _set_neighbors(self,N,NE,E,SE,S,SW,W,NW):
		self.__neighbors["north"] = N
		self.__neighbors["north-east"] = NE
		self.__neighbors["east"] = E
		self.__neighbors["south-east"] = SE
		self.__neighbors["south"] = S
		self.__neighbors["south-west"] = SW
		self.__neighbors["west"] = W
		self.__neighbors["north-west"] = NW

	def colorize(self,x,y):
		if x%2 == 1:
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

	def get_neighbors(Self):
		return self.__neighbors

class Piece:
	def __init__(self,x,y,Board):
		self._vectors = {"Default" : [[None,None]]} #all vectors are relative to white's point of view with a1 at 0,0 
		self._color = None #white:1 or black:0      #vectors are used to implement blocking
		self._name = "Default"						#vectors are sorted from nearest move in a direction [0] to farthest [7]
		self.__possible_moves = [[None,None]] #array of narrowed down moves for this piece
		self._possible_attacks = self.__possible_moves #this is unaltered except for pawns
		self._isKing = False
		self._isPawn = False
		self.num_moves = 0 #necessary for pawn first move, and castling
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
		if self._isPawn:
			if self._color == 0: #black pawn, different initialization than default
				self.__possible_moves = [[self.space.get_x(),self.space.get_y()-2],[self.space.get_x(),self.space.get_y()-1]] 
				self._possible_attacks = [[self.space.get_x()-1,self.space.get_y()-1],[self.space.get_x()+1,self.space.get_y()-1]]
				self._vectors = {"north" : [[self.space.get_x(),self.space.get_y()-2],[self.space.get_x(),self.space.get_y()-1]]}

	def get_color(self):
		return self._color

	def get_name(self):
		return self._name

	def get_vectors(self):
		return self._vectors

	def set_name(self,name):
		self._name = name

	def get_possible_moves(self,Board):
		return self.__possible_moves

	def update(self,Board): #narrows down the moves by searching for blocking among the vectors
		#out of bounds
		for i,move in enumerate(self.__possible_moves):
			if not 1 <= move[0] <= 8:
				del self._possible_moves[i]
			if not 1 <= move[1] <= 8:
				del self._possible_moves[i]
		#TODO implement blocking
		if self._name == "Knight":
			#knights cant be blocked along their attack line
			pass
		else: #all pieces that can be blocked
			if self._isPawn:
				if num_moves > 0: #after the first move pawns can only move 1
					if self._color == 0: #black
						self.__possible_moves = [[self.space.get_x(),self.space.get_y()-1]]
						self._vectors = {"south" : [[self.space.get_x(),self.space.get_y()-1]]}
					else: #white
						self.__possible_moves = [[self.space.get_x(),self.space.get_y()+1]]
						self._vectors = {"north" : [[self.space.get_x(),self.space.get_y()+1]]}
				elif num_moves == 1:
					pass #rules for en-passant go here once movement is figured out
			elif self._isKing:
				#Kings cannot move to any threatened space, also castling
				if num_moves > 0:
					pass

		return self

	def move(self,Board):
		moves = []
		#for space in self.get_possible_moves(): #space is an [x,y]
			#if space

class Pawn(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.__possible_moves = [[self.space.get_x(),self.space.get_y()+2],[self.space.get_x(),self.space.get_y()+1]] #default is initial white pawn
		self._possible_attacks = [[self.space.get_x()+1,self.space.get_y()+1],[self.space.get_x()-1,self.space.get_y()+1]]
		self._vectors = {"north" : [[self.space.get_x(),self.space.get_y()+2],[self.space.get_x(),self.space.get_y()+1]]}
		self.set_name("Pawn")
		self.isPawn = True #for promotion

class King(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.possible()
		self.set_name("King")
		self._isKing = True

	def possible(self):
		self.__possible_moves = [[self.space.get_x()+1,self.space.get_y()+1],[self.space.get_x()+1,self.space.get_y()],[self.space.get_x()+1,self.space.get_y()-1],[self.space.get_x(),self.space.get_y()-1],[self.space.get_x()-1,self.space.get_y()-1],[self.space.get_x()-1,self.space.get_y()],[self.space.get_x()-1,self.space.get_y()+1],[self.space.get_x(),self.space.get_y()+1]]
		self._vectors = {	"north" : [[self.space.get_x(),self.space.get_y()+1]],
							"north-east" : [[self.space.get_x()+1,self.space.get_y()+1]],
							"east"	: [[self.space.get_x()+1,self.space.get_y()]],
							"south-east" : [[self.space.get_x()+1,self.space.get_y()-1]],
							"south" : [[self.space.get_x(),self.space.get_y()-1]],
							"south-west" : [[self.space.get_x()-1,self.space.get_y()-1]],
							"west" 	: [[self.space.get_x()-1,self.space.get_y()]],
							"north-west" : [[self.space.get_x()-1,self.space.get_y()+1]]
						}
		#castling possibilities
		if self._color == 0: #black
			pass
		else:
			pass

class Queen(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.possible()
		self.set_name("Queen")

	def possible(self):
		self.__possible_moves = []
		self._vectors = {	"north" : [],
							"north-east" : [],
							"east"	: [],
							"south-east" : [],
							"south" : [],
							"south-west" : [],
							"west" 	: [],
							"north-west" : []
						}
		for i in range(8):
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()])
			self._vectors["east"].append([self.space.get_x()+i,self.space.get_y()])

			self.__possible_moves.append([self.space.get_x(),self.space.get_y()-i])
			self._vectors["south"].append([self.space.get_x(),self.space.get_y()-i])

			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()+i])
			self._vectors["north-east"].append([self.space.get_x()+i,self.space.get_y()+i])

			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()-i])
			self._vectors["south-east"].append([self.space.get_x()+i,self.space.get_y()-i])

			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()-i])
			self._vectors["south-west"].append([self.space.get_x()-i,self.space.get_y()-i])

			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()])
			self._vectors["west"].append([self.space.get_x()-i,self.space.get_y()])

			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()+i])
			self._vectors["north-west"].append([self.space.get_x()-i,self.space.get_y()+i])

			self.__possible_moves.append([self.space.get_x(),self.space.get_y()+i])
			self._vectors["north"].append([self.space.get_x(),self.space.get_y()+i])

class Bishop(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.possible()
		self.set_name("Bishop")

	def possible(self):
		self.__possible_moves = []
		self._vectors = {	"north-east" : [],
							"south-east" : [],
							"south-west" : [],
							"north-west" : []
						}
		for i in range(8):
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()+i])
			self._vectors["north-east"].append([self.space.get_x()+i,self.space.get_y()+i])

			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()-i])
			self._vectors["south-east"].append([self.space.get_x()+i,self.space.get_y()-i])

			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()-i])
			self._vectors["south-west"].append([self.space.get_x()-i,self.space.get_y()-i])

			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()+i])
			self._vectors["north-west"].append([self.space.get_x()-i,self.space.get_y()+i])

class Knight(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.possible()
		self.set_name("Knight")

	def possible(self):
		self.__possible_moves = [[self.space.get_x()+1,self.space.get_y()+2],[self.space.get_x()-1,self.space.get_y()+2],[self.space.get_x()+1,self.space.get_y()-2],[self.space.get_x()-1,self.space.get_y()-2],[self.space.get_x()+2,self.space.get_y()+1],[self.space.get_x()+2,self.space.get_y()-1],[self.space.get_x()-2,self.space.get_y()+1],[self.space.get_x()-2,self.space.get_y()-1]]
		self._vectors = { "north" : [[None,None]]} #knight cannot be blocked so vectors are irrelevant

class Rook(Piece):
	def __init__(self,x,y,Board):
		Piece.__init__(self,x,y,Board)
		self.possible()
		self.set_name("Rook")

	def possible(self):
		self.__possible_moves = []
		self._vectors = {	"north" : [],
							"east"	: [],
							"south" : [],
							"west" 	: [],
						}
		for i in range(8):
			self.__possible_moves.append([self.space.get_x()+i,self.space.get_y()])
			self._vectors["east"].append([self.space.get_x()+i,self.space.get_y()])

			self.__possible_moves.append([self.space.get_x(),self.space.get_y()-i])
			self._vectors["south"].append([self.space.get_x(),self.space.get_y()-i])

			self.__possible_moves.append([self.space.get_x()-i,self.space.get_y()])
			self._vectors["west"].append([self.space.get_x()-i,self.space.get_y()])

			self.__possible_moves.append([self.space.get_x(),self.space.get_y()+i])
			self._vectors["north"].append([self.space.get_x(),self.space.get_y()+i])

class Player():
	def __init__(self,color,Board,begin=True):
		if begin: #default initialization at turn 0
			self.current_pieces = []
			self.captured_pieces = [] #other player's pieces
			if color%2 == 0:#white
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
		else: #it is not turn 0 so get positions from the Board
			pass

	def get_color(self):
		return self.__color
			
	#TODO add capture method, transfer pieces between arrays
class Game():
	def __init__(self):
		self.__board = Board()
		self._player_one = Player(1,self.__board) #white
		self._player_two = Player(2,self.__board) #black
		self._num_turns = 0
		self._turns = [self.__board.positions()]
		self.__db_init()

	def __repr__(self):
		return self.__board.__repr__()

	def get_board(self):
		return self.__board

	def get_p1(self):
		return self._player_one

	def get_p2(self):
		return self._player_two

	def get_num_turns(self):
		return self._num_turns
	#establishing permanence of a game using the explicit model methods
	def __db_init(self):
		#TODO add read method to check if this game is already in the database
		self._white_turns_db = []
		self._black_turns_db = []
		self._game_db = savedGame.objects.create(numTurns = self._num_turns,whoseTurn = True) #True = White, False = Black
		self._game_db.save()
		self._player1_db = savedPlayer.objects.create(color = self._player_one.get_color(),Game = self._game_db) #White
		self._player2_db = savedPlayer.objects.create(color = self._player_two.get_color(),Game = self._game_db) #Black
		self._player1_db.save()
		self._player2_db.save()
		myPositions = self.__board.positions()
		whiteTurn = Turn.objects.create(Player = self._player1_db, pawns = myPositions['White']['pawns'], knights = myPositions['White']['knights'], bishops = myPositions['White']['bishops'], rooks = myPositions['White']['rooks'], queens = myPositions['White']['queens'], king = myPositions['White']['king'])
		blackTurn = Turn.objects.create(Player = self._player1_db, pawns = myPositions['Black']['pawns'], knights = myPositions['Black']['knights'], bishops = myPositions['Black']['bishops'], rooks = myPositions['Black']['rooks'], queens = myPositions['Black']['queens'], king = myPositions['Black']['king'])
		whiteTurn.save()
		blackTurn.save()
		self._white_turns_db.append(whiteTurn)
		self._black_turns_db.append(blackTurn)


	def _turn(self):
		self._num_turns += 1
		myPositions = self.__board.positions()
		whiteTurn = Turn.objects.create(Player = self._player1_db, pawns = myPositions['White']['pawns'], knights = myPositions['White']['knights'], bishops = myPositions['White']['bishops'], rooks = myPositions['White']['rooks'], queens = myPositions['White']['queens'], king = myPositions['White']['king'])
		blackTurn = Turn.objects.create(Player = self._player1_db, pawns = myPositions['Black']['pawns'], knights = myPositions['Black']['knights'], bishops = myPositions['Black']['bishops'], rooks = myPositions['Black']['rooks'], queens = myPositions['Black']['queens'], king = myPositions['Black']['king'])
		whiteTurn.save()
		blackTurn.save()
		self._white_turns_db.append(whiteTurn)
		self._black_turns_db.append(blackTurn)

#permanent objects 
#the saved data constitutes what we need to rebuild a game if a user went away or closed the browser
#There is a table of Games. Games have many Players (Generally 2). Games have the number of Turns (each Turn composed of each player moving once) and whose turn it is.
#Players have many Turns. Players have a color (white or black). Players have a number of Turns that they have moved.0
#Turns have entries with the piece names and a list of the positions each piece is in.

class savedGame(models.Model):
	numTurns = models.IntegerField(default = 0)
	whoseTurn = models.BooleanField(default = True) #True = White, False = Black

class savedPlayer(models.Model):
	color = models.IntegerField() #0 for black, 1 for white
	Game = models.ForeignKey('savedGame',on_delete=models.CASCADE)

class Turn(models.Model): #takes a server Board function object to create a current layout of the board
	Player = models.ForeignKey('savedPlayer',on_delete=models.CASCADE)
	pawns = ArrayField(
		models.CharField(max_length = 2,blank = True), size=8 #[a4,b6,d5,....]
		)
	knights = ArrayField(
		models.CharField(max_length = 2,blank = True), size=10
		)
	bishops = ArrayField(
		models.CharField(max_length = 2, blank = True), size= 10
		)
	rooks = ArrayField(
		models.CharField(max_length = 2, blank = True), size= 10
		)
	queens = ArrayField(
		models.CharField(max_length = 2, blank = True), size= 10
		)
	king = models.CharField(max_length = 2, blank = True) #ie a1 or h1
