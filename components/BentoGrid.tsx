
import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Container, Zap, GitPullRequest } from 'lucide-react';

const features = [
  {
    title: "Context-Aware Brain",
    description: "CodeSentinel uses AST (Abstract Syntax Tree) parsing to build a mental map of your entire repo. It doesn't just guess; it understands the flow.",
    icon: Brain,
    className: "md:col-span-2",
    accent: "violet"
  },
  {
    title: "Isolated Sandbox",
    description: "Every operation runs in a fresh Docker container. Zero risk to your host machine.",
    icon: Container,
    className: "md:col-span-1",
    accent: "cyan"
  },
  {
    title: "PR Automation",
    description: "Once tests pass, it handles the merge request, changelog, and documentation.",
    icon: GitPullRequest,
    className: "md:col-span-1",
    accent: "violet"
  },
  {
    title: "Self-Healing Loop",
    description: "If a test fails, the agent analyzes the stack trace and fixes its own mistakes in real-time.",
    icon: Zap,
    className: "md:col-span-2",
    accent: "cyan"
  }
];

export const BentoGrid: React.FC = () => {
  return (
    <section className="max-w-7xl mx-auto px-6 py-32">
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-16 gap-8">
        <div>
          <h2 className="text-4xl md:text-5xl font-bold text-white mb-6 tracking-tight">Technical Superiority.</h2>
          <p className="text-gray-400 max-w-xl text-lg font-light leading-relaxed">
            Engineered with a focus on safety and precision. We don't just generate snippets; we solve architecture.
          </p>
        </div>
        <button className="text-sm font-bold text-violet-400 hover:text-violet-300 transition-colors flex items-center gap-2 group">
          EXPLORE TECH STACK <div className="w-12 h-px bg-violet-500/30 group-hover:w-16 transition-all" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {features.map((feature, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ delay: i * 0.1 }}
            whileHover={{ scale: 1.01 }}
            className={`relative group p-10 rounded-[32px] border border-white/10 bg-white/[0.03] backdrop-blur-md overflow-hidden ${feature.className}`}
          >
            {/* Background Accent Glow */}
            <div className={`absolute -top-20 -right-20 p-24 bg-${feature.accent}-500/5 blur-[100px] rounded-full group-hover:bg-${feature.accent}-500/10 transition-colors duration-700`} />
            
            <div className="relative z-10 h-full flex flex-col">
              <div className="w-14 h-14 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-center mb-8 shadow-inner">
                <feature.icon className={`w-7 h-7 text-${feature.accent}-400`} />
              </div>
              <h3 className="text-2xl font-bold text-white mb-4 tracking-tight">{feature.title}</h3>
              <p className="text-gray-400 leading-relaxed font-light text-base">{feature.description}</p>
              
              <div className="mt-auto pt-8">
                <div className="w-full h-px bg-white/5 group-hover:bg-white/10 transition-colors" />
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </section>
  );
};
