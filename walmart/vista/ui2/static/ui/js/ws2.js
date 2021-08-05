$(document).ready(function() {

    var socket = new WebSocket('ws://0.0.0.0:8000');
    socket.onopen = websocket_conexion_ok;
    socket.onmessage = websocket_msj_recibido;



});

function websocket_conexion_ok() {
    //alert('La conexión se ha establecidoo');
}

function websocket_msj_recibido(e) {
    datos = JSON.parse(e.data);
    //alert('mensaje recibido'+datos.fecha);

    //$('#fecha').text( datos.fecha)
    $('#contador').text(datos.monto)

    /*
    codigo = '<div class="col s12">'				+
    			'<div class="nombre">'				+
    				'<h4>'+ datos.nombre +'</h4>'	+
    			'</div>'							+
    			'<div class="contenido">'			+
    				'<p>'+ datos.mensaje +'</p>'	+
    			'</div>'							+
    		'</div>';
    $('#conversacion').append(codigo);
    */
}