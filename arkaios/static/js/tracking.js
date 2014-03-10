function loadPage(){
	$("#submitAttendance").on("click", function(){
		submitClick();
	});
}

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

// Large group tracking - Reset display
function resetScreen(){
	$("input").val("");
	$("select").val("");
	// still need to add the clearing of suggestions
}

// Large group tracking - Submit button click
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
		parseTrackingStatus(data);
	});
}

// Large group tracking - Parse jsonified data
function parseTrackingStatus(data){
	if(data.status=="error"){
		console.log("error");
	} else if(data.status=="success") {
		console.log("success yo");
		resetScreen();
		displayConfirmation();
	}	
}