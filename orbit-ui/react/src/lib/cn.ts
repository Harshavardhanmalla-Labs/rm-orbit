import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Merge Tailwind classes safely — combines clsx (conditionals) with
 * tailwind-merge (deduplication). Use this everywhere in the component lib.
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}
