import { BrowserRouter, Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import Login from './pages/Login';
import { APP_CONTROL } from './utils/myPaths';

export default function Router() {


  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
  );
}
