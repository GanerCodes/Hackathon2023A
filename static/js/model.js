const BatteryStates = Object.freeze({
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
	constructor(state, percent_charged, charging_rate, decharging_rate) {
		this.state = state;
		this.percent_charged = percent_charged;
		this.charging_rate = charging_rate;
		this.decharging_rate = decharging_rate;
		console.log(this);
	}
	// set_charging_rate = (rate) => {
	// 	this.charging_rate = rate;
	// }
	// set_decharging_rate = (rate) => {
	// 	this.decharging_rate = rate;
	// }
}
