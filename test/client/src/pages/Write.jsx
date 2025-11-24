import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function Write() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    const res = await axios.post("/post/api/post_create", { title, content });
    if (res.data.success) {
      alert("작성 완료!");
      navigate("/posts");
    }
  };

  return (
    <div className="container">
      <h2>게시글 작성</h2>

      <input placeholder="제목" onChange={(e)=>setTitle(e.target.value)} />
      <textarea rows="10" placeholder="내용" onChange={(e)=>setContent(e.target.value)} />

      <button onClick={submit}>작성하기</button>
    </div>
  );
}

export default Write;
