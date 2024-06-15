
var fechaActual = new Date();
var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
document.getElementById('fecha').textContent = fechaActual.toLocaleDateString('es-ES', options);

var contenido = document.getElementById("contenido-a-borrar");
setTimeout(function() {
    contenido.innerHTML = '';
}, 10000); 