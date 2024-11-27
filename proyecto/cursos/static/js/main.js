// main.js
function showCourses() {
    document.getElementById('courses-section').classList.toggle('hidden');
}
document.addEventListener("DOMContentLoaded", () => {
    const cartButton = document.getElementById("cart-button");
    const cartDropdown = document.getElementById("cart-dropdown");
    const cartItems = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");
    const checkoutButton = document.getElementById('checkout-button');

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
                    <div class="quantity-controls">
                        <button class="decrease-quantity" data-id="${curso.id}">-</button>
                        <span class="quantity">${curso.cantidad}</span>
                        <button class="increase-quantity" data-id="${curso.id}">+</button>
                    </div>
                `;
                cartItems.appendChild(item);
            });
            const item = document.createElement("div");
            item.classList.add("cart-item");
            item.innerHTML = `<p>Total: ${data.total_precio}€ </p>`;
            
            cartItems.appendChild(item);

            if (cartItems.length === 0) {
                cartItemsContainer.innerHTML = '<p class="empty-cart-message">No hay cursos en el carrito.</p>';
                checkoutButton.style.display = 'none'; // Oculta el botón si el carrito está vacío
            } else {
                checkoutButton.style.display = 'block'; // Muestra el botón si hay elementos
            }
        } catch (error) {
            cartItems.innerHTML = "<p>Error al cargar el carrito.</p>";
        }
    });

    cartItems.addEventListener("click", async (event) => {
        const target = event.target;
        if (target.classList.contains("increase-quantity")){
            const cartItem = target.closest(".cart-item");
            const courseId = target.getAttribute("data-id");
            const quantityElement = cartItem.querySelector(".quantity");
            let quantity = parseInt(quantityElement.textContent);

            if (target.classList.contains("increase-quantity")) {
                quantity++;
            } else if (target.classList.contains("decrease-quantity") && quantity > 1) {
                quantity--;
            }

            // Actualizar la cantidad en la interfaz
            quantityElement.textContent = quantity;
            console.log("aqui")
            // Llamada al servidor para actualizar el carrito
            try {
                const response = await fetch('/api/carrito/agregar/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({ curso_id: courseId, cantidad: quantity })
                });

                if (response.ok) {
                    location.reload()
                } else {
                    showAlert('No hay plazas Disponibles', 'error');
                }
            } catch (error) {
                console.error('Error al actualizar el carrito:', error);
                showAlert('Error al comunicar con el servidor.', 'error');
            }
        }
        else if (target.classList.contains("decrease-quantity")){ 
            const cartItem = target.closest(".cart-item");
            const courseId = target.getAttribute("data-id");
            const quantityElement = cartItem.querySelector(".quantity");
            let quantity = parseInt(quantityElement.textContent);

            if (target.classList.contains("increase-quantity")) {
                quantity++;
            } else if (target.classList.contains("decrease-quantity") && quantity > 1) {
                quantity--;
            }

            // Actualizar la cantidad en la interfaz
            quantityElement.textContent = quantity;
            console.log("aqui")
            try{
            const response = await fetch(`../api/carrito/eliminar/`, {
                method: "DELETE",
                headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': getCookie('csrftoken') // Necesitas configurar el token CSRF
                        },
                        
                body: JSON.stringify({ curso_id: courseId })
            });
            if (response.ok) {
                location.reload()// Actualiza el carrito con la respuesta del servidor
                } else {
                    showAlert('Hubo un problema al actualizar el carrito.', 'error');
                }
            } catch (error) {
                console.error('Error al actualizar el carrito:', error);
                showAlert('Error al comunicar con el servidor.', 'error');
        }
            
        }
    });


    // Obtener token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Mostrar notificación
    function showAlert(message, type) {
        const alertBox = document.createElement('div');
        alertBox.className = `alert ${type}`;
        alertBox.textContent = message;
        document.body.appendChild(alertBox);

        setTimeout(() => {
            alertBox.remove();
        }, 3000); // 3 segundos
    }
});


