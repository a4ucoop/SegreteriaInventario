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

function advancedSearch (argument) {
    var query = "/inventario/table/advancedSearch?";
    var min_id_bene = document.forms["advancedSearchForm"]["min_id_bene"].value;
    var max_id_bene = document.forms["advancedSearchForm"]["max_id_bene"].value;
    var codici_inventario_selezionati = [];
    $("input:checkbox[name=codice_inventario]:checked").each(function(){
        codici_inventario_selezionati.push($(this).val());
    });
    var min_pg_bene = document.forms["advancedSearchForm"]["min_pg_bene"].value;
    var max_pg_bene = document.forms["advancedSearchForm"]["max_pg_bene"].value;
    var ds_bene = document.forms["advancedSearchForm"]["ds_bene"].value;
    var from_dt_acquisto = document.forms["advancedSearchForm"]["from_dt_acquisto"].value;
    var to_dt_acquisto = document.forms["advancedSearchForm"]["to_dt_acquisto"].value;
    var categorie_inventariali_selezionate = [];
    $("input:checkbox[name=categorie_inventariali]:checked").each(function(){
        categorie_inventariali_selezionate.push($(this).val());
    });
    var ubicazione = document.forms["advancedSearchForm"]["ubicazione"].value;
    var ubicazione_precisa = document.forms["advancedSearchForm"]["ubicazione_precisa"].value;
    var from_dt_ini_ammortamento = document.forms["advancedSearchForm"]["from_dt_ini_ammortamento"].value;
    var to_dt_ini_ammortamento = document.forms["advancedSearchForm"]["to_dt_ini_ammortamento"].value;
    var min_valore_convenzionale = document.forms["advancedSearchForm"]["min_valore_convenzionale"].value;
    var max_valore_convenzionale = document.forms["advancedSearchForm"]["max_valore_convenzionale"].value;

    var nome_tipo_dg = document.forms["advancedSearchForm"]["nome_tipo_dg"].value;

    var num_doc_rif = document.forms["advancedSearchForm"]["num_doc_rif"].value;

    var min_num_registrazione = document.forms["advancedSearchForm"]["min_num_registrazione"].value;
    var max_num_registrazione = document.forms["advancedSearchForm"]["max_num_registrazione"].value;

    var denominazione = document.forms["advancedSearchForm"]["denominazione"].value;

    var nome = document.forms["advancedSearchForm"]["nome"].value;

    var cognome = document.forms["advancedSearchForm"]["cognome"].value;

    if(min_id_bene != null && min_id_bene != "")
      query += "min_id_bene=" + min_id_bene + "&";
     if(max_id_bene != null && max_id_bene != "")
      query += "max_id_bene=" + max_id_bene + "&";
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
    if(from_dt_acquisto != null && from_dt_acquisto != "")
      query += "from_dt_acquisto=" + from_dt_acquisto + "&";
    if(to_dt_acquisto != null && to_dt_acquisto != "")
      query += "to_dt_acquisto=" + to_dt_acquisto + "&";
    if(categorie_inventariali_selezionate != null && categorie_inventariali_selezionate.length > 0){
      for (var i = 0; i < categorie_inventariali_selezionate.length; i++) {
        query += "categ=" + categorie_inventariali_selezionate[i] + "&";
      }
    } 
    if(ubicazione != null && ubicazione != "") query += "ubicazione=" + ubicazione + "&";
    if(ubicazione_precisa != null && ubicazione_precisa != "") query += "ubicazione_precisa=" + ubicazione_precisa + "&";
    if(from_dt_ini_ammortamento != null && from_dt_ini_ammortamento != "") 
      query += "from_dt_ini_ammortamento=" + from_dt_ini_ammortamento + "&";
    if(to_dt_ini_ammortamento != null && to_dt_ini_ammortamento != "")
      query += "to_dt_ini_ammortamento=" + to_dt_ini_ammortamento + "&";
    if(min_valore_convenzionale != null && min_valore_convenzionale != "")  
      query += "min_valore_convenzionale=" + min_valore_convenzionale + "&";
    if(max_valore_convenzionale != null && max_valore_convenzionale != "")
      query += "max_valore_convenzionale=" + max_valore_convenzionale + "&";
    if(nome_tipo_dg != null && nome_tipo_dg != "") query += "nome_tipo_dg=" + nome_tipo_dg + "&";
    if(num_doc_rif != null && num_doc_rif != "") query += "num_doc_rif=" + num_doc_rif + "&";
    if(min_num_registrazione != null && min_num_registrazione != "") 
      query += "min_num_registrazione=" + min_num_registrazione + "&";
    if(max_num_registrazione != null && max_num_registrazione != "")
      query += "max_num_registrazione=" + max_num_registrazione + "&";
    if(denominazione != null && denominazione != "") query += "denominazione=" + denominazione + "&";
    if(nome != null && nome != "") query += "nome=" + nome + "&";
    if(cognome != null && cognome != "") query += "cognome=" + cognome + "&";
    $('#table').bootstrapTable('refresh', {url: query});
    $('#advancedSearchModal').modal('hide')
}
