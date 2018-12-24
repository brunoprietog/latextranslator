<?php
	$extensiones = array("txt");
	$f = $_GET["f"];
	if(strpos($f,"/")!==false){
		die("No puedes navegar por otros directorios");
	}
	$ftmp = explode(".",$f);
	$fExt = strtolower($ftmp[count($ftmp)-1]);

	if(!in_array($fExt,$extensiones)){
		die("<b>ERROR!</b> no es posible descargar archivos con la extensión $fExt");
	}

	header("Content-type: application/octet-stream");
	header("Content-Disposition: attachment; filename=\"$f\"\n");
	$fp=fopen("$f", "r");
	fpassthru($fp);
?> 