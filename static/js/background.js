var charge = 0;

function updateDisplay() {
	//"battery-info"
	//document.getElementById("battery-info").innerHTML = charge;
}

function refreshData() {
	//let panelData = getPanelData();
	//console.log(panelData);
}


window.addEventListener("load", () => {
	addPanel(new Panel(
		"test_panel_id",
		new Battery(BatteryStates.CHARGING, 0.5, 0.01, 0.02)
	));
	setTimeout(() => {
		getPanelData("test_panel_id");
	}, 1000);
	setInterval(() => {
		refreshData();
		updateDisplay();
	}, 1000);
});
