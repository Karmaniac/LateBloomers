import { useState } from 'react'
import ee from '@google/earthengine'

function Dashboard() {
	// Initialize client library and run analysis.
	var initialize = function() {
		ee.initialize(null, null, function() {

			var mapContainer = document.getElementById('map-container');
			const embeddedMap = new google.maps.Map(mapContainer, {
				// Pan and zoom initial map viewport to Grand Canyon.
				center: { lng: -44.5626, lat: -2.0164 },
				zoom: 9,
			});

			// Obtain reference to digital elevation model and apply algorithm to
			// calculate slope.
			const srtm = ee.Image("CGIAR/SRTM90_V4");
			const slope = ee.Terrain.slope(srtm);

			// Create a new tile source to fetch visible tiles on demand and display them
			// on the map.
			const mapId = slope.getMapId({ min: 0, max: 60 });
			const tileSource = new ee.layers.EarthEngineTileSource(mapId);
			const overlay = new ee.layers.ImageOverlay(tileSource);
			embeddedMap.overlayMapTypes.push(overlay);
			// var dataset = ee.ImageCollection('LANDSAT/MANGROVE_FORESTS');
			// var mangrovesVis = {
			// 	min: 0,
			// 	max: 1.0,
			// 	palette: ['d401F5'],
			// };
			// Map.setCenter(-44.5626, -2.0164, 9);
			// Map.addLayer(dataset, mangrovesVis, 'Mangroves');
			//ui.DateSlider(start, end, value, period, onChange, disabled, style)

			// Map.add(ui.Slider(2000, 2025, 2010, 1))
			console.log(dataset);
		}, function(e) {
			console.error('Initialization error: ' + e);
		});

		// Run an Earth Engine script.
		// var image = new ee.Image('srtm90_v4');
		// image.getMap({ min: 0, max: 1000 }, function(map) {
		// console.log(map);
		// });
	};

	// Authenticate using an OAuth pop-up.
	ee.data.authenticateViaOauth(import.meta.env.VITE_CLIENT_ID, initialize, function(e) {
		console.error('Authentication error: ');
	}, null, function() {
		console.log('auth popup');
		ee.data.authenticateViaPopup(initialize);
	});

	const [count, setCount] = useState(0);



	return (
		<div id='dashboard'>
			<div id='past'>
				<h1>Past</h1>
				<div id="map-container"></div>
				<div className='graph'>
					GRAPH HERE
				</div>
			</div>
			<div id='future'>
				<h1>Future</h1>
				<div className="card">
					<button onClick={() => setCount((count) => count + 1)}>
						count is {count}
					</button>
				</div>
			</div>
		</div>
	)
}

export default Dashboard
