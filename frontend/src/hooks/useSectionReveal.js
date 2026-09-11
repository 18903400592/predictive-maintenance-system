import { useEffect, useRef, useState } from 'react'

export function useSectionReveal({ threshold = 0.3 } = {}) {
  const ref = useRef(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) {
      return
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold },
    )

    observer.observe(el)

    return () => observer.disconnect()
  }, [threshold])

  return { ref, isVisible }
}
