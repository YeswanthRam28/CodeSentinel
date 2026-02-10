import React from 'react';
import { Navbar } from '../components/Navbar';
import { Hero } from '../components/Hero';
import { BentoGrid } from '../components/BentoGrid';
import { Pipeline } from '../components/Pipeline';
import { Marquee } from '../components/Marquee';
import { Footer } from '../components/Footer';
import { Background } from '../components/Background';

export const Landing: React.FC = () => {
    return (
        <div className="relative min-h-screen bg-[#050505] selection:bg-violet-500/30 font-sans">
            <Background />
            <Navbar />
            <main>
                <Hero />
                <Marquee />
                <BentoGrid />
                <Pipeline />
            </main>
            <Footer />
        </div>
    );
};
