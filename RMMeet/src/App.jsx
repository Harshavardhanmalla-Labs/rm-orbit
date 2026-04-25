import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import HomePage from './pages/HomePage.jsx';
import JoinPage from './pages/JoinPage.jsx';
import RoomPage from './pages/RoomPage.jsx';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/join/:roomId" element={<JoinPage />} />
        <Route path="/room/:roomId" element={<RoomPage />} />
        {/* Legacy: allow ?room=xxx links */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
