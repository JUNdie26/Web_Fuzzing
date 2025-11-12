import React, { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

export default function PostDetail() {
  const { post_uuid } = useParams()
  const [post, setPost] = useState(null)
  const [comments, setComments] = useState([])

  useEffect(() => {
    fetch(`/api/posts/${post_uuid}`)
      .then(res => res.json())
      .then(setPost)
    fetch(`/api/posts/${post_uuid}/comment`)
      .then(res => res.json())
      .then(setComments)
  }, [post_uuid])

  if (!post) return <p className="text-center mt-10">게시글을 불러오는 중...</p>

  return (
    <div className="max-w-3xl mx-auto mt-10 bg-white p-6 rounded shadow">
      <h2 className="text-2xl font-bold mb-2">{post.post_title}</h2>
      <p className="text-gray-700 mb-4">{post.post_content}</p>

      <h3 className="text-lg font-semibold mt-6 mb-2">댓글</h3>
      <ul className="space-y-3">
        {comments.map(c => (
          <li key={c.comment_uuid} className="border-b pb-2">
            <p>{c.comment_content}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}
