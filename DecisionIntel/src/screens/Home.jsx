import { useNavigate } from 'react-router-dom';
import { trackEvent } from '../utils/tracking';

export default function Home() {
  const navigate = useNavigate();

  const handleStart = () => {
    trackEvent('home_cta_clicked', 1);
    navigate('/decide');
  };

  return (
    <div className="min-h-screen bg-white flex items-center justify-center px-4">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          Decide faster.
        </h1>

        <p className="text-lg text-gray-600 mb-12 leading-relaxed">
          Get intelligent guidance on your decisions based on your past choices and patterns.
        </p>

        <button
          onClick={handleStart}
          className="px-8 py-4 bg-gray-900 text-white rounded-lg font-medium text-lg hover:bg-gray-800 transition"
        >
          Make a decision
        </button>

        <div className="mt-12 pt-12 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            Your decisions stay private. No data is stored.
          </p>
        </div>
      </div>
    </div>
  );
}
