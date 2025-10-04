import { useState } from 'react'

function Dashboard() {
	const [count, setCount] = useState(0)

	return (
		<div id='dashboard'>
			<div id='past'>
				<h1>Past</h1>
				<div id='map'>
					MAP HERE
				</div>
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
