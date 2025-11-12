import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function PostCreate() {
  const [post_title, setTitle] = useState('')
  const [post_content, setContent] = useState('')
  const navigate = useNavigate()

  const handleSubmit = async (e) => {
    e.preventDefault()
    const res = await fetch('/api/post_create', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ post_title, post_content }),
    })
    if (res.ok) {
      alert('게시글 작성 완료!')
      navigate('/posts')
    } else {
      alert('게시글 작성 실패')
    }
  }

  return (
    <div className="max-w-2xl mx-auto mt-10 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4 text-center">새 글 작성</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <input type="text" placeholder="제목" value={post_title} onChange={(e) => setTitle(e.target.value)} className="w-full border px-3 py-2 rounded" />
        <textarea placeholder="내용" value={post_content} onChange={(e) => setContent(e.target.value)} className="w-full border px-3 py-2 h-40 rounded"></textarea>
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">등록</button>
      </form>
    </div>
  )
}
