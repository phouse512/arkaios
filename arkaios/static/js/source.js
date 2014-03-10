function pageLoad(){
	reloadAttendanceTable();
	// pill navigation listeners
	$(".nav-pills a").on("click", function(){
		weekNavigation(parseInt($(this).html()));
	});
	$("#sortToggle a").on("click", function(){
		sortToggle(parseInt($(this).attr("value")));
	});
	$("#siftToggle a").on("click", function(){
		siftToggle(parseInt($(this).attr("value")));
		console.log(parseInt($(this).attr("value")));
	});
}

function weekNavigation(selectedWeek){
	$(".nav-pills .active").removeClass("active");
	new_selection = ".nav-pills li:nth-child(x)";
	new_selection = new_selection.replace("x", selectedWeek+1);
	$(new_selection).addClass("active");

	reloadAttendanceTable();
}

function sortToggle(sortedToggle){
	icon = $("#sortToggle i").remove();
	new_sort = "#sortToggle li:nth-child(x) a";
	new_sort = new_sort.replace("x", sortedToggle+1);
	$(new_sort).prepend(icon);

	reloadAttendanceTable();
}

function siftToggle(siftedToggle){
	icon = $("#siftToggle i").remove();
	new_sift = "#siftToggle a";
	$($(new_sift)[siftedToggle]).prepend(icon);

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
        week: weekNumber,
        sort: sortToggleNumber,
        sift: siftToggleNumber
	}, function(data) {
		$("#attendance-data div").html(data);

		//change the properties of the dropdowns

		//change the week currently selected
	});
}