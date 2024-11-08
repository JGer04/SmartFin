document.addEventListener("DOMContentLoaded", function () {
  const sidebar = document.getElementById("sidebar");
  const btnSidebar = document.getElementById("btnSidebar");
  const icon = btnSidebar.querySelector("i");
  const contenedor = document.getElementById("principal");

  // Mostrar el sidebar inicialmente
  sidebar.style.display = "none"; // Cambia esto a 'block' para que sea visible al inicio

  btnSidebar.addEventListener("click", function () {
    if (sidebar.style.display === "none") {
      sidebar.style.display = "block"; // Muestra el sidebar
      icon.classList.remove("bi-chevron-right"); // Cambia el icono
      icon.classList.add("bi-chevron-left"); // Cambia el icono
      contenedor.classList.add("principal");
    } else {
      sidebar.style.display = "none"; // Oculta el sidebar
      icon.classList.remove("bi-chevron-left"); // Cambia el icono
      icon.classList.add("bi-chevron-right"); // Cambia el icono
      contenedor.classList.remove("principal");
    }
  });
});

let gifElement = document.getElementById("gif");
gifElement.style.backgroundImage = "url('https://i.gifer.com/1K9.gif')";

function cambiarGif() {
  gifElement.style.backgroundImage = "url('https://i.gifer.com/QcN.gif')";
}
