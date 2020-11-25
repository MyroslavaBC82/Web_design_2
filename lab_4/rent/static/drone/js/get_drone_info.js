$('#get_drone_info').click(function () {
   let id = window.location.pathname.split('/')[2];
   const base_url = 'http://localhost:8000/drone/list/' + id + '/';

   axios
       .get(base_url)
       .then(r =>{
           $('#back').show();
           $(this).off('click');
           $('div.droned').show();
           let drone = r.data;
           $('p.title').html(drone.model.name + ' ' + drone.name);
           let output = '<i>Engine</i>: ' + drone.engine.name + ', ' +
           drone.engine.power + ' W, <br>' + drone.engine.fuel_type.name + ' ' +
           drone.engine.consumation + ' l.<br><br><i>Model year</i>: ' + drone.model_year +
           '<br><br><i>Additional Equipment</i>: <ul>';
           let equipment = drone.additional_equipment;
           $.each(equipment, function(key, val){
                output += '<li>- ' + val.name + '<li>';
           });
           let img = ''; // rate stars image
           if (!drone.rate)
               img = '<img src="/static/drone/img/0-star.png" height="150" width="150">';
           else if(Math.round(drone.rate) === 1)
               img = '<img src="/static/drone/img/1-star.png" height="150" width="150">';
           else if(Math.round(drone.rate) === 2)
               img = '<img src="/static/drone/img/2-star.png" height="150" width="150">';
           else if(Math.round(drone.rate) === 3)
               img = '<img src="/static/drone/img/3-star.png" height="150" width="150">';
           else if(Math.round(drone.rate) === 4)
               img = '<img src="/static/drone/img/4-star.png" height="150" width="150">';
           else
               img = '<img src="/static/drone/img/5-star.png" height="150" width="150">';

           $('p.subtitle').html(output + '</ul><br><i>Price per hour:</i> <b>$'
                                + '<span id="drone_price">' + drone.price_hourly + '</span></b><br><br>' + img);


       });

   axios
       .get(base_url + 'gallery/')
       .then(r => {
           let gallery = r.data;
           let output = '<div class="w3-content w3-display-container">';
           $.each(gallery, function(key, val) {
               output += '<img class="mySlides" src="' + val.photo + '" style="width:100%;">';
           });

           output += '<button class="w3-button w3-black w3-display-left" onclick="plusDivs(-1)">&#10094;</button>' +
                     '<button class="w3-button w3-black w3-display-right" onclick="plusDivs(1)">&#10095;</button></div>';
            $('div.gallery').html(output);
            $('img.mySlides').hide();
            $('img.mySlides:first').show();
       });

});

