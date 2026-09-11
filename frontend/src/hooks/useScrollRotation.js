import { useEffect, useRef, useState } from 'react'

const SCROLL_DISTANCE = 800

export function useScrollRotation(sectionRef, { range = 240 } = {}) {
  const [rotation, setRotation] = useState(0)
  const frameRef = useRef(null)

  useEffect(() => {
    function computeProgress() {
      const el = sectionRef.current
      const top = el ? el.getBoundingClientRect().top + window.scrollY : 0
      const scrolled = window.scrollY - top
      const clamped = Math.min(Math.max(scrolled, 0), SCROLL_DISTANCE)
      return clamped / SCROLL_DISTANCE
    }

    function onScroll() {
      if (frameRef.current) {
        return
      }
      frameRef.current = requestAnimationFrame(() => {
        frameRef.current = null
        setRotation(computeProgress() * range)
      })
    }

    window.addEventListener('scroll', onScroll, { passive: true })
    onScroll()

    return () => {
      window.removeEventListener('scroll', onScroll)
      if (frameRef.current) {
        cancelAnimationFrame(frameRef.current)
      }
    }
  }, [sectionRef, range])

  return { rotation }
}
