function togglePassword(id) {
    const input = document.getElementById(id);
    input.type = input.type === "password" ? "text" : "password";
}

// Validar campos individuales
function validateField(input, errorElement, validator, errorMessage) {
    if (validator(input.value)) {
        errorElement.textContent = "";
        return true;
    } else {
        errorElement.textContent = errorMessage;
        return false;
    }
}

// Validadores
function validateName(value) {
    return /^[a-zA-Z\s]{1,25}$/.test(value.trim());
}

function validateMatricula(value) {
    return /^[0-9]{1,10}$/.test(value.trim());
}

function validatePhone(value) {
    return /^[0-9]{1,10}$/.test(value.trim());
}

function validateEmail(value) {
    return /^[a-zA-Z0-9._%+-]+@alumno\.ipn\.mx$/.test(value.trim());
}

// Validar contraseña
function validatePassword() {
    const field = document.getElementById("contraseña");
    const error = document.getElementById("contraseñaError");
    const mayus = document.getElementById("mayus");
    const minus = document.getElementById("minus");
    const numero = document.getElementById("numero");
    const especial = document.getElementById("especial");
    const longitud = document.getElementById("longitud");

    let isValid = true;

    if (/[A-Z]/.test(field.value)) mayus.style.color = "green";
    else {
        mayus.style.color = "red";
        isValid = false;
    }

    if (/[a-z]/.test(field.value)) minus.style.color = "green";
    else {
        minus.style.color = "red";
        isValid = false;
    }

    if (/\d/.test(field.value)) numero.style.color = "green";
    else {
        numero.style.color = "red";
        isValid = false;
    }

    if (/[¿?!*$]/.test(field.value)) especial.style.color = "green";
    else {
        especial.style.color = "red";
        isValid = false;
    }

    if (field.value.length >= 10) longitud.style.color = "green";
    else {
        longitud.style.color = "red";
        isValid = false;
    }

    if (!isValid) {
        error.textContent = "La contraseña no cumple con los requisitos.";
    } else {
        error.textContent = "";
    }

    return isValid;
}

// Validar confirmación de contraseña
function validateConfirmPassword() {
    const field = document.getElementById("confirmarContraseña");
    const original = document.getElementById("contraseña");
    const error = document.getElementById("confirmarContraseñaError");
    if (field.value !== original.value) {
        error.textContent = "Las contraseñas no coinciden.";
        return false;
    }
    error.textContent = "";
    return true;
}

// Validar formulario completo y enviar datos
function validateForm() {
    const nombre = document.getElementById("nombre").value;
    const apellidoPaterno = document.getElementById("apellidoPaterno").value;
    const apellidoMaterno = document.getElementById("apellidoMaterno").value;
    const matricula = document.getElementById("matricula").value;
    const telefono = document.getElementById("telefono").value;
    const correo = document.getElementById("correo").value;
    const contraseña = document.getElementById("contraseña").value;

    const isValidName = validateField(
        document.getElementById("nombre"),
        document.getElementById("nombreError"),
        validateName,
        "Debe contener solo letras y un máximo de 25 caracteres."
    );

    const isValidPaterno = validateField(
        document.getElementById("apellidoPaterno"),
        document.getElementById("apellidoPaternoError"),
        validateName,
        "Debe contener solo letras y un máximo de 25 caracteres."
    );

    const isValidMaterno = validateField(
        document.getElementById("apellidoMaterno"),
        document.getElementById("apellidoMaternoError"),
        validateName,
        "Debe contener solo letras y un máximo de 25 caracteres."
    );

    const isValidMatricula = validateField(
        document.getElementById("matricula"),
        document.getElementById("matriculaError"),
        validateMatricula,
        "Debe contener solo números y un máximo de 10 caracteres."
    );

    const isValidEmail = validateField(
        document.getElementById("correo"),
        document.getElementById("correoError"),
        validateEmail,
        "Debe ser un correo válido del tipo @alumno.ipn.mx."
    );

    const isValidPassword = validatePassword();
    const isValidConfirmPassword = validateConfirmPassword();

    if (
        isValidName &&
        isValidPaterno &&
        isValidMaterno &&
        isValidMatricula &&
        isValidEmail &&
        isValidPassword &&
        isValidConfirmPassword
    ) {
        document.getElementById("userForm").submit();
    } else {
        showPopup("Por favor, corrija los errores antes de continuar.");
    }
}

// Limpiar campos 
function clearFields() {
    document.querySelectorAll("input").forEach((input) => {
        input.value = "";
    });
    document.querySelectorAll(".error").forEach((error) => {
        error.textContent = "";
    });
    document.querySelectorAll(".password-info span").forEach((span) => {
        span.style.color = "red";
    });
}

// Mostrar popup
function showPopup(message) {
    const popup = document.getElementById("popup");
    const popupMessage = document.getElementById("popupMessage");
    popupMessage.textContent = message;
    popup.style.display = "flex";
}

// Cerrar popup
function closePopup() {
    const popup = document.getElementById("popup");
    popup.style.display = "none";
}