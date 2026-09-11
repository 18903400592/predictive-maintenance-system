import { useEffect, useRef, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import DeviceVisual from '../components/DeviceVisual'
import { useScrollRotation } from '../hooks/useScrollRotation'

const API_BASE = 'http://localhost:8000'

const FAULT_LABELS = {
  twf: '刀具磨损故障',
  hdf: '散热故障',
  pwf: '功率故障',
  osf: '过载故障',
  rnf: '随机故障',
}

const RISK_LEVEL_BADGE = {
  high: 'badge-danger',
  medium: 'badge-warning',
  low: 'badge-success',
}

const RISK_LEVEL_LABEL = {
  high: '高风险',
  medium: '中风险',
  low: '低风险',
}

const RISK_LEVEL_COLOR = {
  high: 'var(--color-danger)',
  medium: 'var(--color-warning)',
  low: 'var(--color-success)',
}

function MachineDetail() {
  const { udi } = useParams()
  const [machine, setMachine] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const heroRef = useRef(null)
  const { rotation } = useScrollRotation(heroRef, { range: 240 })

  useEffect(() => {
    setLoading(true)
    setError(null)

    fetch(`${API_BASE}/api/machines/${udi}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`请求失败：HTTP ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        setMachine(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [udi])

  if (loading) {
    return <p className="state-msg">加载中...</p>
  }

  if (error) {
    return (
      <div>
        <Link to="/devices" className="back-link">← 返回设备监控</Link>
        <p className="state-msg is-error">加载失败：{error}</p>
      </div>
    )
  }

  const riskPercent = (machine.risk_score * 100).toFixed(2)
  const activeFaults = Object.keys(FAULT_LABELS).filter((key) => machine[key])
  const riskLevel = machine.risk_level

  return (
    <div>
      <Link to="/devices" className="back-link">← 返回设备监控</Link>

      <div className="hero-section" ref={heroRef}>
        <div className="eyebrow">设备详情</div>
        <h1>UDI-{String(machine.udi).padStart(5, '0')}</h1>
        <DeviceVisual size="hero" rotation={rotation} />
        <div className="hero-stat">
          <div className="hero-stat-label">转速</div>
          <div className="hero-stat-value">{machine.rotational_speed_rpm} RPM</div>
        </div>
      </div>

      <div className="page-header">
        <div>
          <div className="eyebrow">类型 {machine.type} · {machine.product_id}</div>
        </div>
        {machine.machine_failure ? (
          <span className="badge badge-danger">实际状态：故障</span>
        ) : (
          <span className="badge badge-success">实际状态：正常</span>
        )}
      </div>

      <div className="glass-card">
        <div className="card-title">设备状态</div>
        <p style={{ fontSize: 16, fontWeight: 600 }}>
          <span className={`status-dot ${machine.machine_failure ? 'is-fail' : 'is-ok'}`} />
          {machine.machine_failure ? '故障' : '运行正常'}
        </p>
      </div>

      <div className="glass-card">
        <div className="card-title">AI 风险评估</div>
        <div style={{ maxWidth: 480 }}>
          <div className="progress-track">
            <div
              className="progress-fill"
              style={{
                width: `${riskPercent}%`,
                background: RISK_LEVEL_COLOR[riskLevel],
              }}
            />
          </div>
          <p style={{ marginTop: 14, fontSize: 13, color: 'var(--color-text-secondary)' }}>
            风险评分{' '}
            <strong style={{ color: 'var(--color-text)', fontFamily: 'var(--mono)', fontSize: 15 }}>
              {riskPercent}%
            </strong>{' '}
            &nbsp;状态 <span className={`badge ${RISK_LEVEL_BADGE[riskLevel]}`}>{RISK_LEVEL_LABEL[riskLevel]}</span>
          </p>
        </div>
      </div>

      <div className="card">
        <div className="card-title">传感器数据</div>
        <div className="info-grid">
          <div className="info-item">
            <div className="info-label">环境温度</div>
            <div className="info-value">{machine.air_temp_k} K</div>
          </div>
          <div className="info-item">
            <div className="info-label">过程温度</div>
            <div className="info-value">{machine.process_temp_k} K</div>
          </div>
          <div className="info-item">
            <div className="info-label">温差</div>
            <div className="info-value">{machine.temp_diff_k.toFixed(2)} K</div>
          </div>
          <div className="info-item">
            <div className="info-label">转速</div>
            <div className="info-value">{machine.rotational_speed_rpm} RPM</div>
          </div>
          <div className="info-item">
            <div className="info-label">扭矩</div>
            <div className="info-value">{machine.torque_nm} Nm</div>
          </div>
          <div className="info-item">
            <div className="info-label">功率</div>
            <div className="info-value">{machine.power_w.toFixed(2)} W</div>
          </div>
          <div className="info-item">
            <div className="info-label">刀具磨损</div>
            <div className="info-value">{machine.tool_wear_min} min</div>
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">故障记录</div>
        <p style={{ marginBottom: 12 }}>
          设备故障：{' '}
          {machine.machine_failure ? (
            <span className="badge badge-danger">是</span>
          ) : (
            <span className="badge badge-success">否</span>
          )}
        </p>
        {activeFaults.length > 0 ? (
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {activeFaults.map((key) => (
              <span key={key} className="badge badge-danger">
                {FAULT_LABELS[key]}
              </span>
            ))}
          </div>
        ) : (
          <p className="subtitle">无故障记录</p>
        )}
      </div>
    </div>
  )
}

export default MachineDetail
