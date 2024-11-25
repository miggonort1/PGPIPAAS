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

    // Función para agregar al carrito
    async function agregarAlCarrito(cursoId, cantidad) {
        const response = await fetch("/api/carrito/agregar/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ curso_id: cursoId, cantidad }),
        });

        const data = await response.json();
        alert(data.message);
    }

    // Función para eliminar del carrito
    async function eliminarDelCarrito(cursoId) {
        const response = await fetch("/api/carrito/eliminar/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ curso_id: cursoId }),
        });

        const data = await response.json();
        alert(data.message);
    }
});
