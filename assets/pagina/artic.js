var productoSeleccionado = {'id': 1, 'nombre': "Bananan't", 'overview': 'Fresh ripe bananas', 'descripcion': 'Yellow bananas, perfect for snacks or smoothies.', 'datos_adicionales': 'Sold in KG', 'categorias': 3, 'link_imagen1': 'https://64.media.tumblr.com/7972fb691435760cf63ce9763591c296/tumblr_inline_osumv1Ah9m1u4cl6w_500.jpg', 'link_imagen2': 'https://64.media.tumblr.com/7972fb691435760cf63ce9763591c296/tumblr_inline_osumv1Ah9m1u4cl6w_500.jpg', 'link_imagen3': 'https://64.media.tumblr.com/7972fb691435760cf63ce9763591c296/tumblr_inline_osumv1Ah9m1u4cl6w_500.jpg', 'precio_antes_descuento': '999.99', 'precio_despues_descuento': '0.00', 'stock_disponible': 16, 'nombre_categoria': 'Meat & Seafood'};

document.getElementById('nombre').textContent = productoSeleccionado.nombre;
document.getElementById('precio_antes_descuento').textContent = `$${productoSeleccionado.precio_antes_descuento}`;
document.getElementById('precio_despues_descuento').textContent = `$${productoSeleccionado.precio_despues_descuento}`;
document.getElementById('Overview').textContent = productoSeleccionado.overview;
document.getElementById('imagen1').src = productoSeleccionado.link_imagen1;
document.getElementById('imagen2').src = productoSeleccionado.link_imagen2;
document.getElementById('imagen3').src = productoSeleccionado.link_imagen3;
document.getElementById('imagenC1').src = productoSeleccionado.link_imagen1;
document.getElementById('imagenC2').src = productoSeleccionado.link_imagen2;
document.getElementById('imagenC3').src = productoSeleccionado.link_imagen3;
document.getElementById('texto').textContent = productoSeleccionado.descripcion;
document.getElementById('categoria').textContent = productoSeleccionado.nombre_categoria;

document.getElementById('descripcion').addEventListener('click', function (event) {
    event.preventDefault();
    cambiarTexto('descripcion');
});

document.getElementById('datos_adicionales').addEventListener('click', function (event) {
    event.preventDefault();
    cambiarTexto('datos_adicionales');
});

document.getElementById('reviews').addEventListener('click', function (event) {
    event.preventDefault();
    cambiarTexto('reviews');
});

// Función para cambiar el contenido y las clases
function cambiarTexto(opcion) {
    let texto = "";
    // Cambiar el texto dependiendo del botón presionado
    if (opcion === 'descripcion') {
        texto = productoSeleccionado.descripcion;
    } else if (opcion === 'datos_adicionales') {
        texto = "<strong>Stock: " + productoSeleccionado.stock_disponible + "</strong><br>" +
            productoSeleccionado.datos_adicionales;
    } else if (opcion === 'reviews') {
        texto = "This system is still under development.";
    }

    // Actualizar el contenido del texto
    document.getElementById('texto').innerHTML = texto;

    // Cambiar las clases de los botones
    cambiarClaseBoton(opcion);
}

// Función para cambiar las clases de los botones
function cambiarClaseBoton(opcionActivo) {
    const botones = ['descripcion', 'datos_adicionales', 'reviews'];
    botones.forEach(function (boton) {
        const element = document.getElementById(boton);
        let clase = element.className;
        let ultimaLetra = clase[clase.length - 1];
        if (boton === opcionActivo) {
            element.className = `u-active-black u-border-5 u-border-custom-color-2 u-border-no-left u-border-no-right u-border-no-top u-btn u-button-style u-hover-custom-color-2 u-white u-btn-${ultimaLetra}`;
        } else {
            element.className = `u-active-black u-border-5 u-border-no-left u-border-no-right u-border-no-top u-border-palette-1-light-3 u-btn u-button-style u-hover-custom-color-2 u-white u-btn-${ultimaLetra}`;
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    // Actualizar el contador del carrito
    function updateCartCounter() {
        const cartCounter = document.getElementById('cart-counter');
        const itemCount = cart.reduce((total, item) => total + item.quantity, 0);

        if (itemCount > 9) {
            cartCounter.textContent = '9+';
        } else {
            cartCounter.innerHTML = itemCount + "&nbsp;";
        }
    }

    updateCartCounter();
});