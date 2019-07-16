$(document).ready(function() {
	lastClickedSquare = undefined
	lastSquares = [undefined]
    $('.chessSquare').click(function(){
    	if (lastClickedSquare !== undefined){ //un-highlights previously highlighted squares
    		lastClickedSquare.removeClass('blueHighlight')
    	}
    	if (lastSquares[0] !== undefined){
    		for(var k = 0; k < lastSquares.length; k++){
    			lastSquares[k].removeClass('yellowHighlight')
    		}
    	}
		sqLabel = $(this).attr('id')
		piece = $(this).children().attr('id')
		if (piece === undefined){

		}
		else{
			//there is a piece on this space
			lastSquares = []
			lastClickedSquare = $(this)
			lastClickedSquare.addClass('blueHighlight')
			pieceChildrenArray = $(this).children().children()
			for(var i = 1; i < pieceChildrenArray.length;i++){
				possibleMoveStr = pieceChildrenArray[i].attributes.id.value //gets all the values of the generated data divs of possible moves
				possibleMoveStr = possibleMoveStr.substring(0, possibleMoveStr.length - 1) //cuts off pipe at end of string
				possibleMoveSquare = $('[id='+ possibleMoveStr +']') //finds id of square to highlight
				possibleMoveSquare.addClass('yellowHighlight')
				lastSquares.push(possibleMoveSquare)
			}
			console.log(lastSquares,lastClickedSquare)
		}
	});
});

