import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Loader2, Sparkles } from 'lucide-react';
import { Terminal, LogEntry } from '../components/Terminal';
import { Navbar } from '../components/Navbar';
import { Background } from '../components/Background';

export const Dashboard: React.FC = () => {
    const [repoUrl, setRepoUrl] = useState('');
    const [task, setTask] = useState('');
    const [loading, setLoading] = useState(false);
    const [logs, setLogs] = useState<LogEntry[]>([
        { text: "> CodeSentinel Dashboard initialized. Standing by for assignment.", status: "INFO", color: "text-gray-400" }
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

    const handleStart = async () => {
        if (!repoUrl || !task) return;
        setLoading(true);
        setLogs([{ text: "> Initializing task execution...", status: "START", color: "text-blue-400" }]);
        try {
            await fetch('http://localhost:8000/execute-task', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ repo_url: repoUrl, task })
            });
        } catch (err) {
            console.error(err);
            setLogs(prev => [...prev, { text: "> Connection error. Is the backend running?", status: "ERROR", color: "text-red-400" }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="relative min-h-screen bg-[#050505] text-white selection:bg-violet-500/30 font-sans overflow-x-hidden">
            <Background />
            <Navbar />

            <main className="relative pt-32 pb-20 px-6 max-w-7xl mx-auto z-10">
                <div className="mb-12">
                    <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-violet-500/20 bg-violet-500/10 text-violet-400 text-[11px] font-bold tracking-wider uppercase mb-4">
                        <Sparkles className="w-3 h-3" />
                        <span>Operational Console</span>
                    </div>
                    <h1 className="text-4xl md:text-5xl font-bold tracking-tight">Deploy Assistant</h1>
                    <p className="text-gray-400 mt-2">Configure and launch your autonomous agent.</p>
                </div>

                <div className="grid lg:grid-cols-2 gap-12 items-start">
                    <motion.div
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        className="space-y-6"
                    >
                        <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-8 backdrop-blur-xl">
                            <div className="space-y-6">
                                <div>
                                    <label className="block text-xs font-bold uppercase tracking-widest text-gray-500 mb-2">Repository URL</label>
                                    <input
                                        type="text"
                                        placeholder="https://github.com/user/repo"
                                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-violet-500/50 transition-all font-mono text-sm"
                                        value={repoUrl}
                                        onChange={(e) => setRepoUrl(e.target.value)}
                                    />
                                </div>
                                <div>
                                    <label className="block text-xs font-bold uppercase tracking-widest text-gray-500 mb-2">Task Description</label>
                                    <textarea
                                        placeholder="E.g. Fix memory leak in auth middleware or Implement OAuth2 with Google"
                                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-4 text-white placeholder:text-gray-600 focus:outline-none focus:ring-2 focus:ring-violet-500/50 transition-all h-40 resize-none text-sm leading-relaxed"
                                        value={task}
                                        onChange={(e) => setTask(e.target.value)}
                                    />
                                </div>
                                <button
                                    onClick={handleStart}
                                    disabled={loading}
                                    className="w-full px-8 py-4 bg-white text-black font-bold rounded-xl overflow-hidden transition-all hover:bg-gray-200 active:scale-95 flex items-center justify-center gap-3 disabled:opacity-50"
                                >
                                    {loading ? (
                                        <>
                                            <Loader2 className="w-5 h-5 animate-spin" />
                                            Executing Protocol...
                                        </>
                                    ) : (
                                        <>
                                            Execute Task <ArrowRight className="w-4 h-4" />
                                        </>
                                    )}
                                </button>
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6">
                                <div className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-1">Status</div>
                                <div className="text-xl font-bold flex items-center gap-2">
                                    <div className={`w-2 h-2 rounded-full ${loading ? 'bg-amber-500 animate-pulse' : 'bg-green-500'}`} />
                                    {loading ? 'Active' : 'Standby'}
                                </div>
                            </div>
                            <div className="bg-white/[0.03] border border-white/10 rounded-2xl p-6">
                                <div className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-1">Compute</div>
                                <div className="text-xl font-bold">Safe Sandbox</div>
                            </div>
                        </div>
                    </motion.div>

                    <motion.div
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                    >
                        <div className="mb-4 flex items-center justify-between">
                            <span className="text-xs font-bold uppercase tracking-widest text-gray-500">Live Agent Stream</span>
                            <span className="text-[10px] mono text-violet-400 animate-pulse">Connection: Active</span>
                        </div>
                        <Terminal logs={logs} />
                    </motion.div>
                </div>
            </main>
        </div>
    );
};
