export function Skeleton({ className = '' }) {
  return <div className={`bg-raised rounded-lg animate-pulse-dot ${className}`} />
}

export function SkeletonCard() {
  return (
    <div className="bg-surface rounded-xl border border-border p-5 space-y-3">
      {/* Badges row */}
      <div className="flex gap-2">
        <Skeleton className="h-5 w-16 rounded-full" />
        <Skeleton className="h-5 w-20 rounded-full" />
      </div>

      {/* Title */}
      <Skeleton className="h-5 w-4/5 rounded-lg" />

      {/* Domain */}
      <Skeleton className="h-3 w-1/2 rounded-lg" />

      {/* Footer with date and button */}
      <div className="flex justify-between items-center pt-2 border-t border-border mt-3">
        <Skeleton className="h-3 w-24 rounded-lg" />
        <Skeleton className="h-7 w-16 rounded-lg" />
      </div>
    </div>
  )
}

export default Skeleton
