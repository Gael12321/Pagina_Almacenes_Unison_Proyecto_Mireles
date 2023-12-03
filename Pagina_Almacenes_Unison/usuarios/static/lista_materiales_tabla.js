
// Agregar funcionalidad de búsqueda con JavaScript
const searchInput = document.getElementById('searchInput');
const materialTable = document.getElementById('materialTable');
const originalTable = materialTable.innerHTML; // Guardar el estado original de la tabla

searchInput.addEventListener('input', function() {
  const searchTerm = searchInput.value.toLowerCase();

  // Filtrar las filas de la tabla según el término de búsqueda
  Array.from(materialTable.rows).forEach(function(row) {
    const materialName = row.cells[0].textContent.toLowerCase();
    row.style.display = materialName.includes(searchTerm) ? '' : 'none';
  });

  // Restaurar la tabla a su estado original si el término de búsqueda está vacío
  if (searchTerm === '') {
    materialTable.innerHTML = originalTable;
  }
});
