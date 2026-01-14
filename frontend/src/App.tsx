import { Header } from './components/Header'
import { Footer } from './components/Footer'
import { UploadPage } from './pages/UploadPage'

function App() {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />
      <main className="flex-grow">
        <UploadPage />
      </main>
      <Footer />
    </div>
  )
}

export default App
