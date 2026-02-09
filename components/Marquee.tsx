
import React from 'react';

const techs = [
  "Python", "Docker", "LangChain", "Next.js", "Gemini 1.5", "PostgreSQL", 
  "AST Parsing", "Rust", "GitHub API", "OpenAI", "K8s", "Terraform"
];

export const Marquee: React.FC = () => {
  return (
    <div className="py-20 bg-white/[0.01] border-y border-white/5 relative overflow-hidden group">
      <div className="absolute inset-y-0 left-0 w-40 bg-gradient-to-r from-[#050505] to-transparent z-10" />
      <div className="absolute inset-y-0 right-0 w-40 bg-gradient-to-l from-[#050505] to-transparent z-10" />
      
      <div className="flex animate-marquee whitespace-nowrap gap-12">
        {[...techs, ...techs].map((tech, i) => (
          <span 
            key={i} 
            className="text-2xl md:text-3xl font-black uppercase tracking-tighter text-gray-800 hover:text-gray-500 transition-colors cursor-default"
          >
            {tech}
          </span>
        ))}
      </div>

      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          animation: marquee 30s linear infinite;
        }
      `}</style>
    </div>
  );
};
