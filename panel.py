from optimizer import Optimizer

Number = float | int

def fit_data(obj, template):
    res = {}
    dict_obj = type(obj) == dict
    for n, t in template.items():
        valid_obj = dict_obj and n in obj
        if isinstance(t, dict):
            res[n] = fit_data(obj[n] if valid_obj else None, t)
        else:
            if valid_obj and isinstance(obj[n], t):
                res[n] = obj[n]
            else:
                res[n] = None
    return res


Panel_template = {
    "id": str,
    "battery": {
        "state": int,
        "percent_charged": Number,
        "charging_rate": Number,
        "decharging_rate": Number
    }
}

Panel_update_template = {
    "battery": {
        "charging_rate": Number,
        "decharging_rate": Number
    }
}

def create_schedule(curve, panel):
    battery = panel['battery']
    optimizer = Optimizer(curve,
                          starting_precentage=battery['percent_charged'],
                          power_gain=battery['charging_rate'],
                          power_draw=battery['decharging_rate'],
                          max_power=1,
                          dt=1/60)
    optimizer.merge_tops()
    return {
        "state_schedule": optimizer.Pa,
        "extremes": optimizer.compute_extremes}
