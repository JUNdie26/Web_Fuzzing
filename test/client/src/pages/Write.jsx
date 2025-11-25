// src/pages/Write.jsx
import React, { useState } from "react";
import axios from "../api/axios";              // ❗ 반드시 이 경로
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

    // TODO: 실제 로그인 유저 구조에 맞게 수정
    const user_id = user?.user_uuid || user?.id || 1;

    try {
      await axios.post("/post/api/post_create", {
        title,
        content,
        user_id,
      });

      alert("게시글이 등록되었습니다.");
      navigate("/post");          // 작성 후 목록으로
    } catch (err) {
      console.error(err);
      alert("게시글 등록 중 오류가 발생했습니다.");
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
