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

function Chart({ data }) {
	const customItems = ["2023-06-28", "2023-06-30", "2023-07-03", "2023-07-05", "2023-07-08", "2023-07-10", "2023-07-10", "2023-07-18", "2023-07-23", "2023-07-25", "2023-07-30"];
	// console.log("hi")
	// console.log(data);
	// if (data != undefined) {
	// setChartOptions((chartOptions.data) => data)
	// };

	const [chartOptions, setChartOptions] = useState({

		// Data: Data to be displayed in the chart
		data:
			[
				{ nvdi: 0.17878426698450536, month: "2023-05-01" },
				{ nvdi: 0.17052881758764113, month: "2023-05-04" },
				{ nvdi: 0.08307045215562565, month: "2023-05-06" },
				{ nvdi: 0.15404168784951702, month: "2023-05-14" },
				{ nvdi: 0.15463917525773196, month: "2023-05-16" },
				{ nvdi: 0.16363636363636364, month: "2023-05-19" },
				{ nvdi: 0.24566088117489987, month: "2023-06-03" },
				{ nvdi: 0.30919623461259954, month: "2023-06-05" },
				{ nvdi: 0.33123425692695213, month: "2023-06-08" },
				{ nvdi: 0.394524959742351, month: "2023-06-10" },
				{ nvdi: 0.4219590958019376, month: "2023-06-13" },
				{ nvdi: 0.49508196721311476, month: "2023-06-15" },
				{ nvdi: 0.7479161404395049, month: "2023-06-28" },
				{ nvdi: 0.7478060046189376, month: "2023-06-30" },
				{ nvdi: 0.6923842707814833, month: "2023-07-03" },
				{ nvdi: 0.754601226993865, month: "2023-07-05" },
				{ nvdi: 0.776084407971864, month: "2023-07-08" },
				{ nvdi: 0.6426764773511152, month: "2023-07-10" },
				{ nvdi: 0.7565485362095532, month: "2023-07-18" },
				{ nvdi: 0.7342657342657343, month: "2023-07-23" },
				{ nvdi: 0.6665046183762762, month: "2023-07-25" },
				{ nvdi: 0.5659490225191784, month: "2023-07-30" },
				{ nvdi: 0.42501481920569056, month: "2023-08-02" },
				{ nvdi: 0.28688879273041973, month: "2023-08-07" },
				{ nvdi: 0.19030792529025745, month: "2023-08-24" },
				{ nvdi: 0.20112676056338027, month: "2023-08-27" },
				{ nvdi: 0.13518273888154997, month: "2023-08-29" },
				{ nvdi: 0.1274542429284526, month: "2023-09-06" },
				{ nvdi: 0.13614103819784526, month: "2023-09-11" },
				{ nvdi: 0.13515655965120887, month: "2023-09-16" },
				{ nvdi: 0.14650698602794412, month: "2023-09-18" },
				{ nvdi: 0.12912912912912913, month: "2023-09-26" },
				{ nvdi: 0.13636363636363635, month: "2023-09-28" },
				{ nvdi: 0.1332398316970547, month: "2023-10-06" },
				{ nvdi: 0.12841670964414648, month: "2023-10-08" },
				{ nvdi: 0.14271047227926079, month: "2023-10-11" },
				{ nvdi: 0.13675213675213677, month: "2023-10-16" },
				{ nvdi: 0.13226452905811623, month: "2023-10-21" }
			],
		// Series: Defines which chart type and data to use
		series: [{
			type: "line",
			xKey: "month",
			yKey: "nvdi",
			yName: "Spring Wheat - Regina, Saskatchewan",
			marker: {
				shape: "diamond",
				size: 24,
				fill: "green",
				itemStyler: ({ datum, fill, highlighted, shape }) => {
					return {
						fill: customItems.includes(datum.month)
							? highlighted
								? "yellow"
								: "red"
							: fill,
						shape: customItems.includes(datum.month)
							? flower : "diamond",
					};
				},
			},
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
					text: "NVDI",
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


export default Chart
