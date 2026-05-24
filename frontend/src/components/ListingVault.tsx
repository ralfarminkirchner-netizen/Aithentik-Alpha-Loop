import React from 'react';
import { ShoppingBag, Copy, CheckCircle2, Sprout, Sparkles } from 'lucide-react';

const ListingVault: React.FC = () => {
    const listings = [
        {
            title: "Lasur-Mesh Abstract Canvas Print | Minimalist Line Art Aesthetics",
            resonance: 92,
            aeo_score: 98,
            tags: ["Abstract", "Minimalist", "Oil Layering", "Etsy Trend"],
            status: "READY"
        },
        {
            title: "Geometric Bauhaus 'Vaterkunst' Poster | Mid-Century Modern Vibes",
            resonance: 85,
            aeo_score: 94,
            tags: ["Bauhaus", "Geometric", "Primary Colors", "Modern Art"],
            status: "READY"
        }
    ];

    return (
        <div className="glass-card p-6 h-full flex flex-col">
            <h3 className="text-lg font-bold mb-6 flex items-center justify-between">
                <div className="flex items-center gap-2">
                    <ShoppingBag className="w-5 h-5 text-[#5566ff]" />
                    AI Listing Vault
                </div>
                <span className="text-[10px] font-mono text-slate-500 bg-white/5 px-2 py-1 rounded">AEO ENGINE v1.1</span>
            </h3>

            <div className="space-y-4 overflow-auto flex-1 pr-2">
                {listings.map((list, i) => (
                    <div key={i} className="p-4 rounded-xl bg-white/5 border border-white/10 hover:border-[#5566ff]/40 transition-all group relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-24 h-24 bg-[#5566ff]/5 blur-3xl -z-10 group-hover:bg-[#5566ff]/10"></div>

                        <div className="flex justify-between items-start mb-3">
                            <div className="flex items-center gap-2">
                                <CheckCircle2 className="w-4 h-4 text-[#00ffcc]" />
                                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-tighter">Validated Opportunity</span>
                            </div>
                            <div className="flex items-center gap-1">
                                <Sparkles className="w-3 h-3 text-[#5566ff]" />
                                <span className="text-xs font-black text-white">{list.aeo_score} AEO</span>
                            </div>
                        </div>

                        <h4 className="text-sm font-bold text-slate-200 mb-3 leading-tight">{list.title}</h4>

                        <div className="flex flex-wrap gap-1.5 mb-4">
                            {list.tags.map((tag, j) => (
                                <span key={j} className="text-[9px] bg-[#5566ff]/10 text-[#5566ff] px-2 py-0.5 rounded-full border border-[#5566ff]/20">
                                    #{tag}
                                </span>
                            ))}
                        </div>

                        <div className="flex gap-2">
                            <button className="flex-1 flex items-center justify-center gap-2 py-2 bg-[#5566ff]/20 hover:bg-[#5566ff]/30 text-[#5566ff] text-xs font-bold rounded-lg border border-[#5566ff]/30 transition-all">
                                <Copy className="w-3.5 h-3.5" /> COPY LISTING
                            </button>
                            <button className="px-3 py-2 bg-white/5 hover:bg-white/10 text-white rounded-lg border border-white/10 transition-all">
                                <Sprout className="w-3.5 h-3.5" />
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-6 pt-6 border-t border-white/5">
                <div className="text-[10px] text-slate-500 mb-2 font-mono">SYSTEM LOG: 2 NEW LISTINGS SYNTHESIZED</div>
                <div className="w-full h-1 bg-white/5 rounded-full overflow-hidden">
                    <div className="w-3/4 h-full bg-gradient-to-r from-[#5566ff] to-[#00ffcc] rounded-full"></div>
                </div>
            </div>
        </div>
    );
};

export default ListingVault;
