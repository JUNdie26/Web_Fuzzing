import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import Header from './components/Header'
import Login from './pages/Login'
import Register from './pages/Register'
import PostList from './pages/PostList'
import PostDetail from './pages/PostDetail'
import PostCreate from './pages/PostCreate'

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      <Header />
      <main className="p-6">
        <Routes>
          <Route path="/" element={<Navigate to="/posts" />} />
          <Route path="/auth/login" element={<Login />} />
          <Route path="/auth/register" element={<Register />} />
          <Route path="/posts" element={<PostList />} />
          <Route path="/posts/:post_uuid" element={<PostDetail />} />
          <Route path="/post_create" element={<PostCreate />} />
        </Routes>
      </main>
    </div>
  )
}
