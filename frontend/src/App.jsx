import "./App.css"

function App(){
  return(
    <div className="app">
      
      <header className="topbar">

        <h1 className="logo">ChronoGlossa</h1>
        <nav className="nav">
          
          <a href="#">Learn</a>
          <a href="#">Practice</a>
          <a href="#">Profile</a>
          
        </nav>
      </header>
      
      <main className="main-content">
        
        <section className="hero">

          <p className="eyebrow">YOUR LANGUAGE LEARNING JOURNEY STARTS HERE</p>
          
          <h2>Keep learning.</h2>
          
          <p className="hero-text">small steps, every day</p>

          <button className="practice-button">
            Continue Practice
          </button>

        </section>
        <section className="stats">
          <div className="stat-card">
          <p>Mastery</p>
          <strong>0%</strong>
          </div>
          <div className="stat-card">
            <p>Words</p>
            <strong>0</strong>
          </div>
          <div className="stat-card">
            <p>Accuracy</p>
            <strong>-</strong>
          </div>
        </section>
        <section className="practice-card">
          <p className="eyebrow">PRACTICE</p>

          <h3>Review what needs attention.</h3>

          <p>
            Chronoglossa will bring you less familiar words
            forward first.
          </p>
        </section>
      </main>
    </div>
  )
}

export default App