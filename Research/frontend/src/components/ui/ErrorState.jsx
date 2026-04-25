import { AlertCircle, RefreshCw } from 'lucide-react'

export default function ErrorState({ message, onRetry }) {
  return (
    <div className="col-span-full flex flex-col items-center gap-4 py-16 text-center">
      <div className="w-12 h-12 rounded-full bg-red/10 flex items-center justify-center">
        <AlertCircle size={20} className="text-red-l" />
      </div>
      <div>
        <p className="text-sm font-bold text-text mb-1">Failed to load</p>
        <p className="text-[12px] text-muted">{message}</p>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="btn btn-ghost text-[12px]"
        >
          <RefreshCw size={12} /> Try again
        </button>
      )}
    </div>
  )
}
