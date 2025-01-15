const matriculaInput = document.getElementById('matricula');
const matriculaError = document.getElementById('matricula-error');
const newPasswordInput = document.getElementById('new-password');
const confirmPasswordInput = document.getElementById('confirm-password');
const passwordRequirements = {
    length: document.getElementById('req-length'),
    uppercase: document.getElementById('req-uppercase'),
    lowercase: document.getElementById('req-lowercase'),
    number: document.getElementById('req-number'),
    symbol: document.getElementById('req-symbol')
};
const passwordMatchMessage = document.getElementById('password-match');
const submitButton = document.getElementById('submit-button');
const popup = document.getElementById('popup');
const popupMessage = document.getElementById('popup-message');
const popupCloseButton = document.getElementById('popup-close-button');

const passwordPattern = {
    length: /.{10,}/,
    uppercase: /[A-Z]/,
    lowercase: /[a-z]/,
    number: /\d/,
    symbol: /[?¿*!]/
};

let isSuccessful = false;

// Validar matrícula
matriculaInput.addEventListener('input', () => {
    if (!/^\d*$/.test(matriculaInput.value)) {
        matriculaError.style.display = 'block';
    } else {
        matriculaError.style.display = 'none';
    }
});

// Validar contraseñas
function validatePassword() {
    const password = newPasswordInput.value;
    let isValid = true;

    for (const key in passwordPattern) {
        if (passwordPattern[key].test(password)) {
            passwordRequirements[key].classList.remove('error');
            passwordRequirements[key].classList.add('valid');
        } else {
            passwordRequirements[key].classList.remove('valid');
            passwordRequirements[key].classList.add('error');
            isValid = false;
        }
    }

    return isValid;
}

function checkPasswordMatch() {
    const match = newPasswordInput.value === confirmPasswordInput.value;
    if (match) {
        passwordMatchMessage.style.display = 'none';
    } else {
        passwordMatchMessage.style.display = 'block';
    }
    return match;
}

function togglePassword(fieldId) {
    const field = document.getElementById(fieldId);
    field.type = field.type === 'password' ? 'text' : 'password';
}

function showPopup(message) {
    popupMessage.textContent = message;
    popup.classList.add('show');
}

function closePopup() {
    popup.classList.remove('show');
    if (isSuccessful) {
        // Limpiar los campos si la operación fue exitosa
        matriculaInput.value = '';
        newPasswordInput.value = '';
        confirmPasswordInput.value = '';
        validatePassword();
        checkPasswordMatch();
    }
}

submitButton.addEventListener('click', () => {
    const isMatriculaValid = matriculaInput.value.trim() !== '' && matriculaError.style.display === 'none';
    const isPasswordValid = validatePassword();
    const isPasswordMatch = checkPasswordMatch();

    if (!isMatriculaValid || !isPasswordValid || !isPasswordMatch) {
        isSuccessful = false;
        showPopup('Por favor, corrija los errores antes de continuar.');
    } else {
        isSuccessful = true;
        showPopup('Contraseña cambiada correctamente.');
    }
});

popupCloseButton.addEventListener('click', closePopup);

[newPasswordInput, confirmPasswordInput].forEach(input => {
    input.addEventListener('input', () => {
        validatePassword();
        checkPasswordMatch();
    });
});