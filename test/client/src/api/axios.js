// src/api/axios.js
import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:5000",  // 🔥 Flask 서버 주소/포트 맞추기
  withCredentials: true,             // 세션/쿠키 쓰면 유지
});

export default instance;
