from optimizer import Optimizer
import matplotlib.pyplot as plt

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
    Id = panel['id']
    optimizer = Optimizer(curve,
                          starting_precentage=battery['percent_charged'],
                          power_gain=battery['charging_rate'],
                          power_draw=battery['decharging_rate'],
                          max_power=1,
                          dt=1/60)

    extremes = optimizer.compute_extremes(
        optimizer.max_p_integral, optimizer.Pm, True)
    plt.plot(optimizer.max_p_integral)
    plt.scatter(*zip(*extremes))
    optimizer.merge_tops()
    plt.plot(optimizer.max_p_integral)
    plt.plot(*zip(*enumerate(optimizer.Pa)))

    img_path = f"./static/panel_images/{Id}.png"
    plt.savefig(img_path)

    return {
        "state_schedule": optimizer.Pa,
        "image": img_path,
        "extremes": [{
            "time": time,
            "type": Type
        } for time, Type in optimizer.compute_extremes(
            optimizer.max_p_integral,
            optimizer.Pm
        )]}

if __name__ == "__main__":
    from forecast import internal_forecast
    create_schedule(internal_forecast(
        36.0663068,
        -94.1738257,
        "America/Chicago"
    ), {
        "id": "A039B8CD",
        "battery": {
            "state": 1,
            "percent_charged": 0.5,
            "charging_rate": 0.15,
            "decharging_rate": 0.05
        }
    })