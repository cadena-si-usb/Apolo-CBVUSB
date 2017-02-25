$(document).ready(function() {
    $(".clickable-row").click(function() {
        window.location = $(this).data("href");
    });

    $("#botton").click(function(){

    		// get the last DIV which ID starts with ^= "comisionPrefab"
	var $div = $('div[id^="comisionPrefab"]:last');

	// Read the Number from that DIV's ID (i.e: 3 from "comisionPrefab3")
	// And increment that number by 1
	var num = parseInt( $div.prop("id").match(/\d+/g), 10 ) +1;

	// Clone it and assign the new ID (i.e: from num 4 to ID "comisionPrefab4")
	var $comisionPrefab = $div.clone().prop('id', 'comisionPrefab'+num );
    	$comisionPrefab.empty();
    	$comisionPrefab.appendTo("#commission");
    });

});
