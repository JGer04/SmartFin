document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const btnSidebar = document.getElementById("btnSidebar");
  const icon = btnSidebar.querySelector("i");
  const contenedor = document.getElementById("principal");

  // Configuración inicial: sidebar visible
  sidebar.style.display = "block";
  icon.classList.add("bi-chevron-left");
  contenedor.classList.add("principal");

  // Alternar la visibilidad del sidebar al hacer clic en el botón
  btnSidebar.addEventListener("click", function () {
    const isVisible = sidebar.style.display === "block";

    if (isVisible) {
      sidebar.style.display = "none"; // Oculta el sidebar
      icon.classList.replace("bi-chevron-left", "bi-chevron-right");
      contenedor.classList.remove("principal");
    } else {
      sidebar.style.display = "block"; // Muestra el sidebar
      icon.classList.replace("bi-chevron-right", "bi-chevron-left");
      contenedor.classList.add("principal");
    }
  });

// Cambiar GIF y redirigir
const gifElement = document.getElementById("gif");
gifElement.style.backgroundImage = "url('https://i.gifer.com/1K9.gif')";

// Crear y estilizar el contador
const contadorElement = document.createElement("div");
contadorElement.style.position = "relative";
contadorElement.style.backgroundColor="transparent"
contadorElement.style.color="Black"
contadorElement.style.justifyContent="center"
contadorElement.style.alignContent="center"
contadorElement.style.top = "60px";
contadorElement.style.left = "9px";
contadorElement.style.padding = "5px 10px";
contadorElement.style.fontSize = "16px";
contadorElement.style.fontWeight="bold"
contadorElement.style.fontFamily = "Arial, sans-serif";
contadorElement.style.zIndex = "10"; // Asegura que el contador esté encima del GIF
contadorElement.style.display = "none"; // Ocultarlo inicialmente

// Agregar el contador al contenedor del GIF
gifElement.appendChild(contadorElement);

gifElement.addEventListener("click", function () {
  // Cambiar al segundo GIF
  gifElement.style.backgroundImage = "url('https://i.gifer.com/QcN.gif')";

  // Duración del segundo GIF en milisegundos
  const gifDuration = 3000; // 3 segundos
  let timeRemaining = gifDuration / 1000; // Convertir a segundos

  // Mostrar el contador
  contadorElement.style.display = "block";

  contadorElement.textContent = `Redirigiendo en: ${timeRemaining}s`;

  // Actualizar el contador cada segundo
  const interval = setInterval(() => {
    timeRemaining--;
    contadorElement.textContent = `Redirigiendo en: ${timeRemaining}s`;

    if (timeRemaining <= 0) {
      clearInterval(interval); // Detener el contador
      contadorElement.style.display = "none"; // Ocultar el contador
    }
  }, 1000);

  // Redirigir a la página de inicio después de que termine el segundo GIF
  setTimeout(() => {
    window.location.href = "/"; // Cambia "/" por la URL deseada
  }, gifDuration);
});

});
