$(document).ready(function() {
	console.log("javascript")
    $('.chessSquare').click(function(){
		sqLabel = this.attr('id')
		piece = this.children().attr('id')
		console.log(sqLabel,piece)
	});
});
