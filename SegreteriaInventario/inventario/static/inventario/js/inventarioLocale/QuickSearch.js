$("#showRapidSearch").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#showRapidSearch").hide();
});

$("#hideRapidSearch").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#showRapidSearch").show();
});

function quickSearch(keyword) {
  searchUrl = "/inventario/table/getData?search=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
}
function locationSearch(keyword, el) {
  searchUrl = "/inventario/table/advancedSearch?ubicazione=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
  $(el).parent().addClass('active');
}
function accurateLocationSearch(keyword, el) {
  searchUrl = "/inventario/table/advancedSearch?ubicazione_precisa=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
  $(el).parent().addClass('active');
}
function possessoriSearch(keyword1, keyword2, el) {
  searchUrl = "/inventario/table/advancedSearch?nome=" + keyword1 + "&cognome=" + keyword2;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
  $(el).parent().addClass('active');
}
function clearFilters() {
    searchUrl = "/inventario/table/getData";
    $('#table').bootstrapTable('refresh', {url: searchUrl});
    $('#advancedSearchForm').trigger("reset");
}
function ricognizioneInventarialeLocationSearch(keyword) {
  searchUrl = "/inventario/table/advancedRicognizioneInventarialeSearch?ubicazione=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
}
function ricognizioneInventarialeAccurateLocationSearch(keyword) {
  searchUrl = "/inventario/table/advancedRicognizioneInventarialeSearch?ubicazione_precisa=" + keyword;
  $('#table').bootstrapTable('refresh', {url: searchUrl});
}
function ricognizioneInventarialeClearFilters() {
    if($('form[name="advancedRicognizioneInventarialeSearchForm"]').length != 0) 
      $('form[name="advancedRicognizioneInventarialeSearchForm"]')[0].reset();
    if ($('form[name="advancedSearchForm"]').length != 0)
      $('form[name="advancedSearchForm"]')[0].reset();
    searchUrl = "/inventario/table/getRicognizioniData";
    $('#table').bootstrapTable('refresh', {url: searchUrl});
}
