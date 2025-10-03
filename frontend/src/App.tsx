import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import ChatPage from './pages/ChatPage'
import SearchPage from './pages/SearchPage'
import { Toaster } from './components/ui/toaster'

function App() {
  return (
    <Router
      future={{
        v7_startTransition: true,
        v7_relativeSplatPath: true,
      }}
    >
      <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
        <Routes>
          <Route path="/" element={<ChatPage />} />
          <Route path="/search" element={<SearchPage />} />
        </Routes>
        <Toaster />
      </div>
    </Router>
  )
}

export default App
