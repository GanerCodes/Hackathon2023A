//GENERAL STUFF
const DAYS = 7;
var autoRefresh = true;
var daylightElements = [],
	cloudcoverElements = [],
	visibilityElements = [],
	weekdayElements = [];

function updateDisplay() {
	//just going to trust the html will have 7 elements lol
	for(let i = 0; i < DAYS; i++) {
		let day_info = forecast[i];
		let sunrise = new Date(day_info.sunrise),
			sunset = new Date(day_info.sunset);
		daylightElements[i].innerHTML = `${zero(sunrise.getHours(), 2)}:${zero(sunrise.getMinutes(), 2)} - ${zero(sunset.getHours(), 2)}:${zero(sunset.getMinutes(), 2)}`;
		cloudcoverElements[i].innerHTML = `${round(day_info.cloudcover, 2)}%`;
		visibilityElements[i].innerHTML = `${round(day_info.visibility, 2)}%`;
		weekdayElements[i].innerHTML = day_info.weekday;
	}
}


//FORECAST STUFF
var forecast = [];
function refreshForecastData() {
	if(!autoRefresh) return;

	getForecast((data) => {
		//divide data into days
		for(let day = 0; day < DAYS; day++) {
			//sunrise/set times
			let sunrise = data[day].sunrise,
				sunset = data[day].sunset;

			//average daily cloudcover and visibility
			let avg_cloudcover = 0,
				avg_visibility = 0;
			for(let hour = 0; hour < 24; hour++) {
				//!	NOTICE: daily cloudcover and visibility is only during daylight hours
				let x = data[day].hourly[hour];
				if(x.time < sunrise || x.time > sunset) continue;
				avg_cloudcover += x.cloudcover;
				avg_visibility += x.visibility;
			}
			avg_cloudcover /= 24;
			avg_visibility /= 24;

			//actually store info
			forecast[day] = new DailyStat(sunrise, sunset, avg_cloudcover, avg_visibility);
		}
	});
}


//PANEL STUFF
var panels = {},
	panelIds = [],
	rollingPanelIndex = -1;

function setPanel(panel) {
	panels[panel.id] = panel;
	if(panelIds.indexOf(panel.id) < 0) {
		panelIds.push(panel.id);
	}
}

function refreshBatteryData() {
	if(!autoRefresh) return;

	//rolling refresh
	if(panelIds.length == 0) return;
	if(rollingPanelIndex < 0) rollingPanelIndex = 0;

	let id = panelIds[rollingPanelIndex];
	getPanelData(id, (data) => {
		panels[id] = data;
	});
	rollingPanelIndex = (rollingPanelIndex + 1) % panelIds.length;
}


window.addEventListener("load", () => {
	//~	testing
	addPanel(new Panel(
		"test_panel_id",
		new Battery(BatteryStates.CHARGING, 0.5, 0.01, 0.02)
	));
	setTimeout(() => {
		getPanelData("test_panel_id", setPanel);
	}, 1000);
	setTimeout(() => {
		setPanelData("test_panel_id", new ChargeRates(0.4, 0.3));
	}, 2000);
	setTimeout(() => {
		getPanelData("test_panel_id", setPanel);
	}, 3000);
	//~	testing

	//get elements
	daylightElements = document.getElementsByClassName("daylight");
	cloudcoverElements = document.getElementsByClassName("cloud-cover");
	visibilityElements = document.getElementsByClassName("visibility");
	weekdayElements = document.getElementsByClassName("day");

	//loops
	setInterval(updateDisplay, 10000);

	refreshBatteryData();
	setInterval(refreshBatteryData, 5000);

	refreshForecastData();
	setInterval(refreshForecastData, 60000,);
});
