/* Si se quiere leer los datos de un JSON que solo contiene un objeto

1-  cambiar por 'dato.JSON' de la linea  
    xhr.open ('GET', 'datos.json', true);

2-  Descomentar la linea 
    //controlador.establecerDatos(datos, DATOS_ADMINISTRACION);

3-  Comentar la linea
    controlador.establecerTodosLosDatos(datos);

    */


// eventListeners
const boton1 = document.getElementById('boton1');
boton1.addEventListener('click', function() {
    //console.log('Se oprimio el botón');

    const xhr = new XMLHttpRequest();
    xhr.open ('GET', 'datos.json', true);

    xhr.onload= function () {
        if (this.status === 200)  {
            const datos = JSON.parse(this.responseText);
            //controlador.establecerDatos(datos, DATOS_ADMINISTRACION);
            controlador.establecerTodosLosDatos(datos);
        }
    }
    xhr.send();
});


/* Definición de la clase Controlador e interfaz */
// encargado de almacenar las variables y controlar el flujo de la información
class Controlador  {

    constructor (numeroDeX, numeroDeY) {

        this.numeroDeX = numeroDeX;
        this.numeroDeY = numeroDeY;
        this.interfaz = new Interfaz();
    }

    leerVariablesDeControl () {

    }

    establecerTodosLosDatos (datos) {
        //console.log(datos);
        datos.forEach(dato => {

            if (dato.tipo_informacion === "ADMINISTRACION") {
                //console.log("Se obtuvieron los datos de administración");
                this.establecerDatos(dato, DATOS_ADMINISTRACION)
            }

            if (dato.tipo_informacion === "CONTROL") {
                //console.log("Se obtuvieron los datos de control");
                this.establecerDatos(dato, DATOS_CONTROL)
            }

            if (dato.tipo_informacion === "ESTADO") {
                //console.log("Se obtuvieron los datos de estado");
                this.establecerDatos(dato, DATOS_ESTADO)
            }
        });
    }



    establecerDatos (datos, tipoDeDato = 0) {

        switch (tipoDeDato ) {
            case DATOS_ADMINISTRACION:

                console.log('Se recibieron los datos de administración ');
                // Validación de datos
                if (datos.fecha === undefined){
                    datos.fecha = "-"
                    console.log('No hay fecha');
                }
    
                if (datos.monto_ingresar === undefined){
                    datos.monto_ingresar = "-"
                }
                if (datos.monto_ingresar === undefined){
                    datos.monto_ingresar = "-"
                }
                if (datos.monto_ingresado === undefined | datos.monto_ingresado === 0){
                    datos.monto_ingresado = "--"
                }
                if (datos.monto_a_dispensar === undefined){
                    datos.monto_a_dispensar = "-"
                }
                if (datos.folio === undefined){
                    datos.folio = "-"
                }
                if (datos.hora_entrada === undefined){
                    datos.hora_entrada = "-"
                }
                if (datos.tiempo_total === undefined){
                    datos.tiempo_total = "-"
                }
                if (datos.descuento === undefined | datos.descuento === 0){
                    datos.descuento = "--"
                }
    
                break;

            case DATOS_CONTROL:
                console.log('Se recibieron los datos de control ');

                break;

            case DATOS_ESTADO:
                console.log('Se recibieron los datos de estado ');
                break;

            default:
                break;

        } // Fin de switch

        // Después de la validación de datos se envían a la interfaz
        this.interfaz.actualizarDatos(datos, tipoDeDato);


    } // Fin del método establecer datos
}


// Se encarga de la interaccion con la pagina Web
class Interfaz {
    constructor () {

    }
    
    actualizarDatos(datos, tipoDeDato) {
        //console.log('Dentro de interfaz');
        //console.log(tipoDeDato);


        let areaDeEscritura;
        let div;
        let texto;

        switch (tipoDeDato) {
            case DATOS_ADMINISTRACION:

                areaDeEscritura = document.getElementById('datos_1');
                div = document.createElement('div');
                div.classList.add('mensaje')
                div.innerHTML = `
                <ul>
                    <li>monto_ingresar: ${datos.monto_ingresar}</li>
                    <li>monto_ingresado: ${datos.monto_ingresado}</li>
                    <li>monto_a_dispensar: ${datos.monto_a_dispensar}</li>
                    <li>datos.folio: ${datos.folio}</li>
                    <li>hora_entrada: ${datos.hora_entrada}</li>
                    <li>tiempo_total: ${datos.tiempo_total}</li>
                    <li>datos.interfaz: ${datos.interfaz}</li>
                    <li>datos.descuento: ${datos.descuento}</li>
                </ul>
                `;

                areaDeEscritura.appendChild(div);

                setTimeout(function() {
                    document.querySelector('.mensaje').remove();
                }, 20000);
                break;

            case DATOS_CONTROL:

                areaDeEscritura = document.getElementById('datos_2');
                div = document.createElement('div');
                div.classList.add('mensaje');

                texto = `<ul>`;
                for (let dato in datos) {
                    texto+=(`<li>${dato} : ${datos[dato]} </li>`);
                }
                texto += `</ul>`

                div.innerHTML = texto
                areaDeEscritura.appendChild(div);

                setTimeout(function() {
                    document.querySelector('.mensaje').remove();
                }, 20000);
                break;

                case DATOS_ESTADO:

                    areaDeEscritura = document.getElementById('datos_3');
                    div = document.createElement('div');
                    div.classList.add('mensaje');
    
                    texto = `<ul>`;
                    for (let dato in datos) {
                        texto+=(`<li>${dato} : ${datos[dato]} </li>`);
                    }
                    texto += `</ul>`
    
                    div.innerHTML = texto
                    areaDeEscritura.appendChild(div);
    
                    setTimeout(function() {
                        document.querySelector('.mensaje').remove();
                    }, 20000);
                    break;
        }
        
    }
}



// Constantes 
const DATOS_ADMINISTRACION = 1;   // Se encarga de las señales para administración del proceso de cobro
const DATOS_CONTROL = 2;          // Señales de activación y desactivación de dispositivos
const DATOS_ESTADO = 3;           // Estado de dispositivos
// Definición del controlador
controlador = new Controlador(2,3);