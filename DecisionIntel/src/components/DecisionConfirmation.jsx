import { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { trackEvent } from '../utils/tracking';
import FeedbackModal from './FeedbackModal';

export default function DecisionConfirmation() {
  const location = useLocation();
  const navigate = useNavigate();
  const { decision, choice, prediction, decisionId } = location.state || {};

  const [showFeedback, setShowFeedback] = useState(false);

  useEffect(() => {
    if (decisionId) {
      trackEvent('decision_confirmed', 1, decisionId);
    }
  }, [decisionId]);

  if (!decision) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <p className="text-gray-600">No decision data available</p>
      </div>
    );
  }

  if (showFeedback) {
    return <FeedbackModal decisionId={decisionId} onClose={() => navigate('/')} />;
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center">
        <div className="mb-8">
          <div className="text-4xl mb-6">✓</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">Decision recorded.</h1>
          <p className="text-gray-600 mb-2">You chose: <strong>{choice}</strong></p>
          <p className="text-lg text-gray-700 font-medium">You moved fast. That's the goal.</p>
        </div>

        <button
          onClick={() => setShowFeedback(true)}
          className="px-8 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition"
        >
          Give feedback
        </button>

        <button
          onClick={() => navigate('/')}
          className="block mt-4 text-gray-600 hover:text-gray-900 text-sm transition"
        >
          Make another decision
        </button>
      </div>
    </div>
  );
}
