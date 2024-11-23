document.addEventListener("DOMContentLoaded", () => {
    const cartCoursesContainer = document.getElementById("cart-courses");
    const checkoutForm = document.getElementById("checkout-form");
    const totalPriceElement = document.getElementById("total-price");
    const cancelButton = document.getElementById("cancel-button");

    // Obtener el carrito desde el servidor
    fetch("/api/carrito/")
        .then(response => response.json())
        .then(data => {
            let totalPrice = 0;

            // Mostrar cada curso en el carrito
            data.cursos.forEach(curso => {
                const courseDiv = document.createElement("div");
                courseDiv.classList.add("cart-course");
                courseDiv.innerHTML = `
                    <h3>${curso.nombre}</h3>
                    <p>Cantidad: ${curso.cantidad}</p>
                    <p>Total: ${curso.precio_total}€</p>
                    <input type="hidden" name="curso_id[]" value="${curso.id}">
                    <input type="hidden" name="cantidad[]" value="${curso.cantidad}">
                      <form id="checkout-form" class="checkout-form">
                        <div>
                            <label for="name">Nombre:</label>
                            <input type="text" id="name" name="name" required>
                        </div>
                        <div>
                            <label for="email">Correo Electrónico:</label>
                            <input type="email" id="email" name="email" required>
                        </div>
                        </form>
                `;
                cartCoursesContainer.appendChild(courseDiv);

                // Actualizar el total
                totalPrice += curso.precio_total;
            });

            // Mostrar el total en el formulario
            totalPriceElement.textContent = `${totalPrice}€`;
        });

    // Enviar el formulario de compra
    checkoutForm.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(checkoutForm);

        // Realizar la compra a través de un POST
        const response = await fetch("/api/confirmar-compra/", {
            method: "POST",
            body: formData
        });

        const result = await response.json();
        if (result.success) {
            alert("Compra realizada con éxito!");
            window.location.href = "/gracias";  // Redirigir a una página de agradecimiento
        } else {
            alert("Hubo un error al procesar tu compra.");
        }
    });

    // Cancelar la compra
    cancelButton.addEventListener("click", () => {
        window.location.href = "/carrito";  // Redirigir al carrito para editarlo si es necesario
    });

    
});
