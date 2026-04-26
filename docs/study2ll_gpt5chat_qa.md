# Study 2 LL × GPT-5-Chat × 5 ep × Budgets 1/3/5 — QA 完整记录

| Budget | Seen | Unseen |
|---|---|---|
| 1 | 63.3% ± 10.1 | 56.7% ± 12.7 |
| 3 | 56.7% ± 8.9 | 73.3% ± 6.7 |
| 5 | 75.0% ± 3.7 | 78.3% ± 2.0 |

全部 5 episodes 在 budget=5 下的 pattern 序列均为 **AO→PI→AO→PI→AO**（fb=0）。

---

## episode_0 (living room)

**PSR**: u@1=83% (B=1), see logs for B=3/5  
**Final state @ B=5**:
- confirmed_actions (7): [('battery-powered remote', 'media drawer'), ('wireless speaker', 'media drawer'), ('wired game console', 'TV stand'), ('corded reading light', 'TV stand'), ('hardcover novel', 'bookshelf'), ('hardcover art book', 'bookshelf'), ('cotton lap blanket', 'storage ottoman')]
- confirmed_preferences (2):
  - **portable media electronics like the wireless speaker and remotes should be kept together i**
    → media drawer, covers ['wireless speaker']
  - **hardcover novels, art books, and other upright reading or reference books should be placed**
    → bookshelf, covers ['hardcover novel', 'hardcover art book']

### QA Sequence (5 turns)
**T? [AO]** target=  
- Q: Where should the battery-powered remote be placed?
- A: That should go in the media drawer, along with other handheld media-control devices like remotes and portable media accessories.
**T? [PI]** target=  
- Q: I'd expect media electronics like your wireless speaker and game console to go in the media drawer with the remote — does that match how you like to organise things?
- A: Yes, that fits perfectly — I keep the wireless speaker and other portable media gadgets in the media drawer with the remotes, while bulkier plug-in entertainment gear like the game console stays on the TV stand.
**T? [AO]** target=  
- Q: Where should the corded reading light be placed?
- A: The corded reading light belongs on the TV stand, since it’s a plug-in piece of wired equipment rather than something handheld or portable.
**T? [PI]** target=  
- Q: I'd expect hardcover and art books to go on the bookshelf — does that match how you like to organise things?
- A: Yes, that matches exactly — hardcover novels, art books, and other upright reading or reference books all go on the bookshelf.
**T? [AO]** target=  
- Q: Where should the cotton lap blanket be placed?
- A: The cotton lap blanket goes in the storage ottoman, where I keep soft comfort items and extra lounge textiles.

---

## episode_17 (living room)

**PSR**: u@1=75% (B=1), see logs for B=3/5  
**Final state @ B=5**:
- confirmed_actions (7): [('leather-bound journal', 'bookshelf'), ('hardcover novel', 'bookshelf'), ('porcelain trinket dish', 'bookshelf'), ('family card game', 'center table'), ('board game box', 'center table'), ('rolled puzzle mat', 'center table'), ('crystal keepsake', 'bookshelf')]
- confirmed_preferences (2):
  - **Books and journals should be stored together upright on the bookshelf.**
    → bookshelf, covers ['hardcover novel', 'leather-bound journal']
  - **Family games and puzzles should be kept together on the center table for tabletop leisure **
    → center table, covers ['family card game', 'board game box', 'rolled puzzle mat']

### QA Sequence (5 turns)
**T? [AO]** target=  
- Q: Where should the leather-bound journal go?
- A: The leather-bound journal should go on the bookshelf along with the other reading and reference books.
**T? [PI]** target=  
- Q: I'd expect books and journals to go together on the bookshelf — does that match how you like to organise things?
- A: Yes, that fits exactly — I keep both books and journals together on the bookshelf with my other reading materials.
**T? [AO]** target=  
- Q: Where should the porcelain trinket dish go?
- A: The porcelain trinket dish should go on the bookshelf with the other fragile display pieces.
**T? [PI]** target=  
- Q: I'd expect family games and puzzles to live inside the storage ottoman — is that right?
- A: No, I actually keep family games and puzzles on the center table — that's where all the tabletop leisure items stay.
**T? [AO]** target=  
- Q: Where should the crystal keepsake go?
- A: The crystal keepsake should go on the bookshelf with the other fragile display pieces.

---

## episode_34 (bedroom)

**PSR**: u@1=83% (B=1), see logs for B=3/5  
**Final state @ B=5**:
- confirmed_actions (7): [('battery-powered massager', 'bedside drawer'), ('rechargeable hand warmer', 'bedside drawer'), ('hardcover sketchbook', 'bedroom bookshelf'), ('ready-to-wear cardigan', 'wardrobe shelf'), ('folded scarf', 'wardrobe shelf'), ('off-season scarf set', 'wardrobe shelf'), ('ceramic jewelry dish', 'vanity tray')]
- confirmed_preferences (2):
  - **Small rechargeable or battery-powered comfort devices should be stored in the bedside draw**
    → bedside drawer, covers ['rechargeable hand warmer', 'battery-powered massager']
  - **Folded wearable accessories and ready-to-wear clothing such as scarves and cardigans shoul**
    → wardrobe shelf, covers ['ready-to-wear cardigan', 'folded scarf', 'off-season scarf set']

### QA Sequence (5 turns)
**T? [AO]** target=  
- Q: Where should the battery-powered massager go?
- A: That should go in the bedside drawer with the other small bedside electronics.
**T? [PI]** target=  
- Q: I'd expect small rechargeable or battery-powered comfort devices to go in the bedside drawer — does that match how you like to organise things?
- A: Yes, that matches perfectly — I keep small rechargeable or battery-powered comfort devices together in the bedside drawer.
**T? [AO]** target=  
- Q: Where should the hardcover sketchbook be placed?
- A: The hardcover sketchbook should go on the bedroom bookshelf with other books and planners.
**T? [PI]** target=  
- Q: I'd guess folded accessories and cardigans belong on a wardrobe shelf — does that match how you organise things?
- A: Yes, that matches — I keep ready-to-wear clothing and folded accessories like scarves or cardigans on the wardrobe shelf.
**T? [AO]** target=  
- Q: Where should the ceramic jewelry dish be placed?
- A: The ceramic jewelry dish should go on the vanity tray with other fragile or display accessories like ring trays and keepsake boxes.

---

## episode_51 (bedroom)

**PSR**: u@1=75% (B=1), see logs for B=3/5  
**Final state @ B=5**:
- confirmed_actions (8): [('portable reading light', 'nightstand drawer'), ('battery-powered massager', 'nightstand drawer'), ('phone charging cable', 'nightstand'), ('plug-in bedside lamp', 'nightstand'), ('hardcover devotional', 'reading shelf'), ('rigid-cover photo diary', 'reading shelf'), ('sleep journal', 'reading shelf'), ('clean cotton pajamas', 'closet shelf')]
- confirmed_preferences (2):
  - **Plug-in bedside electronics like lamps and chargers are kept on the nightstand, while smal**
    → nightstand, covers ['battery-powered massager', 'phone charging cable', 'plug-in bedside lamp']
  - **Bound reading materials like journals, diaries, devotionals, and other sturdy books are ke**
    → reading shelf, covers ['rigid-cover photo diary', 'sleep journal']

### QA Sequence (5 turns)
**T? [AO]** target=  
- Q: Where should the portable reading light go?
- A: The portable reading light should go in the nightstand drawer with the other small bedside electronics and light sources.
**T? [PI]** target=  
- Q: I'd expect small plug-in or battery-powered bedside electronics like lamps or phone chargers to go in or on the nightstand — does that match how you like to organise things?
- A: Yes, that fits. I keep plug-in bedside gear like lamps and chargers on the nightstand itself, while smaller battery-powered items usually go in the nightstand drawer.
**T? [AO]** target=  
- Q: Where should the hardcover devotional be placed?
- A: The hardcover devotional should go on the reading shelf with the other sturdy books I keep for current reading.
**T? [PI]** target=  
- Q: I'd expect bound reading materials like journals, diaries, and devotionals to go on the reading shelf — does that match how you like to organise things?
- A: Yes, that matches. I keep bound reading materials like journals, diaries, devotionals, and other sturdy books on the reading shelf with the items I’m currently reading.
**T? [AO]** target=  
- Q: Where should the clean cotton pajamas go?
- A: The clean cotton pajamas should go on the closet shelf with the other ready-to-wear bedroom clothing.

---

## episode_68 (kitchen)

**PSR**: u@1=75% (B=1), see logs for B=3/5  
**Final state @ B=5**:
- confirmed_actions (5): [('wired coffee grinder', 'prep counter'), ('cut lemon container', 'fridge shelf'), ('opened yogurt tub', 'fridge shelf'), ('plug-in toaster', 'prep counter'), ('battery-powered can opener', 'kitchen drawer')]
- confirmed_preferences (2):
  - **opened or partly used foods should be stored on the fridge shelf**
    → fridge shelf, covers ['cut lemon container', 'opened yogurt tub']
  - **plug-in kitchen appliances that remain plugged in during use should be kept on the prep co**
    → prep counter, covers ['wired coffee grinder', 'plug-in toaster']

### QA Sequence (5 turns)
**T? [AO]** target=  
- Q: Where should the wired coffee grinder be placed in the kitchen?
- A: It should go on the prep counter with the other appliances that plug in while being used.
**T? [PI]** target=  
- Q: I think opened or partly used foods like the yogurt tub or lemon container would stay on a fridge shelf — is that how you like it?
- A: Yes, opened or partly used foods like yogurt or a cut lemon definitely stay on the fridge shelf.
**T? [AO]** target=  
- Q: Where should the plug-in toaster be placed?
- A: The plug-in toaster should go on the prep counter with the other appliances that need power while being used.
**T? [PI]** target=  
- Q: I'd expect small plug-in kitchen appliances to live on the prep counter for easy use — does that match how you like to organise things?
- A: Yes, that matches my setup — plug-in kitchen appliances that stay plugged in while in use live on the prep counter for easy access.
**T? [AO]** target=  
- Q: Where should the battery-powered can opener go?
- A: The battery-powered can opener belongs in the kitchen drawer with the other small powered kitchen gadgets that don’t need to be plugged in.

---
