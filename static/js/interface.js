function getPanelData(solarId) {
	neufetch("getPanelData", { id: solarId }, console.log);
}

function addPanel(panel) {
	neufetch("addPanel", panel, console.log);
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
