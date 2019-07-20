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
					new_space = Space(i,k)	#0,0 = 
				row.append(new_space)
			self.__grid.append(row)
		self.__init_neighbors()
		self._positions = {"" : {"" : [] }}

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

	def get_Space(self,row,col): #y from 1 to 8 counted by 1 = row 8, 2 = row 7, 3 = row 6
		if not 1<=row<=8:		 #x from 1 to 8 counted by 1 = a, 2 = b
			return None
		if not 1<=col<=8:
			return None
		trans_y = [None,8,7,6,5,4,3,2,1,None][col]
		return self.__grid[row][col]

	def get_Space_by_label(self,label):
		check_letter = ['a','b','c','d','e','f','g','h']
		check_num = ["1","2","3","4","5","6","7","8"]
		index = [None,None]
		if len(label) != 2:
			return None
		for i in range(len(check_letter)):
			if label[0] == check_letter[i]:
				for k in range(len(check_num)):
					if label[1] == check_num[k]:
						return self.get_Space(int(check_num[k]),i+1)
		return None
	#this function iterates over each space to find each piece and calculates all the possible moves that all the pieces can make, 
	#taking the board and all the other pieces into account, and assigns the possible move list to that piece object
	#update is overriden for pieces such as Pawns and Knights
	def update(self): 
		for row in self.__grid: #this is my most beautiful function
			if row[1] != None:
				for space in row:
					if space != None:
						if space.piece != None:
							space.piece.update(self) #SO MUCH WORK to get this one line of code

	def is_occupied(self,x,y):
		if not 1<=x<=8:
			return None
		if not 1<=y<=8:
			return None
		return self.__grid[y][x].occupied

	def get_positions(self):
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
		self.__row = x
		self.__col = y
		self.__number = [8,7,6,5,4,3,2,1][self.__row-1] #labels for the space
		self.__letter = ['a','b','c','d','e','f','g','h'][((self.__col-1)%8)]
		self.occupied = False #is a piece here?
		self.piece = None #names the Piece object occupying it
		self.__color = self.colorize(self.__row,self.__col) #0 means black, 1 means white
		self.__neighbors = {"north" : None,"north-east": None,"east":None,"south-east":None,"south" : None,"south-west":None,"west":None,"north-west":None}
		self.isThreatened = [0,0] #0th index = black threatens, 1st index = white threatens

	def __repr__(self):
		# if self.piece == None:
		# 	return "0|"
		# else:
		# 	return self.piece.__repr__()
		return self.label() + '|'
		#return str(self.occupied) + '|'

	def _set_neighbors(self,N,NE,E,SE,S,SW,W,NW):
		self.__neighbors["north"] = N
		self.__neighbors["north-east"] = NE
		self.__neighbors["east"] = E
		self.__neighbors["south-east"] = SE
		self.__neighbors["south"] = S
		self.__neighbors["south-west"] = SW
		self.__neighbors["west"] = W
		self.__neighbors["north-west"] = NW

	def connect_piece(self,Piece):
		return 0

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

	def connect_piece(self,Piece): #returns the previous piece
		ex_piece = self.piece
		self.piece = Piece
		return ex_piece

	def get_row(self):
		return self.__row

	def get_col(self):
		return self.__col

	def label(self):
		output = "" + self.__letter + str(self.__number)
		return output

	def get_color(self):
		return self.__color

	def get_neighbors(self):
		return self.__neighbors

	def occupy(self):
		self.occupied = True

	def leave(self):
		self.occupied = False

class Piece:
	def __init__(self,x,y,Board,color):
		self._vectors = {"Default" : 0} #all vectors are direction and magnitude, with north being 
		self._color = color%2 #white:1 or black:0      #vectors are used to implement blocking
		self._name = "Default"						#vectors are sorted from nearest move in a direction [0] to farthest [7]
		self.__possible_moves = [[None,None]] #array of narrowed down moves for this piece
		self._possible_attacks = self.__possible_moves #this is unaltered except for pawns
		self._isKing = False
		self._isPawn = False
		self.num_moves = 0 #necessary for pawn first move, and castling
		self.space = Board.get_Space(x,y) #names the space object that this piece occupies
		Board.get_Space(x,y).connect_piece(self) #establishes a linked-list type structure of pieces and spaces
		Board.get_Space(x,y).occupy()

	def __repr__(self):
		if self._name[0] != 'K':
			return self._name[0] + '|'
		else:
			return self._name[0] + self._name[1] + '|'

	def set_color(self,color):
		self._color = color

	def castling(self,Board):
		pass

	def connect_space(self,Space):
		ex_space = Space.connect_piece(self)
		return ex_space #returns space that it used to connect to

	def get_color(self):
		return self._color

	def get_vectors(self):
		return self._vectors

	def get_name(self):
		return self._name

	def get_vectors(self):
		return self._vectors

	def set_name(self,name):
		self._name = name

	def get_possible_moves(self):
		return self.__possible_moves

	def set_possible_moves(self,set_to):
		self.__possible_moves = set_to

	def add_possible_move(self,move_to_add):
		self.__possible_moves.append(move_to_add)
	#this is the algorithm that determines whether a piece is blocked along a line of attack at each game state. Each piece calculates this on its own in regards to the board
	#the possible moves are calculated using vectors, which is a dictionary for each piece that has a direction key and magnitude value
	def update(self,Board): #sets the possible moves after moving using vectors
		self.set_possible_moves([])
		if self._name == "Knight": #knight can't be blocked
			raise Exception('Knight did not update its moves correctly') #method is overriden anyway, excess of caution
			return self
		elif self._isPawn:
			raise Exception('Pawn did not update its moves correctly') #method is overriden anyway, excess of caution
			return self
		elif self._isKing:
			self.castling(Board)
		for direction,magnitude in self._vectors.items():
			counter = 0
			curSpace = self.space
			beenBlocked = False
			enemyPiece = False
			while counter < magnitude:
				if curSpace == None: #we have hit the boundary, try a different direction
					break
				myNeighbors = curSpace.get_neighbors()
				if myNeighbors[direction] == None:
					break #hit the boundary
				myNeighbors[direction].isThreatened[self._color%2] += 1
				checkSpace = myNeighbors[direction].occupied
				if not beenBlocked: #if the piece hasn't been blocked we can still capture and move
					if checkSpace: #there is a piece here
						blocker = myNeighbors[direction].piece
						if blocker.get_color() == self.get_color():
							#the piece is the same color as mine and totally blocks it
							beenBlocked = True
							counter = magnitude
							break #GOTO a different direction
						else:
							#there is a piece here to capture, but that piece blocks my move past this location. However, I still threaten beyond this location
							beenBlocked = True
							enemyPiece = True
							self.add_possible_move(myNeighbors[direction])
					else: #no piece here, can move
						self.add_possible_move(myNeighbors[direction])
				if enemyPiece: #we have been blocked by a piece not the same color as mine -> havent broken the loop. We cant attack or move but can still threaten until we meet a piece of the same color as mine
					if checkSpace:
						blocker = myNeighbors[direction].piece
						if blocker.get_color() == self._color: #however now we have been blocked by a piece of the same color
							counter = magnitude
							break #GOTO a different direction
				counter += 1
				curSpace = curSpace.get_neighbors()[direction] #points to next space in $direction
		return self

	def move(self,Board):
		pass

class Pawn(Piece):
	def __init__(self,x,y,Board,color):
		Piece.__init__(self,x,y,Board,color)
		self.set_name("Pawn")
		self._isPawn = True #for promotion
		
	def __possible(self):
		pass #pawn's vectors needs to be more dynamic

	def update(self,Board): #Pawn blocking works different since their move is unequivocally blocked by any piece, but their attacks are never blocked
		self.set_possible_moves([])
		vector_magnitude = 2
		if self.num_moves > 0:
			vector_magnitude = 1
		if self._color == 0: #black pawn
			i = 1
			while i <= vector_magnitude: #moving forward
				newSpace = Board.get_Space(self.space.get_row()+i,self.space.get_col())
				if not newSpace.occupied:
					self.add_possible_move(newSpace)
				i += 1
			self._possible_attacks = [Board.get_Space(self.space.get_row()+1,self.space.get_col()+1),Board.get_Space(self.space.get_row()+1,self.space.get_col()-1)]
			self._vectors = {"south" : vector_magnitude}
		else: #white pawn
			i = 1
			while i <= vector_magnitude: #moving forward
				newSpace = Board.get_Space(self.space.get_row()-i,self.space.get_col())
				if not newSpace.occupied:
					self.add_possible_move(newSpace)
				i += 1
			self._possible_attacks = [Board.get_Space(self.space.get_row()-1,self.space.get_col()-1),Board.get_Space(self.space.get_row()-1,self.space.get_col()+1)]
			self._vectors = {"north" : vector_magnitude}

class King(Piece):
	def __init__(self,x,y,Board,color):
		Piece.__init__(self,x,y,Board,color)
		self.__possible(Board)
		self.set_name("King")
		self._isKing = True
		self.canCastleEast = False
		self.canCastleWest = False

	def __possible(self,Board):
		self._vectors = {	"north" : 1,
							"north-east" : 1,
							"east"	: 1,
							"south-east" : 1,
							"south" : 1,
							"south-west" : 1,
							"west" 	: 1,
							"north-west" : 1
						}
		#castling possibilities
	def castling(self,Board):
		colARook = {}
		colHRook = {}
		self.canCastleEast = False
		self.canCastlewest = False
		if self.get_color() == 0 and self.num_moves == 0: #black King hasnt moved
			colARook = Board.get_Space_by_label("a8").piece
			colHRook = Board.get_Space_by_label("h8").piece
			if colARook.get_name() == "Rook" and colARook.num_moves == 0: #rook hasnt moved
				checkSpaceB = Board.get_Space_by_label("b8")
				checkSpaceC = Board.get_Space_by_label("c8")
				if checkSpaceB.piece == None and checkSpaceC.piece == None: #no pieces in the way
					if checkSpaceB.isThreatened[1] == 0 and checkSpaceC.isThreatened[1] == 0: #no threats from white that king moves through
						self.add_possible_move(Board.get_Space_by_label("b8"))
						self.canCastleWest = True
			elif colHRook.get_name() == "Rook" and colARook.num_moves == 0: #check for other rook
				checkSpaceE = Board.get_Space_by_label("e8")
				checkSpaceF = Board.get_Space_by_label("f8")
				if checkSpaceE.piece == None and checkSpaceF.piece == None:
					if checkSpaceE.isThreatened[1] == 0 and checkSpaceFisThreated[1] == 0:
						self.add_possible_move(Board.get_Space_by_label("f8"))
						self.canCastleEast = True
		elif self.get_color() == 1 and self.num_moves == 0: #white king hasnt moved
			colARook = Board.get_Space_by_label("a1").piece
			colHRook = Board.get_Space_by_label("h1").piece
			if colARook.get_name() == "Rook" and colARook.num_moves == 0: #rook hasnt moved
				checkSpaceB = Board.get_Space_by_label("b1")
				checkSpaceC = Board.get_Space_by_label("c1")
				if checkSpaceB.piece == None and checkSpaceC.piece == None: #no pieces in the way
					if checkSpaceB.isThreatened[0] == 0 and checkSpaceC.isThreatened[0] == 0: #no threats from black that king moves through
						self.add_possible_move(Board.get_Space_by_label("b1"))
						self.canCastleWest = True
			elif colHRook.get_name() == "Rook" and colARook.num_moves == 0: #check for other rook
				checkSpaceE = Board.get_Space_by_label("e1")
				checkSpaceF = Board.get_Space_by_label("f1")
				if checkSpaceE.piece == None and checkSpaceF.piece == None:
					if checkSpaceE.isThreatened[0] == 0 and checkSpaceFisThreated[0] == 0:
						self.add_possible_move(Board.get_Space_by_label("f1"))
						self.canCastleEast = True

class Queen(Piece):
	def __init__(self,x,y,Board,color):
		Piece.__init__(self,x,y,Board,color)
		self.__possible()
		self.set_name("Queen")

	def __possible(self):
		self._vectors = {	"north" : 8,
							"north-east" : 8,
							"east"	: 8,
							"south-east" : 8,
							"south" : 8,
							"south-west" : 8,
							"west" 	: 8,
							"north-west" : 8
						}

class Bishop(Piece):
	def __init__(self,x,y,Board,color):
		Piece.__init__(self,x,y,Board,color)
		self.__possible()
		self.set_name("Bishop")

	def __possible(self):
		self._vectors = {	"north-east" : 8,
							"south-east" : 8,
							"south-west" : 8,
							"north-west" : 8
						}

class Knight(Piece):
	def __init__(self,x,y,Board,color):
		Piece.__init__(self,x,y,Board,color)
		self.set_name("Knight")

	def __possible(self,Board):
		self.set_possible_moves([ #possible function call pattern here is different since Knight doesnt depend on vectors for updating
								Board.get_Space(self.space.get_row()+1,self.space.get_col()+2),
								Board.get_Space(self.space.get_row()-1,self.space.get_col()+2),
								Board.get_Space(self.space.get_row()+1,self.space.get_col()-2),
								Board.get_Space(self.space.get_row()-1,self.space.get_col()-2),
								Board.get_Space(self.space.get_row()+2,self.space.get_col()+1),
								Board.get_Space(self.space.get_row()+2,self.space.get_col()-1),
								Board.get_Space(self.space.get_row()-2,self.space.get_col()+1),
								Board.get_Space(self.space.get_row()-2,self.space.get_col()-1)])
		self._vectors = { "north" : 0 } #knight cannot be blocked so vectors are irrelevant

	def update(self,Board): #the update for Knight is much simpler without having to check for blocking pieces
		self.__possible(Board)
		actualMoves = []
		for move in self.get_possible_moves():
			#piece_here = None
			if move == None:
				pass #if the move is out of bounds
			elif move.piece == None:
				actualMoves.append(move) #there is no piece here, can move
			elif move.piece.get_color() == self.get_color():
				pass #if there is a piece here and its mine
			else: #there is a piece here and its not mine
				actualMoves.append(move)
		self.set_possible_moves(actualMoves)

class Rook(Piece):
	def __init__(self,x,y,Board,color):
		Piece.__init__(self,x,y,Board,color)
		self.__possible()
		self.set_name("Rook")

	def __possible(self):
		self._vectors = {	"north" : 8,
							"east"	: 8,
							"south" : 8,
							"west" 	: 8,
						}

class Player():
	def __init__(self,color,Board,begin=True):
		if begin: #default initialization at turn 0
			self.current_pieces = []
			self.captured_pieces = [] #other player's pieces
			if color%2 == 0:#black
				self.__color = 0
				for i in range(8):
					newPawn = Pawn(2,i+1,Board,self.__color)
					self.current_pieces.append(newPawn)
					if i == 0 or i == 7:
						newRook = Rook(1,i+1,Board,self.__color)
						self.current_pieces.append(newRook)
					elif i == 1 or i == 6:
						newKnight = Knight(1,i+1,Board,self.__color)
						self.current_pieces.append(newKnight)
					elif i == 2 or i == 5:
						newBishop = Bishop(1,i+1,Board,self.__color)
						self.current_pieces.append(newBishop)
					elif i == 4:
						newQueen = Queen(1,i+1,Board,self.__color)
						self.current_pieces.append(newQueen)
					else: #i == 3
						newKing = King(1,i+1,Board,self.__color)
						self.current_pieces.append(newKing)
			else: #white
				self.__color = 1
				for i in range(8):
					newPawn = Pawn(7,i+1,Board,self.__color)
					self.current_pieces.append(newPawn)
					if i == 0 or i == 7:
						newRook = Rook(8,i+1,Board,self.__color)
						self.current_pieces.append(newRook)
					elif i == 1 or i == 6:
						newKnight = Knight(8,i+1,Board,self.__color)
						self.current_pieces.append(newKnight)
					elif i == 2 or i == 5:
						newBishop = Bishop(8,i+1,Board,self.__color)
						self.current_pieces.append(newBishop)
					elif i == 4:
						newQueen = Queen(8,i+1,Board,self.__color)
						self.current_pieces.append(newQueen)
					else: #i == 3
						newKing = King(8,i+1,Board,self.__color)
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
		self.__board.positions()
		self.__board.update() #calls all the updates for the pieces
		self._num_turns = 0
		self._turns = [self.__board.get_positions()] #add to this as the game goes on
		self.__db_init()
		#print(self.__board.get_positions())

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
	#establishing permanence of a game using the Django model methods
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
#Players have many Turns. Players have a color (white or black). Players have a number of Turns that they have moved.
#Turns have entries with the piece names and a list of the positions each piece is in.
class turnManager(models.Manager):
	def move_validator(self,postData):
		errors = {}
		if postData['piece'] not in ['pawn','knight','bishop','rook','queen','king']:
			errors['piece'] = "piece not recognized"
		if len(postData['square']) != 2:
			errors['square'] = "not a square"
		elif postData['square'][0] not in ['a','b','c','d','e','f','g','h']:
			errors['square'] = "square letter not recognized"
		elif postData['square'][1] not in ['1','2','3','4','5','6','7','8']:
			errors['square'] = "square number not recognized"
		return errors
		
class savedGame(models.Model):
	numTurns = models.IntegerField(default = 0)
	whoseTurn = models.BooleanField(default = True) #True = White, False = Black

class savedPlayer(models.Model):
	color = models.IntegerField() #0 for black, 1 for white
	Game = models.ForeignKey('savedGame',on_delete=models.CASCADE)

class turn(models.Model): #takes a server Board function object to create a current layout of the board
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

def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")