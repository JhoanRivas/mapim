function validateForm() {
    const dni = document.getElementById("dni").value;
    const dniRegex = /^(?!([0-9])\1{7})([0-9]{8})$/;

    if (!dniRegex.test(dni)) {
        alert("El DNI debe ser de 8 dígitos numéricos y no puede tener todos los dígitos iguales.");
        return false;
    }

    const nombre = document.getElementById("nombres").value;
    const nombreRegex = /^[A-Za-zÁÉÍÓÚáéíóúÑñ\s]+$/;
    if (!nombreRegex.test(nombre)) {
        alert("El nombre debe contener solo letras y espacios.");
        return false;
    }

    const apellidoPaterno = document.getElementById("apellido_paterno").value;
    if (!nombreRegex.test(apellidoPaterno)) {
        alert("El apellido paterno debe contener solo letras y espacios.");
        return false;
    }

    const apellidoMaterno = document.getElementById("apellido_materno").value;
    if (apellidoMaterno && !nombreRegex.test(apellidoMaterno)) {
        alert("El apellido materno debe contener solo letras y espacios.");
        return false;
    }

    const numeroContacto = document.getElementById("numero_contacto").value;
    const numeroContactoRegex = /^9[0-9]{8}$/;
    if (!numeroContactoRegex.test(numeroContacto)) {
        alert("El número de contacto debe comenzar con '9' y tener 9 dígitos.");
        return false;
    }

    // Ocultar automáticamente los mensajes después de 5 segundos
    document.addEventListener("DOMContentLoaded", () => {
        const alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            setTimeout(() => {
                alert.style.display = "none";
            }, 5000); // 5 segundos
        });
    });


    return true;
}
