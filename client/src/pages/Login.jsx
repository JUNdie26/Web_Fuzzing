import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [user_id, setUserId] = useState('')
  const [user_password, setPassword] = useState('')
  const navigate = useNavigate()

  const handleLogin = async (e) => {
    e.preventDefault()
    try {
      const res = await fetch('/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_id, user_password }),
      })
      if (res.ok) {
        alert('로그인 성공!')
        navigate('/posts')
      } else {
        alert('Login failed. Check credentials.')
      }
    } catch (err) {
      alert('서버 연결 실패: ' + err.message)
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4 text-center">로그인</h2>
      <form onSubmit={handleLogin} className="space-y-4">
        <input type="text" placeholder="아이디" value={user_id} onChange={(e) => setUserId(e.target.value)} className="w-full border px-3 py-2 rounded" />
        <input type="password" placeholder="비밀번호" value={user_password} onChange={(e) => setPassword(e.target.value)} className="w-full border px-3 py-2 rounded" />
        <button type="submit" className="w-full bg-blue-600 text-white py-2 rounded">로그인</button>
      </form>
    </div>
  )
}
