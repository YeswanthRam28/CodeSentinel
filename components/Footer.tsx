
import React from 'react';
import { Shield, Github, Twitter, Linkedin } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="border-t border-white/5 py-12 px-6">
      <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
        <div className="flex items-center gap-2">
          <Shield className="w-6 h-6 text-violet-500" />
          <span className="text-xl font-bold text-white tracking-tighter">CodeSentinel</span>
        </div>

        <div className="flex gap-8 text-sm text-gray-500">
          <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
          <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
          <a href="#" className="hover:text-white transition-colors">Security</a>
        </div>

        <div className="flex gap-4">
          <a href="#" className="p-2 bg-white/5 rounded-full hover:bg-white/10 transition-colors">
            <Github className="w-5 h-5 text-gray-400" />
          </a>
          <a href="#" className="p-2 bg-white/5 rounded-full hover:bg-white/10 transition-colors">
            <Twitter className="w-5 h-5 text-gray-400" />
          </a>
          <a href="#" className="p-2 bg-white/5 rounded-full hover:bg-white/10 transition-colors">
            <Linkedin className="w-5 h-5 text-gray-400" />
          </a>
        </div>
      </div>
      <div className="max-w-7xl mx-auto mt-8 text-center text-xs text-gray-700">
        &copy; {new Date().getFullYear()} CodeSentinel AI. All rights reserved. Built for the future of DevOps.
      </div>
    </footer>
  );
};
