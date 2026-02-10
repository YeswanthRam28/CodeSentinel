import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { BentoGrid } from './components/BentoGrid';
import { Pipeline } from './components/Pipeline';
import { Marquee } from './components/Marquee';
import { Footer } from './components/Footer';
import { Background } from './components/Background';
import { LogEntry } from './components/Terminal';

const App: React.FC = () => {
  const [logs, setLogs] = useState<LogEntry[]>([
    { text: "> CodeSentinel initialized. Standing by for assignment.", status: "INFO", color: "text-gray-400" }
  ]);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws');

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        setLogs(prev => [...prev.slice(-9), data]); // Keep last 10 logs
      } catch (e) {
        console.error("Failed to parse WS message", e);
      }
    };

    return () => ws.close();
  }, []);

  return (
    <div className="relative min-h-screen bg-[#050505] selection:bg-violet-500/30 font-sans">
      <Background />
      <Navbar />
      <main>
        <Hero logs={logs} />
        <Marquee />
        <BentoGrid />
        <Pipeline />
      </main>
      <Footer />
    </div>
  );
};

export default App;
