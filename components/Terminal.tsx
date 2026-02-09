
import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const logs = [
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

export const Terminal: React.FC = () => {
  const [visibleLogs, setVisibleLogs] = useState<number>(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setVisibleLogs((prev) => (prev < logs.length ? prev + 1 : 1));
    }, 1500);
    return () => clearInterval(timer);
  }, []);

  return (
    <motion.div 
      animate={{ y: [0, -15, 0] }}
      transition={{ duration: 6, repeat: Infinity, ease: "easeInOut" }}
      className="w-full max-w-xl mx-auto"
    >
      <div className="relative group perspective-1000">
        <div className="absolute -inset-0.5 bg-gradient-to-r from-violet-500 to-cyan-500 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-1000"></div>
        
        <div className="relative bg-[#050505]/90 backdrop-blur-2xl border border-white/10 rounded-2xl overflow-hidden shadow-2xl shadow-black">
          {/* Mac-style Window Bar */}
          <div className="flex items-center justify-between px-5 py-4 bg-white/[0.03] border-b border-white/10">
            <div className="flex gap-2">
              <div className="w-3 h-3 rounded-full bg-[#ff5f56]" />
              <div className="w-3 h-3 rounded-full bg-[#ffbd2e]" />
              <div className="w-3 h-3 rounded-full bg-[#27c93f]" />
            </div>
            <div className="text-[10px] mono text-gray-500 font-semibold tracking-[0.2em] uppercase">
              codesentinel.sh — 80×24
            </div>
            <div className="w-12" />
          </div>

          {/* Terminal Content */}
          <div className="p-8 h-[380px] overflow-hidden mono text-[13px] leading-relaxed">
            <AnimatePresence mode="popLayout">
              {logs.slice(0, visibleLogs).map((log, i) => (
                <motion.div
                  key={`${i}-${log.text}`}
                  initial={{ opacity: 0, x: -10 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="mb-3 flex items-start gap-4"
                >
                  <span className={`shrink-0 font-bold ${log.color}`}>[{log.status}]</span>
                  <span className="text-gray-300 font-medium">{log.text}</span>
                </motion.div>
              ))}
            </AnimatePresence>
            
            <motion.div
              animate={{ opacity: [1, 0] }}
              transition={{ duration: 0.8, repeat: Infinity }}
              className="w-2 h-5 bg-violet-500 inline-block align-middle ml-1"
            />
          </div>
        </div>
      </div>
    </motion.div>
  );
};
