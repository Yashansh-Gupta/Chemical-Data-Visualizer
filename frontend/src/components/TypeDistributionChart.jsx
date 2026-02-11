import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend,
} from "chart.js";
import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

const TypeDistributionChart = ({ data }) => {
  const labels = Object.keys(data);
  const values = Object.values(data);

  return (
    <Bar
      data={{
        labels,
        datasets: [
          {
            label: "Equipment Count",
            data: values,
            backgroundColor: "#5c77fd",
            borderColor: "#618cf7",
            borderWidth: 1,
          },
        ],
      
      }}
      options={{
          responsive: true,
          plugins: {
            legend: {
              labels: {
                color: "#000000",
              },
            },
          },
          scales: {
            x: {
              ticks: {
                color: "#000000",
              },
              grid: {
                color: "rgba(2, 1, 1, 0.1)",
              },
            },
            y: {
              ticks: {
                color: "#000000",
              },
              grid: {
                color: "rgba(255,255,255,0.1)",
              },
            },
          },
        }}

    />
  );
};

export default TypeDistributionChart;
