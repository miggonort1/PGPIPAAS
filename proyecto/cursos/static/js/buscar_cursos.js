document.addEventListener('DOMContentLoaded', () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart ');

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
                    showAlert(`El curso "${cursoNombre}" se añadió al carrito.`, 'success');
                } else {
                    showAlert('Hubo un problema al añadir el curso al carrito.', 'error');
                }
            })
            .catch(error => console.error('Error al añadir al carrito:', error));
        });
    });
    const cartButton = document.getElementById("cart-button");
    const cartDropdown = document.getElementById("cart-dropdown");
    const cartItems = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");

    cartButton.addEventListener("click", async () => {
        cartDropdown.classList.toggle("hidden");
        cartDropdown.classList.toggle("visible");

        if (!cartDropdown.classList.contains("visible")) return;

        try {
            const response = await fetch("/api/carrito/");
            const data = await response.json();
            cartItems.innerHTML = "";
            cartTotal.innerHTML = "";

            data.cursos.forEach((curso) => {
                const item = document.createElement("div");
                item.classList.add("cart-item");
                item.innerHTML = `
                    <p>${curso.nombre} (x${curso.cantidad})</p>
                    <p>${curso.precio_unitario}€ / Unidad</p>
                `;
                cartItems.appendChild(item);
            });
            const item = document.createElement("div");
            item.classList.add("cart-item");
            item.innerHTML = `<p>Total: ${data.total_precio}€ </p>`;
            
            cartItems.appendChild(item);
        } catch (error) {
            cartItems.innerHTML = "<p>Error al cargar el carrito.</p>";
        }
    });
});
function showAlert(message, type) {
    const alertElement = document.getElementById('custom-alert');
    const alertMessage = document.getElementById('alert-message');
    alertMessage.textContent = message;

    // Establecer el tipo de alerta (éxito o error)
    alertElement.classList.remove('hidden');
    alertElement.classList.remove('error');
    if (type === 'error') {
        alertElement.classList.add('error');
    }

    // Ocultar la alerta después de 5 segundos
    setTimeout(() => {
        alertElement.classList.add('hidden');
    }, 5000);
}
// Función para obtener el token CSRF de las cookies
function getCookie(name) {
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='));
    return cookieValue ? cookieValue.split('=')[1] : null;
}