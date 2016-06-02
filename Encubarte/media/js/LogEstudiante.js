
window.onload=function(){
	CursorOn();
	CursorOut();
}

function CursorOn(celda){
	celda.style.backgroundColor="#FFBF00"
	celda.style.color="#FE2E2E"
}

function CursorOut(celda){
	celda.style.backgroundColor="#FE2E2E"
	celda.style.color="#FFBF00"
}