function getPanelData(solarId) {
	neufetch("getPanelData", { id: solarId }, console.log);
}

function addPanel(panel) {
	//neufetch("addPanel", panel, ()=>{});
	neufetch(
		"addPanel",
		{
			"id": "test_panel_id",
			"battery": {
				"state": 0,
				"percent_charged": 0.5,
				"charging_rate": 0.1,
				"decharging_rate": 0.2
			}
		},
		console.log
	);
}

function setPanelData(solarId) {
	neufetch("setPanelData", {}, ()=>{});
}



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
