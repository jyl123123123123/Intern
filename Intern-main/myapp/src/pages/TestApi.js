// src/pages/TestApi.js
import React, { useState } from "react";
import axios from "axios";

function TestApi() {
  //三个输入框
  const [getInput, setGetInput] = useState("");      // GET的输入框
  const [postBodyInput, setPostBodyInput] = useState("");  // POST body
  const [postParamInput, setPostParamInput] = useState(""); // POST URL 参数

  //显示后端返回的结果
  const [getResult, setGetResult] = useState("");
  const [postResult, setPostResult] = useState("");

  const handleSendGet = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/参数", {
        params: { value: getInput },
      });
      setGetResult(JSON.stringify(res.data));
    } catch (err) {
      console.error(err);
      setGetResult("GET请求出错");
    }
  };

  const handleSendPost = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/参数post",
        { bodyValue: postBodyInput },
        { params: { paramValue: postParamInput } }
      );
      setPostResult(JSON.stringify(res.data));
    } catch (err) {
      console.error(err);
      setPostResult("POST请求出错");
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "sans-serif" }}>
      <h2>React + Flask 前后端联调</h2>

      {/* GET */}
      <div style={{ marginBottom: "30px" }}>
        <h3>1. GET 请求示例</h3>
        <input
          style={{ width: "300px", marginRight: "10px" }}
          placeholder="在这里输入 GET 的参数(value)"
          value={getInput}
          onChange={(e) => setGetInput(e.target.value)}
        />
        <button onClick={handleSendGet}>发送 GET</button>

        <div style={{ marginTop: "10px" }}>
          <span>后端返回：</span>
          <code>{getResult}</code>
        </div>
      </div>

      {/* POST */}
      <div>
        <h3>2. POST 请求示例</h3>
        <div style={{ marginBottom: "10px" }}>
          <div>body(JSON 里的 bodyValue):</div>
          <input
            style={{ width: "300px" }}
            placeholder="这里是 POST body(bodyValue)"
            value={postBodyInput}
            onChange={(e) => setPostBodyInput(e.target.value)}
          />
        </div>

        <div style={{ marginBottom: "10px" }}>
          <div>URL 参数(paramValue):</div>
          <input
            style={{ width: "300px" }}
            placeholder="这里是 URL 参数(paramValue)"
            value={postParamInput}
            onChange={(e) => setPostParamInput(e.target.value)}
          />
        </div>

        <button onClick={handleSendPost}>发送 POST</button>

        <div style={{ marginTop: "10px" }}>
          <span>后端返回：</span>
          <code>{postResult}</code>
        </div>
      </div>
    </div>
  );
}

export default TestApi;
