function loadPage(){
	$("#submitAttendance").on("click", function(){
		submitClick();
	});

	$(".list-group").updateList({}).updateList('template', 
			'<li class="list-group-item">{firstname} {lastname}' + 
			'<span class="pull-right">{year}<input class="dorm" type="hidden" name="dorm" value="{dorm}">' + 
			'<input type="hidden" name="email" value="{email}"></span></li>')
			.updateList('listener', autoSuggestClickListener);

	updateSuggestionsListener();
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

		//add error handling
	} else if(data.status=="success") {
		resetScreen();
		displayConfirmation();
	}	
}

function searchUsers(){
	$.getJSON($SCRIPT_ROOT + '/focus/_search', {
		firstName: $('#firstName').val(),
		lastName: $('#lastName').val(),
		email: $("#email").val(),
		dorm: $("#dorm").val(),
		year: $('select').val()
	}, function(data) {
		updateSuggestions(data);
	});
}

function updateSuggestions(data){
	for(var i=0; i<data.results.length; i++){
		data.results[i] = JSON.parse(data.results[i]);
	}

	$(".list-group").updateList('update', data.results);
}

// listens to any input fields changing
function updateSuggestionsListener(){
	$("input").change(function() {
		searchUsers();
	});
	$("select").change(function() {
		searchUsers();
	});
}

// listens to a user clicking on a suggested user
function autoSuggestClickListener(object){
	$(object).on('click', function(){
		console.log($(this).children());
	});
}