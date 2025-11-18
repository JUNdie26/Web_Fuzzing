export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-6">
      {/* 메인 컨테이너 */}
      <div className="bg-white shadow-lg rounded-2xl p-10 max-w-xl w-full text-center">
        
        {/* 타이틀 */}
        <h1 className="text-3xl font-bold text-gray-800 mb-3">
          엄마 저는 대학에와서 너무 행복해요 사람들 모두 친절하구요 웹 만드는것도 공부하는것도 모의해킹하는것도 너무 즐거워요 아들은 잘지내요 엄마 걱정마세요 👋
        </h1>
        <p className="text-gray-600 mb-8">
          우리 모두 화이팅 해볼까요??!! 여기는 부제목 자리입니당ㅎㅎ
        </p>

        {/* 버튼 영역 */}
        <div className="flex flex-col space-y-3">
          <a
            href="/login"
            className="w-full text-center bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-lg font-medium transition"
          >
            로그인
          </a>

          <a
            href="/register"
            className="w-full text-center bg-gray-200 hover:bg-gray-300 text-gray-800 py-3 rounded-lg font-medium transition"
          >
            회원가입
          </a>
        </div>
      </div>

      {/* 푸터 */}
      <p className="mt-6 text-gray-400 text-sm">
        © 2025 Web Bazhick! Team
      </p>
    </div>
  );
}
