import * as React from "react";
import { cn } from "@/lib/cn";

const sizeClasses = {
  xs: "size-6 text-[9px]",
  sm: "size-8 text-[11px]",
  md: "size-10 text-sm",
  lg: "size-12 text-base",
  xl: "size-16 text-lg",
} as const;

const statusClasses = {
  online:  "bg-success-500",
  offline: "bg-neutral-400",
  busy:    "bg-danger-500",
  away:    "bg-warning-500",
} as const;

const statusSizeClasses = {
  xs: "size-1.5 border",
  sm: "size-2.5 border-2",
  md: "size-3 border-2",
  lg: "size-3.5 border-2",
  xl: "size-4 border-2",
} as const;

function getInitials(name: string): string {
  const parts = name.trim().split(/\s+/).filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

// Deterministic color from name
const avatarColors = [
  "bg-primary-500",
  "bg-info-500",
  "bg-success-600",
  "bg-warning-600",
  "bg-danger-500",
  "bg-neutral-600",
];

function getColorFromName(name: string): string {
  let hash = 0;
  for (let i = 0; i < name.length; i++) hash = name.charCodeAt(i) + ((hash << 5) - hash);
  return avatarColors[Math.abs(hash) % avatarColors.length];
}

// ─── Avatar ─────────────────────────────────────────────────────────────────

export type AvatarProps = {
  src?:       string;
  name?:      string;
  size?:      keyof typeof sizeClasses;
  status?:    keyof typeof statusClasses;
  className?: string;
  alt?:       string;
};

export function Avatar({
  src,
  name = "",
  size = "md",
  status,
  className,
  alt,
}: AvatarProps) {
  const [imgError, setImgError] = React.useState(false);
  const showImage = src && !imgError;

  return (
    <span className={cn("relative inline-flex shrink-0", className)}>
      <span
        className={cn(
          "inline-flex items-center justify-center rounded-full overflow-hidden",
          "font-bold text-white select-none",
          sizeClasses[size],
          !showImage && getColorFromName(name),
        )}
      >
        {showImage ? (
          <img
            src={src}
            alt={alt ?? name ?? "Avatar"}
            className="size-full object-cover"
            onError={() => setImgError(true)}
          />
        ) : (
          <span aria-hidden="true">{getInitials(name)}</span>
        )}
      </span>

      {status && (
        <span
          className={cn(
            "absolute bottom-0 right-0 rounded-full border-surface-base",
            statusClasses[status],
            statusSizeClasses[size],
          )}
          aria-label={status}
        />
      )}
    </span>
  );
}

// ─── AvatarGroup ─────────────────────────────────────────────────────────────

export type AvatarGroupProps = {
  items: Array<{ src?: string; name?: string }>;
  max?:  number;
  size?: AvatarProps["size"];
  className?: string;
};

export function AvatarGroup({ items, max = 4, size = "sm", className }: AvatarGroupProps) {
  const visible  = items.slice(0, max);
  const overflow = items.length - max;

  return (
    <div className={cn("flex items-center", className)}>
      {visible.map((item, i) => (
        <span
          key={i}
          className="ring-2 ring-surface-base rounded-full -ml-2 first:ml-0"
        >
          <Avatar src={item.src} name={item.name ?? ""} size={size} />
        </span>
      ))}
      {overflow > 0 && (
        <span
          className={cn(
            "inline-flex items-center justify-center rounded-full",
            "bg-neutral-200 dark:bg-neutral-700 text-content-secondary font-semibold",
            "-ml-2 ring-2 ring-surface-base",
            sizeClasses[size],
          )}
        >
          +{overflow}
        </span>
      )}
    </div>
  );
}
