window.onload=function(){
	ExtraDates();
}

function ExtraDates(){
	var name = document.getElementById("selTipoDocumento");
	if (name.value == "Cedula"){
		document.getElementById("Menpad").style.display = "none";
		document.getElementById("Menpadtel").style.align = "none";
		document.getElementById("Menmad").style.display = "none";
		document.getElementById("Menmadtel").style.display = "none";
		document.getElementById("Mencol").style.align = "none";
		document.getElementById("Mengrad").style.display = "none";
		document.getElementById("Menjor").style.display = "none";
		document.getElementById("NomAcudiente").style.align = "block";
		document.getElementById("TelAcudiente").style.display = "block";
		document.getElementById("Maylab").style.display = "block";
		document.getElementById("Maylug").style.align = "block";
		document.getElementById("file1").style.display = "block";
		document.getElementById("file2").style.display = "block";
		document.getElementById("file3").style.align = "none";
	}else {
		if (name.value == "Tarjeta de Identidad"){
			document.getElementById("Menpad").style.display = "block";
			document.getElementById("Menpadtel").style.align = "block";
			document.getElementById("Menmad").style.display = "block";
			document.getElementById("Menmadtel").style.display = "block";
			document.getElementById("Mencol").style.align = "block";
			document.getElementById("Mengrad").style.display = "block";
			document.getElementById("Menjor").style.display = "block";
			document.getElementById("NomAcudiente").style.align = "block";
			document.getElementById("TelAcudiente").style.display = "block";
			document.getElementById("Maylab").style.display = "none";
			document.getElementById("Maylug").style.align = "none";
			document.getElementById("file1").style.display = "block";
			document.getElementById("file2").style.display = "block";
			document.getElementById("file3").style.align = "block";

	    }else{
	    	if (name.value == "Registro Civil"){
			document.getElementById("Menpad").style.display = "block";
			document.getElementById("Menpadtel").style.align = "block";
			document.getElementById("Menmad").style.display = "block";
			document.getElementById("Menmadtel").style.display = "block";
			document.getElementById("Mencol").style.align = "block";
			document.getElementById("Mengrad").style.display = "block";
			document.getElementById("Menjor").style.display = "block";
			document.getElementById("NomAcudiente").style.align = "block";
			document.getElementById("TelAcudiente").style.display = "block";
			document.getElementById("Maylab").style.display = "none";
			document.getElementById("Maylug").style.align = "none";
			document.getElementById("file1").style.display = "block";
			document.getElementById("file2").style.display = "block";
			document.getElementById("file3").style.align = "block";
	    	}else{
	    	document.getElementById("Menpad").style.display = "none";
			document.getElementById("Menpadtel").style.align = "none";
			document.getElementById("Menmad").style.display = "none";
			document.getElementById("Menmadtel").style.display = "none";
			document.getElementById("Mencol").style.align = "none";
			document.getElementById("Mengrad").style.display = "none";
			document.getElementById("Menjor").style.display = "none";
			document.getElementById("NomAcudiente").style.align = "none";
			document.getElementById("TelAcudiente").style.display = "none";
			document.getElementById("Maylab").style.display = "none";
			document.getElementById("Maylug").style.align = "none";
			document.getElementById("file1").style.display = "none";
			document.getElementById("file2").style.display = "none";
			document.getElementById("file3").style.align = "none";
	    	}
	    }
	}
	
}
