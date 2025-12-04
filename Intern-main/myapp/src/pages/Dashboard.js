import { useEffect, useState } from "react";
import http from "../api/http";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    http.get("/api/me")
      .then((res) => {
        if (res.data.code === 200) {
          setUser(res.data.user);
        } else {
          throw new Error("not login");
        }
      })
      .catch(() => {
        localStorage.removeItem("token");
        navigate("/login");
      });
  }, [navigate]);

  return (
    <div style={{ padding: 20 }}>
      <h2>数据可视化平台</h2>
      {user && <p>欢迎回来，{user.username}</p>}
      {/* 这里放你的图表组件，比如 RatingChart / MoviesPerYearChart */}
    </div>
  );
}

export default Dashboard;
