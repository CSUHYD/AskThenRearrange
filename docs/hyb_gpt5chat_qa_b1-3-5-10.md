# HYB × GPT-5-Chat × 5 ep × Budgets 1/3/5/10 — QA 完整记录

## PSR 聚合

| Budget | Seen | Unseen |
|---|---|---|
| 1 | 58.3% ± 7.5 | 60.0% ± 6.1 |
| 3 | 68.3% ± 8.5 | 78.3% ± 4.2 |
| 5 | 86.7% ± 5.0 | 86.7% ± 5.7 |
| 10 | 98.3% ± 1.7 | 93.3% ± 4.9 |

## 各 episode 序列 + PSR

| ep | room | u@1 | u@3 | u@5 | u@10 | seq @B=10 | fb |
|---|---|---|---|---|---|---|---|
| episode_0 | living room | 58% | 75% | 83% | 100% | PE→PE→PE→PE→PE→AO→PE→AO→PE→AO | 0 |
| episode_17 | living room | 58% | 75% | 75% | 75% | PE→PE→PE→PE→PE→PE→AO→PE→AO→PE | 0 |
| episode_34 | bedroom | 83% | 92% | 100% | 100% | PE→PE→PE→PE→PE→PE→AO→PE→AO→PE | 0 |
| episode_51 | bedroom | 50% | 67% | 75% | 92% | PE→PE→PE→PE→PE→PE→AO→PE→AO→PE | 0 |
| episode_68 | kitchen | 50% | 83% | 100% | 100% | PE→PE→PE→PE→PE→PE→AO→PE→AO→PE | 0 |

---

## episode_0 (living room)

**PSR**: u@1=58% → u@3=75% → u@5=83% → u@10=100%, fb=0

**末态 confirmed_actions** (12):
- `wired game console` → `TV stand`
- `wireless speaker` → `media drawer`
- `hardcover novel` → `bookshelf`
- `hardcover art book` → `bookshelf`
- `filled ceramic mug` → `side table`
- `sparkling water glass` → `side table`
- `seasonal garland` → `storage basket`
- `spare coaster pouch` → `storage basket`
- `cotton lap blanket` → `storage ottoman`
- `battery-powered remote` → `media drawer`
- `corded reading light` → `TV stand`
- `soft stuffed bear` → `storage ottoman`

**末态 confirmed_preferences** (6):
- *Large plug-in entertainment electronics are kept on the TV stand.*
  - → TV stand, covers ['wired game console', 'wireless speaker']
- *Hardcover reading and art books are kept upright on the bookshelf with other main reading and reference books.*
  - → bookshelf, covers ['hardcover novel', 'hardcover art book']
- *Fragile drinkware made of glass or ceramic is usually kept on the side table with other small tabletop accents and items used while seated.*
  - → side table, covers ['filled ceramic mug', 'sparkling water glass']
- *Seasonal and decorative accent items are stored in the storage basket with other stored or off-season living-room accessories.*
  - → storage basket, covers ['seasonal garland', 'spare coaster pouch']
- *Soft comfort textiles and lap blankets used while seated are kept in the storage ottoman with other cozy lounge items.*
  - → storage ottoman, covers ['cotton lap blanket']
- *Plug-in lighting used for reading or ambient illumination is kept on the TV stand with other large wired and plug-in media equipment.*
  - → TV stand, covers ['corded reading light']

### QA Sequence (10 turns)
**T1 [PE]** target=`large plug-in entertainment electronics`
- Q: How do you usually organize large plug-in entertainment electronics, like a wired game console or a wireless speaker?
- A: I keep large plug-in entertainment electronics, like a wired game console or speaker that stays plugged in, on the TV stand.

**T2 [PE]** target=`hardcover reading and art books`
- Q: How do you usually organize hardcover reading and art books, like a hardcover novel or a hardcover art book?
- A: I keep hardcover reading and art books upright on the bookshelf. That’s where all my main reading and reference books go.

**T3 [PE]** target=`fragile drinkware made of glass or ceramic`
- Q: How do you usually organize fragile drinkware made of glass or ceramic, like a filled ceramic mug or a sparkling water glass?
- A: I keep fragile drinkware like ceramic mugs or glass water glasses on the side table, along with other small tabletop accents and within-reach items I use while seated.

**T4 [PE]** target=`seasonal and decorative accent items`
- Q: How do you usually organize seasonal and decorative accent items, like seasonal garland or spare coaster pouch?
- A: I keep seasonal and decorative accent items, like a seasonal garland or spare coaster pouch, in the storage basket with other stored or off-season living-room accessories.

**T5 [PE]** target=`soft comfort textiles and lap blankets used while seated`
- Q: How do you usually organize soft comfort textiles and lap blankets used while seated, like a cotton lap blanket?
- A: I keep soft comfort textiles and lap blankets, like a cotton lap blanket, in the storage ottoman with other cozy lounge items.

**T6 [AO]** target=`battery-powered remote`
- Q: Where should the battery-powered remote go?
- A: I keep battery-powered remotes in the media drawer, along with other handheld media-control and portable entertainment devices.

**T7 [PE]** target=`plug-in lighting used for reading or ambient illumination`
- Q: How do you usually organize plug-in lighting used for reading or ambient illumination, like your corded reading light?
- A: Plug-in lighting like my corded reading light goes on the TV stand, with the other large wired and plug-in media equipment.

**T8 [AO]** target=`soft stuffed bear`
- Q: Where should the soft stuffed bear go?
- A: The soft stuffed bear should go in the storage ottoman with the other soft comfort items and cozy lounge textiles.

**T9 [PE]** target=`items typically kept in the coffee table`
- Q: What kinds of items do you typically keep in the coffee table?
- A: I haven't really thought about a specific rule for the coffee table.

**T10 [AO]** target=`wireless speaker`
- Q: Where should the wireless speaker go?
- A: The wireless speaker should go in the media drawer with the other handheld media-control and portable entertainment devices.

---

## episode_17 (living room)

**PSR**: u@1=58% → u@3=75% → u@5=75% → u@10=75%, fb=0

**末态 confirmed_actions** (12):
- `family card game` → `center table`
- `board game box` → `center table`
- `leather-bound journal` → `bookshelf`
- `hardcover novel` → `bookshelf`
- `porcelain trinket dish` → `bookshelf`
- `crystal keepsake` → `bookshelf`
- `plastic magazine holder` → `storage basket`
- `plastic tray` → `storage basket`
- `plush ottoman cover` → `storage ottoman`
- `cotton lap blanket` → `storage ottoman`
- `rolled puzzle mat` → `storage basket`
- `seasonal garland` → `storage basket`

**末态 confirmed_preferences** (6):
- *Family entertainment and tabletop leisure items are kept on the center table with other shared or display items.*
  - → center table, covers ['family card game', 'board game box']
- *Bound reading materials with durable covers are kept upright on the bookshelf with other reading and reference books.*
  - → bookshelf, covers ['leather-bound journal', 'hardcover novel']
- *Delicate decorative glass and ceramic keepsakes are kept on the bookshelf along with other fragile display items and drinkware.*
  - → bookshelf, covers ['porcelain trinket dish', 'crystal keepsake']
- *Lightweight plastic organizers and serving pieces are stored together in the storage basket with other durable spare or stored living‑room accessories.*
  - → storage basket, covers ['plastic magazine holder', 'plastic tray']
- *Soft comfort textiles and throws are stored in the storage ottoman with other lounge textiles.*
  - → storage ottoman, covers ['plush ottoman cover', 'cotton lap blanket']
- *Rollable fabric and play‑surface accessories are kept in the storage basket with other durable spare living‑room accessories.*
  - → storage basket, covers ['rolled puzzle mat']

### QA Sequence (10 turns)
**T1 [PE]** target=`family entertainment and tabletop leisure items`
- Q: How do you usually organize family entertainment and tabletop leisure items, like a family card game or board game box?
- A: I keep family entertainment and tabletop leisure things like card games and board games on the center table, along with other shared or display items we use together.

**T2 [PE]** target=`bound reading materials with durable covers`
- Q: How do you usually organize bound reading materials with durable covers, like a leather-bound journal or a hardcover novel?
- A: I keep bound reading materials with durable covers, like leather-bound journals and hardcover novels, upright on the bookshelf with my other reading and reference books.

**T3 [PE]** target=`delicate decorative glass and ceramic keepsakes`
- Q: How do you usually organize delicate decorative glass and ceramic keepsakes, like a porcelain trinket dish or a crystal keepsake?
- A: I keep delicate decorative glass and ceramic keepsakes, like porcelain trinket dishes and crystal pieces, on the bookshelf along with other fragile display items and drinkware.

**T4 [PE]** target=`lightweight plastic organizers and serving pieces`
- Q: How do you usually organize lightweight plastic organizers and serving pieces, like a plastic magazine holder or a plastic tray?
- A: I keep lightweight plastic organizers and serving pieces, like magazine holders or trays, in the storage basket with other durable spare or stored living‑room accessories.

**T5 [PE]** target=`soft comfort textiles and throws`
- Q: How do you usually organize soft comfort textiles and throws, like the plush ottoman cover or cotton lap blanket?
- A: I keep soft comfort textiles and throws, like plush ottoman covers and cotton lap blankets, in the storage ottoman along with other spare lounge textiles.

**T6 [PE]** target=`rollable fabric and play‑surface accessories`
- Q: How do you usually organize rollable fabric and play‑surface accessories like your rolled puzzle mat?
- A: I keep rollable fabric and play‑surface accessories like my rolled puzzle mat in the storage basket with other durable spare living‑room accessories.

**T7 [AO]** target=`seasonal garland`
- Q: Where should the seasonal garland go?
- A: I keep the seasonal garland in the storage basket along with other stored or seasonal living‑room accessories.

**T8 [PE]** target=`items typically kept in the media console`
- Q: What kinds of items do you typically keep in the media console?
- A: I haven't really thought specifically about what goes in the media console.

**T9 [AO]** target=`leather-bound journal`
- Q: Where should the leather-bound journal be placed?
- A: I keep the leather‑bound journal on the bookshelf with my other upright reading and reference books.

**T10 [PE]** target=`items typically kept in the side table`
- Q: What kinds of items do you typically keep in the side table?
- A: I haven't really thought about what goes in the side table.

---

## episode_34 (bedroom)

**PSR**: u@1=83% → u@3=92% → u@5=100% → u@10=100%, fb=0

**末态 confirmed_actions** (12):
- `hair clip box` → `vanity tray`
- `wooden keepsake box` → `vanity tray`
- `battery-powered massager` → `bedside drawer`
- `rechargeable hand warmer` → `bedside drawer`
- `ready-to-wear cardigan` → `wardrobe shelf`
- `off-season scarf set` → `storage bench`
- `hardcover sketchbook` → `bedroom bookshelf`
- `hardcover planner` → `bedroom bookshelf`
- `ceramic jewelry dish` → `vanity tray`
- `porcelain ring tray` → `vanity tray`
- `folded scarf` → `wardrobe shelf`
- `storage pouch` → `storage bench`

**末态 confirmed_preferences** (8):
- *Decorative storage and keepsake containers are kept on the vanity tray with other small personal accessories and fragile keepsakes.*
  - → vanity tray, covers ['hair clip box', 'wooden keepsake box']
- *Small rechargeable personal care devices are stored in the bedside drawer together with other small bedside electronics.*
  - → bedside drawer, covers ['battery-powered massager', 'rechargeable hand warmer']
- *ready-to-wear clothing items stay on the wardrobe shelf while off-season clothing is stored in the storage bench until needed again*
  - → wardrobe shelf, covers ['ready-to-wear cardigan', 'off-season scarf set']
- *Hardcover creative and planning books are kept on the bedroom bookshelf along with other reading and reference books.*
  - → bedroom bookshelf, covers ['hardcover sketchbook', 'hardcover planner']
- *Fragile ceramic and porcelain jewelry holders are kept on the vanity tray with other small personal accessories and delicate keepsakes.*
  - → vanity tray, covers ['ceramic jewelry dish', 'porcelain ring tray']
- *Soft wearable accessories made of fabric are kept on the wardrobe shelf with ready-to-wear clothing, while bulkier or off-season pieces go to the storage bench.*
  - → wardrobe shelf, covers ['folded scarf']
- *Dirty clothes and linens go in the laundry hamper for washing.*
  - → laundry hamper, covers []
- *No specific items are typically kept in the nightstand.*
  - → nightstand, covers []

### QA Sequence (10 turns)
**T1 [PE]** target=`decorative storage and keepsake containers`
- Q: How do you usually organize decorative storage and keepsake containers, like a hair clip box or a wooden keepsake box?
- A: I keep decorative storage and keepsake containers like those on the vanity tray along with other small personal accessories and fragile keepsakes.

**T2 [PE]** target=`small rechargeable personal care devices`
- Q: How do you usually organize small rechargeable personal care devices, like a battery-powered massager or a rechargeable hand warmer?
- A: I keep small rechargeable personal care devices, like a battery-powered massager or a hand warmer, in the bedside drawer with other small bedside electronics.

**T3 [PE]** target=`ready-to-wear and seasonally rotated clothing items`
- Q: How do you usually organize ready-to-wear and seasonally rotated clothing items, like your ready-to-wear cardigan or off-season scarf set?
- A: I keep ready-to-wear clothing like cardigans and scarves on the wardrobe shelf, and I move off-season pieces, such as a scarf set, to the storage bench until they’re needed again.

**T4 [PE]** target=`hardcover creative and planning books`
- Q: How do you usually organize hardcover creative and planning books, like a hardcover sketchbook or a hardcover planner?
- A: I keep hardcover creative and planning books, like a sketchbook or planner, on the bedroom bookshelf along with other reading and reference books.

**T5 [PE]** target=`fragile ceramic and porcelain jewelry holders`
- Q: How do you usually organize fragile ceramic and porcelain jewelry holders, like the ceramic jewelry dish or porcelain ring tray?
- A: I keep fragile ceramic and porcelain jewelry holders, like the jewelry dish or ring tray, on the vanity tray with other small personal accessories and delicate keepsakes.

**T6 [PE]** target=`soft wearable accessories made of fabric`
- Q: How do you usually organize soft wearable accessories made of fabric, like a folded scarf?
- A: I keep soft wearable accessories like a folded scarf on the wardrobe shelf with my ready-to-wear clothing items such as cardigans. Bulkier or off-season fabric accessories move to the storage bench instead.

**T7 [AO]** target=`storage pouch`
- Q: Where should the storage pouch go?
- A: I keep the storage pouch in the storage bench along with other soft or travel-style accessories that aren’t in daily use.

**T8 [PE]** target=`items typically kept in the laundry hamper`
- Q: What kinds of items do you typically keep in the laundry hamper?
- A: I use the laundry hamper just for dirty clothes and linens that need washing.

**T9 [AO]** target=`battery-powered massager`
- Q: Where should the battery-powered massager go?
- A: The battery-powered massager should go in the bedside drawer with other small bedside electronics and light sources.

**T10 [PE]** target=`items typically kept in the nightstand`
- Q: What kinds of items do you typically keep in the nightstand?
- A: I haven’t really thought about having specific things in the nightstand—it’s not where I usually keep anything in particular.

---

## episode_51 (bedroom)

**PSR**: u@1=50% → u@3=67% → u@5=75% → u@10=92%, fb=0

**末态 confirmed_actions** (12):
- `portable reading light` → `nightstand`
- `plug-in bedside lamp` → `nightstand`
- `hardcover devotional` → `reading shelf`
- `rigid-cover photo diary` → `reading shelf`
- `clean cotton pajamas` → `closet shelf`
- `folded linen shirt` → `closet shelf`
- `spare hanger pack` → `storage bench`
- `off-season scarf set` → `storage bench`
- `battery-powered massager` → `nightstand drawer`
- `phone charging cable` → `nightstand`
- `hand lotion` → `nightstand`
- `sleep journal` → `nightstand`

**末态 confirmed_preferences** (6):
- *Small plug-in and battery-powered bedside electronics are kept on the nightstand for easy access while in bed.*
  - → nightstand, covers ['portable reading light', 'plug-in bedside lamp']
- *Hardcover personal reading and reflection books belong on the reading shelf with other sturdy books in current use.*
  - → reading shelf, covers ['hardcover devotional', 'rigid-cover photo diary']
- *Soft cotton clothing and sleepwear are kept on the closet shelf with other ready-to-wear bedroom clothes.*
  - → closet shelf, covers ['clean cotton pajamas', 'folded linen shirt']
- *Seasonal clothing accessories and spare hangers are kept in the storage bench with other soft or overflow bedroom items.*
  - → storage bench, covers ['spare hanger pack', 'off-season scarf set']
- *Small bedside electronics and light sources are kept in the nightstand drawer so they’re tucked away but easy to reach.*
  - → nightstand drawer, covers ['portable reading light', 'battery-powered massager']
- *Corded personal electronics and charging accessories are kept on the nightstand for easy access while in bed.*
  - → nightstand, covers ['phone charging cable']

### QA Sequence (10 turns)
**T1 [PE]** target=`small plug-in and battery-powered bedside electronics`
- Q: How do you usually organize small plug-in and battery-powered bedside electronics, like a portable reading light or a plug-in bedside lamp?
- A: I keep small plug-in and battery-powered bedside electronics—like portable reading lights or bedside lamps—on the nightstand so they're close at hand for use in bed.

**T2 [PE]** target=`hardcover personal reading and reflection books`
- Q: How do you usually organize hardcover personal reading and reflection books, like a hardcover devotional or a rigid-cover photo diary?
- A: I keep hardcover personal reading or reflection books—like devotionals and photo diaries—on the reading shelf along with other sturdy books I'm currently into.

**T3 [PE]** target=`soft cotton clothing and sleepwear`
- Q: How do you usually organize soft cotton clothing and sleepwear, like clean cotton pajamas or folded linen shirt?
- A: I keep soft cotton clothing and sleepwear—like clean cotton pajamas and folded linen shirts—on the closet shelf with other ready-to-wear bedroom clothes.

**T4 [PE]** target=`seasonal clothing accessories and spare hangers`
- Q: How do you usually organize seasonal clothing accessories and spare hangers, like spare hanger pack or off-season scarf set?
- A: I keep seasonal clothing accessories and spare hangers—like off‑season scarf sets or a spare hanger pack—in the storage bench along with other soft or overflow bedroom items.

**T5 [PE]** target=`items typically kept in the nightstand drawer`
- Q: What kinds of items do you typically keep in the nightstand drawer?
- A: I keep small bedside electronics and light sources—like a portable reading light or a battery-powered massager—in the nightstand drawer so they're tucked away but easy to reach.

**T6 [PE]** target=`corded personal electronics and charging accessories`
- Q: How do you usually organize corded personal electronics and charging accessories, like your phone charging cable?
- A: I keep corded personal electronics and charging accessories, like phone charging cables, on the nightstand so they're accessible while I'm in bed.

**T7 [AO]** target=`hand lotion`
- Q: Where should the hand lotion go?
- A: I keep hand lotion on the nightstand along with other nightly-use items I like to have within reach while I'm in bed.

**T8 [PE]** target=`items typically kept in the vanity tray`
- Q: What kinds of items do you typically keep in the vanity tray?
- A: I haven't really thought about what belongs on the vanity tray.

**T9 [AO]** target=`sleep journal`
- Q: Where should the sleep journal go?
- A: The sleep journal goes on the nightstand with my other nightly-use items that I like to have within reach while I'm in bed.

**T10 [PE]** target=`items typically kept in the linen hamper`
- Q: What kinds of items do you typically keep in the linen hamper?
- A: I haven't really thought about what belongs in the linen hamper.

---

## episode_68 (kitchen)

**PSR**: u@1=50% → u@3=83% → u@5=100% → u@10=100%, fb=0

**末态 confirmed_actions** (12):
- `wired coffee grinder` → `prep counter`
- `plug-in toaster` → `prep counter`
- `porcelain teacup set` → `upper cabinet`
- `glass pitcher` → `upper cabinet`
- `cut lemon container` → `fridge shelf`
- `opened yogurt tub` → `fridge shelf`
- `battery-powered can opener` → `kitchen drawer`
- `digital kitchen timer` → `kitchen drawer`
- `wooden citrus reamer` → `kitchen drawer`
- `wooden salad servers` → `kitchen drawer`
- `serving candle set` → `upper cabinet`
- `cake topper tin` → `upper cabinet`

**末态 confirmed_preferences** (6):
- *Plug-in countertop kitchen appliances are kept on the prep counter so they can remain handy and plugged in for use.*
  - → prep counter, covers ['wired coffee grinder', 'plug-in toaster']
- *Fragile glass and porcelain drinkware are kept in the upper cabinet to stay safe and protected.*
  - → upper cabinet, covers ['porcelain teacup set', 'glass pitcher']
- *Perishable or opened refrigerated foods are kept on the fridge shelf to stay cold and fresh.*
  - → fridge shelf, covers ['cut lemon container', 'opened yogurt tub']
- *Small battery-powered kitchen gadgets are kept in the kitchen drawer along with other handheld or cordless tools.*
  - → kitchen drawer, covers ['battery-powered can opener', 'digital kitchen timer']
- *Small wooden food prep and serving utensils are kept in the kitchen drawer with other handheld wooden tools.*
  - → kitchen drawer, covers ['wooden citrus reamer', 'wooden salad servers']
- *Special-occasion serving and decorative items, such as multipiece candle centerpieces or display sets, are kept in the upper cabinet for safe storage until needed.*
  - → upper cabinet, covers ['serving candle set']

### QA Sequence (10 turns)
**T1 [PE]** target=`plug-in countertop kitchen appliances`
- Q: How do you usually organize plug-in countertop kitchen appliances, like a wired coffee grinder or plug-in toaster?
- A: I keep plug-in countertop appliances like the coffee grinder and toaster on the prep counter, since they need to stay handy and plugged in while being used.

**T2 [PE]** target=`fragile glass and porcelain drinkware`
- Q: How do you usually organize fragile glass and porcelain drinkware, like a porcelain teacup set or a glass pitcher?
- A: I keep fragile glass and porcelain pieces, like the teacup set and glass pitcher, in the upper cabinet so they stay safe and protected.

**T3 [PE]** target=`perishable refrigerated food items in open containers`
- Q: How do you usually organize perishable refrigerated food items in open containers, like a cut lemon container or an opened yogurt tub?
- A: I keep perishable or opened refrigerated foods, like a cut lemon container or an opened yogurt tub, on the fridge shelf so they stay cold and fresh.

**T4 [PE]** target=`small battery-powered kitchen gadgets`
- Q: How do you usually organize small battery-powered kitchen gadgets, like a battery-powered can opener or a digital kitchen timer?
- A: I keep small battery-powered kitchen gadgets, like a can opener or digital timer, in the kitchen drawer along with other handheld or cordless tools.

**T5 [PE]** target=`small wooden food prep and serving utensils`
- Q: How do you usually organize small wooden food prep and serving utensils, like the wooden citrus reamer or wooden salad servers?
- A: I keep small wooden food prep and serving utensils, like the citrus reamer and salad servers, in the kitchen drawer with other handheld wooden tools.

**T6 [PE]** target=`decor-focused multipiece candle or centerpiece sets`
- Q: How do you usually organize decor-focused multipiece candle or centerpiece sets, like your serving candle set?
- A: I keep special-occasion serving and decorative items, like multipiece candle centerpieces or display sets, in the upper cabinet so they stay safely stored until I need them.

**T7 [AO]** target=`cake topper tin`
- Q: Where should the cake topper tin go?
- A: I keep the cake topper tin in the upper cabinet with my other special-occasion serving and display items.

**T8 [PE]** target=`items typically kept in the pantry shelf`
- Q: What kinds of items do you typically keep in the pantry shelf?
- A: I haven't really thought about that, I don't have a specific organizing rule for the pantry shelf.

**T9 [AO]** target=`wired coffee grinder`
- Q: Where should the wired coffee grinder go?
- A: The wired coffee grinder should go on the prep counter with other countertop appliances that need power while in use.

**T10 [PE]** target=`items typically kept in the base cabinet`
- Q: What kinds of items do you typically keep in the base cabinet?
- A: I haven't really thought about that, I don't have a specific organizing rule for the base cabinet.

---
