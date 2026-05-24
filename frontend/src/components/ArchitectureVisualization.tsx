import React, { useMemo, useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Line, Float, Html, Sparkles } from '@react-three/drei';
import * as THREE from 'three';

const MyceliumNetwork = () => {
    // Generate random nodes
    const nodes = useMemo(() => {
        const pts = [];
        for (let i = 0; i < 80; i++) {
            pts.push(
                new THREE.Vector3(
                    (Math.random() - 0.5) * 20,
                    (Math.random() - 0.5) * 12,
                    (Math.random() - 0.5) * 20
                )
            );
        }
        return pts;
    }, []);

    // Generate connections based on distance to simulate fractal hyphae
    const connections = useMemo(() => {
        const lines = [];
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                if (nodes[i].distanceTo(nodes[j]) < 5.5) {
                    lines.push([nodes[i], nodes[j]]);
                }
            }
        }
        return lines;
    }, [nodes]);

    const groupRef = useRef<THREE.Group>(null);

    useFrame((state) => {
        if (groupRef.current) {
            groupRef.current.rotation.y = state.clock.elapsedTime * 0.02;
            groupRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.05) * 0.05;
        }
    });

    return (
        <group ref={groupRef}>
            {connections.map((points, idx) => (
                <Line
                    key={idx}
                    points={points}
                    color="#5566ff"
                    lineWidth={1.2}
                    transparent
                    opacity={0.3}
                />
            ))}

            {nodes.map((pos, idx) => {
                const isCore = idx % 8 === 0;
                return (
                    <Float key={idx} speed={1.5} rotationIntensity={0.2} floatIntensity={0.5}>
                        <mesh position={pos}>
                            <sphereGeometry args={[isCore ? 0.12 : 0.06, 16, 16]} />
                            <meshBasicMaterial
                                color={isCore ? '#00ffcc' : '#5566ff'}
                            />
                        </mesh>
                    </Float>
                );
            })}
        </group>
    );
};

const MultiUserActivity = () => {
    // Multi-user features visually integrated as active entities/nodes
    const users = useMemo(() => [
        { name: "Scout_01 (Syncing)", pos: new THREE.Vector3(6, 2, 4), color: "#ff00cc" },
        { name: "Investor_X", pos: new THREE.Vector3(-5, -3, -5), color: "#ffaa00" },
        { name: "Governor_AI", pos: new THREE.Vector3(0, 5, 0), color: "#00ffcc" },
        { name: "Node_77", pos: new THREE.Vector3(-4, 4, 6), color: "#ff00cc" },
        { name: "Guest_4892", pos: new THREE.Vector3(5, -4, -2), color: "#ffffff" }
    ], []);

    return (
        <>
            {users.map((user, idx) => (
                <Float key={idx} speed={3} rotationIntensity={2} floatIntensity={2}>
                    <mesh position={user.pos}>
                        <octahedronGeometry args={[0.4]} />
                        <meshBasicMaterial color={user.color} wireframe />
                        <Html distanceFactor={18} position={[0, 0.8, 0]} center zIndexRange={[100, 0]}>
                            <div className="bg-black/80 px-2 py-1 rounded text-xs border border-white/20 whitespace-nowrap backdrop-blur-md" style={{ color: user.color }}>
                                <span className="animate-pulse mr-1">●</span> {user.name}
                            </div>
                        </Html>
                    </mesh>
                </Float>
            ))}
        </>
    );
};

const ArchitectureVisualization: React.FC = () => {
    return (
        <div className="relative w-full h-full bg-[#050508]">
            <Canvas camera={{ position: [0, 0, 15], fov: 45 }}>
                <color attach="background" args={['#050508']} />
                <fog attach="fog" args={['#050508', 10, 30]} />
                
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={2} color="#00ffcc" />
                <pointLight position={[-10, -10, -10]} intensity={1} color="#5566ff" />

                <MyceliumNetwork />
                <MultiUserActivity />
                
                <Sparkles count={400} scale={25} size={2} speed={0.4} opacity={0.2} color="#00ffcc" />

                <OrbitControls 
                    enablePan={false} 
                    enableZoom={true} 
                    maxDistance={25} 
                    minDistance={5} 
                    autoRotate 
                    autoRotateSpeed={0.5} 
                />
            </Canvas>

            <div className="absolute bottom-6 left-6 flex flex-col gap-2 pointer-events-none">
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#00ffcc] animate-pulse"></div>
                    <span className="text-xs font-bold text-slate-400">DOMINANT DNA (CORE)</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-[#5566ff]"></div>
                    <span className="text-xs font-bold text-slate-400">HYPHAE TRACE (FRACTAL)</span>
                </div>
                <div className="flex items-center gap-2 mt-2">
                    <div className="w-3 h-3 rounded-sm border border-[#ff00cc]"></div>
                    <span className="text-xs font-bold text-slate-400">ACTIVE USERS / SCOUTS</span>
                </div>
            </div>
            
            <div className="absolute top-6 right-6 text-right pointer-events-none">
                <div className="text-2xl font-black text-[#00ffcc] drop-shadow-[0_0_8px_rgba(0,255,204,0.8)]">WOOD WIDE WEB 3D</div>
                <div className="text-[10px] text-[#5566ff] font-bold">CYBERNETIC MULTI-USER MESH v3.0</div>
            </div>
        </div>
    );
};

export default ArchitectureVisualization;
