// client/src/api/axios.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:5000", // Flask 서버 주소
  // 세션 쿠키 안 쓸 거면 withCredentials 안 써도 됨
  // withCredentials: true,
});

export default api;
