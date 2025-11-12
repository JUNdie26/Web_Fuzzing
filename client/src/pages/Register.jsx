import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Register() {
  const [user_id, setUserId] = useState('')
  const [user_password, setPassword] = useState('')
  const [user_name, setName] = useState('')
  const navigate = useNavigate()

  const handleRegister = async (e) => {
    e.preventDefault()
    const res = await fetch('/api/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id, user_password, user_name }),
    })
    if (res.ok) {
      alert('회원가입 성공!')
      navigate('/auth/login')
    } else {
      alert('Registration failed — maybe ID already exists.')
    }
  }

  return (
    <div className="max-w-md mx-auto mt-16 bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4 text-center">회원가입</h2>
      <form onSubmit={handleRegister} className="space-y-4">
        <input type="text" placeholder="아이디" value={user_id} onChange={(e) => setUserId(e.target.value)} className="w-full border px-3 py-2 rounded" />
        <input type="password" placeholder="비밀번호" value={user_password} onChange={(e) => setPassword(e.target.value)} className="w-full border px-3 py-2 rounded" />
        <input type="text" placeholder="이름" value={user_name} onChange={(e) => setName(e.target.value)} className="w-full border px-3 py-2 rounded" />
        <button type="submit" className="w-full bg-green-600 text-white py-2 rounded">회원가입</button>
      </form>
    </div>
  )
}
