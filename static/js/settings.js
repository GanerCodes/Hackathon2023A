var pNameElement,
	pLocationElement,
	pChargeElement,
	pChargingRateElement,
	pDechargingRateElement;

function submitPanel() {
	//check if good
	//

	//actually add panel
	let id = pNameElement.value,
		currentCharge = Number(pChargeElement.value),
		chargingRate = Number(pChargingRateElement.value),
		dischargingRate = Number(pDechargingRateElement.value);
	if(panelIds.indexOf(id) < 0) {
		//doesn't yet exist, add panel
		let newPanel = new Panel(id, new Battery(BatteryStates.CHARGING, currentCharge, chargingRate, dischargingRate));
		addPanel(newPanel);
		panels[id] = newPanel;
		panelIds.push(id);
	}
	else {
		setPanelData(
			id,
			new ChargeRates(
				chargingRate,
				dischargingRate
			)
		);
	}
}

window.addEventListener("load", () => {
	pNameElement = document.getElementById("nameId");
	// pLocationElement = document.getElementById("location");
	pChargeElement = document.getElementById("currentCharge");
	pChargingRateElement = document.getElementById("chargeRate");
	pDechargingRateElement = document.getElementById("dischargeRate");
});
