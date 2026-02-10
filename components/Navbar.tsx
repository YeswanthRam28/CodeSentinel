import React from 'react';
import { Shield, Github, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

export const Navbar: React.FC = () => {
  return (
    <div className="fixed top-0 left-0 right-0 z-50 flex justify-center p-6 pointer-events-none">
      <motion.nav
        initial={{ y: -20, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="pointer-events-auto flex items-center gap-8 px-6 py-3 rounded-full border border-white/10 bg-black/40 backdrop-blur-2xl shadow-2xl"
      >
        <Link to="/" className="flex items-center gap-2 group cursor-pointer">
          <Shield className="w-5 h-5 text-violet-500 group-hover:rotate-12 transition-transform" />
          <span className="text-sm font-bold tracking-tighter text-white">CodeSentinel</span>
        </Link>

        <div className="hidden md:flex items-center gap-6 text-[13px] font-medium text-gray-400">
          <Link to="/" className="hover:text-white transition-colors">Home</Link>
          <Link to="/dashboard" className="hover:text-white transition-colors">Dashboard</Link>
          <a href="#" className="hover:text-white transition-colors">Security</a>
        </div>

        <div className="flex items-center gap-4">
          <div className="w-[1px] h-4 bg-white/10" />
          <a href="https://github.com" className="text-gray-400 hover:text-white transition-colors">
            <Github className="w-4 h-4" />
          </a>
          <button className="flex items-center gap-1.5 px-3 py-1 text-[12px] font-semibold text-white bg-white/10 border border-white/10 rounded-full hover:bg-white/20 transition-all group">
            Login
            <ChevronRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
          </button>
        </div>
      </motion.nav>
    </div>
  );
};
