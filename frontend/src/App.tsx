import React, { useState } from 'react';
import { Zap, DollarSign, Activity, LayoutDashboard, ShoppingBag } from 'lucide-react';
import CashScoreCalculator from './components/CashScoreCalculator';
import OpportunityFlow from './components/OpportunityFlow';
import ArchitectureVisualization from './components/ArchitectureVisualization';
import MarketResonance from './components/MarketResonance';
import ListingVault from './components/ListingVault';

const App: React.FC = () => {
    const [activeTab, setActiveTab] = useState('dashboard');
    const [learningLog] = useState<string[]>([
        "✅ DNA-Verdichtung für 'Vaterkunst' abgeschlossen.",
        "🌐 Scout fand Etsy V3 API Spezifikationen.",
        "🌩️ Myzel-Resonanz zwischen 'Lasur' und 'UI-Layer' berechnet.",
        "🧠 System-Lernen: Isomorphie-Datenbank erweitert (+12).",
        "✨ AI-Synthesis: Listing für 'Lasur-Mesh' generiert (AEO: 98)."
    ]);

    return (
        <div className="min-h-screen bg-[#050508] text-white flex">
            {/* Sidebar */}
            <aside className="w-64 border-r border-white/10 bg-[#0c0c1c] flex flex-col p-6">
                <div className="flex items-center gap-3 mb-12">
                    <Zap className="text-[#00ffcc] w-8 h-8" />
                    <h1 className="text-xl font-bold tracking-tight">ALPHA-LOOP</h1>
                </div>

                <nav className="flex-1 space-y-2">
                    {[
                        { id: 'dashboard', icon: LayoutDashboard, label: 'Dashboard' },
                        { id: 'vault', icon: ShoppingBag, label: 'Listing Vault' },
                        { id: 'cash', icon: DollarSign, label: 'Cash Flow' },
                        { id: 'patterns', icon: Activity, label: 'Patterns' },
                    ].map((item) => (
                        <button
                            key={item.id}
                            onClick={() => setActiveTab(item.id)}
                            className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${activeTab === item.id ? 'bg-[#5566ff]/20 text-[#5566ff] border border-[#5566ff]/30' : 'text-slate-400 hover:text-white'
                                }`}
                        >
                            <item.icon className="w-5 h-5" />
                            <span className="font-medium">{item.label}</span>
                        </button>
                    ))}
                </nav>

                <div className="mt-auto pt-6 border-t border-white/5">
                    <div className="text-xs text-slate-500 uppercase tracking-widest mb-4">Governor Status</div>
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-[#00ffcc] animate-pulse"></div>
                        <span className="text-sm">Active & Learning</span>
                    </div>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 p-10 overflow-auto">
                <header className="flex justify-between items-end mb-12">
                    <div>
                        <h2 className="text-4xl font-bold mb-2">Myzel Core</h2>
                        <p className="text-slate-400">Gnadenlose Kapital-Maximierung & Mustererkennung.</p>
                    </div>
                    <button className="px-6 py-3 bg-[#00ffcc] text-black font-bold rounded-xl hover:shadow-[0_0_20px_rgba(0,255,204,0.5)] transition-all">
                        🌀 GLOBAL PULSE
                    </button>
                </header>

                {activeTab === 'dashboard' && (
                    <div className="grid grid-cols-12 gap-6">
                        <div className="col-span-8 h-[500px] glass-card overflow-hidden">
                            <ArchitectureVisualization />
                        </div>
                        <div className="col-span-4 h-[500px]">
                            <MarketResonance />
                        </div>

                        <div className="col-span-4 space-y-6">
                            <CashScoreCalculator />
                            <div className="glass-card p-6 h-[260px]">
                                <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                                    <Activity className="w-5 h-5 text-[#7755ff]" />
                                    Learning Log
                                </h3>
                                <div className="space-y-3 font-mono text-sm overflow-auto max-h-[160px]">
                                    {learningLog.map((log, i) => (
                                        <div key={i} className="text-[#00ffcc]/80 border-l border-white/10 pl-3 py-1">
                                            {log}
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                        <div className="col-span-8 h-[550px]">
                            <ListingVault />
                        </div>
                        <div className="col-span-12">
                            <OpportunityFlow />
                        </div>
                    </div>
                )}

                {activeTab === 'vault' && (
                    <div className="max-w-4xl mx-auto">
                        <ListingVault />
                    </div>
                )}
            </main>
        </div>
    );
};

export default App;
