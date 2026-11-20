import { useEffect, useRef, useState, useCallback } from 'react';

export interface WebSocketMessage {
  event: string;
  learner_id?: number;
  concept_id?: number;
  concept_code?: string;
  concept_title?: string;
  prior_mastery?: number;
  posterior_mastery?: number;
  is_correct?: boolean;
  status?: string;
  goal_id?: number;
  goal_name?: string;
  current_mastery?: number;
  message?: string;
}

export function useWebSocket(learnerId: number, onUpdate?: (msg: WebSocketMessage) => void) {
  const [isConnected, setIsConnected] = useState(false);
  const [lastMessage, setLastMessage] = useState<WebSocketMessage | null>(null);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback(() => {
    if (!learnerId) return;

    try {
      const wsUrl = `ws://localhost:8000/ws/${learnerId}`;
      const socket = new WebSocket(wsUrl);

      socket.onopen = () => {
        setIsConnected(true);
      };

      socket.onmessage = (event) => {
        try {
          const data: WebSocketMessage = JSON.parse(event.data);
          setLastMessage(data);
          if (onUpdate) {
            onUpdate(data);
          }
        } catch {
          // Non-JSON message (e.g. pong)
        }
      };

      socket.onclose = () => {
        setIsConnected(false);
        // Attempt reconnection after 3 seconds
        setTimeout(() => {
          connect();
        }, 3000);
      };

      socket.onerror = () => {
        setIsConnected(false);
        socket.close();
      };

      wsRef.current = socket;
    } catch (e) {
      console.warn("WebSocket connection error:", e);
    }
  }, [learnerId, onUpdate]);

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [connect]);

  const sendPing = useCallback(() => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send("ping");
    }
  }, []);

  return { isConnected, lastMessage, sendPing };
}
