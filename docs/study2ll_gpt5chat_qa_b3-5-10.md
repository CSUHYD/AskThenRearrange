# Study 2 LL × GPT-5-Chat × 5 ep × Budgets 3/5/10 — QA 完整记录

## PSR 聚合

| Budget | Seen | Unseen |
|---|---|---|
| 3 | 75.0% ± 5.9 | 58.3% ± 16.9 |
| 5 | 78.3% ± 5.7 | 81.7% ± 6.1 |
| 10 | **95.0% ± 2.0** | **91.7% ± 3.7** |

单调递增，无 over-induction 现象。B=10 已接近 ceiling。

## 各 episode @ B=10 模式序列 + PSR 轨迹

| ep | room | seq (10 turns) | u@3 | u@5 | u@10 |
|---|---|---|---|---|---|
| episode_0 | living room | AO→PI→AO→PI→AO→PI→AO→AO→PI→PI | 92% | 83% | 92% |
| episode_17 | living room | PI→AO→PI→AO→PI→AO→AO→AO→PI→AO | 42% | 58% | 83% |
| episode_34 | bedroom | AO→PI→AO→PI→AO→PI→AO→AO→AO→AO | 0% | 92% | 100% |
| episode_51 | bedroom | AO→PI→AO→PI→AO→AO→PI→AO→AO→AO | 83% | 83% | 83% |
| episode_68 | kitchen | AO→AO→PI→AO→PI→AO→AO→AO→PI→AO | 75% | 92% | 100% |

---

## episode_0 (living room)

**PSR 轨迹**: u@3=92% → u@5=83% → u@10=92%, fb=0

**末态 confirmed_actions** (12):
- `battery-powered remote` → `media drawer`
- `wired game console` → `TV stand`
- `wireless speaker` → `media drawer`
- `corded reading light` → `TV stand`
- `hardcover novel` → `bookshelf`
- `hardcover art book` → `bookshelf`
- `cotton lap blanket` → `storage ottoman`
- `filled ceramic mug` → `side table`
- `sparkling water glass` → `side table`
- `spare coaster pouch` → `side table`
- `soft stuffed bear` → `storage ottoman`
- `seasonal garland` → `storage basket`

**末态 confirmed_preferences** (5):
- *larger plug‑in media electronics like the wired game console are kept on the TV stand*
  - → TV stand, covers ['wired game console']
- *hardcover books such as novels or art books should be stored upright on the bookshelf*
  - → bookshelf, covers ['hardcover novel', 'hardcover art book']
- *drinkware and coasters should be kept on the side table for easy reach while seated*
  - → side table, covers ['filled ceramic mug', 'sparkling water glass', 'spare coaster pouch']
- *soft comfort items such as blankets and stuffed toys should be stored together in the storage ottoman when not in use*
  - → storage ottoman, covers ['cotton lap blanket', 'soft stuffed bear']
- *small handheld electronics like remotes or portable speakers should be stored together in the media drawer when not in use*
  - → media drawer, covers ['battery-powered remote', 'wireless speaker']

### QA Sequence (10 turns)
**T1 [AO]** target=`battery-powered remote`
- Q: Where should the battery-powered remote go?
- A: The battery-powered remote should go in the media drawer.

**T2 [PI]** target=`media-related electronics such as speakers or gaming consoles are kept on or inside the TV stand`
- Q: I'd expect media-related electronics like the wireless speaker or game console to stay on or inside the TV stand — does that match how you like to organise things?
- A: Yes, that's close to how I do it — I keep larger plug‑in devices like the game console on the TV stand, but smaller portable electronics such as a wireless speaker stay in the media drawer.

**T3 [AO]** target=`corded reading light`
- Q: Where should the corded reading light be placed in the room?
- A: The corded reading light should go on the TV stand, since I keep plug‑in devices and other wired equipment there.

**T4 [PI]** target=`hardcover books such as novels or art books are generally stored upright on the bookshelf`
- Q: I'd expect hardcover books like novels or art books to go on the bookshelf — does that match how you like to organise things?
- A: Yes, that fits perfectly — I keep upright reading books like hardcover novels, art books, and reference volumes on the bookshelf.

**T5 [AO]** target=`cotton lap blanket`
- Q: Where should the cotton lap blanket be placed?
- A: The cotton lap blanket should be kept in the storage ottoman along with other soft comfort items and lounge textiles.

**T6 [PI]** target=`drink-related items like mugs, glasses, and coasters tend to stay on or near the coffee table for easy access`
- Q: I'd expect drink-related items such as mugs, glasses, or coasters to stay on or near the coffee table — does that match how you organise things?
- A: Not quite — I usually keep drinkware and coasters on the side table, since that’s where I keep within‑reach items people use while seated.

**T7 [AO]** target=`soft stuffed bear`
- Q: Where should the soft stuffed bear be placed?
- A: The soft stuffed bear should be placed in the storage ottoman, with other soft comfort items and lounge textiles.

**T8 [AO]** target=`seasonal garland`
- Q: Where should the seasonal garland be placed?
- A: The seasonal garland should go in the storage basket, where I keep stored or seasonal living‑room accessories.

**T9 [PI]** target=`soft comfort items such as blankets and stuffed toys are stored together in the storage ottoman when not in use`
- Q: I'd expect soft comfort items like blankets and stuffed toys to go in the storage ottoman — does that match how you like to organise things?
- A: Yes, that’s exactly right — I keep soft comfort items like blankets, throws, and stuffed toys in the storage ottoman.

**T10 [PI]** target=`small handheld electronics like remotes or portable speakers are kept together in the media drawer when not in use`
- Q: I'd expect small handheld electronics like remotes or portable speakers to go in the media drawer when not in use — does that match how you like to organise things?
- A: Yes, that matches perfectly — I keep handheld media‑control and portable entertainment devices like remotes and small speakers in the media drawer.

---

## episode_17 (living room)

**PSR 轨迹**: u@3=42% → u@5=58% → u@10=83%, fb=1

**末态 confirmed_actions** (12):
- `leather-bound journal` → `bookshelf`
- `hardcover novel` → `bookshelf`
- `porcelain trinket dish` → `bookshelf`
- `family card game` → `center table`
- `board game box` → `center table`
- `rolled puzzle mat` → `center table`
- `crystal keepsake` → `bookshelf`
- `cotton lap blanket` → `storage ottoman`
- `plush ottoman cover` → `storage ottoman`
- `plastic magazine holder` → `storage basket`
- `plastic tray` → `storage basket`
- `seasonal garland` → `storage basket`

**末态 confirmed_preferences** (4):
- *Books, journals, and other upright reading or reference materials should be kept neatly on the bookshelf.*
  - → bookshelf, covers ['leather-bound journal', 'hardcover novel']
- *Games and puzzles are kept on the center table for easy access during leisure and tabletop activities.*
  - → center table, covers ['family card game', 'board game box', 'rolled puzzle mat']
- *Soft comfort items such as blankets and slipcovers should be stored in the storage ottoman when not in use.*
  - → storage ottoman, covers ['cotton lap blanket', 'plush ottoman cover']
- *Durable or lightweight decorative and utility accessories, such as trays, holders, and seasonal décor, should be kept in the storage basket when not in use.*
  - → storage basket, covers ['plastic magazine holder', 'plastic tray', 'seasonal garland']

### QA Sequence (10 turns)
**T1 [PI]** target=`Books and journals that are read often are kept neatly on the bookshelf.`
- Q: I'd expect books and journals to go on the bookshelf — does that match how you like to organise things?
- A: Yes, that fits perfectly — I keep books, journals, and other upright reading or reference materials on the bookshelf.

**T2 [AO]** target=`porcelain trinket dish`
- Q: Where should the porcelain trinket dish go?
- A: The porcelain trinket dish should go on the bookshelf — that’s where I like to keep fragile display pieces such as little dishes or keepsakes.

**T3 [PI]** target=`Games and entertainment items are often stored together near where people gather, such as in a storage ottoman for easy access during leisure time.`
- Q: I'd guess leisure items like board games and puzzles would go in the storage ottoman for convenient access — does that match how you organise things?
- A: Not quite — I usually keep games and puzzles on the center table since it's the shared spot for leisure and tabletop activities. The storage ottoman is more for soft comfort items like blankets or spare covers.

**T4 [AO]** target=`crystal keepsake`
- Q: Where should the crystal keepsake be placed?
- A: The crystal keepsake should go on the bookshelf — that’s where I like to keep fragile or decorative display pieces.

**T5 [PI]** target=`Soft comfort items such as blankets and slipcovers are usually stored inside the storage ottoman when not in use.`
- Q: I'd expect soft comfort items like blankets or covers to go in the storage ottoman — does that match how you like to organise things?
- A: Yes, that matches my setup — I keep soft comfort pieces like throw blankets, covers, and other spare lounge textiles in the storage ottoman.

**T6 [AO]** target=`plastic magazine holder`
- Q: Where should the plastic magazine holder go?
- A: The plastic magazine holder should go in the storage basket — that’s where I keep sturdier or seldom-used accessories like plastic trays or stored organizers.

**T7 [AO]** target=`plastic tray`
- Q: Where should the plastic tray go?
- A: The plastic tray should go in the storage basket — that’s where I keep durable spare accessories like plastic organizers or trays that aren’t used all the time.

**T8 [AO]** target=`seasonal garland`
- Q: Where should the seasonal garland be placed?
- A: The seasonal garland should go in the storage basket — that’s where I keep stored or seasonal living-room accessories.

**T9 [PI]** target=`Lightweight decorative and utility accessories, such as trays, holders, and seasonal décor, are grouped in the storage basket for easy rotation and display updates.`
- Q: I'd expect lightweight decorative and utility accessories like trays, holders, and seasonal décor to go in the storage basket — does that match how you like to organise things?
- A: Yes, that fits — I keep durable or lightweight utility and decorative accessories, like trays, holders, and seasonal pieces, in the storage basket when they’re not in use.

**T10 [AO]** target=`leather-bound journal`
- Q: Where should the leather-bound journal go?
- A: The leather-bound journal should go on the bookshelf — that’s where I keep upright reading materials like novels and journals.

---

## episode_34 (bedroom)

**PSR 轨迹**: u@3=0% → u@5=92% → u@10=100%, fb=0

**末态 confirmed_actions** (12):
- `battery-powered massager` → `bedside drawer`
- `hardcover sketchbook` → `bedroom bookshelf`
- `hardcover planner` → `bedroom bookshelf`
- `rechargeable hand warmer` → `bedside drawer`
- `ready-to-wear cardigan` → `wardrobe shelf`
- `ceramic jewelry dish` → `vanity tray`
- `porcelain ring tray` → `vanity tray`
- `hair clip box` → `vanity tray`
- `folded scarf` → `wardrobe shelf`
- `wooden keepsake box` → `vanity tray`
- `storage pouch` → `storage bench`
- `off-season scarf set` → `storage bench`

**末态 confirmed_preferences** (3):
- *hardcover notebooks, planners, and other reading or reference books should be kept on the bedroom bookshelf*
  - → bedroom bookshelf, covers ['hardcover sketchbook', 'hardcover planner']
- *small personal care gadgets or handheld electronics used near the bed should be kept in the bedside drawer for easy reach and charging*
  - → bedside drawer, covers ['battery-powered massager', 'rechargeable hand warmer']
- *Jewelry trays and small decorative boxes used for display or keepsakes should be kept on the vanity tray for easy reach while getting ready.*
  - → vanity tray, covers ['ceramic jewelry dish', 'porcelain ring tray', 'hair clip box']

### QA Sequence (10 turns)
**T1 [AO]** target=`battery-powered massager`
- Q: Where should the battery-powered massager go?
- A: It should go in the bedside drawer with other small bedside electronics.

**T2 [PI]** target=`Hardcover creative or planning books such as sketchbooks and planners tend to live on the bedroom bookshelf.`
- Q: I'd guess hardcover notebooks and planners would go on the bedroom bookshelf — is that how you like it?
- A: Yes, I keep hardcover notebooks, planners, and the other reading or reference books on the bedroom bookshelf.

**T3 [AO]** target=`rechargeable hand warmer`
- Q: Where should the rechargeable hand warmer be placed when not in use?
- A: It belongs in the bedside drawer with the other small bedside electronics when it’s not being used.

**T4 [PI]** target=`small personal care gadgets or handheld electronics used near the bed should be kept in the bedside drawer for easy reach and charging`
- Q: I'd expect small personal care gadgets or handheld electronics used near the bed to go in the bedside drawer — does that match how you like to organise things?
- A: Yes, that’s exactly right — small personal care gadgets and handheld electronics that I use near the bed belong in the bedside drawer.

**T5 [AO]** target=`ready-to-wear cardigan`
- Q: Where should the ready-to-wear cardigan be placed?
- A: It should be placed on the wardrobe shelf with the other ready-to-wear clothing items.

**T6 [PI]** target=`Jewelry trays and small decorative organizers tend to stay on a vanity or dresser surface for daily use access.`
- Q: I'd guess jewelry trays and small decorative boxes usually belong on the vanity tray for easy reach when getting ready — is that how you like it?
- A: Yes, that’s exactly right — I keep jewelry trays, small decorative boxes, and other display or keepsake pieces on the vanity tray so they’re easy to reach while getting ready.

**T7 [AO]** target=`folded scarf`
- Q: Where should the folded scarf go?
- A: The folded scarf should go on the wardrobe shelf with the other ready-to-wear clothing items.

**T8 [AO]** target=`wooden keepsake box`
- Q: Where should the wooden keepsake box go?
- A: The wooden keepsake box should go on the vanity tray with the other small decorative and keepsake pieces.

**T9 [AO]** target=`storage pouch`
- Q: Where should the storage pouch go?
- A: The storage pouch should go in the storage bench with other soft or travel-related accessories that aren’t used daily.

**T10 [AO]** target=`off-season scarf set`
- Q: Where should the off-season scarf set be stored?
- A: The off-season scarf set should go in the storage bench with other soft or bulky accessories that aren’t used daily.

---

## episode_51 (bedroom)

**PSR 轨迹**: u@3=83% → u@5=83% → u@10=83%, fb=0

**末态 confirmed_actions** (12):
- `portable reading light` → `nightstand drawer`
- `battery-powered massager` → `nightstand drawer`
- `hardcover devotional` → `reading shelf`
- `sleep journal` → `reading shelf`
- `rigid-cover photo diary` → `reading shelf`
- `phone charging cable` → `nightstand`
- `plug-in bedside lamp` → `nightstand`
- `clean cotton pajamas` → `closet shelf`
- `folded linen shirt` → `closet shelf`
- `hand lotion` → `nightstand`
- `spare hanger pack` → `storage bench`
- `off-season scarf set` → `storage bench`

**末态 confirmed_preferences** (3):
- *Plug-in or battery-powered bedside electronics and light sources are kept on the nightstand if used regularly, or inside the nightstand drawer if smaller or less frequently used.*
  - → None, covers ['battery-powered massager', 'phone charging cable', 'plug-in bedside lamp']
- *Books and journals used for nightly reading or writing are kept on the reading shelf.*
  - → reading shelf, covers ['hardcover devotional', 'sleep journal', 'rigid-cover photo diary']
- *Clean, folded clothing items like pajamas and shirts are stored on the closet shelf.*
  - → closet shelf, covers ['clean cotton pajamas', 'folded linen shirt']

### QA Sequence (10 turns)
**T1 [AO]** target=`portable reading light`
- Q: Where should the portable reading light go?
- A: The portable reading light should go in the nightstand drawer with the other small bedside electronics and light sources.

**T2 [PI]** target=`Small plug-in or battery-powered bedside electronics are usually kept in or on the nightstand for easy reach.`
- Q: I'd expect small plug-in or battery-powered bedside electronics to go in or on the nightstand — does that match how you like to organise things?
- A: Yes, that fits. I keep plug-in or battery-powered bedside electronics and light sources either on the nightstand if they’re used regularly, or inside the nightstand drawer if they’re smaller or kept tucked away.

**T3 [AO]** target=`battery-powered massager`
- Q: Where should the battery-powered massager go?
- A: The battery-powered massager should go in the nightstand drawer with the other small bedside electronics.

**T4 [PI]** target=`Books and journals used for nightly reading or reflection are kept on the nightstand for easy access before sleep.`
- Q: I'd expect books and journals you read or write in at night to stay on the nightstand — does that match how you like to organise things?
- A: Not quite — I actually keep books and journals that I read or write in on the reading shelf rather than the nightstand.

**T5 [AO]** target=`phone charging cable`
- Q: Where should the phone charging cable be placed?
- A: The phone charging cable should stay on the nightstand with the plug-in bedside devices and other nightly-use items I like to keep within reach.

**T6 [AO]** target=`plug-in bedside lamp`
- Q: Where should the plug-in bedside lamp be placed?
- A: The plug-in bedside lamp should stay on the nightstand with the other plug-in bedside devices and nightly-use items that I keep within easy reach.

**T7 [PI]** target=`Everyday sleepwear and other clean clothing items are typically stored folded on the closet shelf rather than left out or in a hamper.`
- Q: I'd expect clean folded clothing like pajamas and shirts to go on the closet shelf — does that match how you like to organise things?
- A: Yes, that matches my setup — clean, folded clothing like pajamas, shirts, and other ready-to-wear items go on the closet shelf.

**T8 [AO]** target=`hand lotion`
- Q: Where should the hand lotion be placed?
- A: The hand lotion should go on the nightstand with other nightly-use items I like to keep within reach, such as the phone charging cable and bedside lamp.

**T9 [AO]** target=`spare hanger pack`
- Q: Where should the spare hanger pack go?
- A: The spare hanger pack should go in the storage bench along with other soft or overflow bedroom accessories.

**T10 [AO]** target=`off-season scarf set`
- Q: Where should the off-season scarf set go?
- A: The off-season scarf set should go in the storage bench, together with other soft or overflow bedroom accessories.

---

## episode_68 (kitchen)

**PSR 轨迹**: u@3=75% → u@5=92% → u@10=100%, fb=0

**末态 confirmed_actions** (12):
- `wired coffee grinder` → `prep counter`
- `plug-in toaster` → `prep counter`
- `battery-powered can opener` → `kitchen drawer`
- `cut lemon container` → `fridge shelf`
- `opened yogurt tub` → `fridge shelf`
- `digital kitchen timer` → `kitchen drawer`
- `porcelain teacup set` → `upper cabinet`
- `glass pitcher` → `upper cabinet`
- `serving candle set` → `upper cabinet`
- `wooden citrus reamer` → `kitchen drawer`
- `cake topper tin` → `upper cabinet`
- `wooden salad servers` → `kitchen drawer`

**末态 confirmed_preferences** (4):
- *Powered appliances that plug in while they're used should be kept on the prep counter.*
  - → prep counter, covers ['wired coffee grinder', 'plug-in toaster']
- *Opened or cut food items should be stored on the fridge shelf to keep them chilled and fresh.*
  - → fridge shelf, covers ['cut lemon container', 'opened yogurt tub']
- *Serving sets and decorative dining items such as teacup sets, pitchers, or candle sets should be kept in the upper cabinet where they stay clean and ready for serving.*
  - → upper cabinet, covers ['porcelain teacup set', 'glass pitcher', 'serving candle set']
- *Small handheld utensils and battery-operated kitchen gadgets should be stored in the kitchen drawer for easy access during meal preparation.*
  - → kitchen drawer, covers ['battery-powered can opener', 'digital kitchen timer', 'wooden citrus reamer', 'wooden salad servers']

### QA Sequence (10 turns)
**T1 [AO]** target=`wired coffee grinder`
- Q: Where should the wired coffee grinder go?
- A: It should go on the prep counter, with the other powered appliances that plug in while they're used.

**T2 [AO]** target=`battery-powered can opener`
- Q: Where should the battery-powered can opener go?
- A: It should go in the kitchen drawer with the other small battery-powered gadgets.

**T3 [PI]** target=`Perishable or open food items should be stored on the fridge shelf to keep them fresh.`
- Q: I'd expect opened or cut food items to go on the fridge shelf — does that match how you like to organise things?
- A: Yes, that fits perfectly — any opened or cut food, like the lemon container or an opened yogurt, should go on the fridge shelf to stay chilled.

**T4 [AO]** target=`digital kitchen timer`
- Q: Where should the digital kitchen timer be placed?
- A: The digital kitchen timer should go in the kitchen drawer with the other small battery-powered kitchen gadgets.

**T5 [PI]** target=`Serving sets and decorative dining items such as teacup sets, pitchers, or candle sets are kept in the upper cabinet where they stay clean and ready for serving.`
- Q: I think serving sets and decorative dining items like teacups, pitchers, or candles would be kept in the upper cabinet — is that right?
- A: Yes, that's right — the upper cabinet is where I keep serving sets and decorative dining pieces like teacups, pitchers, or candles, along with other fragile or special-occasion items.

**T6 [AO]** target=`wooden citrus reamer`
- Q: Where should the wooden citrus reamer go?
- A: The wooden citrus reamer should go in the kitchen drawer with the other small wooden prep utensils.

**T7 [AO]** target=`cake topper tin`
- Q: Where should the cake topper tin go?
- A: The cake topper tin should go in the upper cabinet with the other special-occasion and decorative pieces.

**T8 [AO]** target=`wooden salad servers`
- Q: Where should the wooden salad servers go?
- A: The wooden salad servers should go in the kitchen drawer with the other small wooden prep and serving utensils.

**T9 [PI]** target=`Small handheld utensils and battery-operated kitchen gadgets are stored in the kitchen drawer for easy access during meal prep.`
- Q: I'd expect small handheld utensils and battery-operated gadgets to go in the kitchen drawer — does that match how you like to organise things?
- A: Yes — small handheld utensils and battery‑operated kitchen gadgets both belong in the kitchen drawer. That's where I keep things like the can opener, timer, and small wooden tools.

**T10 [AO]** target=`plug-in toaster`
- Q: Where should the plug-in toaster go?
- A: The plug‑in toaster should go on the prep counter with other powered appliances that need to be plugged in while in use.

---
