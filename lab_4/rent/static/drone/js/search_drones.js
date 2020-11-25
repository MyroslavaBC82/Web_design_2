$('input[type="checkbox"], input[type="radio"], #search_drones').click(function () {
    let url = 'http://localhost:8000/drone/list/';
    const drone_name = $('#drone_name').val().trim();
    const brand = $('#brand').val();
    const model_year = $('#model_year').val();
    const price_from = $('#price_from').val();
    const price_to = $('#price_to').val();
    const top_rated = $('#top_rated:checked').val();
    const fuel_type = $('input[type="radio"]:checked')
                      .parent('label').text();

    if (drone_name)
        url += '?search=' + drone_name;
    else if (brand)
        url += '?search=' + brand;
    else if (model_year) {
        if (model_year === '2000')
            url += '?year_from=0&year_to=2000';
        else if (model_year === '2005')
            url += '?year_from=2001&year_to=2005';
        else if (model_year === '2010')
            url += '?year_from=2006&year_to=2010';
        else if (model_year === '2015')
            url += '?year_from=2011&year_to=2015';
        else
            url += '?year_from=2016&year_to=2018';
    }
    else if (price_from && price_to)
        url += '?price_from=' + price_from + '&price_to=' + price_to;
    else if (top_rated)
        url += '?top_rated=True';
    else if (fuel_type)
        url += '?fuel_type=' + fuel_type;

    axios
        .get(url)
        .then(r => {
            $('#drone_list').show();
            let output = '';
            let drones = r.data;
            let total_drones = Object.keys(drones).length;
            let counter = 0;
            if (!total_drones) {
                $('div.drones').html('<div class="box" style="width:59%; margin-left: 20.5%;">' +
                    '<div class="columns"><div class="column is-5"></div><div class="column">' +
                    '<i style="color:rgb(255, 56, 96);"><b>Oops! No results found.</b></i></div></div></div>' +
                    '<div style="margin-top: 20%;"></div>'); // if drone not found
                return;
            }
            $.each(drones, function (key, val) {
                   if (counter >= 3)
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
            .get('http://localhost:8000/drone/list/' + val.id + '/gallery/')
            .then(r => {
                let photos = r.data;
                let len = photos.length; // number of drone photos
                let i = Math.floor((Math.random() * len)); // get random number from 0 to len
                $('img.drone' + val.id).attr('src', photos[i].photo)
                                     .css({'height': '130px', 'width': '150px'});
                });
           });

            $('div.drones').html('<span style="margin-left: 20.5%;" class="tag is-primary">Total drones: ' + total_drones +
            '</span><br><br><br><div class="columns"><div class="box" style="width:59%; margin-left: 20.5%;">' + output +
            '</div></div></div><div style="margin-top: 5%;"></div>');

        });
});