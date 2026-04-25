import { createContext, useContext, useState } from 'react'

const ModalContext = createContext()

export function ModalProvider({ children }) {
  const [newPaperModalOpen, setNewPaperModalOpen] = useState(false)

  return (
    <ModalContext.Provider value={{ newPaperModalOpen, setNewPaperModalOpen }}>
      {children}
    </ModalContext.Provider>
  )
}

export function useModal() {
  const context = useContext(ModalContext)
  if (!context) {
    throw new Error('useModal must be used within ModalProvider')
  }
  return context
}
