import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import DeviceVisual from '../components/DeviceVisual'

const API_BASE = 'http://localhost:8000'

const STATUS_OPTIONS = ['open', 'in_progress', 'resolved', 'closed']
const PRIORITY_OPTIONS = ['low', 'medium', 'high']

const STATUS_LABEL = {
  open: '待处理',
  in_progress: '处理中',
  resolved: '已解决',
  closed: '已关闭',
}

const STATUS_BADGE = {
  open: 'badge-warning',
  in_progress: 'badge-primary',
  resolved: 'badge-success',
  closed: 'badge-neutral',
}

const PRIORITY_LABEL = {
  low: '低',
  medium: '中',
  high: '高',
}

const PRIORITY_BADGE = {
  low: 'badge-neutral',
  medium: 'badge-warning',
  high: 'badge-danger',
}

function Tickets() {
  const [tickets, setTickets] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const [form, setForm] = useState({
    machine_id: '',
    description: '',
    status: 'open',
    priority: 'medium',
  })
  const [createError, setCreateError] = useState(null)

  const [editingId, setEditingId] = useState(null)
  const [editForm, setEditForm] = useState({ description: '', status: '', priority: '' })

  function loadTickets() {
    setLoading(true)
    setError(null)
    fetch(`${API_BASE}/api/tickets`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`请求失败：HTTP ${res.status}`)
        }
        return res.json()
      })
      .then((data) => {
        setTickets(data.items)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }

  useEffect(() => {
    loadTickets()
  }, [])

  function handleCreate(e) {
    e.preventDefault()
    setCreateError(null)

    fetch(`${API_BASE}/api/tickets`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        machine_id: Number(form.machine_id),
        description: form.description,
        status: form.status,
        priority: form.priority,
      }),
    })
      .then(async (res) => {
        if (!res.ok) {
          const body = await res.json().catch(() => ({}))
          throw new Error(body.detail || `创建失败：HTTP ${res.status}`)
        }
        return res.json()
      })
      .then(() => {
        setForm({ machine_id: '', description: '', status: 'open', priority: 'medium' })
        loadTickets()
      })
      .catch((err) => setCreateError(err.message))
  }

  function startEdit(ticket) {
    setEditingId(ticket.id)
    setEditForm({ description: ticket.description, status: ticket.status, priority: ticket.priority })
  }

  function cancelEdit() {
    setEditingId(null)
  }

  function saveEdit(id) {
    fetch(`${API_BASE}/api/tickets/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(editForm),
    })
      .then(async (res) => {
        if (!res.ok) {
          const body = await res.json().catch(() => ({}))
          throw new Error(body.detail || `更新失败：HTTP ${res.status}`)
        }
        return res.json()
      })
      .then(() => {
        setEditingId(null)
        loadTickets()
      })
      .catch((err) => setError(err.message))
  }

  function handleDelete(id) {
    if (!confirm(`确认删除工单 #${id}？`)) {
      return
    }
    fetch(`${API_BASE}/api/tickets/${id}`, { method: 'DELETE' })
      .then((res) => {
        if (!res.ok && res.status !== 204) {
          throw new Error(`删除失败：HTTP ${res.status}`)
        }
        loadTickets()
      })
      .catch((err) => setError(err.message))
  }

  return (
    <div>
      <div className="ambient-visual bottom-left">
        <DeviceVisual size="ambient" rotation={-30} blur={3} opacity={0.08} />
      </div>

      <Link to="/devices" className="back-link">← 返回设备监控</Link>
      <div className="page-header">
        <div>
          <div className="eyebrow">服务台</div>
          <h1>维修工单</h1>
          <div className="subtitle">将设备风险转化为实际维护行动。</div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">创建工单</div>
        <form onSubmit={handleCreate} className="form-row">
          <div className="field">
            <label>设备 UDI</label>
            <input
              type="number"
              placeholder="设备 UDI"
              value={form.machine_id}
              onChange={(e) => setForm({ ...form, machine_id: e.target.value })}
              required
            />
          </div>
          <div className="field" style={{ flex: 1, minWidth: 240 }}>
            <label>故障描述</label>
            <input
              type="text"
              placeholder="请描述故障情况"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              required
            />
          </div>
          <div className="field">
            <label>状态</label>
            <select value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })}>
              {STATUS_OPTIONS.map((s) => (
                <option key={s} value={s}>
                  {STATUS_LABEL[s]}
                </option>
              ))}
            </select>
          </div>
          <div className="field">
            <label>优先级</label>
            <select value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })}>
              {PRIORITY_OPTIONS.map((p) => (
                <option key={p} value={p}>
                  {PRIORITY_LABEL[p]}
                </option>
              ))}
            </select>
          </div>
          <button type="submit" className="btn-primary">
            创建工单
          </button>
        </form>
        {createError && <p className="state-msg is-error">{createError}</p>}
      </div>

      <div className="card" style={{ marginTop: 20 }}>
        <div className="card-title">工单列表</div>

        {loading && <p className="state-msg">加载中...</p>}
        {error && <p className="state-msg is-error">加载失败：{error}</p>}

        {!loading && !error && (
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>设备 UDI</th>
                  <th>故障描述</th>
                  <th>状态</th>
                  <th>优先级</th>
                  <th>创建时间</th>
                  <th>解决时间</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map((t) => {
                  const isEditing = editingId === t.id
                  return (
                    <tr key={t.id}>
                      <td>{t.id}</td>
                      <td>
                        <Link to={`/machines/${t.machine_id}`}>{t.machine_id}</Link>
                      </td>
                      <td>
                        {isEditing ? (
                          <input
                            type="text"
                            value={editForm.description}
                            onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                          />
                        ) : (
                          t.description
                        )}
                      </td>
                      <td>
                        {isEditing ? (
                          <select
                            value={editForm.status}
                            onChange={(e) => setEditForm({ ...editForm, status: e.target.value })}
                          >
                            {STATUS_OPTIONS.map((s) => (
                              <option key={s} value={s}>
                                {STATUS_LABEL[s]}
                              </option>
                            ))}
                          </select>
                        ) : (
                          <span className={`badge ${STATUS_BADGE[t.status]}`}>{STATUS_LABEL[t.status] || t.status}</span>
                        )}
                      </td>
                      <td>
                        {isEditing ? (
                          <select
                            value={editForm.priority}
                            onChange={(e) => setEditForm({ ...editForm, priority: e.target.value })}
                          >
                            {PRIORITY_OPTIONS.map((p) => (
                              <option key={p} value={p}>
                                {PRIORITY_LABEL[p]}
                              </option>
                            ))}
                          </select>
                        ) : (
                          <span className={`badge ${PRIORITY_BADGE[t.priority]}`}>
                            {PRIORITY_LABEL[t.priority] || t.priority}
                          </span>
                        )}
                      </td>
                      <td>{t.created_at ? new Date(t.created_at).toLocaleString() : ''}</td>
                      <td>{t.resolved_at ? new Date(t.resolved_at).toLocaleString() : ''}</td>
                      <td>
                        {isEditing ? (
                          <div style={{ display: 'flex', gap: 6 }}>
                            <button onClick={() => saveEdit(t.id)} className="btn-primary btn-sm">
                              保存
                            </button>
                            <button onClick={cancelEdit} className="btn-sm">
                              取消
                            </button>
                          </div>
                        ) : (
                          <div style={{ display: 'flex', gap: 6 }}>
                            <button onClick={() => startEdit(t)} className="btn-sm">
                              编辑
                            </button>
                            <button onClick={() => handleDelete(t.id)} className="btn-danger btn-sm">
                              删除
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default Tickets
