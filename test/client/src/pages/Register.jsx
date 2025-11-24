import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function Register() {
  const [user_id, setId] = useState("");
  const [password, setPw] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    try {
      const res = await axios.post("/auth/register", { user_id, password });
      if (res.data.ok) {
        alert("회원가입 성공!");
        navigate("/");
      }
    } catch (e) {
      alert("회원가입 실패!");
    }
  };

  return (
    <div className="container">
      <h2>회원가입</h2>

      <input placeholder="아이디" onChange={(e)=>setId(e.target.value)} />
      <input type="password" placeholder="비밀번호" onChange={(e)=>setPw(e.target.value)} />

      <button onClick={submit}>회원가입</button>
    </div>
  );
}

export default Register;
