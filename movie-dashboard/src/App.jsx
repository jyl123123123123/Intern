// src/App.jsx
import React, { useEffect, useState } from "react";
import ReactECharts from "echarts-for-react";
import axios from "axios";

function App() {
  const [option, setOption] = useState(null);
  const [raw, setRaw] = useState(null);
  const [error, setError] = useState(null);
  const [currentChart, setCurrentChart] = useState("rating_distribution");

  
  const loadChart = (chartType) => {
    setError(null);
    setOption(null);
    setRaw(null);
    setCurrentChart(chartType);

    axios
      .get(`http://127.0.0.1:5000/api/chart/${chartType}`)
      .then((res) => {
        console.log("后端返回的数据:", res.data);
        setRaw(res.data);
        setOption(res.data);
      })
      .catch((err) => {
        console.error("请求出错:", err);
        setError(err.message || "未知错误");
      });
  };

  
  useEffect(() => {
    loadChart("rating_distribution");
  }, []);

  return (
    <div style={{ padding: 24 }}>
      <h1>豆瓣电影图表测试页</h1>

      {/*切换图表的按钮区域*/}
      <div style={{ marginBottom: 16 }}>
        <button
          onClick={() => loadChart("rating_distribution")}
          style={{
            marginRight: 8,
            padding: "6px 12px",
            background:
              currentChart === "rating_distribution" ? "#1677ff" : "#f0f0f0",
            color: currentChart === "rating_distribution" ? "#fff" : "#000",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          评分分布
        </button>

        <button
          onClick={() => loadChart("movies_per_year")}
          style={{
            padding: "6px 12px",
            background:
              currentChart === "movies_per_year" ? "#1677ff" : "#f0f0f0",
            color: currentChart === "movies_per_year" ? "#fff" : "#000",
            border: "none",
            borderRadius: 4,
            cursor: "pointer",
          }}
        >
          年份统计
        </button>
      </div>

      {/*报错*/}
      {error && (
        <div style={{ color: "red", marginBottom: 16 }}>
          请求出错：{error}
        </div>
      )}

      {/*后端返回的原始JSON*/}
      <div style={{ marginBottom: 16 }}>
        <h3>后端返回的原始 JSON：</h3>
        <pre
          style={{
            background: "#f5f5f5",
            padding: 12,
            maxHeight: 200,
            overflow: "auto",
          }}
        >
          {raw ? JSON.stringify(raw, null, 2) : "还没有数据"}
        </pre>
      </div>

      {/*图表区域*/}
      <div style={{ border: "1px solid #ddd", padding: 12 }}>
        <h3>图表区域：</h3>
        {option ? (
          <ReactECharts option={option} style={{ height: 400 }} />
        ) : (
          <div>图表还在加载中...</div>
        )}
      </div>
    </div>
  );
}

export default App;
