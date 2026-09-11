import { useEffect, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import DeviceVisual from '../components/DeviceVisual'
import { useScrollRotation } from '../hooks/useScrollRotation'
import { useSectionReveal } from '../hooks/useSectionReveal'
import { MODEL_METRICS } from '../constants/modelMetrics'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const SHOWCASE_UDI = 46

const RISK_LEVEL_LABEL = {
  high: 'HIGH RISK',
  medium: 'MEDIUM RISK',
  low: 'LOW RISK',
}

const RISK_LEVEL_BADGE = {
  high: 'badge-danger',
  medium: 'badge-warning',
  low: 'badge-success',
}

function Reveal({ as = 'div', className = '', children, ...rest }) {
  const { ref, isVisible } = useSectionReveal()
  const Tag = as
  return (
    <Tag ref={ref} className={`reveal${isVisible ? ' is-visible' : ''} ${className}`} {...rest}>
      {children}
    </Tag>
  )
}

function Home() {
  const [stats, setStats] = useState(null)
  const [speedTorque, setSpeedTorque] = useState(null)
  const [hdfTempDiff, setHdfTempDiff] = useState(null)
  const [osfRisk, setOsfRisk] = useState(null)
  const [showcase, setShowcase] = useState(null)

  const heroRef = useRef(null)
  const showcaseRef = useRef(null)
  const { rotation: showcaseRotation } = useScrollRotation(showcaseRef, { range: 240 })

  useEffect(() => {
    fetch(`${API_BASE}/api/machines/stats`)
      .then((res) => res.json())
      .then(setStats)
      .catch(() => {})

    fetch(`${API_BASE}/api/analytics/speed-torque-region`)
      .then((res) => res.json())
      .then(setSpeedTorque)
      .catch(() => {})

    fetch(`${API_BASE}/api/analytics/hdf-tempdiff`)
      .then((res) => res.json())
      .then(setHdfTempDiff)
      .catch(() => {})

    fetch(`${API_BASE}/api/analytics/osf-risk-index`)
      .then((res) => res.json())
      .then(setOsfRisk)
      .catch(() => {})

    fetch(`${API_BASE}/api/machines/${SHOWCASE_UDI}`)
      .then((res) => res.json())
      .then(setShowcase)
      .catch(() => {})
  }, [])

  return (
    <div className="story">
      {/* 1. 首屏 */}
      <section className="story-section story-hero" ref={heroRef}>
        <h1 className="story-title-xl">从数据，到智能决策。</h1>
        <p className="story-subtitle">一套预测性维护系统的完整故事。</p>
        <div className="story-visual">
          <DeviceVisual size="hero" autoRotate />
        </div>
        <div className="scroll-hint">向下滚动</div>
      </section>

      {/* 2. 为什么 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">为什么要预测性维护？</h2>
        <div className="compare-row">
          <div className="compare-col">
            <div className="compare-label">传统维护</div>
            <p>故障发生后才处理。</p>
          </div>
          <div className="compare-col">
            <div className="compare-label">预测性维护</div>
            <p>故障发生前就发现风险。</p>
          </div>
        </div>
      </Reveal>

      {/* 3. 理解数据 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">先理解数据。</h2>
        <div className="big-number-row">
          <div className="big-number">
            <div className="big-number-value">{stats ? stats.total.toLocaleString() : '—'}</div>
            <div className="big-number-label">台设备</div>
          </div>
          <div className="big-number">
            <div className="big-number-value">{stats ? stats.failure.toLocaleString() : '—'}</div>
            <div className="big-number-label">次真实故障</div>
          </div>
        </div>
        <div className="param-list">
          {['环境温度', '过程温度', '转速', '扭矩', '刀具磨损'].map((p) => (
            <span key={p} className="param-tag">{p}</span>
          ))}
        </div>
      </Reveal>

      {/* 4. 洞察 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">数据不会直接告诉我们答案。</h2>
        <div className="insight-list">
          <div className="insight-item">
            <div className="insight-number">
              {speedTorque ? `${speedTorque.target_failure_rate.toFixed(2)}%` : '—'}
              <span className="insight-number-sub">
                {' '}vs {speedTorque ? `${speedTorque.other_failure_rate.toFixed(2)}%` : '—'}
              </span>
            </div>
            <p>低转速 + 高扭矩区域的故障率，远高于其余区域。</p>
          </div>
          <div className="insight-item">
            <div className="insight-number">{hdfTempDiff ? `${hdfTempDiff.failure_rate.toFixed(2)}%` : '—'}</div>
            <p>温差落在 7.5–8.6K 区间时，故障率明显升高。</p>
          </div>
          <div className="insight-item">
            <div className="insight-number">{osfRisk ? `${osfRisk.failure_rate.toFixed(1)}%` : '—'}</div>
            <p>扭矩 × 刀具磨损的风险指数超过阈值时，故障率极高。</p>
          </div>
        </div>
      </Reveal>

      {/* 5. 模型引入 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">然后，让机器学习参与判断。</h2>
        <div className="flow-line">
          <span>设备类型</span>
          <span>温度</span>
          <span>转速</span>
          <span>扭矩</span>
          <span>刀具磨损</span>
          <span className="flow-arrow">→</span>
          <span className="flow-highlight">Logistic Regression</span>
          <span className="flow-arrow">→</span>
          <span className="flow-highlight">Risk Score</span>
        </div>
      </Reveal>

      {/* 6. 准确率陷阱 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">准确率很高。</h2>
        <div className="big-number-solo">{MODEL_METRICS.accuracy}</div>
        <p className="story-turn">但这还不够。</p>
        <p>
          在默认阈值 {MODEL_METRICS.defaultThreshold} 下，模型只找出了{' '}
          <strong>{MODEL_METRICS.recallAtDefaultThresholdFraction}</strong> 起真实故障，
          召回率仅 {MODEL_METRICS.recallAtDefaultThreshold}。
        </p>
      </Reveal>

      {/* 7. 阈值调整 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">所以，我改变了判断标准。</h2>
        <div className="flow-line">
          <span className="flow-highlight">阈值 {MODEL_METRICS.chosenThreshold}</span>
          <span className="flow-arrow">→</span>
          <span className="flow-highlight">
            召回率 {MODEL_METRICS.recallAtChosenThreshold}（{MODEL_METRICS.recallAtChosenThresholdFraction}）
          </span>
          <span className="flow-arrow">→</span>
          <span>{MODEL_METRICS.falsePositivesAtChosenThreshold} 个误报</span>
        </div>
        <p className="story-note">漏报的代价，远高于误报的代价。</p>
      </Reveal>

      {/* 8. 落地 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">模型不能只停留在实验里。</h2>
        <div className="pipeline-row">
          {['Python', '数据分析', 'Logistic Regression', 'model.joblib', 'PostgreSQL', 'FastAPI', 'React', 'Risk Score', '维修工单'].map(
            (step) => (
              <span key={step} className="pipeline-step">{step}</span>
            ),
          )}
        </div>
      </Reveal>

      {/* 9. 真实设备示例 */}
      <section className="story-section" ref={showcaseRef}>
        <h2 className="story-title">现在，让我们看看一台设备。</h2>
        <div className="story-visual">
          <DeviceVisual size="hero" rotation={showcaseRotation} />
        </div>
        {showcase && (
          <div className="showcase-panel">
            <div className="device-id-tag">设备编号 · UDI-{String(showcase.udi).padStart(5, '0')}</div>
            <div className="info-grid">
              <div className="info-item">
                <div className="info-label">转速</div>
                <div className="info-value">{showcase.rotational_speed_rpm} RPM</div>
              </div>
              <div className="info-item">
                <div className="info-label">扭矩</div>
                <div className="info-value">{showcase.torque_nm} Nm</div>
              </div>
              <div className="info-item">
                <div className="info-label">刀具磨损</div>
                <div className="info-value">{showcase.tool_wear_min} min</div>
              </div>
              <div className="info-item">
                <div className="info-label">风险评分</div>
                <div className="info-value">{(showcase.risk_score * 100).toFixed(1)}%</div>
              </div>
            </div>
            <span className={`badge ${RISK_LEVEL_BADGE[showcase.risk_level]}`}>
              {RISK_LEVEL_LABEL[showcase.risk_level]}
            </span>
          </div>
        )}
      </section>

      {/* 10. 行动 */}
      <Reveal as="section" className="story-section">
        <h2 className="story-title">风险，只有被处理时才有意义。</h2>
        <div className="flow-line">
          <span>风险分数</span>
          <span className="flow-arrow">→</span>
          <span>维修工单</span>
          <span className="flow-arrow">→</span>
          <span>现场处理</span>
        </div>
        <p className="story-turn">让风险，变成行动。</p>
      </Reveal>

      {/* 11. 收尾 */}
      <Reveal as="section" className="story-section story-finale">
        <h2 className="story-title">从数据发现问题，到让问题得到处理。</h2>
        <div className="finale-words">
          <span>数据</span>
          <span className="flow-arrow">→</span>
          <span>洞察</span>
          <span className="flow-arrow">→</span>
          <span>智能</span>
          <span className="flow-arrow">→</span>
          <span>行动</span>
        </div>
        <div className="finale-cta">
          <Link to="/devices" className="btn-primary">查看设备</Link>
          <Link to="/tickets" className="btn-secondary">维修工单</Link>
        </div>
      </Reveal>
    </div>
  )
}

export default Home
