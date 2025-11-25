// client/src/pages/Write.jsx
import React, { useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function Write({ user }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!title || !content) {
      alert("제목과 내용을 모두 입력하세요.");
      return;
    }

    console.log("Write user =", user);
    const user_uuid = user?.user_uuid;   // ★ 여기

    if (!user_uuid) {
      alert("로그인 정보가 없습니다. 다시 로그인 해 주세요.");
      return;
    }

    try {
      const res = await axios.post("/post/api/post_create", {
        title,
        content,
        user_uuid,  // ★ 이 이름으로 보냄
      });

      console.log("post_create response:", res.data);
      alert("게시글이 등록되었습니다.");
      navigate("/post");
    } catch (err) {
      console.error("post_create error:", err.response?.data || err.message);

      const data = err.response?.data;
      const msg =
        data?.error ||
        data?.detail ||
        "게시글 등록 중 오류가 발생했습니다.";
      alert(msg);
    }
  };

  return (
    <div className="container">
      <h2>글쓰기</h2>

      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "1rem" }}>
          <input
            type="text"
            placeholder="제목"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            style={{ width: "100%" }}
          />
        </div>

        <div style={{ marginBottom: "1rem" }}>
          <textarea
            placeholder="내용"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            rows={8}
            style={{ width: "100%" }}
          />
        </div>

        <button type="submit">등록</button>
        <button
          type="button"
          onClick={() => navigate("/post")}
          style={{ marginLeft: "0.5rem" }}
        >
          취소
        </button>
      </form>
    </div>
  );
}

export default Write;
