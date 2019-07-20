$(document).ready(function() {
	window.lastClickedSquare = undefined;
	window.lastSquares = [undefined];
	window.pieceIsSelected = false;
	moveEvent = new Event("move",{bubbles:false,cancelable:false});
	loadEvent = new Event("load",{bubbles:false,cancelable:false});
	window.movePiece = "default";
	window.moveTo = "default";

	//this function fires off the move event should the user click a square to move to
	//this function also fires off the load event when the response is received
	window.addEventListener("move",() => ajaxNewBoard(window,loadEvent), false);

	//this function fires when the board loads and enables move choosing functionality for that new game-state
	window.addEventListener("load",() => assignPossibilities(moveEvent), false);

	//starts the cycle with default board, triggering the first loading event
	ajaxDefaultBoard(window,loadEvent);
});
//this function only binds possibilities to clicking on that chess square
function assignPossibilities(myEvent){
	$('.chessSquare').click(function(){
		possibilities($(this),window,myEvent)
	});
}
//ajax GET HTTP call to load initial board
function ajaxDefaultBoard(myWindow,myEvent){
	$.ajax(
		{
			type: "GET"
			url : "/board",
			success: function(result)
			{
				$('#board').html(result);
				myWindow.dispatchEvent(loadEvent)
			}
		}
	)
}
//ajax POST HTTP call to load any n > 0 boards
function ajaxNewBoard(myWindow,myEvent){
	valid = true
	piece = myWindow.movePiece.toLowerCase()
	square = myWindow.moveTo.toLowerCase()
	if(square.length  != 2){
		valid = false
	}
	else if(!(['a','b','c','d','e','f','g','h'].includes(square[0]))){
		valid = false
	}
	else if(!(['1','2','3','4','5','6','7','8'].includes(square[1]))){
		valid = false
	}
	if(!(['pawn','knight','bishop','rook','queen','king'].includes(piece))){
		valid = false
	}
	postUrl = "/board/new?piece=" + piece + "&" + "square=" + square
	if(valid){
		console.log("POST URL: ",postUrl)
		$.ajax(
		{
			type: "POST",
			url: postUrl,
			success: function(result)
				{
					console.log("POST RESULT: ",result)
					$('#board').html(result)
					myWindow.dispatchEvent(myEvent)
				}	
		})
	}
}
//this function adds highlights and defines a move-click on the loaded board
function possibilities(square,myWindow,myEvent){
	//square is the clicked square, or $this in the caller scope
	//myWindow is the window DOM object
	myWindow.sqLabel = $(square).attr('id');
	if(square[0].className.includes("potentialMove")){ //we have clicked a second time for the correct square for the piece to move to
	//we have selected a potential move square
		myWindow.movePiece = myWindow.clickedPiece
		myWindow.moveTo = myWindow.sqLabel
		myWindow.dispatchEvent(myEvent)
		//TODO add piece move animation to cover loading event
	}
	if (myWindow.lastClickedSquare !== undefined){ //un-highlights previously highlighted squares
		$(myWindow.lastClickedSquare).removeClass('selectedPiece');
	}
	if (myWindow.lastSquares[0] !== undefined){
		for(var k = 0; k < lastSquares.length; k++){
			$(myWindow.lastSquares[k]).removeClass('potentialMove');
		}
	}
	myWindow.lastClickedSquare = $(square)
	myWindow.clickedPiece = $(square).children().attr('id');
	if (myWindow.clickedPiece === undefined){
		myWindow.pieceIsSelected = false;
	}
	else{
		//there is a piece on this space
		myWindow.pieceIsSelected = true;
		myWindow.lastSquares = [];
		$(myWindow.lastClickedSquare).addClass('selectedPiece');
		pieceChildrenArray = $(square).children().children();
		for(var i = 1; i < pieceChildrenArray.length;i++){
			possibleMoveStr = pieceChildrenArray[i].attributes.id.value; //gets all the values of the generated data divs of possible moves
			possibleMoveStr = possibleMoveStr.substring(0, possibleMoveStr.length - 1); //cuts off pipe at end of string
			possibleMoveSquare = document.getElementById(possibleMoveStr); //finds id of square to highlight
			$(possibleMoveSquare).addClass('potentialMove');
			myWindow.lastSquares.push(possibleMoveSquare);
		}
	}
}