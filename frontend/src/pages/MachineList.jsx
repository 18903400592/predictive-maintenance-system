import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import DeviceVisual from '../components/DeviceVisual'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const STATUS_TABS = [
  { value: 'all', label: '全部' },
  { value: 'normal', label: '正常' },
  { value: 'failure', label: '故障' },
]

const RISK_LEVEL_OPTIONS = [
  { value: 'all', label: '全部' },
  { value: 'low', label: '低' },
  { value: 'medium', label: '中' },
  { value: 'high', label: '高' },
]

const RISK_LEVEL_BADGE = {
  high: 'badge-danger',
  medium: 'badge-warning',
  low: 'badge-success',
}

const RISK_LEVEL_LABEL = {
  high: '高',
  medium: '中',
  low: '低',
}

function MachineList() {
  const [machines, setMachines] = useState([])
  const [totalMatched, setTotalMatched] = useState(0)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [typeFilter, setTypeFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [riskLevelFilter, setRiskLevelFilter] = useState('all')

  const [stats, setStats] = useState(null)
  const [statsError, setStatsError] = useState(null)

  useEffect(() => {
    const params = new URLSearchParams({ limit: '50', status: statusFilter, risk_level: riskLevelFilter })
    if (typeFilter) {
      params.set('type', typeFilter)
    }

    setLoading(true)
    setError(null)

    fetch(`${API_BASE}/api/machines?${params.toString()}`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`请求失败：HTTP ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        setMachines(data.items)
        setTotalMatched(data.total_matched)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [typeFilter, statusFilter, riskLevelFilter])

  useEffect(() => {
    fetch(`${API_BASE}/api/machines/stats`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`请求失败：HTTP ${res.status}`)
        }
        return res.json()
      })
      .then((data) => setStats(data))
      .catch((err) => setStatsError(err.message))
  }, [])

  return (
    <div>
      <div className="ambient-visual top-right">
        <DeviceVisual size="ambient" rotation={35} blur={3} opacity={0.08} />
      </div>

      <div className="page-header">
        <div>
          <div className="eyebrow">设备总览</div>
          <h1>设备监控</h1>
          <div className="subtitle">查看设备运行状态，以及模型识别出的潜在风险。</div>
        </div>
      </div>

      <div className="stat-grid">
        <div className="stat-card tone-neutral">
          <div className="stat-label">设备总数</div>
          <div className="stat-value">{stats ? stats.total : '—'}</div>
        </div>
        <div className="stat-card tone-success">
          <div className="stat-label">正常设备</div>
          <div className="stat-value">{stats ? stats.normal : '—'}</div>
        </div>
        <div className="stat-card tone-danger">
          <div className="stat-label">真实故障</div>
          <div className="stat-value">{stats ? stats.failure : '—'}</div>
        </div>
        <div className="stat-card tone-warning">
          <div className="stat-label">高风险设备</div>
          <div className="stat-value">{stats ? stats.high_risk : '—'}</div>
        </div>
      </div>
      {statsError && <p className="state-msg is-error">统计数据加载失败：{statsError}</p>}

      <div className="card">
        <div className="toolbar">
          <div className="field">
            <label>状态（实际）</label>
            <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
              {STATUS_TABS.map((s) => (
                <option key={s.value} value={s.value}>
                  {s.label}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>风险等级（预测）</label>
            <select value={riskLevelFilter} onChange={(e) => setRiskLevelFilter(e.target.value)}>
              {RISK_LEVEL_OPTIONS.map((r) => (
                <option key={r.value} value={r.value}>
                  {r.label}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>设备类型</label>
            <select value={typeFilter} onChange={(e) => setTypeFilter(e.target.value)}>
              <option value="">全部</option>
              <option value="H">H</option>
              <option value="M">M</option>
              <option value="L">L</option>
            </select>
          </div>
        </div>

        {loading && <p className="state-msg">加载中...</p>}
        {error && <p className="state-msg is-error">加载失败：{error}</p>}

        {!loading && !error && (
          <>
            <div className="table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>UDI</th>
                    <th>产品编号</th>
                    <th>类型</th>
                    <th>环境温度 (K)</th>
                    <th>过程温度 (K)</th>
                    <th>转速 (RPM)</th>
                    <th>扭矩 (Nm)</th>
                    <th>刀具磨损 (min)</th>
                    <th>风险评分</th>
                    <th>风险等级</th>
                    <th>状态</th>
                  </tr>
                </thead>
                <tbody>
                  {machines.map((m) => (
                    <tr key={m.udi} className={m.machine_failure ? 'row-failure' : undefined}>
                      <td>
                        <Link to={`/machines/${m.udi}`}>{m.udi}</Link>
                      </td>
                      <td>{m.product_id}</td>
                      <td>{m.type}</td>
                      <td>{m.air_temp_k}</td>
                      <td>{m.process_temp_k}</td>
                      <td>{m.rotational_speed_rpm}</td>
                      <td>{m.torque_nm}</td>
                      <td>{m.tool_wear_min}</td>
                      <td>{(m.risk_score * 100).toFixed(1)}%</td>
                      <td>
                        <span className={`badge ${RISK_LEVEL_BADGE[m.risk_level]}`}>
                          {RISK_LEVEL_LABEL[m.risk_level]}
                        </span>
                      </td>
                      <td>
                        {m.machine_failure ? (
                          <span className="badge badge-danger">故障</span>
                        ) : (
                          <span className="badge badge-success">正常</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <p className="subtitle" style={{ marginTop: 12 }}>
              共 {totalMatched} 台设备符合筛选条件，显示前 {machines.length} 台
            </p>
          </>
        )}
      </div>
    </div>
  )
}

export default MachineList
