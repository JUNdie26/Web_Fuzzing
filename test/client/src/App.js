import React, { useState } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import PostList from "./pages/PostList";
import Write from "./pages/Write";
import PostDetail from "./pages/PostDetail";
import NavBar from "./NavBar";

import axios from "./api/axios";
import "./App.css";

function App() {
  const [user, setUser] = useState(null);
  const isLoggedIn = !!user;

  const handleLogout = async () => {
    try {
      await axios.post("/auth/logout");
    } catch (e) {
      // 서버 에러 나도 프론트 상태는 초기화
    }
    setUser(null);
  };

  return (
    <Router>
      <NavBar isLoggedIn={isLoggedIn} onLogout={handleLogout} />
      <div>
        <Routes>
          {/* 기본 루트 */}
          <Route
            path="/"
            element={
              isLoggedIn ? (
                <Navigate to="/posts" />
              ) : (
                <Login setUser={setUser} />
              )
            }
          />

          {/* 로그인 */}
          <Route
            path="/login"
            element={
              isLoggedIn ? (
                <Navigate to="/posts" />
              ) : (
                <Login setUser={setUser} />
              )
            }
          />

          {/* 회원가입 */}
          <Route
            path="/register"
            element={isLoggedIn ? <Navigate to="/posts" /> : <Register />}
          />

          {/* 게시글 목록 */}
          <Route
            path="/posts"
            element={isLoggedIn ? <PostList /> : <Navigate to="/login" />}
          />

          {/* 게시글 상세 페이지 */}
          <Route
            path="/posts/:id"
            element={isLoggedIn ? <PostDetail /> : <Navigate to="/login" />}
          />

          {/* 글쓰기 페이지 */}
          <Route
            path="/write"
            element={isLoggedIn ? <Write /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
