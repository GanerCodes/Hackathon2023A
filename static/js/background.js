function updateDisplay() {
	//
}

function refreshData() {
	//
}


window.addEventListener("load", () => {
	//~	testing
	addPanel(new Panel(
		"test_panel_id",
		new Battery(BatteryStates.CHARGING, 0.5, 0.01, 0.02)
	));
	setTimeout(() => {
		getPanelData("test_panel_id");
	}, 1000);
	setTimeout(() => {
		setPanelData("test_panel_id", new ChargeRates(0.4, 0.3));
	}, 2000);
	setTimeout(() => {
		getPanelData("test_panel_id");
	}, 3000);
	//~	testing

	setInterval(() => {
		refreshData();
		updateDisplay();
	}, 1000);
});
