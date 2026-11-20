import React, { useEffect, useState } from 'react';

interface AnimatedNumberProps {
  value: number;
  duration?: number;
  fractionDigits?: number;
}

export const AnimatedNumber: React.FC<AnimatedNumberProps> = ({ value, duration = 1000, fractionDigits = 0 }) => {
  const [displayValue, setDisplayValue] = useState(value);
  const displayValueRef = React.useRef(value);
  displayValueRef.current = displayValue;

  useEffect(() => {
    let startTime: number | null = null;
    const startValue = displayValueRef.current;
    const endValue = value;

    if (startValue === endValue) return;

    const animate = (timestamp: number) => {
      if (!startTime) startTime = timestamp;
      const progress = timestamp - startTime;
      
      if (progress < duration) {
        const easeOutQuad = (t: number) => t * (2 - t);
        const t = easeOutQuad(progress / duration);
        setDisplayValue(startValue + (endValue - startValue) * t);
        requestAnimationFrame(animate);
      } else {
        setDisplayValue(endValue);
      }
    };

    const animId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animId);
  }, [value, duration]);

  return <span>{displayValue.toFixed(fractionDigits)}</span>;
};
