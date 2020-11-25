function ResetComponents(){

    $('#brand').change(function () {
    $('#drone_name').val('');
    $('#model_year').val('');
    $('input[type="checkbox"]').prop('checked', false);
    $('input[type="number"]').val('');
    $('input[type="radio"]').prop('checked', false);

});

$('#model_year').change(function () {
    $('#drone_name').val('');
    $('#brand').val('');
    $('input[type="checkbox"]').prop('checked', false);
    $('input[type="number"]').val('');
    $('input[type="radio"]').prop('checked', false);

});

$('input[type="number"]').click(function () {
    $('#drone_name').val('');
    $('select').val('');
    $('input[type="checkbox"]').prop('checked', false);
    $('input[type="radio"]').prop('checked', false);

});

$('input[type="checkbox"]').click(function () {
    $('#drone_name').val('');
    $('select').val('');
    $('input[type="number"]').val('');
    $('input[type="radio"]').prop('checked', false);
});

$('input[type="radio"]').click(function () {
    $('#drone_name').val('');
    $('select').val('');
    $('input[type="number"]').val('');
    $('input[type="checkbox"]').prop('checked', false);
});


$('#drone_name').click(function () {
    $('select').val('');
    $('input[type="number"]').val('');
    $('input[type="checkbox"]').prop('checked', false);
    $('input[type="radio"]').prop('checked', false);
});
}

ResetComponents();

$('#drone_name, input[type="number"]').keyup(function (e) {
    if (e.keyCode === 13)
         $('#search_drones').click();
});

$('select').change(function () {
   $('#search_drones').click();
});


$('#view_drones').click(function(){
    const base_url = 'http://localhost:8000/drone/list/';
    axios
        .get(base_url)
        .then(r => {
            $(this).off('click');
            $('#drone_list').show();
            let output = '';
            let counter = 0;
            let total_drones = Object.keys(r.data).length;
            $.each(r.data, function(key, val) {
                    if (counter >= 3 && !(counter % 3))
                        output += '</div>';
                    if (!(counter % 3))
                        output += '<div class=columns>';
                output += '<div class="column is-4"><div class="droned"><div class="droned-content"><div class="media">' +
                    '<div class="media-left"><figure class="image"><a href="http://localhost:8000/drone/' + val.id + '/info/">' +
                    '<img class="drone' + val.id + '"></a></figure></div><div class="media-content"><p class="title is-5">' +
                     val.model.name + ' ' + val.name + '</p><p class="subtitle is-6"><i>' + val.engine.name + '</i><br>' +
                     val.engine.power + ' W<br>' + val.model_year + '</p></div></div><div class="content">Price per hour: <b>$' +
                     val.price_hourly + '</b><br><a href="http://localhost:8000/drone/' + val.id + '/info/"><span class="tag is-success">' +
                     'Rent a drone</span></a></div></div></div></div>';
                counter++;
    axios
        .get(base_url + val.id + '/gallery/')
        .then(r => {
            let len = r.data.length; // number of drone photos
            let i = Math.floor((Math.random() * len)); // get random number from 0 to len
            $('img.drone' + val.id).attr('src', r.data[i].photo)
                                 .css({'height': '130px', 'width': '150px'});
            });

    });
         $('div.drones').html('<span style="margin-left: 20.5%;" class="tag is-primary">Total drones: ' + total_drones +
            '</span><br><br><br><div class="columns"><div class="box" style="width:59%; margin-left: 20.5%;">' + output +
            '</div></div></div><div style="margin-top: 5%;"></div>');

    });

});
