const API_ADDRESS = `localhost:8000/api`;

async function getPanelData(solarId) {
	fetch(`${API_ADDRESS}/getPanelData?id=lol`).then(res => res.json()).then((data) => {
		console.log(data);
		//resolve(data);
	});
}

function addPanel(panel) {
	fetch(`${API_ADDRESS}/addPanel`);
}

function setPanelData(solarId) {
	fetch(`${API_ADDRESS}/setPanelData`);
}
