import React from 'react'
import { Link } from 'react-router-dom'

export default function Header() {
  return (
    <header className="bg-gray-800 text-white py-4 px-6 flex justify-between items-center">
      <h1 className="text-xl font-bold">
        <Link to="/posts">퍼지..퍼지징...펑 블로그</Link>
      </h1>
      <nav className="space-x-4">
        <Link to="/auth/login" className="hover:underline">로그인</Link>
        <Link to="/auth/register" className="hover:underline">회원가입</Link>
        <Link to="/post_create" className="hover:underline">글쓰기</Link>
      </nav>
    </header>
  )
}
