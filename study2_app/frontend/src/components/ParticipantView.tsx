import React, { useState } from 'react'
import { useSession } from '../App'
import * as api from '../api'
import { primeAudio } from '../voice'
import SceneIntro from './SceneIntro'
import DialogueView from './DialogueView'
import PreferenceForm from './PreferenceForm'
import PredictionView from './PredictionView'
import FinalRanking from './FinalRanking'
import SessionReport from './SessionReport'

export default function ParticipantView() {
  const { session, setSession, setCurrentQuestion, setLoading, setError, loading, error } =
    useSession()
  const [showReport, setShowReport] = useState(false)

  async function handleStart() {
    if (!session) return
    setLoading(true)
    setError(null)
    primeAudio()
    try {
      const q = await api.startDialogue(session.session_id)
      setCurrentQuestion(q)
      const s = await api.getSession(session.session_id)
      setSession(s)
    } catch (e: any) {
      setError(e?.response?.data?.detail ?? String(e))
    } finally {
      setLoading(false)
    }
  }

  if (!session) {
    return (
      <div className="empty-state">
        <p>请在左侧创建会话以开始实验。</p>
      </div>
    )
  }

  const phase = session.phase
  const currentIdx = session.current_trial_index
  const currentTrial = session.trials[currentIdx]
  const lastCompletedTrial =
    currentIdx > 0 ? session.trials[currentIdx - 1] : null

  return (
    <div>
      {error && (
        <div
          style={{
            background: '#fce8e8',
            border: '1px solid #f5c6c6',
            borderRadius: 8,
            padding: '10px 14px',
            marginBottom: 16,
            color: '#7a1a1a',
            fontSize: 13,
          }}
        >
          ⚠ {error}
        </div>
      )}

      {/* Show last trial results while waiting for next trial */}
      {phase === 'created' && lastCompletedTrial?.psr && (
        <PredictionView trial={lastCompletedTrial} showNext />
      )}

      {/* Trial 3 prediction is shown together with the final-ranking page,
          since phase jumps preference_form → final_ranking with no
          intermediate 'created' state to display predictions. */}
      {phase === 'final_ranking' && lastCompletedTrial?.psr && (
        <PredictionView trial={lastCompletedTrial} />
      )}

      {/* Scene is loaded — show scene info */}
      {(phase === 'scene_intro' || phase === 'dialogue' || phase === 'dialogue_complete') &&
        currentTrial && <SceneIntro trial={currentTrial} />}

      {/* Participant-side start button: shown only after scene is loaded
          and before dialogue begins. Triggers the same /dialogue/start
          endpoint as the experimenter's '开始对话' button. */}
      {phase === 'scene_intro' && currentTrial && (
        <div className="participant-card" style={{ textAlign: 'center' }}>
          <button
            className="btn btn-success"
            onClick={handleStart}
            disabled={loading}
            style={{ fontSize: 18, padding: '12px 32px', minWidth: 200 }}
          >
            {loading ? '请稍候…' : '开始'}
          </button>
          <p style={{ fontSize: 12, color: '#888', marginTop: 12 }}>
            熟悉好场景后，点击"开始"开启与机器人的对话
          </p>
        </div>
      )}

      {/* Active or ended dialogue */}
      {(phase === 'dialogue' || phase === 'dialogue_complete') && currentTrial && (
        <DialogueView trial={currentTrial} />
      )}

      {/* Participant fills preference form — shown as soon as dialogue ends */}
      {(phase === 'dialogue_complete' || phase === 'preference_form') && currentTrial && (
        <PreferenceForm trial={currentTrial} />
      )}

      {/* Final ranking after all 3 trials */}
      {phase === 'final_ranking' && <FinalRanking />}

      {/* Session complete */}
      {phase === 'completed' && (
        <>
          <div className="participant-card">
            <h2>实验完成</h2>
            <p style={{ color: '#555', marginTop: 8 }}>感谢参与！所有数据已记录。</p>
            <button
              className="btn btn-primary mt-16"
              onClick={() => setShowReport((v) => !v)}
            >
              {showReport ? '隐藏实验报告' : '查看实验报告'}
            </button>
          </div>
          {showReport && <SessionReport />}
        </>
      )}

      {/* Waiting to load first trial */}
      {phase === 'created' && currentIdx === 0 && (
        <div className="empty-state">
          <p>请在左侧选择场景，然后点击"载入场景"。</p>
        </div>
      )}
    </div>
  )
}
