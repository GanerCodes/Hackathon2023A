//FORECAST STUFF
function getForecast(callback) {
	getLocation((coords) => {
		neufetch("getForecast", {
			latitude: coords.latitude,
			longitude: coords.longitude,
			timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
		}, (data) => {
			console.debug("getForecast", data);
			callback(data);
		});
	});
}
function getPanelSchedule(solarId, callback) {
	getLocation((coords) => {
		neufetch("getPanelSchedule", {
			id: solarId,
			latitude: coords.latitude,
			longitude: coords.longitude,
			timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
		}, (data) => {
			console.debug("getPanelSchedule", data);
			callback(data);
		});
	});
}


//PANEL STUFF
function getPanelData(solarId, callback) {
	neufetch("getPanelData", { id: solarId }, (data) => {
		console.debug("getPanelData", data);
		internal_panels[solarId] = data;
		callback(data);
	});
}

function addPanel(panel) {
	neufetch("addPanel", panel, (data) => {
		console.debug("addPanel", data);
		internal_panels[panel.id] = panel;
	});
}

function setPanelData(solarId, chargeRates) {
	let newPanel = new Panel(internal_panels[solarId], chargeRates);
	neufetch("setPanelData", newPanel, (data) => {
		console.debug("setPanelData", data);
		internal_panels[solarId] = newPanel;
	});
}


//internal
var internal_panels = {};

function neufetch(route, reqData, callback) {
	fetch(`http://localhost:5000/${route}`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify(reqData)
	}).then((res) => (res.json())).then((data) => {
		callback(data);
	}).catch(() => { callback({}); });
}
