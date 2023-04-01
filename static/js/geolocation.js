const DEFAULT_COORDS = new Coordinates(36.0663068, -94.1738257);
const geolocAvailable = "geolocation" in navigator;

function getLocation(callback) {
	if(!geolocAvailable) {
		console.log("geolocation unavailable");
		callback(DEFAULT_COORDS);
	}
	navigator.geolocation.getCurrentPosition((data) => {
		callback(new Coordinates(data.coords.latitude, data.coords.longitude));
	});
}
