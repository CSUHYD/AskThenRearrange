# Study 2 LL 策略与 §3 定义合规性测试报告

**测试规模**: 5 episodes × budget=5（共 25 轮问答）  
**LLM**: qwen3 @ http://110.42.252.68:8080  
**生成时间**: 2026-04-26 14:42:44

## §3 LL 定义复核（核对项）

| 定义维度 | §3 要求 | 实测 | 通过 |
|---|---|---|---|
| 策略组成 | 仅 AO + PI（无 PE） | PE=0 (0.0%) | ✓ |
| PI > PE（计数主导） | PI 数 > PE 数 | PI=16, PE=0 | ✓ |
| PI 假设来源 | 允许 prior knowledge / common sense | 0/16 轮在零 confirmed_actions 状态下提出 PI（即纯 common sense）| N/A（未观察到，可能样本太小） |
| 实现细节：turn 1 即 PI | Study2 设计要求 turn 1 起触发 PI | 5/5 episodes 在 turn 1 出 PI | ✓ |
| AO/PI fallback 率 | PI 提不出假设时回退 AO | 1/25 次回退 | ✓ |

## 各 episode 序列

| episode | room | 模式序列 | 计数 | PI>PE & PE=0 | fallback |
|---|---|---|---|---|---|
| episode_0 | living room | PR→AC→PR→AC→PR | AO=2 PE=0 PI=3 | ✓ | 0 |
| episode_17 | living room | PR→AC→PR→PR→PR | AO=1 PE=0 PI=4 | ✓ | 0 |
| episode_34 | bedroom | PR→AC→PR→PR→AC | AO=2 PE=0 PI=3 | ✓ | 0 |
| episode_51 | bedroom | PR→AC→AC→PR→PR | AO=2 PE=0 PI=3 | ✓ | 1 |
| episode_68 | kitchen | PR→AC→PR→AC→PR | AO=2 PE=0 PI=3 | ✓ | 0 |

## PI 问题样例（前 10 条）

- **episode_0 turn 1** 
  - 假设: *hardcover books → bookshelf*
  - 问题: "I'd expect hardcover books to go in the bookshelf — does that match how you like to organise things?"
- **episode_0 turn 3** 
  - 假设: *small, decorative items should be placed on the coffee table*
  - 问题: "I'd expect small, decorative items to go on the coffee table — does that match how you like to organise things?"
- **episode_17 turn 1** 
  - 假设: *books → bookshelf*
  - 问题: "I'd expect books to go in the bookshelf — does that match how you like to organise things?"
- **episode_17 turn 3** 
  - 假设: *decorative items should be displayed on the center table*
  - 问题: "I'd expect decorative items to go in the center table — does that match how you like to organise things?"
- **episode_34 turn 1** 
  - 假设: *small personal accessories like jewelry and hair clips → vanity tray*
  - 问题: "I'd expect small personal accessories like jewelry and hair clips to go in the vanity tray — does that match how you like to organise things?"
- **episode_34 turn 3** 
  - 假设: *small personal items like scarves and folded clothing should be stored in the storage bench*
  - 问题: "I'd expect small personal items like the folded scarf and off-season scarf set to go in the storage bench — does that match how you like to organise things?"
- **episode_51 turn 1** 
  - 假设: *personal journals and devotional books → reading shelf*
  - 问题: "I'd expect personal journals and devotional books to go in the reading shelf — does that match how you like to organise things?"
- **episode_68 turn 1** 
  - 假设: *wooden kitchen utensils → kitchen drawer*
  - 问题: "I'd expect wooden kitchen utensils to go in the kitchen drawer — does that match how you like to organise things?"
- **episode_68 turn 3** 
  - 假设: *small, frequently used kitchen tools should be placed on the prep counter*
  - 问题: "I'd expect small, frequently used kitchen tools to go on the prep counter — does that match how you like to organise things?"

## 结论

- §3 LL 强约束（PE=0、PI>PE）**全部通过** ✓
