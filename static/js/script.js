// Funciones JavaScript para la aplicación de gestión de contactos

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar tooltips de Bootstrap
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Validación de formularios en el cliente
    const forms = document.querySelectorAll('form[novalidate]');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!validateForm(this)) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    });
    
    // Validación de confirmación de contraseña
    const passwordForm = document.querySelector('form[action*="register"]');
    if (passwordForm) {
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm_password');
        
        if (password && confirmPassword) {
            confirmPassword.addEventListener('input', function() {
                validatePasswordMatch(password, confirmPassword);
            });
        }
    }
    
    // Confirmación antes de eliminar
    const deleteButtons = document.querySelectorAll('a[href*="eliminar"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('¿Estás seguro de que quieres eliminar este contacto? Esta acción no se puede deshacer.')) {
                e.preventDefault();
            }
        });
    });
    
    // Auto-ocultar alertas después de 5 segundos
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
    
    // Formatear números de teléfono mientras se escribe
    const phoneInputs = document.querySelectorAll('input[name="telefono"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            formatPhoneNumber(this);
        });
    });
});

/**
 * Valida un formulario
 * @param {HTMLFormElement} form - El formulario a validar
 * @returns {boolean} - True si es válido, false si no
 */
function validateForm(form) {
    let isValid = true;
    
    // Validar campos requeridos
    const requiredFields = form.querySelectorAll('[required]');
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'Este campo es obligatorio');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    // Validar email si existe
    const emailField = form.querySelector('input[type="email"]');
    if (emailField && emailField.value.trim()) {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(emailField.value)) {
            showFieldError(emailField, 'Por favor ingresa un email válido');
            isValid = false;
        } else {
            clearFieldError(emailField);
        }
    }
    
    return isValid;
}

/**
 * Muestra un error en un campo
 * @param {HTMLElement} field - El campo de entrada
 * @param {string} message - El mensaje de error
 */
function showFieldError(field, message) {
    clearFieldError(field);
    
    field.classList.add('is-invalid');
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    
    field.parentNode.appendChild(errorDiv);
}

/**
 * Limpia el error de un campo
 * @param {HTMLElement} field - El campo de entrada
 */
function clearFieldError(field) {
    field.classList.remove('is-invalid');
    
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

/**
 * Valida que las contraseñas coincidan
 * @param {HTMLElement} passwordField - Campo de contraseña
 * @param {HTMLElement} confirmField - Campo de confirmación
 */
function validatePasswordMatch(passwordField, confirmField) {
    if (passwordField.value !== confirmField.value) {
        showFieldError(confirmField, 'Las contraseñas no coinciden');
        return false;
    } else {
        clearFieldError(confirmField);
        return true;
    }
}

/**
 * Formatea un número de teléfono mientras se escribe
 * @param {HTMLInputElement} input - Campo de teléfono
 */
function formatPhoneNumber(input) {
    // Eliminar todo excepto números
    let value = input.value.replace(/\D/g, '');
    
    // Formatear: (XXX) XXX-XXXX
    if (value.length > 0) {
        value = '(' + value.substring(0, 3) + ') ' + value.substring(3, 6) + '-' + value.substring(6, 10);
    }
    
    // Actualizar valor sin disparar eventos infinitos
    input.value = value;
}

/**
 * Realiza una búsqueda en la tabla de contactos
 */
function searchContacts() {
    const input = document.getElementById('searchInput');
    const filter = input.value.toLowerCase();
    const table = document.querySelector('table');
    const rows = table.getElementsByTagName('tr');
    
    for (let i = 1; i < rows.length; i++) {
        const row = rows[i];
        let text = '';
        
        // Obtener texto de las celdas relevantes
        const cells = row.getElementsByTagName('td');
        for (let j = 0; j < cells.length - 1; j++) { // Excluir columna de acciones
            text += cells[j].textContent || cells[j].innerText;
        }
        
        if (text.toLowerCase().indexOf(filter) > -1) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    }
}

/**
 * Ordena la tabla por columna
 * @param {number} n - Índice de la columna
 */
function sortTable(n) {
    const table = document.querySelector('table');
    let rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    switching = true;
    dir = "asc";
    
    while (switching) {
        switching = false;
        rows = table.rows;
        
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[n];
            y = rows[i + 1].getElementsByTagName("td")[n];
            
            // Verificar si son números
            const xVal = isNaN(parseFloat(x.innerHTML)) ? x.innerHTML.toLowerCase() : parseFloat(x.innerHTML);
            const yVal = isNaN(parseFloat(y.innerHTML)) ? y.innerHTML.toLowerCase() : parseFloat(y.innerHTML);
            
            if (dir === "asc") {
                if (xVal > yVal) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (xVal < yVal) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount ++;
        } else {
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}