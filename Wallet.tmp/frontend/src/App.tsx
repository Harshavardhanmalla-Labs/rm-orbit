import { lazy, Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { PageLoader } from '@orbit-ui/react'
import AppShell from './components/AppShell'
import OrbitDock from './components/OrbitDock'

const Secrets = lazy(() => import('./pages/Secrets'))
const SharedInfo = lazy(() => import('./pages/SharedInfo'))
const AuditLog = lazy(() => import('./pages/AuditLog'))

export default function App() {
  return (
    <>
    <Suspense fallback={<PageLoader />}>
      <Routes>
        <Route element={<AppShell />}>
          <Route index element={<Navigate to="/secrets" replace />} />
          <Route path="secrets" element={<Secrets />} />
          <Route path="shared-info" element={<SharedInfo />} />
          <Route path="audit" element={<AuditLog />} />
        </Route>
        <Route path="*" element={<Navigate to="/secrets" replace />} />
      </Routes>
    </Suspense>
    <OrbitDock />
    </>
  )
}
