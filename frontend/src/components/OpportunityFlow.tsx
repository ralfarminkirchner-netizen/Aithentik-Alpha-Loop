import React from 'react';
import { ArrowRight, Cpu } from 'lucide-react';

const OpportunityFlow: React.FC = () => {
    return (
        <div className="glass-card p-8">
            <h3 className="text-xl font-bold mb-8">Opportunity Flow: Vaterkunst IP</h3>

            <div className="flex items-center gap-4">
                {/* Step 1: Input */}
                <div className="flex-1 p-6 border border-white/10 rounded-2xl bg-white/5 relative group">
                    <div className="absolute -top-3 left-4 bg-[#5566ff] text-[10px] font-bold px-2 py-1 rounded">RAW INPUT</div>
                    <p className="text-sm text-slate-300">"10.000 Skizzen von Vater - Fragmentierung in Etsy-Kataloge."</p>
                    <div className="mt-4 flex items-center gap-2 text-[10px] text-slate-500">
                        <Cpu className="w-3 h-3" /> DNA STRIpping active...
                    </div>
                </div>

                <ArrowRight className="text-slate-700" />

                {/* Step 2: DNA */}
                <div className="flex-1 p-6 border border-[#00ffcc]/30 rounded-2xl bg-[#00ffcc]/5 relative">
                    <div className="absolute -top-3 left-4 bg-[#00ffcc] text-black text-[10px] font-bold px-2 py-1 rounded">AXIOM DNA</div>
                    <div className="space-y-2">
                        <div className="bg-black/40 p-2 rounded text-[10px] font-mono border border-white/5">PATTERN: Multi-Layer-Scarcity</div>
                        <div className="bg-black/40 p-2 rounded text-[10px] font-mono border border-white/5">MECHANIC: Fractional IP Ownership</div>
                    </div>
                </div>

                <ArrowRight className="text-slate-700" />

                {/* Step 3: Resonance */}
                <div className="flex-1 p-6 border border-[#7755ff]/30 rounded-2xl bg-[#7755ff]/5 relative">
                    <div className="absolute -top-3 left-4 bg-[#7755ff] text-white text-[10px] font-bold px-2 py-1 rounded">RESONANCE</div>
                    <ul className="text-[10px] space-y-1 text-slate-300">
                        <li>• Trading: Dynamic Sizing</li>
                        <li>• Architecture: Parametric Design</li>
                        <li>• SaaS: Tiered Metadata Injection</li>
                    </ul>
                </div>

                <ArrowRight className="text-slate-700" />

                {/* Step 4: Alpha */}
                <div className="flex-1 p-6 border border-[#ffaa00]/30 rounded-2xl bg-[#ffaa00]/5 relative">
                    <div className="absolute -top-3 left-4 bg-[#ffaa00] text-black text-[10px] font-bold px-2 py-1 rounded">ALPHA SIGNAL</div>
                    <div className="text-center">
                        <div className="text-2xl font-black text-[#ffaa00] mb-1">SEED V1</div>
                        <div className="text-[10px] font-bold uppercase text-slate-400">Build: Aithentik Etsy-API Wrapper</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OpportunityFlow;
