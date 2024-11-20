

let base64Image = "";  // Variable para almacenar la imagen en base64
let resultado = "";    // Variable para almacenar el resultado de detección
let precision = "";    // Variable para almacenar la precisión

function validateDNI() {
    const dni = document.getElementById("dni").value;
    const dniRegex = /^[0-9]{8}$/;

    // Verificar que el DNI contenga exactamente 8 dígitos numéricos
    if (!dniRegex.test(dni)) {
        alert("El DNI debe contener exactamente 8 dígitos numéricos.");
        return false;
    }
    return true;
}

function buscarPaciente() {
    const dni = document.getElementById('dni').value;
    fetch(`/buscar_paciente/?dni=${dni}`)
        .then(response => response.json())
        .then(data => {
            if (data.existe) {
                document.getElementById('nombre').value = `${data.nombres} ${data.apellido_paterno} ${data.apellido_materno}`;
            } else {
                alert('Paciente no encontrado.');
                document.getElementById('nombre').value = '';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al buscar el paciente.');
        });
}

function openFileDialog() {
    document.getElementById("fileInput").click();
}

function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById("imagePreview").src = e.target.result;
            document.getElementById("imagePreview").style.display = "block";
            base64Image = e.target.result.split(',')[1];  // Almacena la imagen en base64 sin el encabezado
        };
        reader.readAsDataURL(file);
    }
}

async function realizarEscaneo() {
    const formData = new FormData();
    formData.append('imagen', document.getElementById("fileInput").files[0]);
    formData.append('csrfmiddlewaretoken', '{{ csrf_token }}');

    const response = await fetch("{% url 'procesar_imagen' %}", {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        const data = await response.json();
        resultado = data.prediction;  // Guarda el resultado para registrar
        precision = data.probability; // Guarda la precisión para registrar

        // Determinar el color según el resultado
        let colorClass = "";
        if (resultado === "Maligno") {
            colorClass = "text-danger"; // Clase para texto rojo
        } else if (resultado === "Benigno") {
            colorClass = "text-success"; // Clase para texto verde
        } else if (resultado === "Desconocida") {
            colorClass = "text-secondary"; // Clase para texto gris
        }

        // Mostrar el resultado con el color correspondiente
        document.querySelector('.result-container').innerHTML = `
            <p><span class="result-label">Detección:</span> <span class="${colorClass}">${data.prediction}</span></p>
            <p><span class="result-label">Precisión:</span> ${data.probability}%</p>
        `;
    } else {
        alert("Error al procesar la imagen.");
    }
}

async function registrarDeteccion() {
    const dni = document.getElementById("dni").value;

    const response = await fetch("{% url 'guardar_resultado' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: JSON.stringify({
            dni: dni,
            imagen: base64Image,
            resultado: resultado,
            precision: precision
        })
    });

    if (response.ok) {
        alert("Detección registrada exitosamente.");

        // Limpiar los campos después del registro exitoso
        document.getElementById("dni").value = '';
        document.getElementById("nombre").value = '';
        document.getElementById("fileInput").value = '';
        document.getElementById("imagePreview").style.display = "none";
        document.querySelector('.result-container').innerHTML = `
            <p><span class="result-label">Detección:</span> [Resultado de Detección]</p>
            <p><span class="result-label">Precisión:</span> [Precisión]%</p>
        `;
        
        // Resetear variables de resultado
        base64Image = "";
        resultado = "";
        precision = "";

    } else {
        alert("Error al registrar la detección.");
        console.error("Error:", await response.json());
    }
}
