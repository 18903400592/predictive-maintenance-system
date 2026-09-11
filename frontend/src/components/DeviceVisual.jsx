const SIZE_PX = {
  hero: 320,
  ambient: 220,
}

function DeviceVisual({ rotation = 0, blur = 0, opacity = 1, size = 'hero', autoRotate = false }) {
  const px = SIZE_PX[size] ?? SIZE_PX.hero
  const gradientId = `shaverBody-${size}`
  const headGradientId = `shaverHead-${size}`

  return (
    <div
      style={{
        width: px,
        height: px,
        perspective: 900,
        filter: blur ? `blur(${blur}px)` : undefined,
        opacity,
      }}
    >
      <div
        className={autoRotate ? 'device-visual-autorotate' : undefined}
        style={
          autoRotate
            ? { width: '100%', height: '100%', transformStyle: 'preserve-3d' }
            : {
                width: '100%',
                height: '100%',
                transform: `rotateY(${rotation}deg)`,
                transformStyle: 'preserve-3d',
                transition: 'transform 0.05s linear',
              }
        }
      >
        <svg viewBox="0 0 200 200" width="100%" height="100%" style={{ display: 'block' }}>
          <defs>
            <linearGradient id={gradientId} x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#e8ecf1" />
              <stop offset="35%" stopColor="#aab4c2" />
              <stop offset="55%" stopColor="#6b7688" />
              <stop offset="100%" stopColor="#2c3341" />
            </linearGradient>
            <linearGradient id={headGradientId} x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#c8cfd9" />
              <stop offset="100%" stopColor="#4a5262" />
            </linearGradient>
            <radialGradient id={`shadow-${size}`} cx="50%" cy="50%" r="50%">
              <stop offset="0%" stopColor="rgba(0,0,0,0.45)" />
              <stop offset="100%" stopColor="rgba(0,0,0,0)" />
            </radialGradient>
          </defs>

          <ellipse cx="100" cy="182" rx="46" ry="8" fill={`url(#shadow-${size})`} />

          {/* head */}
          <rect x="66" y="18" width="68" height="46" rx="20" fill={`url(#${headGradientId})`} />
          {[28, 36, 44, 52].map((y) => (
            <line key={y} x1="76" y1={y} x2="124" y2={y} stroke="rgba(20,24,32,0.35)" strokeWidth="2" strokeLinecap="round" />
          ))}

          {/* neck */}
          <rect x="88" y="58" width="24" height="14" fill="#3a4150" />

          {/* body */}
          <rect x="72" y="70" width="56" height="102" rx="24" fill={`url(#${gradientId})`} />

          {/* highlight streak */}
          <rect x="82" y="78" width="8" height="86" rx="4" fill="rgba(255,255,255,0.35)" />

          {/* base ring */}
          <rect x="72" y="164" width="56" height="10" rx="5" fill="#20242e" />
        </svg>
      </div>
    </div>
  )
}

export default DeviceVisual
