import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function Login({ setUser }) {
  const [user_id, setId] = useState("");
  const [password, setPw] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    try {
      const res = await axios.post("/auth/login", { user_id, password });

      if (res.data.ok) {
        setUser && setUser(res.data.user);
        alert("로그인 성공");
        navigate("/post");
      } else {
        alert(res.data.error || "로그인 실패");
      }
    } catch (e) {
      const msg =
        e.response?.data?.error ||
        e.response?.data?.detail ||
        "로그인 중 오류가 발생했습니다.";
      alert(msg);
      console.error(e);
    }
  };

  return (
    <div className="container">
      <h2>로그인</h2>
      <input
        placeholder="아이디"
        value={user_id}
        onChange={(e) => setId(e.target.value)}
      />
      <input
        type="password"
        placeholder="비밀번호"
        value={password}
        onChange={(e) => setPw(e.target.value)}
      />
      <button onClick={submit}>로그인</button>
    </div>
  );
}

export default Login;
