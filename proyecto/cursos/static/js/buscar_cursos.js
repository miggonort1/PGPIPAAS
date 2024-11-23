document.addEventListener('DOMContentLoaded', () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const cursoId = event.target.getAttribute('data-curso-id');
            const cursoNombre = event.target.getAttribute('data-curso-nombre');

            // Realizar una solicitud al servidor
            fetch('/api/carrito/agregar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Necesitas configurar el token CSRF
                },
                body: JSON.stringify({ curso_id: cursoId })
            })
            .then(response => {
                if (response.ok) {
                    alert(`El curso "${cursoNombre}" se añadió al carrito.`);
                } else {
                    alert('Hubo un problema al añadir el curso al carrito.');
                }
            })
            .catch(error => console.error('Error al añadir al carrito:', error));
        });
    });
});

// Función para obtener el token CSRF de las cookies
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? cookieValue.split('=')[1] : null;
}