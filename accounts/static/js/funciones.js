
var fechaActual = new Date();
var options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
document.getElementById('fecha').textContent = fechaActual.toLocaleDateString('es-ES', options);

setTimeout(function() {
    var alimentosSeleccionados = document.querySelector('.info_dieta ul');
    var informacionDieta = document.querySelectorAll('.info_dieta ul li');

    alimentosSeleccionados.innerHTML = '';

    informacionDieta.forEach(function(item) {
        item.remove();
    });

    var infoDieta = document.querySelector('.info_dieta');
    var mensaje = document.createElement('p');
    mensaje.textContent = 'No hay alimentos seleccionados.';
    infoDieta.appendChild(mensaje);
}, 10000); // 10 segundos en milisegundos
