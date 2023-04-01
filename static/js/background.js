//GENERAL STUFF
const DAYS = 7;
const BATTERY_BAR_MAX_WIDTH = 400;
var autoRefresh = true;
var daylightElements = [],
	cloudcoverElements = [],
	visibilityElements = [],
	weekdayElements = [];
var batteryTextElement,
	batteryBarElement;

function updateDisplay() {
	//just going to trust the html will have 7 elements lol
	if(forecast.length > 0) {
		for(let i = 0; i < DAYS; i++) {
			let day_info = forecast[i];
			console.log(day_info);
			let sunrise = new Date(day_info.sunrise),
				sunset = new Date(day_info.sunset);
			daylightElements[i].innerHTML = `${zero(sunrise.getHours(), 2)}:${zero(sunrise.getMinutes(), 2)} - ${zero(sunset.getHours(), 2)}:${zero(sunset.getMinutes(), 2)}`;
			cloudcoverElements[i].innerHTML = `${round(100 * day_info.cloudcover, 2)}%`;
			visibilityElements[i].innerHTML = `${round(100 * day_info.visibility, 2)}%`;
			weekdayElements[i].innerHTML = day_info.weekday;
		}
	}

	//change battery info
	if(!!Object.keys(panels).length) {
		let percent_charged = panels[panelIds[0]].battery.percent_charged;
		batteryTextElement.innerHTML = `${Math.round(100 * percent_charged)}`;
		batteryBarElement.style.width = `${percent_charged * BATTERY_BAR_MAX_WIDTH}px`;
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
				avg_visibility = 0,
				daylight_hours = 0;
			for(let hour = 0; hour < 24; hour++) {
				//!	NOTICE: daily cloudcover and visibility is only during daylight hours
				let x = data[day].hourly[hour];
				if(x.time < sunrise || x.time > sunset) continue;
				daylight_hours++;
				avg_cloudcover += x.cloudcover;
				avg_visibility += x.visibility;
			}
			avg_cloudcover /= daylight_hours;
			avg_visibility /= daylight_hours;

			//actually store info
			forecast[day] = new DailyStat(sunrise, sunset, avg_cloudcover, avg_visibility);
		}
		updateDisplay();
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

	updateDisplay();
}


window.addEventListener("load", () => {
	//~	testing
	addPanel(new Panel(
		"test_panel_id",
		new Battery(BatteryStates.CHARGING, Math.random(), Math.random() * 0.2, Math.random() * 0.1)
	));
	setTimeout(() => {
		getPanelData("test_panel_id", setPanel);
	}, 1000);
	setTimeout(() => {
		setPanelData("test_panel_id", new ChargeRates(Math.random() * 0.4, Math.random() * 0.3));
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
	batteryTextElement = document.getElementById("battery-info");
	batteryBarElement = document.getElementById("battery-bar");

	//loops
	refreshBatteryData();
	setInterval(refreshBatteryData, 5000);

	refreshForecastData();
	setInterval(refreshForecastData, 60000);
});
