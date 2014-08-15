// large group attendance page initializer
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

// On changes to the sort/sift toggles, these two functions receive which one 
// fired and modify the view/data accordingly
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

// reloads the attendance data table based on whatever criteria is there
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
		console.log(pieChartData);
	});
}

///////////////////////////////////////
//                                   //
//    Large Group Overview Code      //
//                                   //
///////////////////////////////////////

//loads the the overview data table
function loadOverviewTable(){
	selectedQuarter = $(".nav-pills .active a").attr("value");
	sortToggleNumber = parseInt($("#sortToggle i").parent().attr("value"));
	siftToggleNumber = parseInt($("#siftToggle i").parent().attr("value"));

	$.get($SCRIPT_ROOT + '/admin/large-group/_get_overview_table', {
		quarter: selectedQuarter,
		sort: sortToggleNumber,
		sift: siftToggleNumber
	}, function(data) {
		$("#overview-data").html(data);
	});
}

// large group overview page initializer
function largeGroupOverviewPageLoad(){
	loadOverviewTable();

	$(".nav-pills a").on("click", function(){
		chooseQuarterHandlerOverview($(this).attr("value"));
	});

	$("#sortToggle a").on("click", function(){
		sortHandlerOverview(parseInt($(this).attr("value")));
	});

	$("#siftToggle a").on("click", function(){
		siftHandlerOverview(parseInt($(this).attr("value")));
	});

	displayAttendanceGraphs("hi", pieChartData);
}

// Data Modifier Handlers
function chooseQuarterHandlerOverview(quarter){
	$(".nav-pills .active").removeClass("active");
	$("[value='" + quarter + "']").parent().addClass('active');
	loadOverviewTable();
}

function sortHandlerOverview(sortValue){
	icon = $("#sortToggle i").remove();
	new_sort = "#sortToggle li:nth-child(x) a";
	new_sort = new_sort.replace("x", sortValue+1);
	$(new_sort).prepend(icon);
	largeGroupOverviewPageLoad();
}

function siftHandlerOverview(siftValue){
	icon = $("#siftToggle i").remove();
	new_sift = "#siftToggle a";
	$($(new_sift)[siftValue]).prepend(icon);
	largeGroupOverviewPageLoad();
}

// Graphing functions

function displayAttendanceGraphs(quarter, pieChart){
	//dummy var
	quarter = 'w14'
	var graphData = {
		labels: ['Week 1','Week 2','Week 3','Week 4','Week 5','Week 6','Week 7','Week 8','Week 9','Week 10'],
		datasets: [
			{
				label: 'Week Number',
	            fillColor: "rgba(151,187,205,0.5)",
	            strokeColor: "rgba(151,187,205,0.8)",
	            highlightFill: "rgba(151,187,205,0.75)",
	            highlightStroke: "rgba(151,187,205,1)"
	        }
		]
	};
	$.get($SCRIPT_ROOT + '/admin/large-group/_get_overview_graphs/' + quarter, function(data){
		graphData.datasets[0].data = data.week;
		var ctx = document.getElementById("weekly-attendance-graph").getContext("2d");
		var attendanceBarChart = new Chart(ctx).Line(graphData);

		for(var i=0; i < pieChart.length; i++){
			pieChart[i].value = data.year[i];
		}

		var ctx2 = document.getElementById("class-attendance-graph").getContext("2d");
		var attendancePieChart = new Chart(ctx2).Doughnut(pieChart, { legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<segments.length; i++){%><li><span style=\"background-color:<%=segments[i].fillColor%>\"></span><%if(segments[i].label){%><%=segments[i].label%><%}%></li><%}%></ul>"});
		var legend = attendancePieChart.generateLegend();
		$("#doughnut-legend").html(legend);
		console.log(legend);
	});
}

