import { useState } from "react";
import http from "../api/http";
import { useNavigate, Link } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");

    try {
      const res = await http.post("/api/login", { username, password });
      if (res.data.code === 200) {
        localStorage.setItem("token", res.data.token);
        setMsg("登录成功，正在跳转...");
        navigate("/dashboard");
      } else {
        setMsg(res.data.msg || "登录失败");
      }
    } catch (err) {
      console.error(err);
      setMsg(err.response?.data?.msg || "服务器错误");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>数据可视化平台 - 登录</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>用户名：</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="输入用户名"
          />
        </div>
        <div>
          <label>密码：</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="输入密码"
          />
        </div>
        <button type="submit" style={{ marginTop: 10 }}>登录</button>
      </form>
      {msg && <p style={{ color: "red" }}>{msg}</p>}
      <p>
        没有账号？<Link to="/register">去注册</Link>
      </p>
    </div>
  );
}

export default Login;
