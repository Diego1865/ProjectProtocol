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

// Enviar correo de bienvenida
function sendEmail(data) {
    const emailDetails = {
        to: data.correo,
        subject: "Asignación de Personal",
        html: `
            <div style="font-family: Arial, sans-serif; color: #333;">
                <h1>¡Bienvenido!</h1>
                <p>Hola <strong>${data.nombre} ${data.apellidoPaterno} ${data.apellidoMaterno}</strong>,</p>
                <p>Te damos la bienvenida al sistema. Se te ha asignado el rol de <strong>${data.rol}</strong>.</p>
                <p>A continuación, te compartimos tus credenciales de acceso:</p>
                <ul>
                    <li><strong>Matrícula:</strong> ${data.matricula}</li>
                    <li><strong>Contraseña:</strong> ${data.contraseña}</li>
                </ul>
                <p>Por favor, no compartas esta información con nadie.</p>
                <p>¡Gracias por unirte al equipo!</p>
            </div>
        `,
    };

    fetch('http://localhost:3000/send-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(emailDetails),
    })
        .then(response => {
            if (response.ok) {
                showPopup(`Personal agregado. Correo enviado correctamente a ${data.correo}.`);
            } else {
                response.text().then(err => {
                    console.error('Error del servidor:', err);
                    showPopup("Hubo un error al enviar el correo.", true);
                });
            }
        })
        .catch(error => {
            console.error('Error en la conexión al servidor:', error);
            showPopup("Error de conexión con el servidor.", true);
        });
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