function pageLoad(){
	reloadAttendanceTable();
	// pill navigation listeners
	$(".nav-pills a").on("click", function(){
		weekNavigation(parseInt($(this).html()));
	});
}

function weekNavigation(selectedWeek){
	$(".nav-pills .active").removeClass("active");
	new_selection = ".nav-pills li:nth-child(x)";
	new_selection = new_selection.replace("x", selectedWeek+1);
	console.log(new_selection);
	$(new_selection).addClass("active");

	reloadAttendanceTable();
}

function reloadAttendanceTable(){
	// harvest currently selected properties
	currentQuarter = $("#currentQuarter").html();
	weekNumber = parseInt($(".nav-pills .active a").html());
	sortToggleNumber = parseInt($("#sortToggle i").parent().attr("value"));
	siftToggleNumber = parseInt($("#siftToggle i").parent().attr("value"));

	// build url for ajax call - feed input and get data
	$.get($SCRIPT_ROOT + '/admin/large-group/_get_event_table', {
        quarter: currentQuarter,
        week: weekNumber
	}, function(data) {
		console.log(data);
		$("#attendance-data div").html(data);

		//change the properties of the dropdowns

		//change the week currently selected
	});
}