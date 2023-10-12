
import './App.css';
import Header from './Components/Header/Header';
import { Routes, Route, useNavigate, useLocation } from 'react-router-dom';
import TextToSpeech from './Components/TextToSpeech/TextToSpeech';
import SpeechToSpeech from './Components/SpeechToSpeech/SpeechToSpeech';
import { useEffect } from 'react';

function App() {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (location.pathname === '/') {
      navigate('/text-to-speech');
    }
  }, [navigate, location]);


  return (
      <div>
        <Header />
        <Routes>
          <Route path='/text-to-speech' element={<TextToSpeech />} />
          <Route path='/speech-to-speech' element={<SpeechToSpeech />} />
        </Routes>
      </div>
  )
}

export default App;
