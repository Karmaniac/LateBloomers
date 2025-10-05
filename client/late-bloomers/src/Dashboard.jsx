import { useState } from 'react'
import Chart from './Chart.jsx'
import chart from './chart.png';


function Dashboard() {
	const [count, setCount] = useState(0);
	const [year, setYear] = useState(2023);
	const [location, setLocation] = useState([50.17272365327966, -104.04759247548621]);
	const [nvdi, setNvdi] = useState()


	// const data = [];
	// get_data(year, location).then(data => { console.log(data.ndvi); console.log(data.dates); setNvdi((nvdi) => { data.date, data.ndvi }) });

	return (
		<div id='dashboard'>
			<div id='past'>
				<div id="map-container">
					<iframe src='https://bloomwatch-nasasapceapps.projects.earthengine.app/view/car-with-agri-plots' title='Google Earth Engine Map'></iframe>
				</div>
				<div className='graph'>
					<Chart data={nvdi} />
				</div>
			</div>
			<div id='future'>
				<form action="">
					<select name="years" id="years">
						<option value="2023">2020</option>
						<option value="2023">2021</option>
						<option value="2023">2022</option>
						<option value="2023" selected="selected">2023</option>
						<option value="2024">2024</option>
						<option value="2025">2025</option>
					</select>
					<select name="location" id="location">
						<option value="-104.04759247548621, 50.17272365327966">Regina, Saskatchewan</option>
						<option value="0, 0">Calgary, Alberta</option>
						<option value="0, 0">Winnipeg, Manitoba</option>
					</select>
					<input type="submit" value="Submit" />
				</form>
				<div className='card'>
					<div className='card_content'>
						<ul>
							<h3>Current readings:</h3>
							<li>Temperature: 7.321 C</li>
							<li>Soil temp: 9.825 C</li>
							<li>Surface pressure: 96811 Pa</li>
							<li>NDVI: 0.137</li>
							<li>Total evaporation: -0.0023870 m</li>
							<li>Total precipitation: 1.246942 m</li>
						</ul>

					</div>
				</div>
				<div className='card'>
					<div className='card_content'><img src={chart} alt="Chart" /></div>
				</div>
			</div>
		</div>
	)
}

// Get data from the server
// Return promise
async function get_data(year, location) {
	const server_endpoint = import.meta.env.VITE_SERVER;

	try {
		// Post number of planets and receive list of n planets
		const response = await fetch(server_endpoint + "/getData", {
			method: "POST",
			body: JSON.stringify({
				"latitude": location[0],
				"longitude": location[1],
				"year": year,
			}),
			headers: {
				"Content-type": "application/json"
			}
		});

		if (!response.ok) {
			throw new Error(`Response status: ${response.status}`);
		}

		const result = await response.json();
		console.log(result);

		return result;

	} catch (error) {
		console.error(error.message);
	}
}

export default Dashboard
