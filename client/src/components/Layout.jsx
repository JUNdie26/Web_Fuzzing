import { Link } from "react-router-dom";

export default function Layout({ children }) {
  return (
    <div className="min-h-screen bg-[#f0eded] text-[#011022]">

      {/* NAVBAR */}
      <header className="bg-white shadow">
        <nav className="max-w-5xl mx-auto px-6 py-4 flex justify-between items-center">

          {/* 로고 */}
          <Link to="/" className="text-2xl font-bold">
            <span className="text-[#f0ab52]">Fuzz</span> Blog
          </Link>

          {/* 메뉴 */}
          <ul className="flex gap-4 font-medium">
            <li>
              <Link 
                to="/" 
                className="px-3 py-2 rounded hover:bg-[#f0ab52] hover:text-white transition"
              >
                홈
              </Link>
            </li>

            <li>
              <Link 
                to="/post_create" 
                className="px-3 py-2 rounded hover:bg-[#f0ab52] hover:text-white transition"
              >
                글쓰기
              </Link>
            </li>

            <li>
              <Link 
                to="/Login" 
                className="px-3 py-2 rounded hover:bg-[#f0ab52] hover:text-white transition"
              >
                로그인
              </Link>
            </li>
          </ul>
        </nav>
      </header>

      {/* 각 페이지 콘텐츠 */}
      <main className="max-w-5xl mx-auto px-6 py-6">
        {children}
      </main>

    </div>
  );
}
