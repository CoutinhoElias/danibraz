function addNewForm(tbody_selector, prefix) {
    var total_elem = $('#id_' + prefix + '-TOTAL_FORMS');
    var total = total_elem.val();
//    alert(total);
    var $tbody = $(tbody_selector);
    var $newRow = $tbody.find('tr:first').clone();
    $newRow.html($newRow.html().replace(/__prefix__/g, total));
    $newRow.show();
    $tbody.find('tr:last').after($newRow);

    total_elem.val(parseInt(total) + 1);

    $(".trGrid").css({ display : 'table-row' });
}

function calcularTotal() {
    var total = 0.0;
    // Pega os "forms"
    var forms = $(".item-form");
    forms.each(function(index, form) {
        // form contem o QTD e o VL
        form = $(form)

        // Converter esse valor para um numero que o JS entenda
        // (lembrando que o JS não entende valores com virgula e sim valores com . ex: 1.00)
        var quantidade = form.find(".qtd").val();
        // Tratar quando retornar valor vazio ou zero
        var valor = form.find(".vl").val();
        total += quantidade * valor;
    });
    // Campo total recebe o valor total calculado
    // Formatar o campo para ser interpretado conforme o padrão brasileiro
    $("#id_total_prop").val(total);

}