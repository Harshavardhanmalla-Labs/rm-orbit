import { useState, useRef, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { trackEvent } from '../utils/tracking';
import { useScrollDepth, useElementVisible, useHoverDuration } from '../hooks/useTracking';

export default function PredictionResult() {
  const location = useLocation();
  const navigate = useNavigate();

  const { decision, context, prediction, decisionId } = location.state || {};

  const [showLowConfidenceDetails, setShowLowConfidenceDetails] = useState(false);
  const topConfirmRef = useRef(null);
  const bottomConfirmRef = useRef(null);
  const insightsRef = useRef(null);
  const scrollTimeoutRef = useRef(null);
  const scrollDepthRef = useRef(0);

  useScrollDepth(decisionId);
  useElementVisible(insightsRef, 'insights', decisionId);

  // Track hesitation: 8+ seconds without action AND low scroll depth
  useEffect(() => {
    const checkHesitation = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = window.scrollY;
      const scrollDepth = scrollHeight > 0 ? Math.round((scrolled / scrollHeight) * 100) : 0;
      scrollDepthRef.current = scrollDepth;

      if (scrollDepth < 40) {
        trackEvent('hesitation_detected', 8000, decisionId);
      }
    };

    scrollTimeoutRef.current = setTimeout(checkHesitation, 8000);
    return () => clearTimeout(scrollTimeoutRef.current);
  }, [decisionId]);

  useHoverDuration(topConfirmRef, 'top_confirm_hovered', decisionId, 3000);
  useHoverDuration(bottomConfirmRef, 'bottom_confirm_hovered', decisionId, 3000);

  if (!prediction) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <p className="text-gray-600">No prediction data available</p>
      </div>
    );
  }

  const handleConfirm = (choice) => {
    trackEvent(
      'prediction_vs_user_choice',
      JSON.stringify({
        match: choice === prediction.recommendation,
        system_confidence: prediction.confidence,
        user_choice: choice,
        prediction: prediction.recommendation,
      }),
      decisionId
    );

    navigate('/confirmation', {
      state: {
        decision,
        choice,
        prediction,
        decisionId,
      },
    });
  };

  const handleAddContext = () => {
    trackEvent('add_context_clicked', 1, decisionId);
    navigate('/decide', { state: { decision, decisionId } });
  };

  return (
    <div className="min-h-screen bg-white px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <button
          onClick={() => navigate('/decide')}
          className="text-sm text-gray-600 hover:text-gray-900 mb-8"
        >
          ← Back
        </button>

        <div className="mb-12">
          <h2 className="text-sm font-medium text-gray-600 mb-2">Your decision</h2>
          <p className="text-gray-900">{decision}</p>
          {context.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-3">
              {context.map((c) => (
                <span key={c} className="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                  {c}
                </span>
              ))}
            </div>
          )}
        </div>

        {prediction.confidence >= 0.6 ? (
          // High confidence mode
          <div className="border border-gray-200 rounded-lg p-8 mb-8">
            <p className="text-sm text-gray-600 mb-4">My recommendation</p>
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              {prediction.recommendation}
            </h2>
            <p className="text-sm text-gray-600 mb-8">
              Confidence: {Math.round(prediction.confidence * 100)}%
            </p>

            {prediction.insights && prediction.insights.length > 0 && (
              <div className="mb-8 p-4 bg-gray-50 rounded">
                <p className="text-sm font-medium text-gray-900 mb-3">Why</p>
                <ul className="space-y-2">
                  {prediction.insights.map((insight, idx) => (
                    <li key={idx} className="text-sm text-gray-700">
                      • {insight}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <button
              onClick={() => handleConfirm(prediction.recommendation)}
              className="w-full py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition mb-3"
            >
              Go with {prediction.recommendation}
            </button>
            <button
              onClick={() => handleConfirm('USER_DECIDED_INDEPENDENTLY')}
              className="w-full py-3 border border-gray-300 text-gray-900 rounded-lg font-medium hover:bg-gray-50 transition mb-3"
            >
              I'll decide myself
            </button>
            <button
              onClick={handleAddContext}
              className="w-full text-sm py-2 text-gray-600 hover:text-gray-900 transition"
            >
              Add more context
            </button>
          </div>
        ) : (
          // Low confidence coaching mode
          <div>
            <h2 className="text-lg font-bold text-gray-900 mb-4">
              I don't have a strong pattern here yet.
            </h2>
            <p className="text-gray-800 mb-8">
              Your past decisions don't point strongly either way. I shouldn't pretend to be
              confident. So—what would you do?
            </p>

            <div className="space-y-3 mb-6">
              <div ref={topConfirmRef} className="p-4 bg-white rounded border border-gray-200">
                <p className="text-sm text-gray-700 mb-3">
                  If you want to move quickly: I lean toward <strong>{prediction.recommendation}</strong>.
                </p>
                <button
                  onClick={() => handleConfirm(prediction.recommendation)}
                  className="text-sm px-4 py-2 bg-gray-900 text-white rounded hover:bg-gray-800 transition"
                >
                  Go with {prediction.recommendation}
                </button>
              </div>

              <div
                ref={bottomConfirmRef}
                className="p-4 bg-white rounded border border-gray-200"
              >
                <p className="text-sm text-gray-700 mb-3">
                  If you'd rather decide yourself. You know this situation better than any pattern.
                </p>
                <button
                  onClick={() => handleConfirm('USER_DECIDED_INDEPENDENTLY')}
                  className="text-sm px-4 py-2 border border-gray-300 text-gray-900 rounded hover:bg-gray-50 transition"
                >
                  I'll decide myself
                </button>
              </div>

              <button
                onClick={handleAddContext}
                className="w-full text-sm px-4 py-2 text-gray-600 hover:text-gray-900 transition"
              >
                Add more context
              </button>
            </div>

            <div className="border-t border-gray-200 pt-4">
              <button
                onClick={() => {
                  setShowLowConfidenceDetails(!showLowConfidenceDetails);
                  trackEvent('low_confidence_details_expanded', !showLowConfidenceDetails, decisionId);
                }}
                className="text-sm font-medium text-gray-700 hover:text-gray-900 flex items-center gap-2"
              >
                {showLowConfidenceDetails ? '▼' : '▶'} See why this is unclear
              </button>

              {showLowConfidenceDetails && (
                <div ref={insightsRef} className="mt-4 space-y-3 text-xs text-gray-700">
                  {prediction?.insights && prediction.insights.length > 0 && (
                    <div>
                      <p className="font-medium text-gray-900 mb-2">
                        Signals toward {prediction.recommendation}
                      </p>
                      <ul className="space-y-1">
                        {prediction.insights.slice(0, 2).map((item, idx) => (
                          <li key={idx}>• {item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {prediction?.whyNot && prediction.whyNot.length > 0 && (
                    <div>
                      <p className="font-medium text-gray-900 mb-2">Signals against</p>
                      <ul className="space-y-1">
                        {prediction.whyNot.slice(0, 2).map((item, idx) => (
                          <li key={idx}>• {item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
