import { useState } from 'react';
import { trackEvent } from '../utils/tracking';

export default function FeedbackModal({ decisionId, onClose }) {
  const [page, setPage] = useState(0);
  const [responses, setResponses] = useState({
    helped_decide_faster: null,
    most_helpful: '',
    confusing: '',
    trust_score: null,
    use_again: null,
    do_differently: '',
  });

  const [submitted, setSubmitted] = useState(false);

  const questions = [
    {
      key: 'helped_decide_faster',
      question: 'Did this help you decide faster?',
      type: 'yesno',
    },
    {
      key: 'most_helpful',
      question: 'What was most helpful?',
      type: 'text',
      placeholder: 'e.g., The recommendation, seeing the reasoning, being honest about uncertainty...',
    },
    {
      key: 'confusing',
      question: 'What was confusing or unclear?',
      type: 'text',
      placeholder: 'Optional. What could we improve?',
    },
    {
      key: 'trust_score',
      question: 'How much did you trust this guidance?',
      type: 'scale',
      min: 1,
      max: 5,
    },
    {
      key: 'use_again',
      question: 'Would you use this again?',
      type: 'yesno',
    },
    {
      key: 'do_differently',
      question: 'What would you do differently?',
      type: 'text',
      placeholder: 'Optional. Any other feedback?',
    },
  ];

  const currentQuestion = questions[page];

  const handleYesNo = (key, value) => {
    setResponses((prev) => ({ ...prev, [key]: value }));
    trackEvent(`feedback_${key}`, value ? 'yes' : 'no', decisionId);
    setTimeout(() => setPage(page + 1), 300);
  };

  const handleText = (key, value) => {
    setResponses((prev) => ({ ...prev, [key]: value }));
  };

  const handleScale = (key, value) => {
    setResponses((prev) => ({ ...prev, [key]: value }));
    trackEvent(`feedback_${key}`, value, decisionId);
    setTimeout(() => setPage(page + 1), 300);
  };

  const handleTextNext = () => {
    trackEvent(`feedback_${currentQuestion.key}`, responses[currentQuestion.key].length, decisionId);
    setPage(page + 1);
  };

  const handleSubmit = () => {
    trackEvent('feedback_submitted', JSON.stringify(responses), decisionId);
    setSubmitted(true);
    setTimeout(onClose, 2000);
  };

  const canProceed = () => {
    if (currentQuestion.type === 'yesno' || currentQuestion.type === 'scale') {
      return responses[currentQuestion.key] !== null;
    }
    return true;
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center px-4">
        <div className="max-w-2xl w-full text-center">
          <div className="text-4xl mb-6">✓</div>
          <h1 className="text-2xl font-bold text-gray-900">Thank you for your feedback.</h1>
          <p className="text-gray-600 mt-4">We'll use this to improve.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4">
      <div className="max-w-2xl w-full">
        <div className="mb-8">
          <div className="flex gap-1 mb-4">
            {questions.map((_, idx) => (
              <div
                key={idx}
                className={`flex-1 h-1 rounded-full transition ${
                  idx < page ? 'bg-gray-900' : idx === page ? 'bg-gray-400' : 'bg-gray-200'
                }`}
              />
            ))}
          </div>
          <p className="text-xs text-gray-600">
            {page + 1} of {questions.length}
          </p>
        </div>

        <h2 className="text-2xl font-bold text-gray-900 mb-8">{currentQuestion.question}</h2>

        {currentQuestion.type === 'yesno' && (
          <div className="flex gap-3">
            <button
              onClick={() => handleYesNo(currentQuestion.key, true)}
              className="flex-1 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition"
            >
              Yes
            </button>
            <button
              onClick={() => handleYesNo(currentQuestion.key, false)}
              className="flex-1 py-3 border border-gray-300 text-gray-900 rounded-lg font-medium hover:bg-gray-50 transition"
            >
              No
            </button>
          </div>
        )}

        {currentQuestion.type === 'text' && (
          <div>
            <textarea
              value={responses[currentQuestion.key]}
              onChange={(e) => handleText(currentQuestion.key, e.target.value)}
              placeholder={currentQuestion.placeholder}
              className="w-full px-4 py-3 border border-gray-200 rounded-lg text-gray-900 placeholder-gray-500 focus:outline-none focus:border-gray-900 focus:ring-1 focus:ring-gray-900 resize-none h-20 mb-4"
            />
            <button
              onClick={handleTextNext}
              className="w-full py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition"
            >
              Next
            </button>
          </div>
        )}

        {currentQuestion.type === 'scale' && (
          <div>
            <div className="flex gap-2 mb-8">
              {[1, 2, 3, 4, 5].map((num) => (
                <button
                  key={num}
                  onClick={() => handleScale(currentQuestion.key, num)}
                  className={`flex-1 py-3 rounded-lg font-medium transition ${
                    responses[currentQuestion.key] === num
                      ? 'bg-gray-900 text-white'
                      : 'border border-gray-300 text-gray-900 hover:bg-gray-50'
                  }`}
                >
                  {num}
                </button>
              ))}
            </div>
            <p className="text-sm text-gray-600 text-center">
              <span className="block float-left">Low</span>
              <span className="block float-right">High</span>
            </p>
          </div>
        )}

        {page === questions.length && (
          <button
            onClick={handleSubmit}
            className="w-full py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition"
          >
            Submit feedback
          </button>
        )}
      </div>
    </div>
  );
}
