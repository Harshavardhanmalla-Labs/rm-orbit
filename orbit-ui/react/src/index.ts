// ─── Utilities ───────────────────────────────────────────────────────────────
export { cn } from "@/lib/cn";

// ─── Primitives ──────────────────────────────────────────────────────────────
export { Button }              from "@/components/Button/Button";
export type { ButtonProps }    from "@/components/Button/Button";

export { IconButton }          from "@/components/Button/IconButton";
export type { IconButtonProps }from "@/components/Button/IconButton";

export { Input }               from "@/components/Input/Input";
export type { InputProps }     from "@/components/Input/Input";

export { Badge }               from "@/components/Badge/Badge";
export type { BadgeProps }     from "@/components/Badge/Badge";

// ─── Data Display ────────────────────────────────────────────────────────────
export { Card }                from "@/components/Card/Card";
export type { CardProps }      from "@/components/Card/Card";

export { Avatar, AvatarGroup } from "@/components/Avatar/Avatar";
export type { AvatarProps, AvatarGroupProps } from "@/components/Avatar/Avatar";

export { EmptyState }          from "@/components/EmptyState/EmptyState";
export type { EmptyStateProps }from "@/components/EmptyState/EmptyState";

export { Skeleton, SkeletonText, SkeletonCard } from "@/components/Skeleton/Skeleton";
export type { SkeletonProps }  from "@/components/Skeleton/Skeleton";

// ─── Feedback ────────────────────────────────────────────────────────────────
export { Spinner, PageLoader } from "@/components/Spinner/Spinner";
export type { SpinnerProps }   from "@/components/Spinner/Spinner";

export { ToastProvider, useToast } from "@/components/Toast/Toast";
export type { ToastItem, ToastVariant } from "@/components/Toast/Toast";

// ─── Overlays ────────────────────────────────────────────────────────────────
export { Modal }               from "@/components/Modal/Modal";
export type { ModalProps }     from "@/components/Modal/Modal";

// ─── Form ────────────────────────────────────────────────────────────────────
export { Textarea }            from "@/components/Input/Textarea";
export type { TextareaProps }  from "@/components/Input/Textarea";

export { Select }              from "@/components/Input/Select";
export type { SelectProps }    from "@/components/Input/Select";

export { Checkbox }            from "@/components/Checkbox/Checkbox";
export type { CheckboxProps }  from "@/components/Checkbox/Checkbox";

export { Switch }              from "@/components/Switch/Switch";
export type { SwitchProps }    from "@/components/Switch/Switch";

// ─── Layout ──────────────────────────────────────────────────────────────────
export { Divider }             from "@/components/Divider/Divider";
export type { DividerProps }   from "@/components/Divider/Divider";

export { Progress, ProgressStacked } from "@/components/Progress/Progress";
export type { ProgressProps, ProgressStackedProps, ProgressSegment } from "@/components/Progress/Progress";

// ─── Menus ───────────────────────────────────────────────────────────────────
export {
  Dropdown,
  DropdownTrigger,
  DropdownContent,
  DropdownItem,
  DropdownSubTrigger,
  DropdownSeparator,
  DropdownLabel,
}                              from "@/components/Dropdown/Dropdown";
export type {
  DropdownProps,
  DropdownContentProps,
  DropdownItemProps,
}                              from "@/components/Dropdown/Dropdown";

// ─── Navigation ──────────────────────────────────────────────────────────────
export { Sidebar, useSidebar } from "@/components/Sidebar/Sidebar";
export type { SidebarProps, SidebarItemProps } from "@/components/Sidebar/Sidebar";

export { Tabs }                from "@/components/Tabs/Tabs";
export type { TabsProps, TabProps } from "@/components/Tabs/Tabs";

// ─── Alerts & Tooltips ───────────────────────────────────────────────────────
export { Alert }               from "@/components/Alert/Alert";
export type { AlertProps }     from "@/components/Alert/Alert";

export { Tooltip }             from "@/components/Tooltip/Tooltip";
export type { TooltipProps }   from "@/components/Tooltip/Tooltip";

// ─── Form ────────────────────────────────────────────────────────────────────
export { RadioGroup, Radio }       from "@/components/Radio/Radio";
export type { RadioGroupProps, RadioProps } from "@/components/Radio/Radio";

export { NumberInput }             from "@/components/NumberInput/NumberInput";
export type { NumberInputProps }   from "@/components/NumberInput/NumberInput";

export { Slider }                  from "@/components/Slider/Slider";
export type { SliderProps }        from "@/components/Slider/Slider";

// ─── Data Display ────────────────────────────────────────────────────────────
export { Table }                   from "@/components/Table/Table";
export type { TableProps, Column, SortDir } from "@/components/Table/Table";

export { Tag, TagInput }           from "@/components/Tag/Tag";
export type { TagProps, TagInputProps, TagVariant, TagSize } from "@/components/Tag/Tag";

export { Accordion }               from "@/components/Accordion/Accordion";
export type { AccordionProps, AccordionItem } from "@/components/Accordion/Accordion";

// ─── Navigation ──────────────────────────────────────────────────────────────
export { Breadcrumb }              from "@/components/Breadcrumb/Breadcrumb";
export type { BreadcrumbProps, BreadcrumbItem } from "@/components/Breadcrumb/Breadcrumb";

export { Pagination }              from "@/components/Pagination/Pagination";
export type { PaginationProps }    from "@/components/Pagination/Pagination";

export { Steps }                   from "@/components/Steps/Steps";
export type { StepsProps, StepItem, StepStatus } from "@/components/Steps/Steps";

// ─── Overlays ────────────────────────────────────────────────────────────────
export { Drawer }                  from "@/components/Drawer/Drawer";
export type { DrawerProps, DrawerSide, DrawerSize } from "@/components/Drawer/Drawer";

export { Popover, PopoverHeader, PopoverBody, PopoverFooter } from "@/components/Popover/Popover";
export type { PopoverProps, PopoverAlign, PopoverSide } from "@/components/Popover/Popover";

// ─── Utilities ────────────────────────────────────────────────────────────────
export { CommandPalette, useCommandPalette } from "@/components/CommandPalette/CommandPalette";
export type { CommandPaletteProps, CommandItem } from "@/components/CommandPalette/CommandPalette";

// ─── Button extras ────────────────────────────────────────────────────────────
export { ButtonGroup }             from "@/components/Button/ButtonGroup";
export type { ButtonGroupProps }   from "@/components/Button/ButtonGroup";

// ─── Date & Time ──────────────────────────────────────────────────────────────
export { DatePicker }              from "@/components/DatePicker/DatePicker";
export type { DatePickerProps, DatePickerMode, DateRange } from "@/components/DatePicker/DatePicker";

export { TimePicker }              from "@/components/TimePicker/TimePicker";
export type { TimePickerProps, TimeValue } from "@/components/TimePicker/TimePicker";

// ─── File Upload ──────────────────────────────────────────────────────────────
export { FileUpload }              from "@/components/FileUpload/FileUpload";
export type { FileUploadProps, FileItem, FileUploadStatus } from "@/components/FileUpload/FileUpload";

// ─── Context Menu ─────────────────────────────────────────────────────────────
export { ContextMenu }             from "@/components/ContextMenu/ContextMenu";
export type { ContextMenuProps, ContextMenuItemProps } from "@/components/ContextMenu/ContextMenu";

// ─── Theme ───────────────────────────────────────────────────────────────────
export { ThemeProvider, ThemeToggle, useTheme } from "@/components/ThemeToggle/ThemeToggle";
