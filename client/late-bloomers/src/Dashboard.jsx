import { useState } from 'react'
import Chart from './Chart.jsx'

function Dashboard() {
	const [count, setCount] = useState(0);

	return (
		<div id='dashboard'>
			<div id='past'>
				<div id="map-container">
					<iframe src='https://bloomwatch-nasasapceapps.projects.earthengine.app/view/late-bloomers' title='Google Earth Engine Map'></iframe>
				</div>
				<div className='graph'>
					<Chart />
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
