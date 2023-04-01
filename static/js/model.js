const BatteryStates = Object.freeze({
	DISCONNECTED: 0,
	CHARGING: 1,
	EMPTY: 2
});

class Panel {
	constructor(id_or_original, battery_or_newChargeRates) {
		if(battery_or_newChargeRates instanceof ChargeRates) {
			this.id = id_or_original.id;
			this.battery = new Battery(
				id_or_original.battery.state,
				id_or_original.battery.percent_charged,
				battery_or_newChargeRates.charging_rate,
				battery_or_newChargeRates.decharging_rate
			);
		}
		else {
			this.id = id_or_original;
			this.battery = battery_or_newChargeRates;
		}
	}
}

class Battery {
	constructor(state, percent_charged, charging_rate, decharging_rate) {
		this.state = state;
		this.percent_charged = percent_charged;
		this.charging_rate = charging_rate;
		this.decharging_rate = decharging_rate;
	}
}

class ChargeRates {
	constructor(charging_rate, decharging_rate) {
		this.charging_rate = charging_rate;
		this.decharging_rate = decharging_rate;
	}
}
