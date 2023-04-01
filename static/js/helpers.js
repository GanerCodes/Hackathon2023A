function zero(x, d) {
	while(x.length < d) {
		x = "0" + x;
	}
	return x;
}

function round(x, d) {
	let m = Math.pow(10, d);
	return Math.round(x * m) / m;
}
