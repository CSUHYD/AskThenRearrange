# UL × GPT-5-Chat × 5 ep × Budgets 1/3/5/10 — QA 完整记录（去掉 turn-0 hack）

## PSR 聚合

| Budget | Seen | Unseen |
|---|---|---|
| 1 | 65.0% ± 7.2 | 66.7% ± 9.1 |
| 3 | 81.7% ± 3.1 | 81.7% ± 4.1 |
| 5 | 85.0% ± 4.1 | 85.0% ± 4.9 |
| 10 | 98.3% ± 1.7 | 93.3% ± 3.1 |

注：相比修复前（turn-0 hardcoded "How do you usually like to organize your room?" 一次性 dump 全部 receptacle），低 budget 数字明显下降，更符合真实 UL 行为。

## 各 episode 序列 + PSR

| ep | room | u@1 | u@3 | u@5 | u@10 | seq @ B=10 |
|---|---|---|---|---|---|---|
| episode_0 | living room | 92% | 92% | 92% | 92% | PE→PE→PE→PE→PE→PE→PE→PE→PE→AO |
| episode_17 | living room | 42% | 83% | 75% | 83% | PE→PE→PE→PE→PE→PE→PE→PE→PE→PE |
| episode_34 | bedroom | 58% | 67% | 83% | 100% | PE→PE→PE→PE→PE→PE→PE→PE→PE→AO |
| episode_51 | bedroom | 83% | 83% | 75% | 92% | PE→PE→PE→PE→PE→PE→PE→PE→PE→PE |
| episode_68 | kitchen | 58% | 83% | 100% | 100% | PE→PE→PE→PE→PE→PE→PE→PE→PE→AO |

---

## episode_0 (living room)

**PSR**: u@1=92% → u@3=92% → u@5=92% → u@10=92%, fb=1

**末态 confirmed_actions** (12):
- `battery-powered remote` → `media drawer`
- `wireless speaker` → `media drawer`
- `wired game console` → `TV stand`
- `corded reading light` → `TV stand`
- `hardcover novel` → `bookshelf`
- `hardcover art book` → `bookshelf`
- `filled ceramic mug` → `side table`
- `sparkling water glass` → `side table`
- `cotton lap blanket` → `storage ottoman`
- `soft stuffed bear` → `storage ottoman`
- `seasonal garland` → `storage basket`
- `spare coaster pouch` → `storage basket`

**末态 confirmed_preferences** (8):
- *Small battery-powered handheld devices are kept in the media drawer.*
  - → media drawer, covers ['battery-powered remote', 'wireless speaker']
- *Large plug-in entertainment and lighting devices are kept on the TV stand.*
  - → TV stand, covers ['wired game console', 'corded reading light']
- *All upright reading and reference books, including hardcover novels and art books, are kept on the bookshelf.*
  - → bookshelf, covers ['hardcover novel', 'hardcover art book']
- *Fragile glass and ceramic drinkware are kept on the side table for easy reach while seated.*
  - → side table, covers ['filled ceramic mug', 'sparkling water glass']
- *Soft comfort items and extra lounge textiles are kept inside the storage ottoman.*
  - → storage ottoman, covers ['cotton lap blanket']
- *Soft decorative and comforting plush items are kept inside the storage ottoman with other cozy lounge textiles.*
  - → storage ottoman, covers ['soft stuffed bear']
- *Decorative and seasonal display materials are stored in the storage basket along with other archived living-room accessories.*
  - → storage basket, covers ['seasonal garland']
- *Small fabric or textile accessory pouches are kept in the storage basket along with other stored or archived living-room accessories.*
  - → storage basket, covers ['spare coaster pouch']

### QA Sequence (10 turns)
**T1 [PE]** target=`small battery-powered handheld devices`
- Q: How do you usually organize small battery-powered handheld devices, like a battery-powered remote or a wireless speaker?
- A: I keep small battery-powered handheld devices like remotes and portable speakers in the media drawer.

**T2 [PE]** target=`large plug-in entertainment and lighting devices`
- Q: How do you usually organize large plug-in entertainment and lighting devices, like a wired game console or a corded reading light?
- A: I keep large plug-in entertainment and lighting devices, such as wired game consoles and corded reading lights, on the TV stand.

**T3 [PE]** target=`hardcover reading and art books`
- Q: How do you usually organize hardcover reading and art books, like hardcover novels or hardcover art books?
- A: I keep all of my upright reading and reference books, including hardcover novels and hardcover art books, on the bookshelf.

**T4 [PE]** target=`fragile glass and ceramic drinkware`
- Q: How do you usually organize fragile glass and ceramic drinkware, like a filled ceramic mug or a sparkling water glass?
- A: I keep glass and ceramic drinkware—like mugs and water glasses—on the side table, since that’s where I keep within-reach drinkware and other small tabletop items I use while seated.

**T5 [PE]** target=`soft comfort textiles used for seating warmth`
- Q: How do you usually organize soft comfort textiles used for seating warmth, like a cotton lap blanket?
- A: I keep soft comfort items and extra lounge textiles, like a cotton lap blanket, inside the storage ottoman.

**T6 [PE]** target=`soft decorative and comforting plush items`
- Q: How do you usually organize soft decorative and comforting plush items, like your soft stuffed bear?
- A: I keep soft decorative and comforting plush items, like my stuffed bear, inside the storage ottoman along with other cozy lounge textiles.

**T7 [PE]** target=`items typically kept in the coffee table`
- Q: What kinds of items do you typically keep in the coffee table?
- A: I haven't really thought about a specific set of items for the coffee table.

**T8 [PE]** target=`decorative and seasonal display materials`
- Q: How do you usually organize decorative and seasonal display materials, like seasonal garland?
- A: I keep decorative and seasonal display materials, like seasonal garland, in the storage basket along with other stored or archived living-room accessories.

**T9 [PE]** target=`small fabric or textile accessory pouches`
- Q: How do you usually organize small fabric or textile accessory pouches, like spare coaster pouch?
- A: I keep small fabric or textile accessory pouches, like a spare coaster pouch, in the storage basket along with other stored or archived living-room accessories.

**T10 [AO]** target=`battery-powered remote`
- Q: Where should the battery-powered remote go?
- A: The battery-powered remote should go in the media drawer along with other handheld media-control and portable entertainment devices.

---

## episode_17 (living room)

**PSR**: u@1=42% → u@3=83% → u@5=75% → u@10=83%, fb=0

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
- `seasonal garland` → `storage basket`
- `rolled puzzle mat` → `storage basket`

**末态 confirmed_preferences** (7):
- *Family games and tabletop entertainment items are kept on the center table for easy access during game nights.*
  - → center table, covers ['family card game', 'board game box']
- *Hardcover literary reading materials are kept upright on the bookshelf.*
  - → bookshelf, covers ['leather-bound journal', 'hardcover novel']
- *Fragile decorative glass and ceramic keepsakes are displayed on the bookshelf with other delicate display items.*
  - → bookshelf, covers ['porcelain trinket dish', 'crystal keepsake']
- *Lightweight plastic organizers and serving pieces are kept together in the storage basket with other durable spare accessories.*
  - → storage basket, covers ['plastic magazine holder', 'plastic tray']
- *Soft comfort textiles and protective covers are kept in the storage ottoman with other lounge textiles for easy relaxation.*
  - → storage ottoman, covers ['plush ottoman cover', 'cotton lap blanket']
- *Decorative seasonal foliage and ornamental garlands are stored in the storage basket along with other stored or seasonal living-room accessories.*
  - → storage basket, covers ['seasonal garland']
- *Large rolled leisure mats or other durable accessories not used frequently are kept in the storage basket.*
  - → storage basket, covers ['rolled puzzle mat']

### QA Sequence (10 turns)
**T1 [PE]** target=`family tabletop entertainment items`
- Q: How do you usually organize family tabletop entertainment items, like family card game or board game box?
- A: I keep family games like card decks, board game boxes, and anything else we play together on the center table so they're handy for game nights.

**T2 [PE]** target=`literary reading materials with hard covers`
- Q: How do you usually organize literary reading materials with hard covers, like a leather-bound journal or a hardcover novel?
- A: I keep hardcover reading materials like leather-bound journals, novels, and reference books upright on the bookshelf.

**T3 [PE]** target=`fragile decorative glass and ceramic keepsakes`
- Q: How do you usually organize fragile decorative glass and ceramic keepsakes, like a porcelain trinket dish or a crystal keepsake?
- A: I display fragile decorative glass or ceramic keepsakes like porcelain trinket dishes and crystal pieces on the bookshelf, along with other delicate display items.

**T4 [PE]** target=`lightweight plastic organizers and serving pieces`
- Q: How do you usually organize lightweight plastic organizers and serving pieces, like a plastic magazine holder or a plastic tray?
- A: I keep lightweight plastic organizers and serving pieces like magazine holders and trays in the storage basket with other durable spare accessories.

**T5 [PE]** target=`soft comfort textiles and protective covers`
- Q: How do you usually organize soft comfort textiles and protective covers, like your plush ottoman cover or cotton lap blanket?
- A: I keep soft comfort items and protective covers like plush ottoman covers and cotton lap blankets in the storage ottoman, along with other lounge textiles that make relaxing easier.

**T6 [PE]** target=`decorative seasonal foliage and ornamental garlands`
- Q: How do you usually organize decorative seasonal foliage and ornamental garlands, like a seasonal garland?
- A: I keep decorative seasonal foliage and ornamental garlands in the storage basket along with other stored or seasonal living-room accessories.

**T7 [PE]** target=`items typically kept in the media console`
- Q: What kinds of items do you typically keep in the media console?
- A: I haven't really thought about what to keep in the media console, so I don't have a specific organizing rule for that spot.

**T8 [PE]** target=`large rolled leisure activity mats used for puzzling or tabletop play`
- Q: How do you usually organize large rolled leisure activity mats used for puzzling or tabletop play, like a rolled puzzle mat?
- A: I keep large rolled leisure mats like puzzle mats in the storage basket together with other durable or stored accessories that aren’t in frequent use.

**T9 [PE]** target=`items typically kept in the side table`
- Q: What kinds of items do you typically keep in the side table?
- A: I haven't really thought about what to keep in the side table, so I don't have a specific organizing rule for that spot.

**T10 [PE]** target=`items typically kept in the side drawer`
- Q: What kinds of items do you typically keep in the side drawer?
- A: I haven't really thought about what to keep in the side drawer, so I don't have a specific organizing rule for that spot.

---

## episode_34 (bedroom)

**PSR**: u@1=58% → u@3=67% → u@5=83% → u@10=100%, fb=1

**末态 confirmed_actions** (12):
- `ready-to-wear cardigan` → `wardrobe shelf`
- `folded scarf` → `wardrobe shelf`
- `ceramic jewelry dish` → `vanity tray`
- `porcelain ring tray` → `vanity tray`
- `hardcover sketchbook` → `bedroom bookshelf`
- `hardcover planner` → `bedroom bookshelf`
- `battery-powered massager` → `bedside drawer`
- `rechargeable hand warmer` → `bedside drawer`
- `hair clip box` → `vanity tray`
- `wooden keepsake box` → `vanity tray`
- `off-season scarf set` → `storage bench`
- `storage pouch` → `storage bench`

**末态 confirmed_preferences** (8):
- *Soft wearable textiles and accessories are stored on the wardrobe shelf where ready-to-wear clothing lives.*
  - → wardrobe shelf, covers ['ready-to-wear cardigan', 'folded scarf']
- *Fragile ceramic and porcelain jewelry holders are kept on the vanity tray with other delicate display accessories and keepsakes.*
  - → vanity tray, covers ['ceramic jewelry dish', 'porcelain ring tray']
- *Hardcover creative and planning notebooks are kept on the bedroom bookshelf with other books and reference materials.*
  - → bedroom bookshelf, covers ['hardcover sketchbook', 'hardcover planner']
- *Small battery-powered handheld comfort gadgets are kept in the bedside drawer with other small bedside electronics.*
  - → bedside drawer, covers ['battery-powered massager', 'rechargeable hand warmer']
- *Small decorative wooden and fabric storage boxes are kept on the vanity tray with other personal accessories and keepsakes.*
  - → vanity tray, covers ['hair clip box', 'wooden keepsake box']
- *Off-season clothing accessories are stored in the storage bench with other soft or bulky items not currently in rotation.*
  - → storage bench, covers ['off-season scarf set']
- *Dirty clothes and linens that need washing go in the laundry hamper.*
  - → laundry hamper, covers []
- *Soft portable storage items are kept in the storage bench with other soft or bulky accessories that aren’t used daily.*
  - → storage bench, covers ['storage pouch']

### QA Sequence (10 turns)
**T1 [PE]** target=`soft wearable textiles and accessories`
- Q: How do you usually organize soft wearable textiles and accessories, like your ready-to-wear cardigan or folded scarf?
- A: I keep soft wearable things like cardigans and scarves on the wardrobe shelf since that’s where my ready-to-wear clothing lives.

**T2 [PE]** target=`fragile ceramic and porcelain jewelry holders`
- Q: How do you usually organize fragile ceramic and porcelain jewelry holders, like a ceramic jewelry dish or a porcelain ring tray?
- A: I keep fragile ceramic and porcelain jewelry holders on the vanity tray along with other delicate display accessories and keepsakes.

**T3 [PE]** target=`hardcover creative and planning notebooks`
- Q: How do you usually organize hardcover creative and planning notebooks, like a hardcover sketchbook or a hardcover planner?
- A: I keep hardcover creative and planning notebooks, like sketchbooks and planners, on the bedroom bookshelf along with other books and reference items.

**T4 [PE]** target=`small battery-powered handheld comfort devices`
- Q: How do you usually organize small battery-powered handheld comfort devices, like a battery-powered massager or a rechargeable hand warmer?
- A: I keep small battery-powered comfort gadgets, like a massager or rechargeable hand warmer, in the bedside drawer with my other small bedside electronics.

**T5 [PE]** target=`small decorative wood and fabric storage containers`
- Q: How do you usually organize small decorative wood and fabric storage containers, like the hair clip box or the wooden keepsake box?
- A: I keep small decorative wooden and fabric boxes, like the hair clip box or wooden keepsake box, on the vanity tray with my other small personal accessories and keepsakes.

**T6 [PE]** target=`seasonal clothing accessories stored for off-season use`
- Q: How do you usually organize seasonal clothing accessories stored for off-season use, like an off-season scarf set?
- A: I store off-season clothing accessories, like an off-season scarf set, in the storage bench along with other soft or bulky items that aren’t part of my current wardrobe rotation.

**T7 [PE]** target=`items typically kept in the nightstand`
- Q: What kinds of items do you typically keep in the nightstand?
- A: I don't have a specific organizing rule for the nightstand.

**T8 [PE]** target=`items typically kept in the laundry hamper`
- Q: What kinds of items do you typically keep in the laundry hamper?
- A: I usually put dirty clothes and linens that need to be washed in the laundry hamper.

**T9 [PE]** target=`small portable soft storage items`
- Q: How do you usually organize small portable soft storage items, like storage pouch?
- A: I keep soft portable storage items, like a storage pouch, in the storage bench along with other soft or bulky accessories that don’t need to be out for daily use.

**T10 [AO]** target=`battery-powered massager`
- Q: Where should the battery-powered massager be placed?
- A: I keep small bedside electronics, like a battery-powered massager, in the bedside drawer with similar items such as the rechargeable hand warmer.

---

## episode_51 (bedroom)

**PSR**: u@1=83% → u@3=83% → u@5=75% → u@10=92%, fb=0

**末态 confirmed_actions** (12):
- `portable reading light` → `nightstand drawer`
- `plug-in bedside lamp` → `nightstand`
- `hardcover devotional` → `reading shelf`
- `rigid-cover photo diary` → `reading shelf`
- `sleep journal` → `reading shelf`
- `clean cotton pajamas` → `closet shelf`
- `folded linen shirt` → `closet shelf`
- `phone charging cable` → `nightstand`
- `hand lotion` → `nightstand`
- `off-season scarf set` → `storage bench`
- `battery-powered massager` → `nightstand drawer`
- `spare hanger pack` → `storage bench`

**末态 confirmed_preferences** (8):
- *Plug-in bedside devices stay on the nightstand, while battery-powered ones are kept in the nightstand drawer.*
  - → nightstand, covers ['portable reading light', 'plug-in bedside lamp']
- *Hardcover books and personal journals, such as devotionals or photo diaries, belong on the reading shelf along with other sturdy reading materials.*
  - → reading shelf, covers ['hardcover devotional', 'rigid-cover photo diary', 'sleep journal']
- *Clean cotton and linen sleepwear and ready-to-wear garments should be folded and kept on the closet shelf.*
  - → closet shelf, covers ['clean cotton pajamas', 'folded linen shirt']
- *Corded charging and connectivity accessories are kept on the nightstand with plug-in bedside devices used regularly.*
  - → nightstand, covers ['phone charging cable']
- *Skincare and moisturizing items are kept on the nightstand for easy access before sleeping.*
  - → nightstand, covers ['hand lotion']
- *Lightweight unused seasonal clothing accessories are kept in the storage bench with other soft or bulky items not needed daily.*
  - → storage bench, covers ['off-season scarf set']
- *Small battery-powered personal care devices are kept in the nightstand drawer together with other small bedside electronics and light sources that run on batteries.*
  - → nightstand drawer, covers ['battery-powered massager']
- *Unused clothing maintenance accessories and hanging supplies are stored in the storage bench with other soft or overflow items not used daily.*
  - → storage bench, covers ['spare hanger pack']

### QA Sequence (10 turns)
**T1 [PE]** target=`plug-in and battery-powered bedside devices`
- Q: How do you usually organize plug-in and battery-powered bedside devices, like a portable reading light or a plug-in bedside lamp?
- A: Plug-in bedside lamps stay on the nightstand, while smaller battery-powered devices like portable reading lights go in the nightstand drawer.

**T2 [PE]** target=`hardcover books and journals for personal reflection`
- Q: How do you usually organize hardcover books and journals for personal reflection, like a hardcover devotional or a rigid-cover photo diary?
- A: I keep hardcover books and personal journals, such as devotionals or photo diaries, on the reading shelf along with other sturdy reading materials.

**T3 [PE]** target=`soft cotton and linen sleepwear and garments`
- Q: How do you usually organize soft cotton and linen sleepwear and garments, like clean cotton pajamas or a folded linen shirt?
- A: I keep clean cotton and linen sleepwear and other ready-to-wear garments folded on the closet shelf.

**T4 [PE]** target=`corded electronic accessories for charging or connectivity`
- Q: How do you usually organize corded electronic accessories for charging or connectivity, like your phone charging cable?
- A: I keep corded charging and connectivity accessories like my phone charging cable right on the nightstand along with the plug-in bedside devices I use regularly.

**T5 [PE]** target=`personal skincare and moisturizing items`
- Q: How do you usually organize personal skincare and moisturizing items, like hand lotion?
- A: I keep skincare and moisturizing items, like hand lotion, right on the nightstand with other things I reach for nightly before sleeping.

**T6 [PE]** target=`lightweight unused seasonal clothing accessories`
- Q: How do you usually organize lightweight unused seasonal clothing accessories, like an off-season scarf set?
- A: I keep lightweight unused seasonal accessories, like off-season scarf sets, in the storage bench along with other soft or bulky items I don't need every day.

**T7 [PE]** target=`small battery-powered personal care devices`
- Q: How do you usually organize small battery-powered personal care devices, like a battery-powered massager?
- A: I keep small battery-powered personal care devices, like a battery-powered massager, in the nightstand drawer together with other small bedside electronics and light sources that run on batteries.

**T8 [PE]** target=`items typically kept in the vanity tray`
- Q: What kinds of items do you typically keep in the vanity tray?
- A: I haven't really thought about what I keep on the vanity tray.

**T9 [PE]** target=`items typically kept in the linen hamper`
- Q: What kinds of items do you typically keep in the linen hamper?
- A: I don't have a specific organizing rule for the linen hamper.

**T10 [PE]** target=`unused clothing maintenance accessories and hanging supplies`
- Q: How do you usually organize unused clothing maintenance accessories and hanging supplies, like spare hanger pack?
- A: I keep unused clothing maintenance accessories and hanging supplies, like spare hanger packs, in the storage bench with other soft or overflow items I don't use daily.

---

## episode_68 (kitchen)

**PSR**: u@1=58% → u@3=83% → u@5=100% → u@10=100%, fb=1

**末态 confirmed_actions** (12):
- `wired coffee grinder` → `prep counter`
- `plug-in toaster` → `prep counter`
- `cut lemon container` → `fridge shelf`
- `opened yogurt tub` → `fridge shelf`
- `porcelain teacup set` → `upper cabinet`
- `glass pitcher` → `upper cabinet`
- `battery-powered can opener` → `kitchen drawer`
- `digital kitchen timer` → `kitchen drawer`
- `wooden citrus reamer` → `kitchen drawer`
- `wooden salad servers` → `kitchen drawer`
- `cake topper tin` → `upper cabinet`
- `serving candle set` → `upper cabinet`

**末态 confirmed_preferences** (6):
- *Plug-in breakfast appliances are kept on the prep counter so they are ready to use near a power outlet.*
  - → prep counter, covers ['wired coffee grinder', 'plug-in toaster']
- *Opened or partially used refrigerated foods are kept on the fridge shelf to stay fresh.*
  - → fridge shelf, covers ['cut lemon container', 'opened yogurt tub']
- *Fragile glass and porcelain serving drinkware are stored in the upper cabinet for safety and convenient access when serving.*
  - → upper cabinet, covers ['porcelain teacup set', 'glass pitcher']
- *Small battery-powered handheld kitchen tools are kept in the kitchen drawer along with other powered gadgets that do not plug in.*
  - → kitchen drawer, covers ['battery-powered can opener', 'digital kitchen timer']
- *Small wooden handheld prep and serving tools are kept in the kitchen drawer with other wooden or bamboo utensils.*
  - → kitchen drawer, covers ['wooden citrus reamer', 'wooden salad servers']
- *Decorative or celebratory table accessories made of metal or wax are kept in the upper cabinet with other special‑occasion serving and display items.*
  - → upper cabinet, covers ['cake topper tin', 'serving candle set']

### QA Sequence (10 turns)
**T1 [PE]** target=`plug-in countertop breakfast appliances`
- Q: How do you usually organize plug-in countertop breakfast appliances, like a wired coffee grinder or a plug-in toaster?
- A: I keep plug-in breakfast appliances like the coffee grinder and toaster on the prep counter so they're ready to use near a power outlet.

**T2 [PE]** target=`opened or partially used refrigerated food containers`
- Q: How do you usually organize opened or partially used refrigerated food containers, like a cut lemon container or an opened yogurt tub?
- A: I keep any opened or partially used refrigerated foods, like cut fruit containers or opened yogurt tubs, on the fridge shelf so they stay fresh.

**T3 [PE]** target=`fragile glass and porcelain serving drinkware`
- Q: How do you usually organize fragile glass and porcelain serving drinkware, like a porcelain teacup set or a glass pitcher?
- A: I keep all fragile glass and porcelain serving drinkware, like a teacup set or a glass pitcher, in the upper cabinet where they’re safe and out of the way but easy to reach for serving.

**T4 [PE]** target=`small battery-powered handheld kitchen tools`
- Q: How do you usually organize small battery-powered handheld kitchen tools, like a battery-powered can opener or a digital kitchen timer?
- A: I keep small battery-powered handheld kitchen tools, like a can opener or digital timer, in the kitchen drawer along with other powered gadgets that don’t plug in.

**T5 [PE]** target=`small wooden handheld prep and serving tools`
- Q: How do you usually organize small wooden handheld prep and serving tools, like wooden citrus reamers or wooden salad servers?
- A: I keep small wooden handheld prep and serving tools, like citrus reamers or salad servers, in the kitchen drawer along with other wooden or bamboo utensils.

**T6 [PE]** target=`decorative or celebratory table accessories made of metal or wax`
- Q: How do you usually organize decorative or celebratory table accessories made of metal or wax, like a cake topper tin or serving candle set?
- A: I keep decorative or celebratory table accessories, like metal cake toppers or wax serving candles, in the upper cabinet along with other special-occasion serving and display items.

**T7 [PE]** target=`items typically kept in the pantry shelf`
- Q: What kinds of items do you typically keep in the pantry shelf?
- A: I haven't really thought about what goes on the pantry shelf.

**T8 [PE]** target=`items typically kept in the base cabinet`
- Q: What kinds of items do you typically keep in the base cabinet?
- A: I haven't really thought about what goes in the base cabinet.

**T9 [PE]** target=`items typically kept in the produce basket`
- Q: What kinds of items do you typically keep in the produce basket?
- A: I haven't really thought about what goes in the produce basket.

**T10 [AO]** target=`wired coffee grinder`
- Q: Where should the wired coffee grinder go?
- A: The wired coffee grinder should go on the prep counter with the other countertop appliances that need to be plugged in while in use, like the toaster.

---
