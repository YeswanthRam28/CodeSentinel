import React, { useState, useEffect } from 'react';
import { motion, Variants } from 'framer-motion';
import { Sparkles, ArrowRight, Loader2 } from 'lucide-react';
import { Link } from 'react-router-dom';
import { Terminal, LogEntry } from './Terminal';

const landingLogs: LogEntry[] = [
  { text: "> Fetching GitHub Issue #1042...", status: "WAIT", color: "text-gray-400" },
  { text: "> Cloning repository: /auth-service...", status: "DONE", color: "text-blue-400" },
  { text: "> Initializing AST context engine...", status: "OK", color: "text-green-400" },
  { text: "> Traversing dependency graph...", status: "OK", color: "text-green-400" },
  { text: "> Found: Unhandled JWT exception", status: "BUG", color: "text-red-400" },
  { text: "> Executing Docker sandbox session...", status: "RUN", color: "text-violet-400" },
  { text: "> Patching 'middleware/auth.ts'...", status: "FIX", color: "text-cyan-400" },
  { text: "> Running unit tests: 42 passed", status: "PASS", color: "text-green-400" },
  { text: "> Generating Pull Request summary...", status: "OK", color: "text-blue-400" },
  { text: "> SENTINEL: Task completed.", status: "IDLE", color: "text-white" },
];

export const Hero: React.FC = () => {
  const [visibleLogs, setVisibleLogs] = useState<LogEntry[]>([]);

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setVisibleLogs(landingLogs.slice(0, (i % landingLogs.length) + 1));
      i++;
    }, 1500);
    return () => clearInterval(interval);
  }, []);

  const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: { opacity: 1, transition: { staggerChildren: 0.2 } }
  };

  const itemVariants: Variants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }
    }
  };

  return (
    <section className="relative pt-44 pb-20 px-6 max-w-7xl mx-auto">
      <div className="grid lg:grid-cols-2 gap-16 items-center">
        <motion.div variants={containerVariants} initial="hidden" animate="visible" className="relative z-10">
          <motion.div variants={itemVariants} className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-violet-500/20 bg-violet-500/10 text-violet-400 text-[11px] font-bold tracking-wider uppercase mb-8">
            <Sparkles className="w-3 h-3" />
            <span>v2.0: Now with AST Self-Healing</span>
          </motion.div>

          <motion.h1 variants={itemVariants} className="text-6xl lg:text-8xl font-bold tracking-tight mb-8 leading-[0.9] text-transparent bg-clip-text bg-gradient-to-b from-white via-white to-gray-500 text-balance">
            Fix Bugs While You Sleep.
          </motion.h1>

          <motion.p variants={itemVariants} className="text-xl text-gray-400 mb-10 max-w-lg leading-relaxed font-light">
            CodeSentinel is an autonomous AI agent that clones your repo, analyzes AST structure, and merges PRs. No human input required.
          </motion.p>

          <motion.div variants={itemVariants} className="flex flex-col sm:flex-row gap-4">
            <Link to="/dashboard" className="px-8 py-4 bg-white text-black font-bold rounded-full overflow-hidden transition-all hover:bg-gray-200 active:scale-95 flex items-center justify-center gap-2">
              Get Started <ArrowRight className="w-4 h-4" />
            </Link>
            <button className="px-8 py-4 bg-white/5 border border-white/10 text-white font-bold rounded-full hover:bg-white/10 hover:border-white/20 transition-all active:scale-95">
              Watch Demo
            </button>
          </motion.div>

          <motion.div variants={itemVariants} className="mt-16 flex items-center gap-4 text-xs font-medium text-gray-500 uppercase tracking-widest">
            <span>Powered by</span>
            <div className="h-px w-12 bg-white/10" />
            <div className="flex gap-4 grayscale opacity-50">
              <span className="font-bold tracking-tighter">GEMINI 1.5</span>
              <span className="font-bold tracking-tighter">LANGGRAPH</span>
              <span className="font-bold tracking-tighter">DOCKER</span>
            </div>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1.2, ease: [0.16, 1, 0.3, 1] as [number, number, number, number] }}
          className="relative flex items-center justify-center"
        >
          <Terminal logs={visibleLogs} />
        </motion.div>
      </div>
    </section>
  );
};
