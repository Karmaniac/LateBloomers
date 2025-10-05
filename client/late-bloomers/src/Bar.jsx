import { AgCharts } from 'ag-charts-react';
import { useState } from 'react'

const flower = ({ x, y, path, size }) => {
	const r = size / 4;
	const yCoord = y + r / 2;
	path.clear();
	path.arc(x + r, yCoord - r, r, 0, 2 * Math.PI);
	path.closePath();
	path.arc(x - r, yCoord - r, r, 0, 2 * Math.PI);
	path.closePath();
	path.arc(x + r, yCoord + r, r, 0, 2 * Math.PI);
	path.closePath();
	path.arc(x - r, yCoord + r, r, 0, 2 * Math.PI);
	path.closePath();
	path.arc(x, yCoord, r, 0, 2 * Math.PI);
	path.closePath();
};

function Bar() {
	const customItems = ["Jun", "Jul", "Aug", "Sep"];

	const [chartOptions, setChartOptions] = useState({
		// Data: Data to be displayed in the chart
		data: [
			{ month: 'Jan', avgTemp: 2.3, iceCreamSales: 162000 },
			{ month: 'Feb', avgTemp: 2.3, iceCreamSales: 162000 },
			{ month: 'Mar', avgTemp: 6.3, iceCreamSales: 302000 },
			{ month: 'Apr', avgTemp: 6.3, iceCreamSales: 302000 },
			{ month: 'May', avgTemp: 16.2, iceCreamSales: 800000 },
			{ month: 'Jun', avgTemp: 16.2, iceCreamSales: 800000 },
			{ month: 'Jul', avgTemp: 22.8, iceCreamSales: 1254000 },
			{ month: 'Aug', avgTemp: 16.2, iceCreamSales: 800000 },
			{ month: 'Sep', avgTemp: 14.5, iceCreamSales: 950000 },
			{ month: 'Oct', avgTemp: 16.2, iceCreamSales: 800000 },
			{ month: 'Nov', avgTemp: 8.9, iceCreamSales: 200000 },
			{ month: 'Dec', avgTemp: 8.9, iceCreamSales: 200000 },
		],
		// Series: Defines which chart type and data to use
		series: [{
			type: "bar",
			xKey: "month",
			yKey: "avgTemp",
			yName: "Temperature",
			fill: "green",
			stroke: "green",
		}],
		legend: {
			enabled: true,
			position: "top",
			toggleSeries: false,
		},
		axes: [
			{
				position: "bottom",
				type: "category",
				title: {
					text: "Month",
				},
				crossLines: [
					{
						type: "range",
						range: ["Jun", "Sep"],
					},
				],
			},
			{
				position: "left",
				type: "number",
				title: {
					text: "Temperature (°C)",
				},
				// crossLines: [
				// {
				// type: "line",
				// value: 11,
				// },
				// ],
			},
		],
	});

	return (
		<AgCharts options={chartOptions} />
	);
}


export default Bar
