import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function PostList() {
  const [posts, setPosts] = useState([]);
  const [page, setPage] = useState(1);       // 페이지 번호
  const [search, setSearch] = useState("");  // 검색어
  const navigate = useNavigate();

  const loadPosts = async () => {
    try {
      const res = await axios.get("/post/api/all", {
        params: { page, search },
      });

      setPosts(res.data.posts || []);
    } catch (e) {
      console.error(e);
      alert("게시글 불러오기 실패");
    }
  };

  useEffect(() => {
    loadPosts();
  }, [page, search]);

  return (
    <div className="container">
      <h2>게시글 목록</h2>

      {/* 검색 */}
      <div style={{ marginBottom: "1rem" }}>
        <input
          placeholder="검색어"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {/* 글쓰기 버튼 */}
      <button onClick={() => navigate("/post/create")}>글쓰기</button>

      {/* 게시글 리스트 */}
      <ul>
        {posts.map((p) => (
          <li key={p.id} style={{ marginBottom: "1rem" }}>
            <h3>{p.title}</h3>
            <p>{p.content}</p>
            <small>{p.created_at}</small>
          </li>
        ))}
      </ul>

      {/* 페이지 네비게이션 */}
      <div style={{ marginTop: "1rem" }}>
        <button
          onClick={() => setPage((prev) => Math.max(1, prev - 1))}
          disabled={page <= 1}
        >
          이전
        </button>
        <span style={{ margin: "0 8px" }}>페이지 {page}</span>
        <button onClick={() => setPage((prev) => prev + 1)}>다음</button>
      </div>
    </div>
  );
}

export default PostList;
