import React, { useEffect, useState } from "react";
import axios from "../api/axios";
import { useNavigate } from "react-router-dom";

function PostList() {
  const [posts, setPosts] = useState([]);
  const navigate = useNavigate();

  const loadPosts = async () => {
    const res = await axios.get("/post/api/all");
    setPosts(res.data.posts);
  };

  useEffect(() => {
    loadPosts();
  }, []);

  return (
    <div className="container">
      <h2>게시글 목록</h2>

      {posts.map((p) => (
        <div className="post-card" key={p.id} onClick={() => navigate(`/posts/${p.id}`)}>
          <h3>{p.title}</h3>
          <p style={{ opacity: 0.7 }}>{p.created_at}</p>
        </div>
      ))}
    </div>
  );
}

export default PostList;
