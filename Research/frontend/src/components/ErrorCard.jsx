import { AlertCircle, RefreshCw } from 'lucide-react'

export default function ErrorCard({ message, onRetry }) {
  return (
    <div className="flex flex-col items-center gap-4 p-8 rounded-xl border border-red/25 bg-red/5 text-center max-w-md mx-auto">
      <div className="w-12 h-12 rounded-full flex items-center justify-center bg-red/10">
        <AlertCircle size={24} className="text-red" />
      </div>
      <div>
        <p className="font-medium mb-1 text-text">Something went wrong</p>
        <p className="text-sm text-muted">{message || 'An unexpected error occurred.'}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors bg-red/10 text-red-l border border-red/25 hover:bg-red/20"
        >
          <RefreshCw size={14} />
          Try Again
        </button>
      )}
    </div>
  )
}
