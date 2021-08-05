var pago_cancelado = 0
$(document).ready(function() {

    var socket = new WebSocket('ws://127.0.0.1:8000');
    socket.onopen = websocket_conexion_ok;

    socket.onmessage = websocket_msj_recibido;


});

function opcionPresionada(opcion) {
    var op1 = $("input[type=checkbox][name=op1]:checked").val()
    var op2 = $("input[type=checkbox][name=op2]:checked").val()
    var op3 = $("input[type=checkbox][name=op3]:checked").val()
    if (opcion == 1) {
        deshabilitar_opciones();
        habilitar_opcion("#op1")
    } else if (opcion == 2) {
        deshabilitar_opciones();
        habilitar_opcion("#op2")
    } else if (opcion == 3) {
        deshabilitar_opciones();
        habilitar_opcion("#op3")
    }



    // $('#cobro').trigger('click');
    // $('#recarga').trigger('click');
    $('[href="#recarga"]').tab('show');
    // console.log("fin");
}

function habilitar_opcion(opcion) {
    console.log("opcion:...", opcion);
    $(opcion).prop("checked", true);
}

function deshabilitar_opciones(num) {
    $("#op1").prop("checked", false);
    $("#op2").prop("checked", false);
    $("#op3").prop("checked", false);
}

function aler() {
    pago_cancelado = 1
    alert(pago_cancelado);
}

function enviar_respuesta() {
    console.log(pago_cancelado)
}

function websocket_conexion_ok() {
    //alert();

}

function websocket_msj_recibido(e) {

    datos = JSON.parse(e.data);
    //alert('mensaje recibido' + datos.fecha);
    enviar_respuesta()
    $('#contador').text(datos.monto)
    if (datos.fecha == undefined) { datos.fecha = "-" }
    if (datos.monto_ingresar == undefined) { datos.monto_ingresar = "-" }
    if (datos.monto_ingresado == undefined | datos.monto_ingresado == 0) { datos.monto_ingresado = "--" }
    if (datos.monto_a_dispensar == undefined) { datos.monto_a_dispensar = "-" }
    if (datos.folio == undefined) { datos.folio = "-" }
    if (datos.hora_entrada == undefined) { datos.hora_entrada = "-" }
    if (datos.tiempo_estacionado == undefined) { datos.tiempo_estacionado = "-" }
    if (datos.descuento == undefined) { datos.descuento = "--" }

    if (datos.X_17 == undefined) { datos.X_17 = "-" } else { datos.X_17 = "$" + datos.X_17 + ".00" }
    if (datos.X_20 == undefined) { datos.X_20 = "-" } else { datos.X_20 = "$" + datos.X_20 + ".00" }

    if (datos.ph == undefined) { datos.ph = "-" } else { datos.ph = datos.ph }
    if (datos.ec == undefined) { datos.ec = "-" } else { datos.ec = datos.ec }
    if (datos.temperatura == undefined) { datos.temperatura = "-" } else { datos.temperatura = datos.temperatura + "°C" }

    $('#sensor-ph').text(datos.ph)
    $('#sensor-ec').text(datos.ec)
    $('#sensor-temperatura').text(datos.temperatura)


    $('.date').text(datos.fecha)
    $('.total-td').text(datos.X_17)
    $('.ingresado-td').text(datos.X_20)

    $('#monto_ingresar').text(datos.monto_ingresar)
    $('#monto_ingresado').text(datos.monto_ingresado)
    $('#monto_a_dispensar').text(datos.monto_a_dispensar)
    $('#folio').text(datos.folio)
    $('#hora_entrada').text(datos.hora_entrada)
    $('#tiempo_estacionado').text(datos.tiempo_estacionado)
    $('#descuento').text(datos.descuento)
        //$("#t1").click(function () {
    if (datos.interfaz == 1) {
        $("#tab-4").prop("checked", true);
    }
    if (datos.interfaz == 2) {
        $("#tab-5").prop("checked", true);
    }
    if (datos.interfaz == 3) {
        $("#tab-6").prop("checked", true);
    }
    if (datos.interfaz == 6) {
        $("#expedidora").prop("active", true);
    }

    if (datos.presencia == 1) {
        $("#presencia").css("background-color", "rgb(51, 214, 51)");
    }
    if (datos.retorno == 1) {
        $("#retorno").css("background-color", "rgb(51, 214, 51)");
    }
    if (datos.boton_ticket == 1) {
        $("#boton_ticket").css("background-color", "rgb(51, 214, 51)");
    }
    if (datos.secuencia_expedicion == 2) {
        $(".insert-ticket").text("Imprmiendo");
    }
    if (datos.secuencia_expedicion == 3) {
        $(".insert-ticket").text("Lo siento");
    }
    if (datos.secuencia_expedicion == 4) {
        $(".insert-ticket").text("Bienvenido");
    }
    if (datos.secuencia_expedicion == 5) {
        $(".insert-ticket").text("Por favor espere...");
        $("#img_secuencia_expedicion").attr("src", "{% static 'ui/images/insertar_ticket.gif' %}");
    }
    //$("#tab-4").prop("checked", true);
    //$("#tab-4").attr("checked", "checked");
    //alert($('input:radio[id=tab-4]:checked').val());
    //$("#tab-4").attr("checked", "checked");

    //	})
    //$('#X_20').text(datos.monto)

    //$('#tabs').tabs('opcion','active',2)
    //$tabs.tabs('select', 1);
    //$("#tabs").tabs("option", "active", 1);

    //var tabs = $("#tabs").tabs();
    //var $tabs = $('#tabs').tabs(); // first tab selected
    //$tabs.tabs('select', 1);

    $('.tabs a[href="#tab-1"]').tab('show')

    //$("#tab-5").prop("checked", false);
    $("#t1").prop("checked", true);

    //var index = $('#tabs a[href="#tab-1"]').parent().index();
    //$("#tabs").tabs("option", "active", index);


}