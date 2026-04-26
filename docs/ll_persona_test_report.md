# Study 2 LL × 多用户画像 测试报告

**配置**: 3 episodes (idx=[0, 34, 68]) × 3 personas × budget=5  
**LLM**: qwen3 @ http://110.42.252.68:8080  
**生成**: 2026-04-25 19:47:23

## 一、整体 bug 探测器

| 检测项 | 期望 | 实测 | 状态 |
|---|---|---|---|
| PI 问题漂成 PE 句式 | 0 | 0/27 | ✓ |
| 拒绝 PI 时 counter-placement 丢失 | 0（拒绝时若有 receptacle 应进 counter / 改向） | 0/27 | ✓ |

## 二、按 persona 分组

### cooperative_precise — 合作-精确

- 模式分布: AO=7, PI=8
- 状态累积: confirmed_actions=+22, confirmed_preferences=+8, negative_preferences=+0

### terse — 简短

- 模式分布: AO=7, PI=8
- 状态累积: confirmed_actions=+23, confirmed_preferences=+8, negative_preferences=+0

### resistant_redirect — 抗拒-改向

- 模式分布: AO=4, PI=11
- 状态累积: confirmed_actions=+22, confirmed_preferences=+9, negative_preferences=+2

## 三、逐轮明细

### cooperative_precise / episode_0 (living room)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the battery-powered remote go? | Yes — the battery-powered remote belongs on the me… | +1 | +0 | +0 |  |
| 2 | PR | small, portable electronics → TV stand | I'd expect small, portable electronics to go in the TV stand… | Yes — small, portable electronics belong on the TV… | +1 | +1 | +0 |  |
| 3 | PR | books should be placed on the bookshelf | I'd expect books to go on the bookshelf — does that match ho… | Yes — books belong on the bookshelf. | +2 | +1 | +0 |  |
| 4 | PR | small, corded electronics should be stor… | I'd expect small, corded electronics to go in the media draw… | Yes — small, corded electronics belong in the medi… | +2 | +1 | +0 |  |
| 5 | PR | soft, decorative items should be display… | I'd expect soft, decorative items to go on the coffee table … | Yes — soft, decorative items belong on the coffee … | +2 | +1 | +0 |  |

- 末态 confirmed_actions (8): [{'object_name': 'battery-powered remote', 'receptacle': 'media drawer'}, {'object_name': 'wireless speaker', 'receptacle': 'TV stand'}, {'object_name': 'hardcover novel', 'receptacle': 'bookshelf'}, {'object_name': 'hardcover art book', 'receptacle': 'bookshelf'}, {'object_name': 'wired game console', 'receptacle': 'media drawer'}, {'object_name': 'corded reading light', 'receptacle': 'media drawer'}, {'object_name': 'seasonal garland', 'receptacle': 'coffee table'}, {'object_name': 'soft stuffed bear', 'receptacle': 'coffee table'}]
- 末态 confirmed_preferences (4): [('small, portable electronics should be stored on the TV stand', 'TV stand'), ('books should be placed on the bookshelf', 'bookshelf'), ('small, corded electronics should be stored in the media drawer', 'media drawer'), ('soft, decorative items should be displayed on the coffee table', 'coffee table')]
- 末态 negative_preferences (0): []

### cooperative_precise / episode_34 (bedroom)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the battery-powered massager go? | Yes — battery-powered massager belongs on the beds… | +1 | +0 | +0 |  |
| 2 | PR | hardcover books → bedroom bookshelf | I'd expect hardcover books to go in the bedroom bookshelf — … | Yes — hardcover books belong on the bedroom booksh… | +2 | +1 | +0 |  |
| 3 | PR | folded scarves and off-season scarves → … | I'd expect folded scarves and off-season scarves to go in th… | Yes — folded scarves and off-season scarves belong… | +2 | +1 | +0 |  |
| 4 | AC |  | Where should the rechargeable hand warmer go? | Yes — rechargeable hand warmer belongs on the beds… | +1 | +0 | +0 |  |
| 5 | PR | small plug-in bedside electronics → nigh… | I'd expect small plug-in bedside electronics to go in the ni… | Yes — small plug-in bedside electronics belong on … | +0 | +1 | +0 |  |

- 末态 confirmed_actions (6): [{'object_name': 'battery-powered massager', 'receptacle': 'bedside drawer'}, {'object_name': 'hardcover sketchbook', 'receptacle': 'bedroom bookshelf'}, {'object_name': 'hardcover planner', 'receptacle': 'bedroom bookshelf'}, {'object_name': 'folded scarf', 'receptacle': 'wardrobe shelf'}, {'object_name': 'off-season scarf set', 'receptacle': 'wardrobe shelf'}, {'object_name': 'rechargeable hand warmer', 'receptacle': 'bedside drawer'}]
- 末态 confirmed_preferences (3): [('hardcover books should go on the bedroom bookshelf', 'bedroom bookshelf'), ('folded scarves and off-season scarves should go on the wardrobe shelf', 'wardrobe shelf'), ('small plug-in bedside electronics should go on the bedside drawer', 'bedside drawer')]
- 末态 negative_preferences (0): []

### cooperative_precise / episode_68 (kitchen)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the wired coffee grinder go? | Yes — the wired coffee grinder belongs on the prep… | +1 | +0 | +0 |  |
| 2 | PR | small kitchen tools and utensils → base … | I'd expect small kitchen tools and utensils to go in the bas… | Yes — small kitchen tools and utensils belong in t… | +4 | +1 | +0 |  |
| 3 | AC |  | Where should the plug-in toaster go? | Yes — the plug-in toaster belongs on the prep coun… | +1 | +0 | +0 |  |
| 4 | AC |  | Where should the battery-powered can opener go? | Yes — the battery-powered can opener belongs in th… | +1 | +0 | +0 |  |
| 5 | AC |  | Where should the digital kitchen timer go? | Yes — the digital kitchen timer belongs in the kit… | +1 | +0 | +0 |  |

- 末态 confirmed_actions (8): [{'object_name': 'wired coffee grinder', 'receptacle': 'prep counter'}, {'object_name': 'wooden citrus reamer', 'receptacle': 'base cabinet'}, {'object_name': 'wooden salad servers', 'receptacle': 'base cabinet'}, {'object_name': 'cake topper tin', 'receptacle': 'base cabinet'}, {'object_name': 'serving candle set', 'receptacle': 'base cabinet'}, {'object_name': 'plug-in toaster', 'receptacle': 'prep counter'}, {'object_name': 'battery-powered can opener', 'receptacle': 'kitchen drawer'}, {'object_name': 'digital kitchen timer', 'receptacle': 'kitchen drawer'}]
- 末态 confirmed_preferences (1): [('small kitchen tools and utensils should be stored in the base cabinet', 'base cabinet')]
- 末态 negative_preferences (0): []

### terse / episode_0 (living room)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the battery-powered remote go? | media drawer | +1 | +0 | +0 |  |
| 2 | PR | hardcover books → bookshelf | I'd expect hardcover books to go in the bookshelf — does tha… | yes | +2 | +1 | +0 |  |
| 3 | PR | small plug-in bedside electronics → side… | I'd expect small plug-in bedside electronics to go in the si… | yes | +2 | +1 | +0 |  |
| 4 | PR | cozy textiles and soft items should go o… | I'd expect cozy textiles and soft items to go on the coffee … | yes | +2 | +1 | +0 |  |
| 5 | PR | drinkware and beverages should go on the… | I'd expect drinkware and beverages to go on the TV stand — d… | yes | +2 | +1 | +0 |  |

- 末态 confirmed_actions (9): [{'object_name': 'battery-powered remote', 'receptacle': 'media drawer'}, {'object_name': 'hardcover novel', 'receptacle': 'bookshelf'}, {'object_name': 'hardcover art book', 'receptacle': 'bookshelf'}, {'object_name': 'wireless speaker', 'receptacle': 'side table'}, {'object_name': 'corded reading light', 'receptacle': 'side table'}, {'object_name': 'cotton lap blanket', 'receptacle': 'coffee table'}, {'object_name': 'soft stuffed bear', 'receptacle': 'coffee table'}, {'object_name': 'filled ceramic mug', 'receptacle': 'TV stand'}, {'object_name': 'sparkling water glass', 'receptacle': 'TV stand'}]
- 末态 confirmed_preferences (4): [('hardcover books should go on the bookshelf', 'bookshelf'), ('small plug-in bedside electronics should go on the side table', 'side table'), ('cozy textiles and soft items should go on the coffee table', 'coffee table'), ('drinkware and beverages should go on the TV stand', 'TV stand')]
- 末态 negative_preferences (0): []

### terse / episode_34 (bedroom)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the battery-powered massager go? | bedside drawer | +1 | +0 | +0 |  |
| 2 | PR | hardcover books → bedroom bookshelf | I'd expect hardcover books to go in the bedroom bookshelf — … | yes | +2 | +1 | +0 |  |
| 3 | PR | folded scarves and off-season scarves → … | I'd expect folded scarves and off-season scarves to go in th… | yes | +2 | +1 | +0 |  |
| 4 | AC |  | Where should the rechargeable hand warmer go? | bedside drawer | +1 | +0 | +0 |  |
| 5 | PR | small plug-in bedside electronics → nigh… | I'd expect small plug-in bedside electronics to go in the ni… | yes | +0 | +1 | +0 |  |

- 末态 confirmed_actions (6): [{'object_name': 'battery-powered massager', 'receptacle': 'bedside drawer'}, {'object_name': 'hardcover sketchbook', 'receptacle': 'bedroom bookshelf'}, {'object_name': 'hardcover planner', 'receptacle': 'bedroom bookshelf'}, {'object_name': 'folded scarf', 'receptacle': 'wardrobe shelf'}, {'object_name': 'off-season scarf set', 'receptacle': 'wardrobe shelf'}, {'object_name': 'rechargeable hand warmer', 'receptacle': 'bedside drawer'}]
- 末态 confirmed_preferences (3): [('hardcover books should go on the bedroom bookshelf', 'bedroom bookshelf'), ('folded scarves and off-season scarves should go on the wardrobe shelf', 'wardrobe shelf'), ('small plug-in bedside electronics should go on the nightstand', 'nightstand')]
- 末态 negative_preferences (0): []

### terse / episode_68 (kitchen)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the wired coffee grinder go? | prep counter | +1 | +0 | +0 |  |
| 2 | PR | small kitchen tools and utensils → base … | I'd expect small kitchen tools and utensils to go in the bas… | yes | +4 | +1 | +0 |  |
| 3 | AC |  | Where should the plug-in toaster go? | prep counter | +1 | +0 | +0 |  |
| 4 | AC |  | Where should the battery-powered can opener go? | kitchen drawer | +1 | +0 | +0 |  |
| 5 | AC |  | Where should the digital kitchen timer go? | kitchen drawer | +1 | +0 | +0 |  |

- 末态 confirmed_actions (8): [{'object_name': 'wired coffee grinder', 'receptacle': 'prep counter'}, {'object_name': 'wooden citrus reamer', 'receptacle': 'base cabinet'}, {'object_name': 'wooden salad servers', 'receptacle': 'base cabinet'}, {'object_name': 'cake topper tin', 'receptacle': 'base cabinet'}, {'object_name': 'serving candle set', 'receptacle': 'base cabinet'}, {'object_name': 'plug-in toaster', 'receptacle': 'prep counter'}, {'object_name': 'battery-powered can opener', 'receptacle': 'kitchen drawer'}, {'object_name': 'digital kitchen timer', 'receptacle': 'kitchen drawer'}]
- 末态 confirmed_preferences (1): [('small kitchen tools and utensils should be stored in the base cabinet', 'base cabinet')]
- 末态 negative_preferences (0): []

### resistant_redirect / episode_0 (living room)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the battery-powered remote go? | The battery-powered remote goes in the media drawe… | +1 | +0 | +0 |  |
| 2 | PR | hardcover books → bookshelf | I'd expect hardcover books to go in the bookshelf — does tha… | Yes, hardcover books go on the bookshelf — that's … | +2 | +1 | +0 |  |
| 3 | PR | small plug-in bedside electronics → side… | I'd expect small plug-in bedside electronics to go in the si… | Yes, small plug-in bedside electronics go on the s… | +2 | +1 | +0 |  |
| 4 | PR | cozy textiles and soft items should go o… | I'd expect cozy textiles and soft items to go on the coffee … | Yes, cozy textiles and soft items go on the storag… | +2 | +1 | +0 |  |
| 5 | PR | drinkware and beverages should go on the… | I'd expect drinkware and beverages to go on the coffee table… | No, drinkware and beverages go on the side table —… | +2 | +1 | +0 |  |

- 末态 confirmed_actions (9): [{'object_name': 'battery-powered remote', 'receptacle': 'media drawer'}, {'object_name': 'hardcover novel', 'receptacle': 'bookshelf'}, {'object_name': 'hardcover art book', 'receptacle': 'bookshelf'}, {'object_name': 'wireless speaker', 'receptacle': 'side table'}, {'object_name': 'corded reading light', 'receptacle': 'side table'}, {'object_name': 'cotton lap blanket', 'receptacle': 'storage ottoman'}, {'object_name': 'soft stuffed bear', 'receptacle': 'storage ottoman'}, {'object_name': 'filled ceramic mug', 'receptacle': 'side table'}, {'object_name': 'sparkling water glass', 'receptacle': 'side table'}]
- 末态 confirmed_preferences (4): [('hardcover books should go on the bookshelf', 'bookshelf'), ('small plug-in bedside electronics should go on the side table', 'side table'), ('cozy textiles and soft items should go on the storage ottoman', 'storage ottoman'), ('drinkware and beverages should go on the side table', 'side table')]
- 末态 negative_preferences (0): []

### resistant_redirect / episode_34 (bedroom)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the battery-powered massager go? | The battery-powered massager goes in the bedside d… | +1 | +0 | +0 |  |
| 2 | PR | hardcover books → bedroom bookshelf | I'd expect hardcover books to go in the bedroom bookshelf — … | Yes, hardcover books go on the bedroom bookshelf —… | +2 | +1 | +0 |  |
| 3 | PR | folded scarves and off-season scarves → … | I'd expect folded scarves and off-season scarves to go in th… | Yes, folded scarves and off-season scarves go on t… | +2 | +1 | +0 |  |
| 4 | AC |  | Where should the rechargeable hand warmer go? | The rechargeable hand warmer goes in the bedside d… | +1 | +0 | +0 |  |
| 5 | PR | small plug-in bedside electronics → nigh… | I'd expect small plug-in bedside electronics to go in the ni… | No, small plug-in bedside electronics go on the ni… | +0 | +1 | +0 |  |

- 末态 confirmed_actions (6): [{'object_name': 'battery-powered massager', 'receptacle': 'bedside drawer'}, {'object_name': 'hardcover sketchbook', 'receptacle': 'bedroom bookshelf'}, {'object_name': 'hardcover planner', 'receptacle': 'bedroom bookshelf'}, {'object_name': 'folded scarf', 'receptacle': 'wardrobe shelf'}, {'object_name': 'off-season scarf set', 'receptacle': 'wardrobe shelf'}, {'object_name': 'rechargeable hand warmer', 'receptacle': 'bedside drawer'}]
- 末态 confirmed_preferences (3): [('hardcover books should go on the bedroom bookshelf', 'bedroom bookshelf'), ('folded scarves and off-season scarves should go on the wardrobe shelf', 'wardrobe shelf'), ('small plug-in bedside electronics should go on the nightstand', 'nightstand')]
- 末态 negative_preferences (0): []

### resistant_redirect / episode_68 (kitchen)

| turn | pattern | hyp | Q | A | Δca | Δcp | Δnp | drift |
|---|---|---|---|---|---|---|---|---|
| 1 | AC |  | Where should the wired coffee grinder go? | The wired coffee grinder goes on the prep counter. | +1 | +0 | +0 |  |
| 2 | PR | small kitchen tools and utensils → base … | I'd expect small kitchen tools and utensils to go in the bas… | No, small kitchen tools and utensils like the batt… | +1 | +0 | +1 |  |
| 3 | PR | small, frequently used kitchen gadgets →… | I'd expect small, frequently used kitchen gadgets → prep cou… | Yes, small, frequently used kitchen gadgets like t… | +2 | +1 | +0 |  |
| 4 | PR | utensils and serving items → base cabine… | I'd expect utensils and serving items to go in the base cabi… | No, utensils and serving items like the wooden sal… | +1 | +0 | +1 |  |
| 5 | PR | glass and porcelain items → upper cabine… | I'd expect glass and porcelain items to go in the upper cabi… | Yes, glass and porcelain items like the glass pitc… | +2 | +1 | +0 |  |

- 末态 confirmed_actions (7): [{'object_name': 'wired coffee grinder', 'receptacle': 'prep counter'}, {'object_name': 'wooden citrus reamer', 'receptacle': 'kitchen drawer'}, {'object_name': 'digital kitchen timer', 'receptacle': 'prep counter'}, {'object_name': 'cut lemon container', 'receptacle': 'prep counter'}, {'object_name': 'wooden salad servers', 'receptacle': 'upper cabinet'}, {'object_name': 'porcelain teacup set', 'receptacle': 'upper cabinet'}, {'object_name': 'glass pitcher', 'receptacle': 'upper cabinet'}]
- 末态 confirmed_preferences (2): [('small, frequently used kitchen gadgets should go on the prep counter', 'prep counter'), ('glass and porcelain items should go in the upper cabinet', 'upper cabinet')]
- 末态 negative_preferences (2): ['small kitchen tools and utensils → base cabinet', 'utensils and serving items → base cabinet']

## 四、结论

- 两个上一轮报出的 bug 在所有 persona / 所有房间下均**未复现** ✓
