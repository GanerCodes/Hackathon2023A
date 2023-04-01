
class Panel:
    STATES = {0: "disconnected",
              1: "charging",
              2: "empty"}

    class Battery:
        def Battery(self,
                    precent_charged: float,
                    charging_rate: float,
                    decharging_rate: float):
            self.precent_charged = precent_charged
            self.charging_rate = charging_rate
            self.decharging_rate = decharging_rate

    def Panel(self, ID: str, battery: Battery):
        self.ID = ID
        self.battery = battery
