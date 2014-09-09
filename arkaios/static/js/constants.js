var pieChartData = [
    {
        value: 300,
        color:"#425865",
        highlight: "#576A76",
        label: "Freshmen"
    },
    {
        value: 50,
        color: "#55B7A0",
        highlight: "#68BFAB",
        label: "Sophomores"
    },
    {
        value: 100,
        color: "#EFCD58",
        highlight: "#F1D26A",
        label: "Juniors"
    },
    {
        value: 300,
        color: "#E07F4C",
        highlight: "#E48D60",
        label: "Seniors"
    },
    {
        value: 300,
        color: "#D93C42",
        highlight: "#DD5055",
        label: "Others"
    }
]

var helpText = '<div id="help" class="alert alert-info"><div class="up-arrow">' + 
                        '</div>If you see your name suggested above, click on it to ' + 
                        'automatically fill in the form!</div>';

var optionsListJs = {
    item: '<li class="list-group-item"><h4 class="list-group-item-heading name"></h4><input type="hidden" class="id" /></li>'
};