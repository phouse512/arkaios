function largeGroupAttendancePageLoad(){
	reloadAttendanceTable();
	// pill navigation listeners
	$(".nav-pills a").on("click", function(){
		weekNavigation(parseInt($(this).attr("value")));
	});
	$("#sortToggle a").on("click", function(){
		sortToggle(parseInt($(this).attr("value")));
	});
	$("#siftToggle a").on("click", function(){
		siftToggle(parseInt($(this).attr("value")));
		console.log(parseInt($(this).attr("value")));
	});
	$("#exportEvent").on("click", function(){
		downloadCSV();
	});

	chooseQuarter();
}

// the function responsible for setting up and listening for clicks on the quarter
// choosing modal
function chooseQuarter(){
	$("#chooseQuarter a").on("click", function(e){
		currentlySelected = $("#chooseQuarter .active");
		justClicked = $(this);
		if(justClicked.attr("value") == currentlySelected.attr("value")){
			currentlySelected.removeClass("active");
		} else {
			currentlySelected.removeClass("active");
			justClicked.addClass("active");
		}
	});

	$("#selectQuarter").on("click", function(e){
		e.preventDefault();
		quarter = $("#chooseQuarter .active").attr("value");
		window.location.replace($SCRIPT_ROOT + "/admin/large-group/" + quarter);
	});
}

// the following three functions all have to do with updating the data that's displayed
// by changing either the week, the sorting mechanism, or the sifting mechanism
function weekNavigation(selectedWeek){
	$(".nav-pills .active").removeClass("active");
	new_selection = ".nav-pills li:nth-child(x)";
	if(selectedWeek != -1){
		new_selection = new_selection.replace("x", selectedWeek+1);
	} else {
		new_selection = new_selection.replace("x", 12);
	}
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

// reloads the data table based on whatever criteria is there
function reloadAttendanceTable(type){
	// harvest currently selected properties
	currentQuarter = $("#currentQuarter").html();
	weekNumber = parseInt($(".nav-pills .active a").attr("value"));
	sortToggleNumber = parseInt($("#sortToggle i").parent().attr("value"));
	siftToggleNumber = parseInt($("#siftToggle i").parent().attr("value"));

	// build url for ajax call - feed input and get data
	$.get($SCRIPT_ROOT + '/admin/large-group/_get_event_table', {
        quarter: currentQuarter,
        week: weekNumber,
        sort: sortToggleNumber,
        sift: siftToggleNumber,
        returnType: 0
	}, function(data) {
		$("#attendance-data div").html(data);

		//change the properties of the dropdowns

		//change the week currently selected
	});
}

function loadOverviewTable(){
	$.get($SCRIPT_ROOT + '/admin/large-group/_get_overview_table', {
		quarter: 'w14'
	}, function(data) {
		$("#overview-data").html(data);
	});

}

function downloadCSV(){
	currentQuarter = $("#currentQuarter").html();
	weekNumber = parseInt($(".nav-pills .active a").attr("value"));
	sortToggleNumber = parseInt($("#sortToggle i").parent().attr("value"));
	siftToggleNumber = parseInt($("#siftToggle i").parent().attr("value"));
	
	url = $SCRIPT_ROOT + "/admin/large-group/_get_event_table?quarter=" + currentQuarter + "&week=" + weekNumber + "&sort=" + sortToggleNumber + "&sift=" + siftToggleNumber + "&returnType=1";
	window.location.replace(url);
}



function downloadTable(){
	currentQuarter = $("#currentQuarter").html();
	weekNumber = parseInt($(".nav-pills .active a").html());
	sortToggleNumber = parseInt($("#sortToggle i").parent().attr("value"));
	siftToggleNumber = parseInt($("#siftToggle i").parent().attr("value"));
		
	$.get($SCRIPT_ROOT + '/admin/large-group/_get_event_table', {
        quarter: currentQuarter,
        week: weekNumber,
        sort: sortToggleNumber,
        sift: siftToggleNumber,
        returnType: 1
	}, function(data) {
		console.log(data);

		//change the properties of the dropdowns

		//change the week currently selected
	});
}