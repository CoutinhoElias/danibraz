function addNewAddress(evt){
    tipo = $("#id_tipo").val()
    zipcode = $("#id_zipcode").val()
    number = $("#id_number").val()
    city = $("#id_city").val()
    state = $("#id_state").val()    
    public_place = $("#id_public_place").val()
    country = $("#id_country").val()
    neighborhood = $("#id_neighborhood").val()
    edit =   '<a type="hidden" class="tiny btn-floating waves-effect waves-light teal lighten-2"><i class="tiny material-icons">mode_edit</i></a>'
    mode_delete =   '<a class="tiny btn-floating waves-effect waves-light red"><i class="tiny material-icons">delete</i></a>'


    row = $("<tr>")
    input_tipo = $('<input type="hidden">').val(tipo)
    col_tipo = $("<td>").html(tipo).append(input_tipo)
    row.append(col_tipo)

    input_public_place = $('<input type="hidden">').val(public_place)
    col_public_place = $("<td>").html(public_place).append(input_public_place)
    row.append(col_public_place)

    input_number = $('<input type="hidden">').val(number)
    col_number = $("<td>").html(number).append(input_number)
    row.append(col_number)
        
    input_city = $('<input type="hidden">').val(city)
    col_city = $("<td>").html(city).append(input_city)
    row.append(col_city)
    
    input_state = $('<input type="hidden">').val(state)
    col_state = $("<td>").html(state).append(input_state)
    row.append(col_state)
        
    input_zipcode = $('<input type="hidden">').val(zipcode)
    col_zipcode = $("<td>").html(zipcode).append(input_zipcode)
    row.append(col_zipcode)  
            
    input_country = $('<input type="hidden">').val(country)
    col_country = $("<td>").html(country).append(input_country)
    row.append(col_country)
                 
    input_neighborhood = $('<input type="hidden">').val(neighborhood)
    col_neighborhood = $("<td>").html(neighborhood).append(input_neighborhood)
    row.append(col_neighborhood)

    input_edit = $().val(edit)
    col_edit = $("<td>").html(edit).append(input_edit)
    row.append(col_edit)

    input_mode_delete = $().val(mode_delete)
    col_mode_delete = $("<td>").html(mode_delete).append(input_mode_delete)
    row.append(col_mode_delete)


    $('#address_table tbody').append(row)
}

