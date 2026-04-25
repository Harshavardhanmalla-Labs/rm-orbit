export default function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="col-span-full flex flex-col items-center gap-5 py-24 text-center">
      {Icon && (
        <div className="w-14 h-14 rounded-2xl bg-accent/10 border border-accent/20 flex items-center justify-center">
          <Icon size={24} className="text-accent" />
        </div>
      )}
      <div>
        <p className="text-base font-bold text-text mb-2">{title}</p>
        <p className="text-[13px] text-muted max-w-xs leading-relaxed">{description}</p>
      </div>
      {action}
    </div>
  )
}
