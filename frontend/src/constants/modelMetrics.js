// 静态叙事文案数字 —— 来自 backend/scripts/train_model.py 的离线评估输出。
// 这些数字未被持久化到数据库，也没有对应的 API 端点，因此无法实时获取，
// 仅作为首页故事的叙事文案硬编码在此处。与真实设备数据（sensor readings、
// risk_score、fleet 统计等，均来自 API）严格分开，不混入任何组件的实时数据流。
export const MODEL_METRICS = {
  accuracy: '96.85%',
  defaultThreshold: 0.5,
  recallAtDefaultThreshold: '14.71%',
  recallAtDefaultThresholdFraction: '10/68',
  chosenThreshold: 0.031,
  recallAtChosenThreshold: '77.94%',
  recallAtChosenThresholdFraction: '53/68',
  falsePositivesAtChosenThreshold: 346,
}
