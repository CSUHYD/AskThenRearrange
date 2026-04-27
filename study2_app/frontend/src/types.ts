export interface AgentStateSnapshot {
  room?: string | null
  receptacles: string[]
  seen_objects: string[]
  unseen_objects: string[]
  qa_turns: number
  confirmed_actions: Array<{ object_name: string; receptacle: string }>
  negative_actions: Array<{ object_name: string; receptacle: string }>
  confirmed_preferences: Array<{
    hypothesis: string
    covered_objects?: string[]
    receptacle?: string | null
  }>
  negative_preferences: Array<{
    hypothesis: string
    covered_objects?: string[]
    receptacle?: string | null
  }>
  unresolved_objects: string[]
}

export interface QATurn {
  turn_index: number
  pattern: string
  question: string
  answer: string
  state_after?: AgentStateSnapshot | null
}

export interface TrialSnapshot {
  trial_index: number
  strategy: string
  room_type: string
  episode_index: number
  receptacles: string[]
  seen_objects: string[]
  unseen_objects: string[]
  name_mapping?: Record<string, string>  // en -> zh display labels
  dialogue: QATurn[]
  turns_used: number
  stop_reason: string | null
  preference_assignments: Record<string, string> | null
  seen_placements: Record<string, string> | null
  unseen_placements: Record<string, string> | null
  predicted_placements: Record<string, string> | null
  psr: {
    seen_psr: number
    unseen_psr: number
    total_psr: number
    item_scores: Record<string, boolean>
  } | null
  phase: string
}

export interface SessionSnapshot {
  session_id: string
  participant_id: string
  latin_square_row: number
  trial_order: Array<{ strategy: string; room_type: string }>
  current_trial_index: number
  trials: TrialSnapshot[]
  phase: string
  notes: string
  agent_state?: AgentStateSnapshot | null
  strategy_ranking?: string[] | null
  final_comment?: string
  budget_total?: number
}

export interface NextQuestionResponse {
  question: string
  pattern: string
  turn_index: number
  dialogue_complete: boolean
}

export interface ScoreResponse {
  seen_psr: number
  unseen_psr: number
  total_psr: number
  item_scores: Record<string, boolean>
}

export const STRATEGY_LABELS: Record<string, string> = {
  TO: '任务专注（TO）',
  UL: '用户主导（UL）',
  LL: '学习者主导（LL）',
  HYB: '混合（HYB）',
  // Legacy aliases — historical sessions logged short codes DQ/UPF/PAR.
  DQ: '任务专注（TO，旧名 DQ）',
  UPF: '用户主导（UL，旧名 UPF）',
  PAR: '学习者主导（LL，旧名 PAR）',
}

export const PATTERN_LABELS: Record<string, string> = {
  action_oriented: '动作导向',
  preference_eliciting: '偏好探询',
  preference_induction: '偏好归纳',
}

export const ROOM_LABELS: Record<string, string> = {
  // Study 2 SOP v2.5 scenes
  study_desk: '书桌',
  bar_kitchen: '厨房',
  fridge: '冰箱',
  bedroom_practice: '卧室（练习）',
  // Legacy keys (kept so historical sessions still render).
  'living room': '客厅',
  bedroom: '卧室',
  kitchen: '厨房',
}

export const PHASE_LABELS: Record<string, string> = {
  created: '待载入场景',
  scene_intro: '场景介绍',
  dialogue: '对话进行中',
  dialogue_complete: '对话已结束',
  preference_form: '偏好分配中',
  final_ranking: '策略排名',
  completed: '实验完成',
}
