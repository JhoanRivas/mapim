// Validación en tiempo real para solo letras en el campo "Nombre Completo"
document.querySelector('.formulario__register input[placeholder="Nombre Completo"]').addEventListener('input', function (e) {
    const regex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]*$/;
    if (!regex.test(e.target.value)) {
        e.target.value = e.target.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\s]/g, '');
    }
});
// Evento para el botón de registro
document.getElementById("registerButton").addEventListener("click", function() {
    const nombreCompleto = document.getElementById("nombreCompleto").value.trim();
    const correo = document.getElementById("correo").value.trim();
    const usuario = document.getElementById("usuario").value.trim();
    const contraseña = document.getElementById("contraseña").value.trim();

    if (nombreCompleto === "" || correo === "" || usuario === "" || contraseña === "") {
        alert("Por favor, completa todos los campos.");
    } else {
        localStorage.setItem("nombreCompleto", nombreCompleto);
        localStorage.setItem("correo", correo);
        localStorage.setItem("usuario", usuario);
        localStorage.setItem("contraseña", contraseña);

        alert("Registro exitoso!");
        document.getElementById("registerForm").reset();
    }
});

// Evento para el botón de login
document.getElementById("loginButton").addEventListener("click", function() {
    const correoLogin = document.getElementById("correoLogin").value.trim();
    const contraseñaLogin = document.getElementById("contraseñaLogin").value.trim();

    // Verificar que los campos de correo y contraseña no estén vacíos
    if (correoLogin === "" || contraseñaLogin === "") {
        alert("Por favor, completa todos los campos de inicio de sesión.");
    } else {
        // Validación básica de inicio de sesión usando localStorage
        const correoRegistrado = localStorage.getItem("correo");
        const contraseñaRegistrada = localStorage.getItem("contraseña");

        if (correoLogin === correoRegistrado && contraseñaLogin === contraseñaRegistrada) {
            alert("Inicio de sesión exitoso!");
            // Redirecciona a la página de inicio en Django
            window.location.href = "/inicio/";  // Redirige a /inicio/ en lugar de /inicio.html
        } else {
            alert("Correo o contraseña incorrectos.");
        }
    }
});