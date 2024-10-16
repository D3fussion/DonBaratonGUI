var productoSeleccionado = {'id': 14, 'nombre': 'Harina de Trigo Escudo Anaya', 'overview': 'Harina de Trigo Escudo Anaya Extra Fina', 'descripcion': 'Lleva a la pr�ctica cada una de las recetas de postres que tienes en mente, no dejes de agregar a tu despensa la calidad de la harina de trigo de Escudo Anaya.', 'datos_adicionales': '10 pzas de 1kg', 'categorias': 6, 'link_imagen1': 'https://i5-mx.walmartimages.com/samsmx/images/product-images/img_large/000118712-3l.jpg?odnHeight=612&odnWidth=612&odnBg=FFFFFF?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 'link_imagen2': 'https://i5-mx.walmartimages.com/samsmx/images/product-images/img_large/000118712-1l.jpg?odnHeight=612&odnWidth=612&odnBg=FFFFFF?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 'link_imagen3': 'https://i5-mx.walmartimages.com/samsmx/images/product-images/img_large/000118712-2l.jpg?odnHeight=612&odnWidth=612&odnBg=FFFFFF?odnHeight=612&odnWidth=612&odnBg=FFFFFF', 'precio_antes_descuento': '250.00', 'precio_despues_descuento': '225.06', 'stock_disponible': 40, 'nombre_categoria': 'Bakery & Pastries'};

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