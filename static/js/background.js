var charge = 0;

function updateDisplay() {
	//"battery-info"
	document.getElementById("battery-info").innerHTML = charge;
}

async function refreshData() {
	let panelData = await getPanelData();
	console.log(panelData);
}


window.addEventListener("load", () => {
	setInterval(() => {
		refreshData();
		updateDisplay();
	}, 1000);
});
