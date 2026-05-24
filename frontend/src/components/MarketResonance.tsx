import React from 'react';
import { TrendingUp, Target, BarChart3, ArrowUpRight } from 'lucide-react';

const MarketResonance: React.FC = () => {
    const trends = [
        { topic: "Minimalist Line Art", resonance: 92, status: "High Potential" },
        { topic: "Boho Textures", resonance: 78, status: "Steady" },
        { topic: "Geometric Bauhaus", resonance: 85, status: "Rising" }
    ];

    return (
        <div className="glass-card p-6 h-full">
            <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-[#00ffcc]" />
                Etsy Market Resonance
            </h3>

            <div className="space-y-4">
                {trends.map((trend, i) => (
                    <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#00ffcc]/30 transition-all group">
                        <div className="flex justify-between items-start mb-2">
                            <div>
                                <span className="text-xs font-bold text-[#00ffcc] uppercase tracking-wider">{trend.status}</span>
                                <h4 className="font-bold text-slate-200">{trend.topic}</h4>
                            </div>
                            <div className="text-right">
                                <div className="text-xl font-black text-white">{trend.resonance}%</div>
                                <div className="text-[10px] text-slate-500">Resonance Score</div>
                            </div>
                        </div>

                        <div className="w-full bg-white/5 h-1.5 rounded-full overflow-hidden mt-3">
                            <div
                                className="h-full bg-gradient-to-r from-[#00ffcc] to-[#5566ff] rounded-full transition-all duration-1000"
                                style={{ width: `${trend.resonance}%` }}
                            ></div>
                        </div>

                        <div className="flex justify-between items-center mt-3 opacity-0 group-hover:opacity-100 transition-opacity">
                            <span className="text-[10px] text-slate-400">Match quality: Optimal</span>
                            <button className="flex items-center gap-1 text-[10px] font-bold text-[#5566ff]">
                                ANALYZE ISOMORPHY <ArrowUpRight className="w-3 h-3" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-6 p-4 rounded-xl bg-[#5566ff]/10 border border-[#5566ff]/20">
                <div className="flex gap-3">
                    <div className="p-2 bg-[#5566ff]/20 rounded-lg h-fit">
                        <Target className="w-4 h-4 text-[#5566ff]" />
                    </div>
                    <div>
                        <div className="text-xs font-bold text-white mb-1">Aithentik Prediction</div>
                        <p className="text-[10px] text-slate-400 leading-relaxed">
                            Resonanz zwischen 'Lasur-Technik' und 'Minimalist Line Art' erreicht Peak. Empfehlung: Batch-Generierung von digitalen Kunstdrucken einleiten.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default MarketResonance;
