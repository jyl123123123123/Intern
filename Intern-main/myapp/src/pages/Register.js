import { useState } from "react";
import http from "../api/http";
import { useNavigate, Link } from "react-router-dom";

function Register() {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirmPassword: "",
  });
  const [msg, setMsg] = useState("");
  const navigate = useNavigate();

  const handleChange = (key, value) => {
    setForm({ ...form, [key]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMsg("");

    if (form.password !== form.confirmPassword) {
      setMsg("两次输入的密码不一致");
      return;
    }

    try {
      const res = await http.post("/api/register", {
        username: form.username,
        email: form.email,
        password: form.password,
      });
      if (res.data.code === 200) {
        setMsg("注册成功，正在跳转到登录页");
        setTimeout(() => navigate("/login"), 800);
      } else {
        setMsg(res.data.msg || "注册失败");
      }
    } catch (err) {
      console.error(err);
      setMsg(err.response?.data?.msg || "服务器错误");
    }
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>数据可视化平台 - 注册</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>用户名：</label>
          <input
            value={form.username}
            onChange={(e) => handleChange("username", e.target.value)}
          />
        </div>
        <div>
          <label>邮箱：</label>
          <input
            type="email"
            value={form.email}
            onChange={(e) => handleChange("email", e.target.value)}
          />
        </div>
        <div>
          <label>密码：</label>
          <input
            type="password"
            value={form.password}
            onChange={(e) => handleChange("password", e.target.value)}
          />
        </div>
        <div>
          <label>确认密码：</label>
          <input
            type="password"
            value={form.confirmPassword}
            onChange={(e) => handleChange("confirmPassword", e.target.value)}
          />
        </div>
        <button type="submit" style={{ marginTop: 10 }}>注册</button>
      </form>
      {msg && <p style={{ color: "red" }}>{msg}</p>}
      <p>
        已有账号？<Link to="/login">去登录</Link>
      </p>
    </div>
  );
}

export default Register;
