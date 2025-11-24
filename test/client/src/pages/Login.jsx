import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [user_id, setId] = useState("");
  const [password, setPw] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    try {
      const res = await axios.post("/auth/login", { user_id, password });
      if (res.data.ok) {
        alert("로그인 성공!");
        navigate("/posts");
      }
    } catch (e) {
      alert("로그인 실패!");
    }
  };

  return (
    <div className="container">
      <h2>로그인</h2>

      <input placeholder="아이디" onChange={(e)=>setId(e.target.value)} />
      <input type="password" placeholder="비밀번호" onChange={(e)=>setPw(e.target.value)} />

      <button onClick={submit}>로그인</button>

      <button onClick={()=>navigate("/register")} style={{background:"#3a4b6b"}}>
        회원가입
      </button>
    </div>
  );
}

export default Login;
