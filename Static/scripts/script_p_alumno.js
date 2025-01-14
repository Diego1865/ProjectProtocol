document.getElementById('registro-protocolo-form').addEventListener('submit', async function (e) {
    e.preventDefault(); // Evita el envío tradicional del formulario

    const form = e.target;
    const formData = new FormData(form);
    const mensajeDiv = document.getElementById('protocolo-mensaje');

    try {
        const response = await fetch('/subir_protocolo', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        // Mostrar mensaje dinámico
        mensajeDiv.classList.remove('hidden');
        if (result.success) {
            mensajeDiv.className = 'mensaje.success'; // Mensaje de éxito
            mensajeDiv.innerHTML = `<p>${result.message}</p>`;
        } else {
            mensajeDiv.className = 'mensaje.error'; // Mensaje de error
            mensajeDiv.innerHTML = `<p>${result.message}</p>`;
        }
    } catch (error) {
        mensajeDiv.classList.remove('hidden');
        mensajeDiv.className = 'mensaje.error'; // Error del servidor
        mensajeDiv.innerHTML = `<p>Ocurrió un error al subir el protocolo. Inténtalo más tarde.</p>`;
        console.error(error);
    }
});

document.getElementById('ver-estado').addEventListener('click', function() {
    document.getElementById('estado-detalle').innerHTML = '<p>Estado actual: En revisión</p>';
});

document.getElementById('subir-correcciones-form').addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Correcciones subidas exitosamente.');
});

// Simulación de notificaciones
document.getElementById('notificaciones-lista').innerHTML = `
    <ul>
        <li>Asignación de sinodales completada.</li>
        <li>Protocolo en revisión por evaluadores.</li>
    </ul>
`;

function showSection(sectionId) {
    // Ocultar todas las secciones
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => {
        section.classList.add('hidden');
    });

    // Mostrar la sección seleccionada
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.remove('hidden');
    }
}
