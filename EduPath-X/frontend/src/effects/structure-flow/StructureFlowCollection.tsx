import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

export interface TopologyFieldProps {
  hue?: number;
  saturation?: number;
  brightness?: number;
  className?: string;
  style?: React.CSSProperties;
}

export function TopologyField({
  hue = 0,
  saturation = 1,
  brightness = 1,
  className,
  style,
}: TopologyFieldProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const glowRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const container = containerRef.current;
    if (!canvas || !container) return;

    let animationFrameId: number;
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    // Three.js Scene Setup (exact nexus-topology authored specification)
    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x0a0a0a, 300, 950);

    const camera = new THREE.PerspectiveCamera(60, width / height, 1, 2000);
    camera.position.z = 650;

    const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    const group = new THREE.Group();
    scene.add(group);

    // 120 Nodes distributed on a sphere
    const numNodes = 120;
    const nodes: THREE.Mesh<THREE.SphereGeometry, THREE.MeshBasicMaterial>[] = [];
    const nodeGeo = new THREE.SphereGeometry(1, 16, 16);

    for (let i = 0; i < numNodes; i++) {
      const phi = Math.acos(-1 + (2 * i) / numNodes);
      const theta = Math.sqrt(numNodes * Math.PI) * phi;
      const x = Math.cos(theta) * Math.sin(phi);
      const y = Math.sin(theta) * Math.sin(phi);
      const z = Math.cos(phi);

      const mesh = new THREE.Mesh(
        nodeGeo,
        new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.9 })
      );
      mesh.position.set(x, y, z);
      mesh.userData = {
        baseSize: Math.random() * 1.5 + 1.0,
        pulseSpeed: Math.random() * 0.02 + 0.015,
        pulseOffset: Math.random() * Math.PI * 2,
      };
      group.add(mesh);
      nodes.push(mesh);
    }

    // Connect nodes with line segments based on distance threshold
    const linePos: number[] = [];
    const lineColors: number[] = [];
    const threshold = 0.45;

    for (let i = 0; i < numNodes; i++) {
      for (let j = i + 1; j < numNodes; j++) {
        const dist = nodes[i].position.distanceTo(nodes[j].position);
        if (dist < threshold) {
          linePos.push(nodes[i].position.x, nodes[i].position.y, nodes[i].position.z);
          linePos.push(nodes[j].position.x, nodes[j].position.y, nodes[j].position.z);

          const alpha = (1 - dist / threshold) * 0.8;
          lineColors.push(alpha, alpha, alpha);
          lineColors.push(alpha, alpha, alpha);
        }
      }
    }

    const lineGeo = new THREE.BufferGeometry();
    lineGeo.setAttribute('position', new THREE.Float32BufferAttribute(linePos, 3));
    lineGeo.setAttribute('color', new THREE.Float32BufferAttribute(lineColors, 3));
    const lineMat = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.65,
    });
    const lines = new THREE.LineSegments(lineGeo, lineMat);
    group.add(lines);

    const resize = () => {
      if (!container) return;
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);

      const R = width > 768 ? 380 : 200;
      group.scale.set(R, R, R);

      const centerX = width > 768 ? width * 0.2 : 0;
      const centerY = width > 768 ? -height * 0.05 : -height * 0.2;
      group.position.set(centerX, centerY, 0);

      const glow = glowRef.current;
      if (glow) {
        glow.style.left = `${width / 2 + centerX}px`;
        glow.style.top = `${height / 2 - centerY}px`;
        glow.style.width = `${R * 2.8}px`;
        glow.style.height = `${R * 2.8}px`;
      }
    };

    window.addEventListener('resize', resize);
    resize();

    let time = 0;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      time += 1;

      group.rotation.y = time * 0.0018;
      group.rotation.x = 0.2;
      group.rotation.z = time * 0.0006;

      nodes.forEach((mesh) => {
        const p = mesh.userData;
        const pulse = (Math.sin(time * p.pulseSpeed + p.pulseOffset) + 1) / 2;
        const targetRadius = p.baseSize + pulse * 1.8;
        const scale = targetRadius / group.scale.x;

        mesh.scale.set(scale, scale, scale);
        mesh.material.opacity = 0.4 + pulse * 0.6;
      });

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('resize', resize);
      cancelAnimationFrame(animationFrameId);
      nodeGeo.dispose();
      lineGeo.dispose();
      lineMat.dispose();
      renderer.dispose();
    };
  }, []);

  const filterStyle =
    hue !== 0 || saturation !== 1 || brightness !== 1
      ? `hue-rotate(${hue}deg) saturate(${saturation}) brightness(${brightness})`
      : undefined;

  return (
    <div
      ref={containerRef}
      className={`relative w-full h-full overflow-hidden pointer-events-none select-none ${className || ''}`}
      style={{
        background: 'radial-gradient(circle at bottom right, #18181b 0%, #050508 50%, #000000 100%)',
        filter: filterStyle,
        ...style,
      }}
    >
      <div
        ref={glowRef}
        className="absolute pointer-events-none rounded-full blur-[140px] opacity-[0.16] bg-indigo-500 transition-all duration-1000"
        style={{ zIndex: 0, transform: 'translate(-50%, -50%)' }}
      />
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full z-0 pointer-events-none" />
    </div>
  );
}

export type StructureFlowVariant = 'topology-field';

export interface StructureFlowCollectionProps {
  variant?: StructureFlowVariant;
  hue?: number;
  saturation?: number;
  brightness?: number;
  className?: string;
  style?: React.CSSProperties;
}

export function StructureFlowCollection({
  variant = 'topology-field',
  hue = 0,
  saturation = 1,
  brightness = 1,
  className,
  style,
}: StructureFlowCollectionProps) {
  if (variant === 'topology-field') {
    return (
      <TopologyField
        hue={hue}
        saturation={saturation}
        brightness={brightness}
        className={className}
        style={style}
      />
    );
  }
  return null;
}
