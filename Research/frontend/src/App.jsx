import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { ModalProvider } from './context/ModalContext'
import AppShell from './components/shell/AppShell.jsx'
import PapersList from './pages/PapersList.jsx'
import Upload from './pages/Upload.jsx'
import Pipeline from './pages/Pipeline.jsx'
import Preview from './pages/Preview.jsx'
import Export from './pages/Export.jsx'
import System from './pages/System.jsx'

export default function App() {
  return (
    <ModalProvider>
      <BrowserRouter>
        <Toaster position="top-right" />
        <Routes>
          <Route path="/" element={<AppShell />}>
            <Route index element={<Navigate to="/papers" replace />} />
            <Route path="papers" element={<PapersList />} />
            <Route path="new" element={<Navigate to="/papers" replace />} />
            <Route path="system" element={<System />} />
            <Route path="paper/:paperId/upload" element={<Upload />} />
            <Route path="paper/:paperId/pipeline" element={<Pipeline />} />
            <Route path="paper/:paperId/preview" element={<Preview />} />
            <Route path="paper/:paperId/export" element={<Export />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ModalProvider>
  )
}
