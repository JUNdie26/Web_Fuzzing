// client/src/App.js
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
      console.error(e);
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
                <Navigate to="/post" />
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
                <Navigate to="/post" />
              ) : (
                <Login setUser={setUser} />
              )
            }
          />

          {/* 회원가입 */}
          <Route
            path="/register"
            element={isLoggedIn ? <Navigate to="/post" /> : <Register />}
          />

          {/* 게시글 목록 */}
          <Route
            path="/post"
            element={isLoggedIn ? <PostList /> : <Navigate to="/login" />}
          />

          {/* 게시글 상세 */}
          <Route
            path="/post/:id"
            element={isLoggedIn ? <PostDetail /> : <Navigate to="/login" />}
          />

          {/* 글쓰기 */}
          <Route
            path="/post/create"
            element={isLoggedIn ? <Write user={user} /> : <Navigate to="/login" />}
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
