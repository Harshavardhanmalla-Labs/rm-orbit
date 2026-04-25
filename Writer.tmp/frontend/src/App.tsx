import { Suspense, lazy, useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@orbit-ui/react';
import Layout from './components/Layout';
import OrbitDock from './components/OrbitDock';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Document = lazy(() => import('./pages/Document'));
const Sheets = lazy(() => import('./pages/Sheets'));

function App() {
  const [isOffline, setIsOffline] = useState(!navigator.onLine);

  useEffect(() => {
    const onOnline = () => setIsOffline(false);
    const onOffline = () => setIsOffline(true);
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    return () => {
      window.removeEventListener('online', onOnline);
      window.removeEventListener('offline', onOffline);
    };
  }, []);

  return (
    <ThemeProvider>
      <Router>
        {isOffline && (
          <div className="bg-danger-500 text-white text-sm py-2 px-4 flex items-center justify-center gap-2 z-50 fixed top-0 w-full">
            <span className="material-symbols-outlined text-[16px]">wifi_off</span>
            You are currently offline. Some features may be unavailable.
          </div>
        )}
        <Suspense fallback={<div className="flex h-screen w-screen items-center justify-center bg-surface-muted"><div className="h-8 w-8 animate-spin rounded-full border-4 border-primary-500 border-t-transparent"></div></div>}>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Dashboard />} />
              <Route path="document" element={<Document />} />
              <Route path="sheets" element={<Sheets />} />
              <Route path="*" element={<div className="p-10 text-center text-content-muted">Placeholder Component</div>} />
            </Route>
          </Routes>
        </Suspense>
      </Router>
      <OrbitDock />
    </ThemeProvider>
  );
}

export default App;
