import React, { useEffect, useState, useCallback } from "react";
import axios from "../api/axios";
import { useParams } from "react-router-dom";

function PostDetail() {
  const { id } = useParams();
  const [post, setPost] = useState(null);

  const loadPost = useCallback(async () => {
    const res = await axios.get(`/post/api/post/${id}`);
    setPost(res.data.post);
  }, [id]);

  useEffect(() => {
    loadPost();
  }, [loadPost]);

  if (!post) return <div className="container">Loading...</div>;

  return (
    <div className="container">
      <h2>{post.title}</h2>
      <p style={{ whiteSpace: "pre-wrap" }}>{post.content}</p>
    </div>
  );
}

export default PostDetail;
