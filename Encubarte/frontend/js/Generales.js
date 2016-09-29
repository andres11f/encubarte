function cambiarDisplay(id) {
	if (!document.getElementById) return false;

	fila = document.getElementById(id);
	if (fila.style.display != "none") 
	{
		fila.style.display = "none"; //ocultar fila 
	} 
	else 
	{
		fila.style.display = ""; //mostrar fila 
		}
}