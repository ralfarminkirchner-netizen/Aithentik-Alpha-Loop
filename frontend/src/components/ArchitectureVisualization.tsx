import React, { useEffect, useRef } from 'react';

const ArchitectureVisualization: React.FC = () => {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        if (!ctx) return;

        let animationFrameId: number;
        let particles: any[] = [];

        const init = () => {
            canvas.width = canvas.parentElement?.clientWidth || 800;
            canvas.height = 600;
            particles = [];
            for (let i = 0; i < 40; i++) {
                particles.push({
                    x: Math.random() * canvas.width,
                    y: Math.random() * canvas.height,
                    vx: (Math.random() - 0.5) * 0.5,
                    vy: (Math.random() - 0.5) * 0.5,
                    r: Math.random() * 3 + 2,
                });
            }
        };

        const draw = () => {
            ctx.fillStyle = 'rgba(5, 5, 8, 0.2)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            ctx.beginPath();
            ctx.strokeStyle = 'rgba(85, 102, 255, 0.1)';
            for (let i = 0; i < particles.length; i++) {
                const p1 = particles[i];
                p1.x += p1.vx;
                p1.y += p1.vy;

                if (p1.x < 0 || p1.x > canvas.width) p1.vx *= -1;
                if (p1.y < 0 || p1.y > canvas.height) p1.vy *= -1;

                for (let j = i + 1; j < particles.length; j++) {
                    const p2 = particles[j];
                    const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y);
                    if (dist < 150) {
                        ctx.moveTo(p1.x, p1.y);
                        ctx.lineTo(p2.x, p2.y);
                    }
                }

                ctx.fillStyle = i % 5 === 0 ? '#00ffcc' : '#5566ff';
                ctx.shadowBlur = 10;
                ctx.shadowColor = ctx.fillStyle;
                ctx.beginPath();
                ctx.arc(p1.x, p1.y, p1.r, 0, Math.PI * 2);
                ctx.fill();
            }
            ctx.stroke();

            animationFrameId = requestAnimationFrame(draw);
        };

        init();
        draw();

        window.addEventListener('resize', init);
        return () => {
            cancelAnimationFrame(animationFrameId);
            window.removeEventListener('resize', init);
        };
    }, []);

    return (
        <div className="relative w-full h-full">
            <canvas ref={canvasRef} className="block" />
            <div className="absolute bottom-6 left-6 flex flex-col gap-2">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#00ffcc]"></div>
                    <span className="text-xs font-bold text-slate-400">DOMINANT DNA</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#5566ff]"></div>
                    <span className="text-xs font-bold text-slate-400">PATTERN TRACE</span>
                </div>
            </div>
            <div className="absolute top-6 right-6 text-right">
                <div className="text-2xl font-black text-[#00ffcc]">WOOD WIDE WEB</div>
                <div className="text-[10px] text-[#5566ff] font-bold">CYBERNETIC NEURAL MESH v2.0</div>
            </div>
        </div>
    );
};

export default ArchitectureVisualization;
