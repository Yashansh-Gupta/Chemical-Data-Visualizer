import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import TypeDistributionChart from "../components/TypeDistributionChart";
import { useAuth } from "../auth/AuthContext";



const Dashboard = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();
  const { logout } = useAuth();


  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await api.get("/api/history/");
        setHistory(res.data);
      } catch (err) {
        console.error("DASHBOARD ERROR:", err);

        if (err.response?.status === 401) {
          // token invalid or expired
          localStorage.removeItem("access");
          localStorage.removeItem("refresh");
          navigate("/");
          return;
        }
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (loading) {
    return <div>Loading dashboard...</div>;
  }

  return (
    <div>
      <h2>Dashboard</h2>

      <button
        onClick={() => {
          logout();
          navigate("/");
        }}
        style={{
          marginBottom: "20px",
          padding: "8px 14px",
          cursor: "pointer"
        }}
      >
        Logout
      </button>


      {history.length === 0 ? (
        <p>No datasets yet</p>
      ) : (
        history.map((item, idx) => (
          <div key={idx} style={{ marginBottom: "20px" }}>
            <h4>{item.name}</h4>

            <ul>
              <li>Total equipment: {item.summary.total_equipment}</li>
              <li>Avg flowrate: {item.summary.avg_flowrate.toFixed(2)}</li>
              <li>Avg pressure: {item.summary.avg_pressure.toFixed(2)}</li>
              <li>Avg temperature: {item.summary.avg_temperature.toFixed(2)}</li>
              
              <button
                onClick={() =>
                  window.open(
                    `http://127.0.0.1:8000/api/report/${item.id}/`,
                    "_blank"
                  )
                }
              >
                Download PDF
              </button>


              <h4>Equipment Type Distribution</h4>

              <div style={{ width: "80%", marginTop: "20px" }}>
                <TypeDistributionChart data={item.summary.type_distribution} />
              </div>


            </ul>
          </div>

        ))
      )}
    </div>
  );
};

export default Dashboard;
