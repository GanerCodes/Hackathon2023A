const PanelStates = Object.freeze({
	DISCONNECTED: 0,
	CHARGING: 1,
	EMPTY: 2
});

class Panel {
	constructor(id, battery) {
		this.id = id;
		this.battery = battery;
	}
}

class Battery {
	constructor(percent_charged, charging_rate, decharging_rate) {
		this.percent_charged = percent_charged;
		this.charging_rate = charging_rate;
		this.decharging_rate = decharging_rate;
	}
}
