import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import PostList from "./pages/PostList";
import Write from "./pages/Write";
import PostDetail from "./pages/PostDetail";
import NavBar from "./NavBar";

import "./App.css";

function App() {
  return (
    <Router>
      <NavBar />
      <div>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* 게시글 목록 */}
          <Route path="/posts" element={<PostList />} />

          {/* 게시글 상세 페이지 */}
          <Route path="/posts/:id" element={<PostDetail />} />

          {/* 글쓰기 페이지 */}
          <Route path="/write" element={<Write />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
