import React, { useEffect, useState } from "react";
import { BrowserRouter as Router, Routes, Route, Link, useNavigate, useParams } from "react-router-dom";

// Simple single-file React app for the blog frontend.
// Tailwind is used for styling (assume Tailwind is configured in the project).
// Default export a top-level component so the canvas preview can render.

/* ----------------------
   API helper
   ---------------------- */
const API = (() => {
  const base = ""; // if backend hosted under same origin, keep empty. otherwise set e.g. "http://localhost:5000"

  const getAuthHeader = () => {
    const token = localStorage.getItem("auth_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
  };

  return {
    login: async (user_id, user_password) => {
      const res = await fetch(`${base}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, user_password }),
        credentials: "include",
      });
      if (!res.ok) throw res;
      return res.json();
    },
    register: async (user_id, user_password, user_name) => {
      const res = await fetch(`${base}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id, user_password, user_name }),
      });
      if (!res.ok) throw res;
      return res.json();
    },
    fetchPosts: async () => {
      const res = await fetch(`${base}/api/posts`, { headers: getAuthHeader() });
      if (!res.ok) throw res;
      return res.json();
    },
    fetchPost: async (post_uuid) => {
      const res = await fetch(`${base}/api/posts/${post_uuid}`, { headers: getAuthHeader() });
      if (!res.ok) throw res;
      return res.json();
    },
    createPost: async (post_title, post_content) => {
      const res = await fetch(`${base}/api/post_create`, {
        method: "POST",
        headers: { ...getAuthHeader(), "Content-Type": "application/json" },
        body: JSON.stringify({ post_title, post_content }),
        credentials: "include",
      });
      if (!res.ok) throw res;
      return res.json();
    },
    fetchComments: async (post_uuid) => {
      const res = await fetch(`${base}/api/posts/${post_uuid}/comment`, { headers: getAuthHeader() });
      if (!res.ok) throw res;
      return res.json();
    },
    createComment: async (post_uuid, comment_content) => {
      const res = await fetch(`${base}/api/posts/${post_uuid}/comment`, {
        method: "POST",
        headers: { ...getAuthHeader(), "Content-Type": "application/json" },
        body: JSON.stringify({ comment_content }),
        credentials: "include",
      });
      if (!res.ok) throw res;
      return res.json();
    },
    fetchMe: async () => {
      const res = await fetch(`${base}/api/users/me`, { headers: getAuthHeader(), credentials: "include" });
      if (!res.ok) throw res;
      return res.json();
    },
    updateMe: async (data) => {
      const res = await fetch(`${base}/api/users/me`, {
        method: "PUT",
        headers: { ...getAuthHeader(), "Content-Type": "application/json" },
        body: JSON.stringify(data),
        credentials: "include",
      });
      if (!res.ok) throw res;
      return res.json();
    },
  };
})();

/* ----------------------
   Small UI primitives
   ---------------------- */
function Container({ children }) {
  return <div className="max-w-3xl mx-auto p-4">{children}</div>;
}

function Nav({ onLogout }) {
  const [me, setMe] = useState(null);

  useEffect(() => {
    API.fetchMe()
      .then((r) => setMe(r))
      .catch(() => setMe(null));
  }, []);

  return (
    <nav className="flex items-center justify-between py-4">
      <div className="flex items-center gap-4">
        <Link to="/" className="text-xl font-semibold">
          MyBlog
        </Link>
        <Link to="/post_create" className="text-sm">New Post</Link>
      </div>
      <div className="flex items-center gap-3">
        {me ? (
          <>
            <Link to="/users/me" className="text-sm">{me.user_name}</Link>
            <button className="text-sm underline" onClick={onLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/auth/login" className="text-sm">Login</Link>
            <Link to="/auth/register" className="text-sm">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

/* ----------------------
   Pages
   ---------------------- */

function Home() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    API.fetchPosts()
      .then((data) => setPosts(data))
      .catch((e) => setError("Failed to load posts"))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Container>
      <h1 className="text-2xl font-bold mb-4">Recent posts</h1>
      {loading && <p>Loading...</p>}
      {error && <p className="text-red-600">{error}</p>}
      <ul className="space-y-3">
        {posts.map((p) => (
          <li key={p.post_uuid} className="p-3 border rounded-md">
            <Link to={`/posts/${p.post_uuid}`} className="block">
              <h2 className="text-lg font-semibold">{p.post_title}</h2>
              <p className="text-sm text-gray-600">by {p.user_name ?? 'Unknown'} — {p.create_time}</p>
              <p className="mt-2 line-clamp-3">{p.post_content}</p>
            </Link>
          </li>
        ))}
        {posts.length === 0 && !loading && <p>No posts yet — be the first!</p>}
      </ul>
    </Container>
  );
}

function Login() {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [err, setErr] = useState(null);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setErr(null);
    try {
      const res = await API.login(userId, password);
      // expect backend to return an auth token or set cookie.
      if (res.token) localStorage.setItem("auth_token", res.token);
      navigate("/");
    } catch (e) {
      setErr("Login failed. Check credentials.");
    }
  };

  return (
    <Container>
      <h1 className="text-2xl font-bold mb-4">Login</h1>
      <form onSubmit={submit} className="space-y-3">
        <div>
          <label className="block text-sm">ID</label>
          <input className="w-full border p-2 rounded" value={userId} onChange={(e) => setUserId(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Password</label>
          <input type="password" className="w-full border p-2 rounded" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        {err && <p className="text-red-600">{err}</p>}
        <div>
          <button className="px-4 py-2 rounded bg-blue-600 text-white">Login</button>
        </div>
      </form>
    </Container>
  );
}

function Register() {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");
  const [msg, setMsg] = useState(null);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      await API.register(userId, password, name);
      setMsg("Registration successful — redirecting to login...");
      setTimeout(() => navigate("/auth/login"), 800);
    } catch (e) {
      setMsg("Registration failed — maybe ID already exists.");
    }
  };

  return (
    <Container>
      <h1 className="text-2xl font-bold mb-4">Register</h1>
      <form onSubmit={submit} className="space-y-3">
        <div>
          <label className="block text-sm">ID</label>
          <input className="w-full border p-2 rounded" value={userId} onChange={(e) => setUserId(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Password</label>
          <input type="password" className="w-full border p-2 rounded" value={password} onChange={(e) => setPassword(e.target.value)} />
        </div>
        <div>
          <label className="block text-sm">Name</label>
          <input className="w-full border p-2 rounded" value={name} onChange={(e) => setName(e.target.value)} />
        </div>
        {msg && <p className="text-sm text-gray-600">{msg}</p>}
        <div>
          <button className="px-4 py-2 rounded bg-green-600 text-white">Register</button>
        </div>
      </form>
    </Container>
  );
}

function PostCreate() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [msg, setMsg] = useState(null);
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    try {
      const res = await API.createPost(title, content);
      // assume backend returns created post with post_uuid
      navigate(`/posts/${res.post_uuid}`);
    } catch (e) {
      setMsg("Failed to create post — are you logged in?");
    }
  };

  return (
    <Container>
      <h1 className="text-2xl font-bold mb-4">Create Post</h1>
      <form onSubmit={submit} className="space-y-3">
        <div>
          <label className="block text-sm">Title</label>
          <input className="w-full border p-2 rounded" value={title} onChange={(e) => setTitle(e.target.value)} required />
        </div>
        <div>
          <label className="block text-sm">Content</label>
          <textarea className="w-full border p-2 rounded h-40" value={content} onChange={(e) => setContent(e.target.value)} required />
        </div>
        {msg && <p className="text-red-600">{msg}</p>}
        <div>
          <button className="px-4 py-2 rounded bg-indigo-600 text-white">Publish</button>
        </div>
      </form>
    </Container>
  );
}

function PostView() {
  const { post_uuid } = useParams();
  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [commentInput, setCommentInput] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    Promise.all([API.fetchPost(post_uuid), API.fetchComments(post_uuid)])
      .then(([p, c]) => {
        setPost(p);
        setComments(c);
      })
      .catch(() => setError("Failed to load post or comments"))
      .finally(() => setLoading(false));
  }, [post_uuid]);

  const submitComment = async (e) => {
    e.preventDefault();
    if (!commentInput.trim()) return;
    try {
      const newComment = await API.createComment(post_uuid, commentInput);
      // append new comment optimistically
      setComments((s) => [newComment, ...s]);
      setCommentInput("");
    } catch (e) {
      alert("Failed to post comment — are you logged in?");
    }
  };

  if (loading) return <Container><p>Loading...</p></Container>;
  if (error) return <Container><p className="text-red-600">{error}</p></Container>;
  if (!post) return <Container><p>Post not found.</p></Container>;

  return (
    <Container>
      <article className="border rounded p-4">
        <h1 className="text-2xl font-bold">{post.post_title}</h1>
        <p className="text-sm text-gray-600">by {post.user_name ?? 'Unknown'} — {post.create_time}</p>
        <div className="mt-4 whitespace-pre-wrap">{post.post_content}</div>
      </article>

      <section className="mt-6">
        <h2 className="text-xl font-semibold mb-2">Comments</h2>
        <form onSubmit={submitComment} className="space-y-2">
          <textarea className="w-full border p-2 rounded" value={commentInput} onChange={(e) => setCommentInput(e.target.value)} placeholder="Write a comment..." />
          <div>
            <button className="px-3 py-1 rounded bg-slate-700 text-white">Comment</button>
          </div>
        </form>

        <ul className="mt-4 space-y-3">
          {comments.map((c) => (
            <li key={c.comment_uuid} className="p-3 border rounded">
              <p className="text-sm text-gray-600">{c.user_name ?? 'Unknown'} — {c.create_time}</p>
              <p className="mt-1 whitespace-pre-wrap">{c.comment_content}</p>
            </li>
          ))}
          {comments.length === 0 && <p className="text-sm text-gray-600">No comments yet.</p>}
        </ul>
      </section>
    </Container>
  );
}

function UserMe() {
  const [me, setMe] = useState(null);
  const [editing, setEditing] = useState(false);
  const [name, setName] = useState("");
  const [msg, setMsg] = useState(null);

  useEffect(() => {
    API.fetchMe()
      .then((u) => {
        setMe(u);
        setName(u.user_name || "");
      })
      .catch(() => setMe(null));
  }, []);

  const save = async (e) => {
    e.preventDefault();
    try {
      const updated = await API.updateMe({ user_name: name });
      setMe(updated);
      setEditing(false);
      setMsg("Saved.");
    } catch (e) {
      setMsg("Failed to save.");
    }
  };

  if (!me) return <Container><p>Not logged in or failed to load.</p></Container>;

  return (
    <Container>
      <h1 className="text-2xl font-bold mb-4">My Profile</h1>
      {!editing ? (
        <div className="space-y-2">
          <p><strong>ID:</strong> {me.user_id}</p>
          <p><strong>Name:</strong> {me.user_name}</p>
          <p><strong>Joined:</strong> {me.create_time}</p>
          <div>
            <button className="px-3 py-1 rounded bg-slate-700 text-white" onClick={() => setEditing(true)}>Edit</button>
          </div>
        </div>
      ) : (
        <form onSubmit={save} className="space-y-3">
          <div>
            <label className="block text-sm">Name</label>
            <input className="w-full border p-2 rounded" value={name} onChange={(e) => setName(e.target.value)} />
          </div>
          <div>
            <button className="px-3 py-1 rounded bg-green-600 text-white">Save</button>
            <button type="button" className="ml-2 px-3 py-1 rounded border" onClick={() => setEditing(false)}>Cancel</button>
          </div>
        </form>
      )}
      {msg && <p className="text-sm text-gray-600 mt-2">{msg}</p>}
    </Container>
  );
}

/* ----------------------
   Main App
   ---------------------- */
export default function App() {
  const navigate = useNavigate ? undefined : undefined; // silence unused warning in some linters

  const handleLogout = () => {
    localStorage.removeItem("auth_token");
    // if server uses cookie sessions, you might want to call a logout endpoint.
    window.location.href = "/";
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Container>
        <Router>
          <Nav onLogout={handleLogout} />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/auth/login" element={<Login />} />
            <Route path="/auth/register" element={<Register />} />
            <Route path="/post_create" element={<PostCreate />} />
            <Route path="/posts/:post_uuid" element={<PostView />} />
            <Route path="/users/me" element={<UserMe />} />
            <Route path="*" element={<Container><p>Page not found</p></Container>} />
          </Routes>
        </Router>
      </Container>
    </div>
  );
}

/*
Notes / integration tips:
- Tailwind is assumed to be available. If not, replace classes with your preferred CSS.
- API base is left empty to use same origin. Change `base` in API helper to your backend address if needed.
- Login: the frontend expects either the backend to return a JSON { token: "..." } or to set an httpOnly cookie. If using cookie session, you may remove token handling and rely on server-set cookies.
- Endpoints used:
  - POST /api/auth/login
  - POST /api/auth/register
  - GET  /api/posts
  - GET  /api/posts/:post_uuid
  - POST /api/post_create
  - GET  /api/posts/:post_uuid/comment
  - POST /api/posts/:post_uuid/comment
  - GET  /api/users/me
  - PUT  /api/users/me

This single-file app is intentionally minimal but covers the requested pages and flows.
*/
