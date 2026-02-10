import React, { useState } from 'react';
import { motion, Variants } from 'framer-motion';
import { Sparkles, ArrowRight, Loader2 } from 'lucide-react';
import { Terminal, LogEntry } from './Terminal';

interface HeroProps {
  logs: LogEntry[];
}

export const Hero: React.FC<HeroProps> = ({ logs }) => {
  const [repoUrl, setRepoUrl] = useState('');
  const [task, setTask] = useState('');
  const [loading, setLoading] = useState(false);

  const handleStart = async () => {
    if (!repoUrl || !task) return;
    setLoading(true);
    try {
      await fetch('http://localhost:8000/execute-task', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ repo_url: repoUrl, task })
      });
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

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
            Deploy CodeSentinel to any GitHub repo. It plan, researches, and fixes bugs autonomously in a secure sandbox.
          </motion.p>

          <motion.div variants={itemVariants} className="space-y-4 max-w-md">
            <div className="relative">
              <input
                type="text"
                placeholder="GitHub Repo URL (e.g., https://github.com/user/repo)"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500/50 transition-all"
                value={repoUrl}
                onChange={(e) => setRepoUrl(e.target.value)}
              />
            </div>
            <div className="relative">
              <textarea
                placeholder="Assigned Task (e.g., Fix the JWT exception in middleware)"
                className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-white placeholder:text-gray-500 focus:outline-none focus:ring-2 focus:ring-violet-500/50 transition-all h-24 resize-none"
                value={task}
                onChange={(e) => setTask(e.target.value)}
              />
            </div>
            <button
              onClick={handleStart}
              disabled={loading}
              className="w-full px-8 py-4 bg-white text-black font-bold rounded-xl overflow-hidden transition-all hover:bg-gray-200 active:scale-95 flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <>Deploy Sentinel <ArrowRight className="w-4 h-4" /></>}
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
          <Terminal logs={logs} />
        </motion.div>
      </div>
    </section>
  );
};
