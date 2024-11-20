// Validación en tiempo real para solo letras en el campo "Nombre Completo"
document.querySelector('.formulario__register input[placeholder="Nombre Completo"]').addEventListener('input', function (e) {
    const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$/;
    if (!regex.test(e.target.value)) {
        e.target.value = e.target.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
    }
});

// ***** Login
document.addEventListener('DOMContentLoaded', function () {

    const formLogin = document.getElementById('loginForm');
    const formRegister = document.getElementById('registerForm');
    const registerLink = document.getElementById('registerButton');
    const loginLink = document.getElementById('loginButton');

    registerLink.addEventListener('click', function (e) {
        e.preventDefault();
        formLogin.classList.add('d-none');
        formRegister.classList.remove('d-none');
    });

    loginLink.addEventListener('click', function (e) {
        e.preventDefault();
        formRegister.classList.add('d-none');
        formLogin.classList.remove('d-none');
    });

    setTimeout(function() {
        document.getElementById("alert-conteiner").style.display = "none";
    }, 3000);

});


