import React from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import OrbitDock from './components/OrbitDock';
import { generateCodeVerifier, generateCodeChallenge } from './utils/auth';
import { useEffect, useState } from 'react';

function Home() {
  const [config, setConfig] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch('/oauth-config')
      .then(res => res.json())
      .then(setConfig)
      .catch(console.error);
  }, []);

  const handleLogin = async () => {
    const app = config.find(a => a.name === 'Snitch');
    if (!app) return alert('oauth config not available');
    const clientId = app.client_id;
    const redirectUri = `${window.location.origin}/callback`;
    const verifier = generateCodeVerifier();
    const challenge = await generateCodeChallenge(verifier);
    localStorage.setItem('pkce_verifier', verifier);
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: clientId,
      redirect_uri: redirectUri,
      scope: 'openid profile email',
      code_challenge: challenge,
      code_challenge_method: 'S256',
    });
    localStorage.setItem('oauth_client_id', clientId);
    window.location = `http://localhost:45001/api/v1/oauth/authorize?${params}`;
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center p-4">
      <h1 className="text-3xl font-bold mb-6">Snitch Prototype Launcher</h1>
      <button onClick={handleLogin} className="px-6 py-3 bg-green-600 text-white rounded">
        Login with Gate
      </button>
    </div>
  );
}

function Callback() {
  const location = useLocation();
  const navigate = useNavigate();
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const code = params.get('code');
    if (!code) return;
    const verifier = localStorage.getItem('pkce_verifier');
    if (!verifier) return;
    const clientId = localStorage.getItem('oauth_client_id') || '';
    // exchange code for tokens
    fetch('http://localhost:45001/api/v1/oauth/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams({
        grant_type: 'authorization_code',
        code,
        redirect_uri: `${window.location.origin}/callback`,
        client_id: clientId,
        code_verifier: verifier,
      }),
    })
      .then(r => r.json())
      .then(tok => {
        localStorage.setItem('access_token', tok.access_token);
        localStorage.setItem('refresh_token', tok.refresh_token);
        navigate('/app');
      })
      .catch(console.error);
  }, [location, navigate]);
  return <div>Signing in…</div>;
}

function AppContent() {
  const [user, setUser] = useState(null);
  const [apps, setApps] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) return;
    fetch('http://localhost:45001/api/v1/auth/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then(r => r.json())
      .then(setUser);
    fetch('/oauth-config')
      .then(r => r.json())
      .then(setApps);
  }, []);

  if (!user) return <div>Loading user…</div>;

  const createSampleDoc = () => {
    const token = localStorage.getItem('access_token');
    fetch('http://localhost:6002/docs', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
        'X-Org-Id': user.organization_id || 'default',
      },
      body: JSON.stringify({ slug: 'welcome', title: 'Welcome', content: 'Hello world' }),
    })
      .then(r => r.json())
      .then(data => alert('Doc created: ' + JSON.stringify(data)))
      .catch(console.error);
  };

  return (
    <div className="p-4">
      <h2>Welcome, {user.name || user.email}</h2>
      <p>Your ID: {user.id}</p>
      <p>Organization: {user.organization_id || 'n/a'}</p>
      <button
        className="mt-4 px-4 py-2 bg-indigo-600 text-white rounded"
        onClick={createSampleDoc}
      >
        Create Sample Doc in Learn Service
      </button>
      <h3 className="mt-6 text-xl font-semibold">Prototypes</h3>
      <ul className="list-disc list-inside">
        {apps.map(app => {
          const portMap = { Learn: 45009, 'Capital Hub': 45013, Secure: 45012 };
          const port = portMap[app.name] || 5179;
          return (
            <li key={app.name}>
              <a
                href={`http://localhost:${port}`}
                target="_blank"
                rel="noreferrer"
                className="text-blue-600 hover:underline"
              >
                {app.name}
              </a>
            </li>
          );
        })}
      </ul>
    </div>
  );
}

import EventMonitor from './pages/EventMonitor';

export default function App() {
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
    <Router>
      {isOffline && (
        <div className="bg-red-500 text-white text-sm py-2 px-4 flex items-center justify-center gap-2 z-50 fixed top-0 w-full shrink-0">
          <span className="material-symbols-outlined text-[16px]">wifi_off</span>
          You are currently offline. Some features may be unavailable.
        </div>
      )}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/callback" element={<Callback />} />
        <Route path="/app" element={<AppContent />} />
        <Route path="/monitor" element={<EventMonitor />} />
      </Routes>
      <OrbitDock />
    </Router>
  );
}
