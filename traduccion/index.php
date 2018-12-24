<!DOCTYPE html>
<html>

	<head>
		<title>LaTex Translator</title>
		<link rel="shortcut icon" href="../css/ilt.ico">
		<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
		<link rel="stylesheet" type="text/css" href="../css/style.css">
		<link rel="stylesheet" type="text/css" href="../css/menu.css">
		<link rel="stylesheet" type="text/css" href="../iconos/iconos.css">
		<link rel="stylesheet" type="text/css" href="../main.css">
	</head>

	<body>
		<header class="header">
			<div class="top">
				<img class="latex-icono" src="../css/ilt.png">
				<h1 class="titulo"><a href="../">LaTex Translator</a></h1>
				<input type="checkbox" id="boton-menu" name="Menu">
				<label class="icon-icon-list" for="boton-menu"></label>
				<nav class="top-menu">
					<ul class="menu">
						<li class="secciones-menu"><a href="../">Inicio</a></li>
						<li class="secciones-menu"><a href="../instrucciones/">Instrucciones de uso</a></li>
						<li class="secciones-menu"><a href="../quienes-somos/">Quiénes somos</a></li>
						<li class="secciones-menu"><a href="../mas/">Más sobre Latex Translator</a></li>
					</ul>
				</nav>
			</div>
		</header>

		<main class="main">
			<div class="titulo-centro">
				<h1>TRADUCTOR</h1>
			</div>
			<div class="cuerpo-centro">
				<div class="traductor">
					<form action="../traduccion/" method="post" enctype="multipart/form-data">
						<div class="cargar">
							<input name="userfile" id="examinar-boton" type="file">
							<label class="icon-examinar" for="examinar-boton"> CARGAR UN ARCHIVO</label>
						</div>
						<div class="traducir">
							<input id="traducir-boton" type="submit" value="Traducir">
							<label class="icon-traducir" for="traducir-boton"> TRADUCIR</label>
						</div>
					</form>
					<?php
					$error = "";
					$folder = "descargar/"; // Carpeta a la que queremos subir los archivos
					$maxlimit = 90000000000000000; // Máximo límite de tamaño (en bits)
					$allowed_ext = "tex"; // Extensiones permitidas
					$overwrite = "no"; // Permitir sobreescritura? (yes/no)
					$match = ""; 
					$filesize = $_FILES['userfile']['size']; // toma el tamaño del archivo
					$filename = $_FILES['userfile']['name'];
					if(!$filename || $filename==""){ // mira si no se ha seleccionado ningún archivo
						$error = "- Ningún archivo selecccionado para subir.
";
					}elseif(file_exists($folder.$filename) && $overwrite=="no"){ // comprueba si el archivo existe ya
						$error = "- El archivo $filename ya existe
";
					}
					// comprobar tamaño de archivo
					if($filesize < 1){ // el archivo está vacío
						$error .= "- Archivo vacío.
";
					}elseif($filesize > $maxlimit){ // el archivo supera el máximo
						$error .= "- Este archivo supera el máximo de tamaño permitido.
";
					}
					$file_ext = preg_split("/\./",$filename); // aquí no tengo claro lo que hace xD
					$allowed_ext = preg_split("/\,/",$allowed_ext); // ídem, algo con las extensiones
					foreach($allowed_ext as $ext){
						if($ext==$file_ext[1]) $match = "1"; // Permite el archivo
					}
					// Extensión no permitida
					if(!$match){
						$error .= "- Este tipo de archivo no está permitido: $filename
";
					}
					if($error){
						print "Se ha producido el siguiente error al subir el archivo:
						$error"; // Muestra los errores
					}else{
						if(move_uploaded_file($_FILES['userfile']['tmp_name'], $folder.$filename)){ // Finalmente sube el archivo
							$mensaje_traduccion = exec('LANG=en_US.UTF-8 python3.6 Main.py "descargar/'.$filename.'"');
							shell_exec('rm "descargar/'.$filename.'"');
							$traducido = substr($filename, 0, -4).' traducido.txt';
							echo '<p class="mensaje-traducido">'.$mensaje_traduccion.'</p>
							<form action="descargar?f='.$traducido.'" method="post">
								<input id="descarga-boton" type="submit" value="Descargar">
								<label class="icon-download" for="descarga-boton">DESCARGAR ARCHIVO FINAL</label>
							</form>';
						}else{
							print "Error! El tamaño supera el máximo permitido por el servidor. Inténtelo de nuevo."; // Otro error
						}
					}
					?>

				</div>
			</div>
		</main>

		<footer class="footer">
			<dir class="social">
				<a class="texto-mail" href="mailto:latextranslator@gmail.com">latextranslator@gmail.com</a>
				<a class="icon-mail" href="mailto:latextranslator@gmail.com" title="Mail(latextranslator@gmail.com)"></a>
				<a class="icon-facebook-squared" href="https://www.facebook.com/latextranslator" name="Facebook" title="Facebook" target="_blank"></a>
			</dir>
			<div class="bot">
				<h4 class="creditos">&copy; LaTeX Translator. All Rights Reserved. </h4>
			</div>
		</footer>
	</body>

</html>