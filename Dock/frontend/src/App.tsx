import { lazy, Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { PageLoader } from '@orbit-ui/react'
import AppShell from './components/AppShell'
import OrbitDock from './components/OrbitDock'

const Catalog = lazy(() => import('./pages/Catalog'))
const MyApps = lazy(() => import('./pages/MyApps'))
const Licenses = lazy(() => import('./pages/Licenses'))
const Assignments = lazy(() => import('./pages/Assignments'))
const Requests = lazy(() => import('./pages/Requests'))
const AuditLog = lazy(() => import('./pages/AuditLog'))

export default function App() {
  return (
    <>
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Navigate to="/catalog" replace />} />
          <Route path="catalog" element={<Catalog />} />
          <Route path="my-apps" element={<MyApps />} />
          <Route path="licenses" element={<Licenses />} />
          <Route path="assignments" element={<Assignments />} />
          <Route path="requests" element={<Requests />} />
          <Route path="audit" element={<AuditLog />} />
        </Route>
        <Route path="*" element={<Navigate to="/catalog" replace />} />
      </Routes>
    </Suspense>
    <OrbitDock />
    </>
  )
}
