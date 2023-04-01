function wowForecast() {
	let id = panelIds[0];
	getPanelSchedule(id, (x) => {
		document.getElementById("schedule-img").src = `./panel_images/${id}.png`;
	});
}
