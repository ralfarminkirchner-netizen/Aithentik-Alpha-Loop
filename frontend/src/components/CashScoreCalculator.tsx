import React, { useState } from 'react';
import { DollarSign, AlertCircle } from 'lucide-react';
import { ResponsiveContainer, AreaChart, Area } from 'recharts';

const data = [
    { name: 'Jan', val: 400 },
    { name: 'Feb', val: 300 },
    { name: 'Mar', val: 600 },
    { name: 'Apr', val: 800 },
    { name: 'May', val: 500 },
    { name: 'Jun', val: 900 },
];

const CashScoreCalculator: React.FC = () => {
    const [dominance, setDominance] = useState(85);
    const [anomalie, setAnomalie] = useState(40);

    const cashScore = Math.round((dominance * 0.6) + (anomalie * 0.4));

    return (
        <div className="glass-card p-6">
            <div className="flex justify-between items-center mb-6">
                <h3 className="text-lg font-bold flex items-center gap-2">
                    <DollarSign className="w-5 h-5 text-[#00ffcc]" />
                    Cash Score Dynamics
                </h3>
                <span className={`text-2xl font-black ${cashScore > 70 ? 'text-[#00ffcc]' : 'text-[#ffaa00]'}`}>
                    {cashScore}%
                </span>
            </div>

            <div className="h-[120px] mb-6">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorVal" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#00ffcc" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#00ffcc" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <Area type="monotone" dataKey="val" stroke="#00ffcc" fillOpacity={1} fill="url(#colorVal)" />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            <div className="space-y-4">
                <div>
                    <div className="flex justify-between text-xs text-slate-400 mb-1">
                        <span>DOMINANZ</span>
                        <span>{dominance}%</span>
                    </div>
                    <input
                        type="range"
                        className="w-full accent-[#00ffcc]"
                        value={dominance}
                        onChange={(e) => setDominance(Number(e.target.value))}
                    />
                </div>
                <div>
                    <div className="flex justify-between text-xs text-slate-400 mb-1">
                        <span>ANOMALIE</span>
                        <span>{anomalie}%</span>
                    </div>
                    <input
                        type="range"
                        className="w-full accent-[#7755ff]"
                        value={anomalie}
                        onChange={(e) => setAnomalie(Number(e.target.value))}
                    />
                </div>
            </div>

            <div className="mt-6 p-3 bg-[#5566ff]/10 border border-[#5566ff]/20 rounded-lg flex items-start gap-3">
                <AlertCircle className="w-4 h-4 text-[#5566ff] mt-0.5" />
                <p className="text-[10px] text-[#5566ff] font-bold uppercase tracking-wider">
                    Signal: High Alpha identified in "Vaterkunst/Etsy V3" Layer.
                </p>
            </div>
        </div>
    );
};

export default CashScoreCalculator;
