import { Outlet } from 'react-router-dom'
import { useModal } from '../../context/ModalContext'
import Sidebar from './Sidebar'
import TopBar from './TopBar'
import NewPaperModal from '../papers/NewPaperModal'

export default function AppShell() {
  const { newPaperModalOpen, setNewPaperModalOpen } = useModal()

  return (
    <div className="flex h-screen overflow-hidden bg-bg">
      {/* Sidebar */}
      <Sidebar />

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        {/* Top bar */}
        <TopBar />

        {/* Page content */}
        <main className="flex-1 overflow-y-auto bg-canvas">
          <Outlet />
        </main>
      </div>

      {/* New Paper Modal */}
      <NewPaperModal
        open={newPaperModalOpen}
        onClose={() => setNewPaperModalOpen(false)}
      />
    </div>
  )
}
