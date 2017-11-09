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

