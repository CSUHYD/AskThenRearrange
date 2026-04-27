import React, { useState } from 'react'
import { useSession } from '../App'
import * as api from '../api'

export default function SessionCreate() {
  const { setSession, setLoading, setError, loading, error } = useSession()
  const [participantId, setParticipantId] = useState('')
  const [notes, setNotes] = useState('')

  async function handleCreate() {
    if (!participantId.trim()) {
      setError('请输入参与者 ID')
      return
    }
    setLoading(true)
    setError(null)
    try {
      // Latin square row is derived server-side from participant_id per SOP §A
      // (P01–P04 row 1, P05–P08 row 2, ...).
      const s = await api.createSession(participantId.trim(), notes.trim())
      setSession(s)
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div className="form-group">
        <label className="form-label">参与者 ID</label>
        <input
          className="form-input"
          value={participantId}
          onChange={(e) => setParticipantId(e.target.value)}
          placeholder="例如：P01"
        />
      </div>
      <div className="form-group">
        <label className="form-label">备注（可选）</label>
        <input
          className="form-input"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          placeholder="实验备注"
        />
      </div>
      {error && (
        <div style={{ color: '#ff6b6b', fontSize: 12 }}>{error}</div>
      )}
      <button className="btn btn-primary" onClick={handleCreate} disabled={loading}>
        {loading ? '创建中…' : '创建会话'}
      </button>
    </div>
  )
}
