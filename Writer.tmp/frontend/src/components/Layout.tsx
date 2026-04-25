import { useState, type FormEvent } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { writerApi } from '../utils/api';

export default function Layout() {
    const [mobileOpen, setMobileOpen] = useState(false);
    const [feedbackOpen, setFeedbackOpen] = useState(false);
    const [feedbackRating, setFeedbackRating] = useState(5);
    const [feedbackMessage, setFeedbackMessage] = useState("");
    const [sendingFeedback, setSendingFeedback] = useState(false);
    const [feedbackAck, setFeedbackAck] = useState("");
    const location = useLocation();

    const submitFeedback = async (event: FormEvent) => {
        event.preventDefault();
        setSendingFeedback(true);
        setFeedbackAck("");
        try {
            await writerApi<{ status: string; received_at: string }>("/feedback", {
                method: "POST",
                body: {
                    rating: feedbackRating,
                    area: location.pathname === "/" ? "dashboard" : location.pathname.replace("/", ""),
                    message: feedbackMessage.trim() || undefined,
                    page: location.pathname,
                },
            });
            setFeedbackMessage("");
            setFeedbackAck("Thanks, feedback saved.");
            window.setTimeout(() => setFeedbackOpen(false), 900);
        } catch (error: unknown) {
            const message = error instanceof Error ? error.message : "Could not submit feedback.";
            setFeedbackAck(message);
        } finally {
            setSendingFeedback(false);
        }
    };

    return (
        <div className="flex h-screen w-full overflow-hidden bg-surface-muted relative">
            <Sidebar mobileOpen={mobileOpen} setMobileOpen={setMobileOpen} />
            <div className="flex-1 flex flex-col h-full overflow-hidden relative">
                <header className="lg:hidden flex items-center p-4 border-b border-border-default bg-surface-base shrink-0">
                   <button onClick={() => setMobileOpen(true)} className="p-2 -ml-2 text-content-muted hover:bg-surface-muted rounded-lg">
                       <span className="material-symbols-outlined pointer-events-none">menu</span>
                   </button>
                   <span className="ml-2 font-bold text-content-primary">RM Writer</span>
                </header>
                <Outlet />
            </div>
            <div className="fixed bottom-4 right-4 z-50">
                {feedbackOpen ? (
                    <form
                        onSubmit={submitFeedback}
                        className="w-72 rounded-xl border border-border-default bg-surface-base shadow-xl p-3 space-y-2"
                    >
                        <div className="flex items-center justify-between">
                            <h3 className="text-sm font-semibold text-content-primary">Quick Feedback</h3>
                            <button
                                type="button"
                                onClick={() => setFeedbackOpen(false)}
                                className="text-content-muted hover:text-content-primary text-xs"
                            >
                                Close
                            </button>
                        </div>
                        <label className="text-xs text-content-muted block">
                            Rating
                            <select
                                value={feedbackRating}
                                onChange={(event) => setFeedbackRating(Number(event.target.value))}
                                className="mt-1 h-8 w-full rounded-lg border border-border-default bg-surface-base px-2 text-sm text-content-primary"
                            >
                                <option value={5}>5 - Excellent</option>
                                <option value={4}>4 - Good</option>
                                <option value={3}>3 - Okay</option>
                                <option value={2}>2 - Needs work</option>
                                <option value={1}>1 - Poor</option>
                            </select>
                        </label>
                        <textarea
                            value={feedbackMessage}
                            onChange={(event) => setFeedbackMessage(event.target.value)}
                            className="h-16 w-full rounded-lg border border-border-default bg-surface-base px-2 py-1.5 text-xs text-content-primary"
                            placeholder="What should we improve?"
                        />
                        {feedbackAck && <p className="text-[11px] text-content-secondary">{feedbackAck}</p>}
                        <button
                            type="submit"
                            disabled={sendingFeedback}
                            className="h-8 w-full rounded-lg bg-primary text-white text-xs font-semibold disabled:opacity-60"
                        >
                            {sendingFeedback ? "Sending..." : "Send Feedback"}
                        </button>
                    </form>
                ) : (
                    <button
                        onClick={() => setFeedbackOpen(true)}
                        className="h-9 rounded-full border border-border-default bg-surface-base px-3 text-xs font-semibold text-content-secondary shadow-md hover:text-content-primary"
                    >
                        Feedback
                    </button>
                )}
            </div>
        </div>
    );
}
