$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});

function quickSearch(keyword) {
  searchUrl = "/inventario/table/getData?search=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
}
function locationSearch(keyword) {
  searchUrl = "/inventario/table/advancedSearch?ubicazione=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
}
function accurateLocationSearch(keyword) {
  searchUrl = "/inventario/table/advancedSearch?ubicazione_precisa=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
}
function clearFilters() {
    searchUrl = "/inventario/table/getData";
    $('#table').bootstrapTable('refresh', {url: searchUrl});
}