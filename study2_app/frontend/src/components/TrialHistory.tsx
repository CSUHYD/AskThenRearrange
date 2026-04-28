import React, { useState } from 'react'
import { useSession } from '../App'
import { ROOM_LABELS, STRATEGY_LABELS, PATTERN_LABELS } from '../types'

export default function TrialHistory() {
  const { session } = useSession()
  const [openIdx, setOpenIdx] = useState<number | null>(null)

  if (!session) return null
  const trialsWithDialogue = session.trials.filter((t) => t.dialogue.length > 0)
  if (trialsWithDialogue.length === 0) return null

  return (
    <div className="exp-section">
      <div className="exp-label">问答历史（按场景）</div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {trialsWithDialogue.map((t) => {
          const open = openIdx === t.trial_index
          const zh = (n: string) => t.name_mapping?.[n] ?? n
          return (
            <div
              key={t.trial_index}
              style={{
                background: '#f8f9fa',
                border: '1px solid #e0e0e0',
                borderRadius: 6,
                overflow: 'hidden',
              }}
            >
              <button
                onClick={() => setOpenIdx(open ? null : t.trial_index)}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '8px 12px',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: 13,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <span>
                  Trial {t.trial_index + 1} ·{' '}
                  {STRATEGY_LABELS[t.strategy] ?? t.strategy} ·{' '}
                  {ROOM_LABELS[t.room_type] ?? t.room_type}
                </span>
                <span style={{ color: '#888', fontSize: 12 }}>
                  {t.dialogue.length} 轮 {open ? '▲' : '▼'}
                </span>
              </button>
              {open && (
                <div style={{ padding: '8px 12px', borderTop: '1px solid #e0e0e0' }}>
                  {t.dialogue.map((turn, i) => (
                    <div
                      key={i}
                      style={{
                        marginBottom: 10,
                        fontSize: 12,
                        lineHeight: 1.5,
                      }}
                    >
                      <div style={{ color: '#666', marginBottom: 2 }}>
                        T{turn.turn_index + 1}{' '}
                        <span
                          style={{
                            background: '#dde7f5',
                            padding: '1px 6px',
                            borderRadius: 3,
                            fontSize: 11,
                            color: '#3a5a8c',
                          }}
                        >
                          {PATTERN_LABELS[turn.pattern] ?? turn.pattern}
                        </span>
                      </div>
                      <div style={{ marginBottom: 2 }}>
                        <strong style={{ color: '#3a5a8c' }}>Q:</strong>{' '}
                        {zh(turn.question)}
                      </div>
                      <div>
                        <strong style={{ color: '#5a3a8c' }}>A:</strong>{' '}
                        {turn.answer ? zh(turn.answer) : <em style={{ color: '#999' }}>（无应答）</em>}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
