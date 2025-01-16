// Mostrar la sección seleccionada en el menú
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

document.addEventListener('DOMContentLoaded', () => {
    fetch('/validar_protocolos', { method: 'GET' })
        .then(response => response.json())
        .then(protocolos => {
            const tableBody = document.querySelector('#protocolos-table tbody');
            tableBody.innerHTML = '';
            protocolos.forEach(protocolo => {
                const [id, titulo, estado, alumnoId, archivo] = protocolo;
            
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${id}</td>
                    <td><a href="${archivo}" target="_blank">${titulo}</a></td>
                    <td>${alumnoId}</td>
                    <td>
                        <button onclick="populateForm(${id}, '${titulo}', 'validar')">Validar</button>
                        <button onclick="populateForm(${id}, '${titulo}', 'rechazar')">Rechazar</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        });

    document.querySelector('#validar-protocolo-form').addEventListener('submit', event => {
        event.preventDefault();
        sendProtocolUpdate('Validar');
    });

    document.querySelector('#rechazar-protocolo-form').addEventListener('submit', event => {
        event.preventDefault();
        sendProtocolUpdate('Rechazar');
    });
});

function clearForms() {
    document.querySelector('#validar-protocolo-form').reset();
    document.querySelector('#rechazar-protocolo-form').reset();
}

function populateForm(id, titulo, action) {
    const validarForm = document.querySelector('#validar-protocolo-form');
    const rechazarForm = document.querySelector('#rechazar-protocolo-form');

    clearForms();

    if (action === 'validar') {
        // Mostrar formulario de validar y ocultar el de rechazar
        validarForm.style.display = 'block';
        rechazarForm.style.display = 'none';

        // Llenar campos del formulario de validar
        document.querySelector('#protocolo-id').value = id;
        document.querySelector('#nuevo-titulo').value = `${titulo} - 2019-B`;
    } else if (action === 'rechazar') {
        // Mostrar formulario de rechazar y ocultar el de validar
        rechazarForm.style.display = 'block';
        validarForm.style.display = 'none';

        // Llenar campos del formulario de rechazar
        document.querySelector('#rechazar-protocolo-id').value = id;
    }
}

function sendProtocolUpdate(action) {
    const protocoloId = action === 'Validar'
        ? document.querySelector('#protocolo-id').value
        : document.querySelector('#rechazar-protocolo-id').value;

    const data = {
        protocolo_id: protocoloId,
        accion: action,
    };

    if (action === 'Rechazar') {
        data.razon_rechazo = document.querySelector('#razon-rechazo').value;
    }

    console.log("Datos enviados al servidor:", data); // Para depuración

    fetch('/validar_protocolos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const accion = action === 'Validar' ? 'validado' : 'rechazado';
                alert(`Protocolo ${accion} correctamente`);
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => console.error('Error en la solicitud:', error));
}



// Generar contraseña personalizada
function generatePassword(nombre, apellidoPaterno, apellidoMaterno, matricula) {
    const nombrePart = nombre.charAt(0).toUpperCase() + nombre.charAt(1).toLowerCase() + nombre.charAt(2).toLowerCase();
    const apellidoPaternoPart = apellidoPaterno.slice(0, 2).toLowerCase();
    const apellidoMaternoPart = apellidoMaterno.slice(0, 2).toLowerCase();
    const matriculaPart = matricula.slice(-2);
    return `${nombrePart}${apellidoPaternoPart}${apellidoMaternoPart}${matriculaPart}?`;
}

// Mostrar mensaje en el popup
function showPopup(message, isError = false) {
    const popup = document.getElementById('popup');
    const popupMessage = document.getElementById('popupMessage');
    popupMessage.textContent = message;

    if (isError) {
        popupMessage.style.color = 'black';
    } else {
        popupMessage.style.color = 'black';
    }

    popup.style.display = 'block'; // Mostrar el popup
}

function closePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'none'; // Ocultar el popup
}


// Validar el formulario de Agregar Personal
document.getElementById('agregar-personal-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío automático del formulario

    // Obtener los valores de los campos
    const matricula = document.getElementById('matricula-personal').value.trim();
    const nombre = document.getElementById('nombre-personal').value.trim();
    const apellidoPaterno = document.getElementById('apellido-paterno-personal').value.trim();
    const apellidoMaterno = document.getElementById('apellido-materno-personal').value.trim();
    const correo = document.getElementById('correo-personal').value.trim();
    const rol = document.getElementById('rol-personal').value;

    // Validar cada campo
    if (!/^[0-9]{1,10}$/.test(matricula)) {
        alert('La matrícula debe contener solo números y tener un máximo de 10 caracteres.');
        return;
    }

    if (!/^[a-zA-Z\s]+$/.test(nombre)) {
        alert('El nombre debe contener solo letras.');
        return;
    }

    if (!/^[a-zA-Z\s]+$/.test(apellidoPaterno)) {
        alert('El apellido paterno debe contener solo letras.');
        return;
    }

    if (!/^[a-zA-Z\s]+$/.test(apellidoMaterno)) {
        alert('El apellido materno debe contener solo letras.');
        return;
    }

    if (!/^[a-zA-Z0-9._%+-]+@alumno\.ipn\.mx$/.test(correo)) {
        alert('El correo debe ser válido y tener formato @alumno.ipn.mx.');
        return;
    }

    if (!rol) {
        alert('Debe seleccionar un rol.');
        return;
    }

    const contraseña = generatePassword(nombre, apellidoPaterno, apellidoMaterno, matricula);

    // Crear el objeto de datos
    const data = { matricula, nombre, apellidoPaterno, apellidoMaterno, correo, rol, contraseña };

    // Simular envío de datos al servidor
    console.log('Datos enviados: ', data);

    sendEmail(data);
    clearForm(); // Limpiar el formulario
});

function clearForm() {
    document.getElementById('matricula-personal').value = '';
    document.getElementById('nombre-personal').value = '';
    document.getElementById('apellido-paterno-personal').value = '';
    document.getElementById('apellido-materno-personal').value = '';
    document.getElementById('correo-personal').value = '';
    document.getElementById('rol-personal').value = '';
}