import { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { generateDecisionId, trackEvent } from '../utils/tracking';

const CONTEXT_SUGGESTIONS = [
  'Time pressure',
  'Budget constraint',
  'Team input',
  'Data available',
  'Risk factor',
];

function generateMockPrediction(decisionText) {
  const options = ['Option A', 'Option B'];
  const recommendation = options[Math.random() > 0.5 ? 0 : 1];
  const confidence = Math.random() * 0.8 + 0.2;

  const insights =
    confidence > 0.6
      ? [
          'Similar pattern from 3 past decisions',
          'Aligns with your stated goals',
          'Matches peer recommendations',
        ]
      : ['Unclear signal from history', 'Few comparable precedents'];

  const whyNot =
    confidence > 0.6 ? ['Some uncertainty in context'] : ['Multiple competing patterns'];

  return {
    recommendation,
    confidence: parseFloat(confidence.toFixed(2)),
    insights,
    whyNot,
  };
}

export default function Decide() {
  const navigate = useNavigate();
  const decisionIdRef = useRef(generateDecisionId());
  const debounceTimerRef = useRef(null);

  const [decision, setDecision] = useState('');
  const [context, setContext] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleDecisionChange = (e) => {
    const value = e.target.value;
    setDecision(value);

    if (debounceTimerRef.current) clearTimeout(debounceTimerRef.current);
    debounceTimerRef.current = setTimeout(() => {
      if (value.trim().length > 0) {
        trackEvent('decision_started', value.trim().length, decisionIdRef.current);
      }
    }, 1000);
  };

  const toggleContext = (chip) => {
    setContext((prev) =>
      prev.includes(chip) ? prev.filter((c) => c !== chip) : [...prev, chip]
    );
    trackEvent('context_added', 1, decisionIdRef.current);
  };

  const handleSubmit = async () => {
    if (decision.trim().length === 0) return;

    setIsLoading(true);

    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 800));

    const prediction = generateMockPrediction(decision);

    trackEvent('decision_submitted', decision.length, decisionIdRef.current);

    navigate('/prediction', {
      state: {
        decision,
        context,
        prediction,
        decisionId: decisionIdRef.current,
      },
    });
  };

  const isReady = decision.trim().length > 0;

  return (
    <div className="min-h-screen bg-white px-4 py-8">
      <div className="max-w-2xl mx-auto">
        <button
          onClick={() => navigate('/')}
          className="text-sm text-gray-600 hover:text-gray-900 mb-8"
        >
          ← Back
        </button>

        <h1 className="text-3xl font-bold text-gray-900 mb-2">What's your decision?</h1>
        <p className="text-gray-600 mb-8">
          Be clear and specific about what you're deciding.
        </p>

        <textarea
          value={decision}
          onChange={handleDecisionChange}
          placeholder="Should I... Accept the job offer? Launch the feature? Change my approach?"
          className="w-full px-4 py-3 border border-gray-200 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 mb-8 resize-none h-24"
        />

        <div>
          <label className="block text-sm font-medium text-gray-900 mb-3">
            Context (optional)
          </label>
          <div className="flex flex-wrap gap-2 mb-8">
            {CONTEXT_SUGGESTIONS.map((chip) => (
              <button
                key={chip}
                onClick={() => toggleContext(chip)}
                className={`px-3 py-1 rounded-full text-sm transition ${
                  context.includes(chip)
                    ? 'bg-gray-900 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {chip}
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleSubmit}
          disabled={!isReady || isLoading}
          className={`w-full py-3 rounded-lg font-medium text-white transition ${
            isReady && !isLoading
              ? 'bg-gray-900 hover:bg-gray-800'
              : 'bg-gray-400 cursor-not-allowed'
          }`}
        >
          {isLoading ? 'Thinking...' : 'Get guidance'}
        </button>
      </div>
    </div>
  );
}
