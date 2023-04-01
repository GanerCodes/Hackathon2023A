function getPanelData(solarId) {
	neufetch("getPanelData", { id: solarId }, (data) => {
		console.log("get", data);
		panels[solarId] = data;
	});
}

function addPanel(panel) {
	neufetch("addPanel", panel, (data) => {
		console.log("add", data);
		panels[panel.id] = panel;
	});
}

function setPanelData(solarId, chargeRates) {
	let newPanel = new Panel(panels[solarId], chargeRates);
	neufetch("setPanelData", newPanel, (data) => {
		console.log("set", data);
		panels[solarId] = newPanel;
	});
}


//internal
var panels = {};

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
