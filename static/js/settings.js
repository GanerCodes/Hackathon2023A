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
		addPanel(
			new Panel(
				id,
				new Battery(
					BatteryStates.CHARGING,
					currentCharge,
					chargingRate,
					dischargingRate
				)
			)
		);
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
	pNameElement = document.getElementById("id");
	pLocationElement = document.getElementById("location");
	pChargeElement = document.getElementById("currcharge");
	pChargingRateElement = document.getElementById("chargerate");
	pDechargingRateElement = document.getElementById("dischargerate");
});
