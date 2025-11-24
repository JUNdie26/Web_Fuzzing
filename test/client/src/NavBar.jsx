import React from "react";
import { Link } from "react-router-dom";
import "./App.css";

function NavBar() {
  return (
    <div className="navbar">
      <Link to="/posts">게시글 목록</Link>
      <Link to="/write">글쓰기</Link>
      <Link to="/">로그아웃</Link>
    </div>
  );
}

export default NavBar;
