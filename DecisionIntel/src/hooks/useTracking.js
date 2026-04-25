import { useEffect, useRef } from 'react';
import { trackEvent } from '../utils/tracking';

export function useDecisionTiming(decisionId) {
  const startTimeRef = useRef(Date.now());

  return () => {
    const elapsed = Date.now() - startTimeRef.current;
    trackEvent('time_to_decision', elapsed, decisionId);
    return elapsed;
  };
}

export function useScrollDepth(decisionId) {
  const milestonesRef = useRef(new Set());

  useEffect(() => {
    const handleScroll = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrolled = window.scrollY;
      const depth = scrollHeight > 0 ? Math.round((scrolled / scrollHeight) * 100) : 0;

      const milestones = [25, 50, 75, 100];
      milestones.forEach((milestone) => {
        if (depth >= milestone && !milestonesRef.current.has(milestone)) {
          milestonesRef.current.add(milestone);
          trackEvent('scroll_depth', milestone, decisionId);
        }
      });
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [decisionId]);
}

export function useElementVisible(ref, elementName, decisionId) {
  const hasTrackedRef = useRef(false);

  useEffect(() => {
    if (!ref.current) return;

    let visibilityTimer = null;
    const VISIBILITY_DURATION = 1500;

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !hasTrackedRef.current) {
          visibilityTimer = setTimeout(() => {
            trackEvent(`${elementName}_read`, 1, decisionId);
            hasTrackedRef.current = true;
          }, VISIBILITY_DURATION);
        } else if (!entry.isIntersecting) {
          if (visibilityTimer) clearTimeout(visibilityTimer);
        }
      },
      { threshold: 0.5 }
    );

    observer.observe(ref.current);
    return () => {
      observer.disconnect();
      if (visibilityTimer) clearTimeout(visibilityTimer);
    };
  }, [ref, elementName, decisionId]);
}

export function useHoverDuration(ref, eventName, decisionId, triggerMs = 8000) {
  const hoverTimerRef = useRef(null);
  const hasTriggeredRef = useRef(false);

  useEffect(() => {
    if (!ref.current) return;

    const handleMouseEnter = () => {
      hoverTimerRef.current = setTimeout(() => {
        if (!hasTriggeredRef.current) {
          trackEvent(eventName, triggerMs, decisionId);
          hasTriggeredRef.current = true;
        }
      }, triggerMs);
    };

    const handleMouseLeave = () => {
      if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current);
    };

    const element = ref.current;
    element.addEventListener('mouseenter', handleMouseEnter);
    element.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      element.removeEventListener('mouseenter', handleMouseEnter);
      element.removeEventListener('mouseleave', handleMouseLeave);
      if (hoverTimerRef.current) clearTimeout(hoverTimerRef.current);
    };
  }, [ref, eventName, decisionId, triggerMs]);
}
