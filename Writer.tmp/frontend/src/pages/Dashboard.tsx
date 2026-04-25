import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { getWorkspaceId, WRITER_DEFAULT_WORKSPACE, WRITER_WORKSPACE_KEY, writerApi } from '../utils/api';

interface DocumentSummary {
    id: string;
    title: string;
    workspace_id: string;
    root_block_id: string | null;
    block_count: number;
    created_at: string;
    updated_at: string;
}

interface FeedbackAreaSummary {
    area: string;
    count: number;
    average_rating: number;
}

interface FeedbackRecentItem {
    id: number;
    rating: number;
    area: string;
    page: string | null;
    message: string | null;
    created_at: string;
}

interface FeedbackSummary {
    days: number;
    total: number;
    average_rating: number;
    areas: FeedbackAreaSummary[];
    recent: FeedbackRecentItem[];
}

export default function Dashboard() {
    const navigate = useNavigate();
    const [workspaceId, setWorkspaceId] = useState(getWorkspaceId());
    const [documents, setDocuments] = useState<DocumentSummary[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [creating, setCreating] = useState(false);
    const [feedbackSummary, setFeedbackSummary] = useState<FeedbackSummary | null>(null);

    const fetchDocuments = useCallback(async (activeWorkspaceId = workspaceId) => {
        setLoading(true);
        setError("");
        try {
            const docs = await writerApi<DocumentSummary[]>("/documents?limit=24", {
                workspaceId: activeWorkspaceId,
            });
            setDocuments(docs);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Could not load documents.";
            setError(message);
            setDocuments([]);
        } finally {
            setLoading(false);
        }
    }, [workspaceId]);

    const fetchFeedbackSummary = useCallback(async (activeWorkspaceId = workspaceId) => {
        try {
            const summary = await writerApi<FeedbackSummary>("/feedback/summary?days=14&recent_limit=3", {
                workspaceId: activeWorkspaceId,
            });
            setFeedbackSummary(summary);
        } catch {
            setFeedbackSummary(null);
        }
    }, [workspaceId]);

    useEffect(() => {
        fetchDocuments(workspaceId);
        fetchFeedbackSummary(workspaceId);
    }, [workspaceId, fetchDocuments, fetchFeedbackSummary]);

    const handleWorkspaceChange = (value: string) => {
        const next = value.trim() || WRITER_DEFAULT_WORKSPACE;
        window.localStorage.setItem(WRITER_WORKSPACE_KEY, next);
        setWorkspaceId(next);
    };

    const openDocument = (doc: DocumentSummary) => {
        navigate("/document", {
            state: {
                workspaceId,
                documentId: doc.id,
                documentTitle: doc.title,
            },
        });
    };

    const handleCreateDocument = async () => {
        setCreating(true);
        setError("");
        try {
            const timestamp = new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
            const created = await writerApi<DocumentSummary>("/documents", {
                method: "POST",
                workspaceId,
                body: {
                    title: `Untitled ${timestamp}`,
                    initial_block_type: "text",
                    initial_content: {
                        text: "Start writing here. RM Writer will preserve this as structured block content.",
                    },
                },
            });
            await fetchDocuments(workspaceId);
            openDocument(created);
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : "Could not create a document.";
            setError(message);
        } finally {
            setCreating(false);
        }
    };

    const handleRefresh = async () => {
        await Promise.all([fetchDocuments(workspaceId), fetchFeedbackSummary(workspaceId)]);
    };

    return (
        <main className="flex-1 overflow-y-auto p-8 custom-scrollbar">
            <header className="flex items-center justify-between mb-8">
                <div className="flex flex-1 max-w-xl">
                    <div className="relative w-full group">
                        <div className="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                            <span className="material-symbols-outlined text-content-muted group-focus-within:text-primary transition-colors">search</span>
                        </div>
                        <input className="block w-full p-2.5 pl-10 text-sm text-content-primary bg-surface-base border border-border-default rounded-lg focus:ring-1 focus:ring-primary focus:border-primary placeholder-slate-400 shadow-sm transition-all" placeholder="Search commands, documents, or ask AI..." type="text"/>
                        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                            <span className="text-xs text-content-muted border border-border-default bg-surface-muted rounded px-1.5 py-0.5">⌘K</span>
                        </div>
                    </div>
                </div>
                <div className="flex items-center gap-4 ml-6">
                    <label className="text-xs text-content-muted flex flex-col gap-1">
                        Workspace
                        <input
                            defaultValue={workspaceId}
                            onBlur={(event) => handleWorkspaceChange(event.target.value)}
                            className="h-9 w-40 rounded-lg border border-border-default bg-surface-base px-3 text-sm text-content-primary"
                            placeholder="workspace id"
                        />
                    </label>
                    <button
                        onClick={handleCreateDocument}
                        disabled={creating}
                        className="flex items-center justify-center gap-2 h-9 px-4 rounded-lg bg-primary hover:bg-primary-hover text-white text-sm font-medium shadow-md shadow-primary/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        <span className="material-symbols-outlined text-[18px]">add</span>
                        <span>{creating ? "Creating..." : "New Document"}</span>
                    </button>
                </div>
            </header>

            <div className="max-w-5xl mx-auto mb-10">
                <h2 className="text-2xl font-bold text-content-primary mb-6">Good morning, Alex</h2>
                <div className="relative group">
                    <div className="absolute -inset-0.5 bg-gradient-to-r from-primary/50 to-blue-400/50 rounded-xl blur opacity-20 group-hover:opacity-40 transition duration-500"></div>
                    <div className="relative flex items-center bg-surface-base rounded-xl border border-border-default shadow-sm p-1">
                        <div className="pl-4 pr-2 text-primary">
                            <span className="material-symbols-outlined">auto_awesome</span>
                        </div>
                        <input className="w-full bg-transparent border-none text-content-primary placeholder-slate-400 focus:ring-0 py-3 px-2 text-base outline-none" placeholder="Ask RM AI to generate a report, summarize notes, or draft an email..." type="text"/>
                        <button className="bg-primary hover:bg-primary-hover text-white px-4 py-1.5 rounded-lg text-sm font-medium transition-colors shadow-sm">
                            Generate
                        </button>
                    </div>
                </div>
                <div className="flex gap-3 mt-4 overflow-x-auto pb-2 scrollbar-hide">
                    <button className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-border-default bg-surface-base hover:bg-surface-muted text-content-secondary hover:text-content-primary text-xs transition-colors whitespace-nowrap shadow-sm">
                        <span className="material-symbols-outlined text-[16px]">summarize</span> Summarize last meeting
                    </button>
                    <button className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-border-default bg-surface-base hover:bg-surface-muted text-content-secondary hover:text-content-primary text-xs transition-colors whitespace-nowrap shadow-sm">
                        <span className="material-symbols-outlined text-[16px]">edit_document</span> Draft Q4 proposal
                    </button>
                </div>
                {feedbackSummary && (
                    <div className="mt-4 rounded-xl border border-border-default bg-surface-base px-4 py-3">
                        <div className="flex items-center justify-between mb-2">
                            <h4 className="text-sm font-semibold text-content-primary">User Feedback (last {feedbackSummary.days} days)</h4>
                            <span className="text-xs text-content-muted">{feedbackSummary.total} responses · Avg {feedbackSummary.average_rating.toFixed(1)}/5</span>
                        </div>
                        <div className="flex flex-wrap gap-2 mb-2">
                            {feedbackSummary.areas.slice(0, 3).map((area) => (
                                <span key={area.area} className="rounded-full border border-border-default bg-surface-muted px-2 py-1 text-[11px] text-content-secondary">
                                    {area.area} · {area.count} · {area.average_rating.toFixed(1)}
                                </span>
                            ))}
                        </div>
                        {feedbackSummary.recent[0]?.message && (
                            <p className="text-xs text-content-secondary line-clamp-2">
                                Latest: {feedbackSummary.recent[0].message}
                            </p>
                        )}
                    </div>
                )}
            </div>

            <div className="max-w-5xl mx-auto">
                <div className="flex items-center justify-between mb-6">
                    <h3 className="text-lg font-semibold text-content-primary flex items-center gap-2">
                        <span className="material-symbols-outlined text-content-muted">schedule</span>
                        Recent Work
                    </h3>
                    <button
                        onClick={handleRefresh}
                        className="text-xs font-medium px-3 py-1.5 rounded-lg border border-border-default bg-surface-base hover:bg-surface-muted"
                    >
                        Refresh
                    </button>
                </div>
                {error && (
                    <div className="mb-4 rounded-lg border border-red-200 bg-red-50 px-3 py-2 text-sm text-red-700">
                        {error}
                    </div>
                )}
                {loading ? (
                    <div className="rounded-xl border border-border-default bg-surface-base p-8 text-center text-sm text-content-muted">
                        Loading workspace documents...
                    </div>
                ) : documents.length === 0 ? (
                    <div className="rounded-xl border border-border-default bg-surface-base p-8 text-center">
                        <p className="text-content-secondary font-medium mb-2">No documents in this workspace yet.</p>
                        <p className="text-sm text-content-muted mb-4">Create your first structured document and start building the block graph.</p>
                        <button
                            onClick={handleCreateDocument}
                            className="inline-flex items-center gap-2 rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white"
                        >
                            <span className="material-symbols-outlined text-[18px]">add</span>
                            Create Document
                        </button>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                        {documents.slice(0, 8).map((doc) => (
                            <button
                                key={doc.id}
                                onClick={() => openDocument(doc)}
                                className="group relative flex flex-col text-left bg-surface-base border border-border-default rounded-xl overflow-hidden hover:border-primary/50 hover:shadow-md transition-all cursor-pointer h-64"
                            >
                                <div className="h-32 bg-gradient-to-br from-blue-50 via-white to-indigo-100 relative overflow-hidden w-full">
                                    <div className="absolute top-3 right-3 z-20">
                                        <div className="bg-surface-base/90 backdrop-blur rounded p-1 shadow-sm">
                                            <span className="material-symbols-outlined text-primary text-[16px]">description</span>
                                        </div>
                                    </div>
                                    <div className="absolute left-4 bottom-3 text-[11px] font-semibold uppercase tracking-wide text-content-muted">
                                        Workspace {workspaceId}
                                    </div>
                                </div>
                                <div className="flex flex-col flex-1 p-4 w-full">
                                    <h4 className="text-content-primary font-semibold text-sm mb-1 group-hover:text-primary transition-colors line-clamp-2">
                                        {doc.title}
                                    </h4>
                                    <p className="text-content-muted text-xs mb-auto">
                                        {doc.block_count} blocks · Updated {new Date(doc.updated_at).toLocaleString()}
                                    </p>
                                    <span className="mt-3 inline-flex items-center text-xs font-medium text-primary">
                                        Open Document
                                        <span className="material-symbols-outlined text-[14px] ml-1">arrow_forward</span>
                                    </span>
                                </div>
                            </button>
                        ))}
                    </div>
                )}
            </div>
        </main>
    );
}
