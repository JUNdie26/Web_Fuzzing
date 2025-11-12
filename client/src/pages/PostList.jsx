import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'

export default function PostList() {
  const [posts, setPosts] = useState([])

  useEffect(() => {
    fetch('/api/posts')
      .then(res => res.json())
      .then(data => setPosts(data))
      .catch(() => alert('게시글 불러오기 실패'))
  }, [])

  return (
    <div className="max-w-3xl mx-auto mt-10">
      <h2 className="text-2xl font-bold mb-6">게시글 목록</h2>
      <ul className="space-y-4">
        {posts.map(post => (
          <li key={post.post_uuid} className="p-4 bg-white rounded shadow">
            <Link to={`/posts/${post.post_uuid}`} className="text-xl font-semibold text-blue-700 hover:underline">
              {post.post_title}
            </Link>
            <p className="text-gray-600 mt-1">{post.post_content.slice(0, 100)}...</p>
          </li>
        ))}
      </ul>
    </div>
  )
}
