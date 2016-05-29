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
    var min_id = document.forms["advancedSearchForm"]["min_id"].value;
    var max_id = document.forms["advancedSearchForm"]["max_id"].value;
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

    var min_amm_iva_detr = document.forms["advancedSearchForm"]["min_amm_iva_detr"].value;
    var max_amm_iva_detr = document.forms["advancedSearchForm"]["max_amm_iva_detr"].value;

    var min_amm_iva_indetr = document.forms["advancedSearchForm"]["min_amm_iva_indetr"].value;
    var max_amm_iva_indetr = document.forms["advancedSearchForm"]["max_amm_iva_indetr"].value;

    var nome_tipo_dg = document.forms["advancedSearchForm"]["nome_tipo_dg"].value;

    var min_num_doc_rif = document.forms["advancedSearchForm"]["min_num_doc_rif"].value;
    var max_num_doc_rif = document.forms["advancedSearchForm"]["max_num_doc_rif"].value;

    var min_num_registrazione = document.forms["advancedSearchForm"]["min_num_registrazione"].value;
    var max_num_registrazione = document.forms["advancedSearchForm"]["max_num_registrazione"].value;

    var denominazione = document.forms["advancedSearchForm"]["denominazione"].value;

    if((min_id != null && min_id != "") &&  (max_id != null && max_id != "")) 
      query += "min_id=" + min_id + "&max_id=" + max_id + "&";
    if(codici_inventario_selezionati != null && codici_inventario_selezionati.length > 0){
      // cis = codici inventario selezionati
      for (var i = 0; i < codici_inventario_selezionati.length; i++) {
        query += "cods=" + codici_inventario_selezionati[i] + "&";
      }
    } 

    if((min_pg_bene != null && min_pg_bene != "") && (max_pg_bene != null && max_pg_bene != ""))
      query += "min_pg_bene=" + min_pg_bene + "&max_pg_bene=" + max_pg_bene + "&";
    if(ds_bene != null && ds_bene != "") query += "ds_bene=" + ds_bene + "&";
    if((from_dt_acquisto != null && from_dt_acquisto != "") && (to_dt_acquisto != null && to_dt_acquisto != ""))
      query += "from_dt_acquisto=" + from_dt_acquisto + "&to_dt_acquisto=" + to_dt_acquisto + "&";
    if(categorie_inventariali_selezionate != null && categorie_inventariali_selezionate.length > 0){
      for (var i = 0; i < categorie_inventariali_selezionate.length; i++) {
        query += "categ=" + categorie_inventariali_selezionate[i] + "&";
      }
    } 
    if(ubicazione != null && ubicazione != "") query += "ubicazione=" + ubicazione + "&";
    if(ubicazione_precisa != null && ubicazione_precisa != "") query += "ubicazione_precisa=" + ubicazione_precisa + "&";
    if((from_dt_ini_ammortamento != null && from_dt_ini_ammortamento != "") && (to_dt_ini_ammortamento != null && to_dt_ini_ammortamento != ""))
      query += "from_dt_ini_ammortamento=" + from_dt_ini_ammortamento + "&to_dt_ini_ammortamento=" + to_dt_ini_ammortamento + "&";
    if((min_valore_convenzionale != null && min_valore_convenzionale != "") &&  (max_valore_convenzionale != null && max_valore_convenzionale != "")) 
      query += "min_valore_convenzionale=" + min_valore_convenzionale + "&max_valore_convenzionale=" + max_valore_convenzionale + "&";
    if((min_amm_iva_detr != null && min_amm_iva_detr != "") &&  (max_amm_iva_detr != null && max_amm_iva_detr != "")) 
      query += "min_amm_iva_detr=" + min_amm_iva_detr + "&max_amm_iva_detr=" + max_amm_iva_detr + "&";
    if((min_amm_iva_indetr != null && min_amm_iva_indetr != "") &&  (max_amm_iva_indetr != null && max_amm_iva_indetr != "")) 
      query += "min_amm_iva_indetr=" + min_amm_iva_indetr + "&max_amm_iva_indetr=" + max_amm_iva_indetr + "&";
    if(nome_tipo_dg != null && nome_tipo_dg != "") query += "nome_tipo_dg=" + nome_tipo_dg + "&";
    if((min_num_doc_rif != null && min_num_doc_rif != "") &&  (max_num_doc_rif != null && max_num_doc_rif != "")) 
      query += "min_num_doc_rif=" + min_num_doc_rif + "&max_num_doc_rif=" + max_num_doc_rif + "&";
    if((min_num_registrazione != null && min_num_registrazione != "") &&  (max_num_registrazione != null && max_num_registrazione != "")) 
      query += "min_num_registrazione=" + min_num_registrazione + "&max_num_registrazione=" + max_num_registrazione + "&";
    if(denominazione != null && denominazione != "") query += "denominazione=" + denominazione + "&";
    $('#table').bootstrapTable('refresh', {url: query});
    $('#advancedSearchModal').modal('hide')
}