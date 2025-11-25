import React from "react";
import { Link } from "react-router-dom";
import "./App.css";

function NavBar({ isLoggedIn, onLogout }) {
  return (
    <div className="navbar">
      {isLoggedIn ? (
        <>
          <Link to="/posts">게시글 목록</Link>
          <Link to="/write">글쓰기</Link>
          <button
            onClick={onLogout}
            className="navbar-button"
          >
            로그아웃
          </button>
        </>
      ) : (
        <>
          <Link to="/login">로그인</Link>
          <Link to="/register">회원가입</Link>
        </>
      )}
    </div>
  );
}

export default NavBar;
