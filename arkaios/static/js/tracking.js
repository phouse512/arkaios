function displayConfirmation(){
	$("#input-form").fadeOut("slow", function(){
		$("#confirmation").fadeIn("slow");
	});
	setTimeout(function() {
		$("#confirmation").fadeOut("slow", function() {
			$("#input-form").fadeIn();
		});
	}, 2000);
}

function submitClick(){
	$.getJSON($SCRIPT_ROOT + '/focus/_track', {
		firstName: $('#firstName').val(),
        lastName: $('#lastName').val(),
        email: $('#email').val(),
        dorm: $('#dorm').val(),
        year: $('select').val(),
        quarter: $('#quarter').html(),
        week: $('#week').html()
	}, function(data) {
		console.log(data);
	});
}