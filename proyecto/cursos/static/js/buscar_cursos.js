document.addEventListener('DOMContentLoaded', () => {
    const addToCartButtons = document.querySelectorAll('.add-to-cart ');

    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const cursoId = event.target.getAttribute('data-curso-id');
            const cursoNombre = event.target.getAttribute('data-curso-nombre');
            const cantidad = document.getElementById('cantidad-cursos').value;  // Obtener la cantidad seleccionada
            const cartDropdown = document.getElementById("cart-dropdown");
    
            // Comprobar si la cantidad es válida
            
    
            // Realizar una solicitud al servidor
            fetch('/api/carrito/agregar/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken') // Necesitas configurar el token CSRF
                },
                body: JSON.stringify({ curso_id: cursoId, cantidad: cantidad })
            })
            .then(response => {
                if (response.ok) {
                    showAlert(`El curso "${cursoNombre}" se añadió al carrito.`, 'success');
                } else {
                    showAlert('No hay suficientes plazas disponibles', 'error');
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
                    location.reload()// Actualiza el carrito con la respuesta del servidor
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
            const response = await fetch(`../../api/carrito/eliminar/`, {
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
        }
            
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