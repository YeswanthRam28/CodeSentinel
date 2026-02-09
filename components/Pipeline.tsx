
import React from 'react';
import { motion } from 'framer-motion';
import { Github, Cpu, Box, CheckCircle } from 'lucide-react';

const steps = [
  { icon: Github, label: "GitHub Issue", color: "text-gray-400" },
  { icon: Cpu, label: "Agent Planner", color: "text-violet-400" },
  { icon: Box, label: "Docker Sandbox", color: "text-cyan-400" },
  { icon: CheckCircle, label: "Verified PR", color: "text-green-400" },
];

export const Pipeline: React.FC = () => {
  return (
    <section className="max-w-7xl mx-auto px-6 py-32 overflow-hidden">
      <div className="text-center mb-20">
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">Autonomous Pipeline</h2>
        <p className="text-gray-400">From problem to solution, fully automated.</p>
      </div>

      <div className="relative flex flex-col md:flex-row items-center justify-between gap-12 md:gap-4 max-w-5xl mx-auto">
        {/* Connection Beams (Desktop) */}
        <div className="absolute top-1/2 left-0 right-0 -translate-y-1/2 hidden md:block z-0 px-20">
          <svg className="w-full h-2 overflow-visible">
            <motion.path
              d="M 0 4 H 800"
              stroke="url(#gradient)"
              strokeWidth="2"
              fill="none"
              strokeDasharray="10 10"
              initial={{ pathLength: 0, opacity: 0 }}
              whileInView={{ pathLength: 1, opacity: 1 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            />
            <defs>
              <linearGradient id="gradient" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0%" stopColor="#8B5CF6" />
                <stop offset="100%" stopColor="#06B6D4" />
              </linearGradient>
            </defs>
          </svg>
        </div>

        {steps.map((step, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.2 }}
            className="relative z-10 flex flex-col items-center group"
          >
            <div className="w-20 h-20 rounded-2xl bg-[#0d1117] border border-white/10 flex items-center justify-center mb-4 group-hover:border-violet-500/50 transition-colors shadow-2xl">
              <step.icon className={`w-8 h-8 ${step.color}`} />
            </div>
            <span className="text-sm font-semibold text-white tracking-tight">{step.label}</span>
            <div className="mt-2 text-[10px] text-gray-500 mono uppercase tracking-widest">Phase 0{i+1}</div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};
