import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './screens/Home';
import Decide from './screens/Decide';
import PredictionResult from './screens/PredictionResult';
import DecisionConfirmation from './components/DecisionConfirmation';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/decide" element={<Decide />} />
        <Route path="/prediction" element={<PredictionResult />} />
        <Route path="/confirmation" element={<DecisionConfirmation />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
