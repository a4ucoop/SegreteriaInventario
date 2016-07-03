// il modal della ricerca avanzata deve essere più largo
$(".modal-wide").on("show.bs.modal", function() {
  var height = $(window).height() - 200;
  $(this).find(".modal-body").css("max-height", height);
});

// inizializza i datepicker modal di ricerca
$(function() {
  $.datepicker.setDefaults(
    $.extend(
      {'dateFormat':'dd-mm-yy'},
      $.datepicker.regional['it']
    )
  );
  $( ".datepicker" ).datepicker({
      changeMonth: true,
      changeYear: true
    });
});

function advancedSearchRicInv(argument) {
    var query = "/inventario/table/advancedRicognizioneInventarialeSearch?";
    var min_id = document.forms["advancedRicognizioneInventarialeSearchForm"]["min_id"].value;
    var max_id = document.forms["advancedRicognizioneInventarialeSearchForm"]["max_id"].value;
    var codici_inventario_selezionati = [];
    $("input:checkbox[name=codice_inventario]:checked").each(function(){
        codici_inventario_selezionati.push($(this).val());
    });
    var min_pg_bene = document.forms["advancedRicognizioneInventarialeSearchForm"]["min_pg_bene"].value;
    var max_pg_bene = document.forms["advancedRicognizioneInventarialeSearchForm"]["max_pg_bene"].value;
    var ds_bene = document.forms["advancedRicognizioneInventarialeSearchForm"]["ds_bene"].value;
    var categorie_inventariali_selezionate = [];
    $("input:checkbox[name=categorie_inventariali]:checked").each(function(){
        categorie_inventariali_selezionate.push($(this).val());
    });
    var ubicazione = document.forms["advancedRicognizioneInventarialeSearchForm"]["ubicazione"].value;
    var ubicazione_precisa = document.forms["advancedRicognizioneInventarialeSearchForm"]["ubicazione_precisa"].value;

    if(min_id != null && min_id != "")
      query += "min_id=" + min_id + "&";
     if(max_id != null && max_id != "")
      query += "max_id=" + max_id + "&";
    if(codici_inventario_selezionati != null && codici_inventario_selezionati.length > 0){
      // cis = codici inventario selezionati
      for (var i = 0; i < codici_inventario_selezionati.length; i++) {
        query += "cods=" + codici_inventario_selezionati[i] + "&";
      }
    } 

    if(min_pg_bene != null && min_pg_bene != "") 
      query += "min_pg_bene=" + min_pg_bene + "&";
    if(max_pg_bene != null && max_pg_bene != "")
      query += "max_pg_bene=" + max_pg_bene + "&";
    if(ds_bene != null && ds_bene != "") query += "ds_bene=" + ds_bene + "&";
    if(categorie_inventariali_selezionate != null && categorie_inventariali_selezionate.length > 0){
      for (var i = 0; i < categorie_inventariali_selezionate.length; i++) {
        query += "categ=" + categorie_inventariali_selezionate[i] + "&";
      }
    } 
    if(ubicazione != null && ubicazione != "") query += "ubicazione=" + ubicazione + "&";
    if(ubicazione_precisa != null && ubicazione_precisa != "") query += "ubicazione_precisa=" + ubicazione_precisa + "&";
    $('#table').bootstrapTable('refresh', {url: query});
    $('#advancedSearchModal').modal('hide')
}
