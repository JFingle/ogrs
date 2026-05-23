# OGRS Food & Farming — Design Document

> **Vision:** Farming feeds Cooking. Complex multi-ingredient dishes from world cuisines heal far more than vanilla RSC's max (shark = 20 HP). Sourcing ingredients across the world makes farming a real economic engine. Each ingredient has its own art asset, growing cycle, harvest yield, and use in 1+ recipes.

---

## 1. Healing Tier Bands (constrained by 99 HP cap)

**Hard fact:** RSC max Hits stat = 99. A food healing for more than 99 is wasted. All numbers in this doc are **CAPPED at 99**.

**Existing OGRS/RSC food data** (parsed from `server/conf/server/defs/extras/ItemEdibleHeals.xml` — 126 edible items):

| Heal value | # foods at this value | Examples |
|---:|---:|---|
| 26 | 1 | **Seaweed soup** (current outlier — top heal in vanilla) |
| 20 | 3 | **Shark, Manta ray, Sea turtle** (the iconic "top food" trio) |
| 19 | 4 | Curry, Special curry, Ugthanki Kebab, Tasty Ugthanki Kebab |
| 15 | 3 | Chocolate bomb, Tangled toads legs |
| 14 | 3 | Swordfish, Pumpkin, Easter egg |
| 12-13 | 8 | Lobster, Bass, Vegball, Wormhole |
| 10-11 | 19 | Cooked mid-tier fish, basic meals |
| 7-9 | 22 | Standard cooked meals |
| 4-6 | 21 | Bread, snacks, basic cooked |
| 1-3 | 41 | Raw foods, fruit, bread, milk |
| -2 | 1 | One item DAMAGES you (rotten?) |

So **vanilla ceiling is 20 (sharks)** with one quest outlier at 26. OGRS keeps the existing curve, then adds a small number of complex new recipes climbing toward 99.

### Rebalanced tier table

| Tier | Complexity | Ingredients | HP healed | Coverage | Examples |
|---|---|---:|---:|---|---|
| **0** | Raw | 1 | 1-3 | Vanilla 41 foods | Apple, raw potato |
| **1** | Simple cook | 1-2 | 4-8 | Vanilla 21 foods | Baked potato, fried egg, bread |
| **2** | Basic recipe | 2-3 | 10-15 | Vanilla 19 foods | Stew, basic cooked fish, snack |
| **3** | Standard dish | 4-5 | 18-22 | Vanilla ceiling (Shark=20, Curry=19) + ~10 NEW recipes | Pizza Margherita, Tacos, basic Curry |
| **4** | Complex dish | 6-7 | 25-35 | **NEW** territory above vanilla | Lasagna, Biryani, Ramen, Pad Thai |
| **5** | Masterwork | 8-9 | 40-55 | **NEW** | Paella, Beef Bourguignon, Mole |
| **6** | Legendary | 10+ | 60-80 | **NEW**, very rare | Multi-course feast |
| **7** | Sacred/Blessed | quest-locked | **99** (full restore) | **NEW**, ~1 dish | Last Supper Spread — full heal, once per real-world week |

**The "one food heals 100" idea becomes: one Sacred dish heals to full HP (99).** Capped at max — it's not 100 numerically, but it heals you to the cap regardless of how much you were missing. Quest-locked, Galilee-only, week-cooldown.

**Bonus multipliers (apply BEFORE the 99 cap):**
- Cooked on proper station (oven/firepit vs portable fire): ×1.1
- Player Cooking level ≥ recipe req: ×1.0 (below req = burn risk)
- "Blessed by Yahwist priest" buff: ×1.3 (Galilee priests, once/day per player)
- Eating the same masterwork dish ×3 in one meal = "feast" status: +5 HP regen/tick for 60 seconds (regen, not instant heal — works WITH the cap, not against it)

**Important design note:** OGRS shouldn't bypass the 99 cap. Instead, the value of high-tier food comes from:
1. **Single-bite full heals** — a Tier 5 dish at 50 HP can fully restore you from 49 HP, vs needing 3 sharks
2. **Inventory efficiency** — 1 slot of legendary food replaces 4-5 slots of sharks
3. **Status buffs** — masterwork dishes give "feast" regen instead of just instant heal
4. **Combat windows** — legendary dishes can be eaten without breaking combat tempo (vs 3 sharks = 3 ticks)

---

## 2. Growables Catalog

### Tier 1 — Starter Crops (Allotment patches, fast cycle 15-30 min)

Lumbridge allotment already has 3 of these. Adding 9 more for variety:

| Crop | Status | Cooking uses | Notes |
|---|---|---|---|
| Potato | ✅ shipped | Soups, stews, fries, casseroles | Already implemented |
| Onion | ✅ shipped | Almost every savory recipe | Already implemented |
| Tomato | ✅ shipped | Sauces, pizza, salads | Already implemented |
| Cabbage | ❌ | Coleslaw, kimchi, soup | Existing item in vanilla |
| Lettuce | ❌ | Salad base | Light snack |
| Garlic | ❌ | Aroma for every cuisine | Vampire deterrent (lore) |
| Beans | ❌ | Chili, refried, soup | Multi-use staple |
| Peas | ❌ | Side dish, soup, curry | Spring crop |
| Corn | ❌ | Tortilla, polenta, popcorn | Mexican/American |
| Carrots | ❌ | Stew, salad, cake | Universal |
| Cucumber | ❌ | Salads, tzatziki, pickles | Greek/Mediterranean |
| Bell Peppers | ❌ | Stir-fry, fajitas, stuffed | 3 colors (red/green/yellow) |

### Tier 2 — Mid Crops (longer cycle 45-90 min, more advanced patches)

| Crop | Cooking uses | Notes |
|---|---|---|
| Wheat | ✅ existing | Flour → bread → pizza dough → pasta | Already in game |
| Mushrooms | Pizza topping, stews, sauce | Forageable + farmable both |
| Strawberries | Jam, cake, dessert | Sweet, decorative patch |
| Blueberries | Jam, muffins, smoothies | Same |
| Hot Peppers | Curry, hot sauce, mole | Spicy crops, chili pepper |
| Rice | Curry, sushi, paella, biryani | Wet patch — Karamja or Galilee |
| Eggplant | Moussaka, baba ghanoush, parm | Mediterranean staple |
| Zucchini | Ratatouille, bread, fritters | Versatile vegetable |
| Spinach | Salads, lasagna, smoothies | Iron-rich (small Defense buff?) |
| Pumpkin | Pie, soup, halloween-themed | Seasonal |

### Tier 3 — Slow Crops (2-4 hour cycle, special patches)

| Crop | Cooking uses | Notes |
|---|---|---|
| Wine Grapes | Wine production, juice | Vineyard patch (Galilee?) |
| Olives | Oil, tapenade, garnish | Olive tree — Galilee canon |
| Figs | Fig newtons, biblical dishes | Galilee canon ([[project-ogrs]] memory item 14 Layer 8) |
| Apples | Pie, cider, eating | Orchard tree |
| Pears | Pie, brandy, dessert | Orchard |
| Cherries | Jam, pie, garnish | Orchard, decorative |
| Pineapples | Pizza topping (controversial!), Hawaiian | Tropical, Karamja |
| Bananas | Bread, smoothie, dessert | Karamja, ✅ via Bones-to-Bananas |
| Coconuts | Curry, dessert, milk | Karamja tropical |
| Avocado | Guacamole, toast, sushi | Tropical |

### Tier 4 — Rare Crops (Quest unlock, 6-24 hour cycle)

| Crop | Cooking uses | Notes |
|---|---|---|
| Saffron | Paella, biryani, premium dishes | Most expensive spice IRL; rare gold-yield |
| Truffles | Pasta, omelet, garnish | Forageable from a special tree |
| Vanilla Beans | Desserts, cakes, ice cream | Slow + premium |
| Cocoa Pods | Chocolate, mole | Tropical, makes confectionery possible |
| Coffee Beans | Coffee, mocha, espresso | Bonus: +Attention/Energy buff |
| Tea Leaves | Tea, herbal medicine | + Healing/Calm buff |
| Mustard Seed | Mustard condiment, biblical lore | Galilee canon (parable: faith of) |
| Ginseng | Tonic, premium tea | Rare herbalist crop |

### Tier 5 — Sacred / Galilee Crops (Quest only, blessed yield)

These tie to OGRS's biblical lore track. Per project memory, "Galilee fields for sacred crops":

| Crop | Cooking uses | Lore tie |
|---|---|---|
| Wheat (Blessed) | Communion bread | Eucharistic theming |
| Wine Grapes (Blessed) | Wine for Communion | Same |
| Figs (Sacred Tree) | Restoration dish | Genesis fig leaves, "He hungered" |
| Olives (Olive Tree) | Anointing oil | Priestly anointing |
| Mustard Seed (Faith) | Tonic of trust | "Faith as a mustard seed" |
| Manna | Trail bread | Exodus reference, light/portable food |
| Pomegranate | Premium dessert | Garden of Eden / Promised Land symbol |

---

## 3. Flowers (Decoration + Utility + Potion Ingredients)

Per memory item 14 Layer 4 ("Living crops"), tend-able patches. Flowers are a new growable category:

### Common (decorative + light potion use)
| Flower | Potion use | Other |
|---|---|---|
| Rose | Beauty tonic (Charisma +5) | Sold to florist NPC |
| Lavender | Sleep tonic (Prayer regen) | Calming |
| Daisy | Cheer tonic (small XP boost 1hr) | Common |
| Sunflower | Daylight tonic (Attack +1) | Yellow/cheerful |
| Tulip | Beauty tonic stronger | Spring crop |
| Poppy | Mild sleep potion ingredient | Caution: addictive in lore |
| Marigold | Bug repellent for crops | Plant adjacent for yield+ |

### Magical (quest-related, potion key ingredients)
| Flower | Potion use | Notes |
|---|---|---|
| Moonflower | Night vision potion | Blooms only at night (clever mechanic) |
| Sunflower (large) | Solar charge battery for spells | Daytime power crystal alt |
| Nightshade | Poison damage potion | Dangerous, illegal to grow in cities |
| Phoenix Bloom | Resurrection ingredient | 1-per-month flower |
| Mandrake Root | Major restore (50+ HP) | Quest unlock |

### Sacred/Galilee
| Flower | Use | Lore |
|---|---|---|
| Lily of the Valley | Blessing potion | "Lilies of the field" parable |
| Hyssop | Cleansing tonic | Used in Mosaic purification |
| Cedar Sprig | Protection charm | Cedar of Lebanon symbolism |

---

## 4. Cooking Recipe Catalog

Recipes are stored in `content/recipes/*.yaml` (proposed) with this schema:
```yaml
id: pizza_margherita
display_name: Pizza Margherita
cooking_level_req: 35
ingredients:
  - {item: dough, qty: 1}
  - {item: tomato_sauce, qty: 1}
  - {item: cheese, qty: 1}
  - {item: basil, qty: 1}
heals: 20
xp: 80
cooks_on: oven
burn_threshold: 25   # below this level = burn
cultural_origin: "Italian"
```

### Tier 3 (4-5 ingredients, 18-22 HP) — World Sampler

Matches the top of vanilla (Shark=20, Curry=19). These are the "you've leveled cooking" dishes.

| Dish | Origin | Ingredients | HP | Lvl req |
|---|---|---|---:|---:|
| **Pizza Margherita** | Italian | dough + tomato + cheese + basil + olive oil | 20 | 35 |
| **Tacos** | Mexican | tortilla + meat + onion + tomato + cheese | 19 | 30 |
| **Caesar Salad** | American | lettuce + croutons + parmesan + dressing + egg | 18 | 25 |
| **Greek Salad** | Greek | cucumber + tomato + olive + feta + onion | 19 | 28 |
| **Spaghetti Bolognese** | Italian | pasta + tomato + meat + onion + herbs | 20 | 32 |
| **Curry (upgraded)** | Indian | rice + chicken + onion + tomato + curry spices | 22 | 35 |
| **Sushi Roll** | Japanese | rice + fish + nori + cucumber + soy | 22 | 38 |
| **Tom Yum Soup** | Thai | broth + shrimp + lime + lemongrass + chili | 20 | 30 |
| **Hummus + Pita** | Middle Eastern | chickpea + olive oil + lemon + garlic + bread | 18 | 22 |
| **Borscht** | Russian | beet + cabbage + meat + onion + sour cream | 20 | 32 |

### Tier 4 (6-7 ingredients, 25-35 HP) — Above-vanilla complex

| Dish | Origin | Ingredients | HP | Lvl req |
|---|---|---|---:|---:|
| **Lasagna** | Italian | pasta + meat + tomato + cheese + onion + herbs + bechamel | 30 | 50 |
| **Biryani** | Indian | rice + chicken + onion + tomato + saffron + spice mix + yogurt | 32 | 55 |
| **Ramen** | Japanese | broth + noodle + egg + meat + bamboo + scallion + nori | 28 | 50 |
| **Pad Thai** | Thai | noodle + shrimp + peanut + lime + bean sprout + egg + tamarind | 28 | 48 |
| **Coq au Vin** | French | chicken + wine + mushroom + bacon + onion + herbs + carrot | 32 | 55 |
| **Mole** | Mexican | chicken + chili + chocolate + spice mix + tomato + onion + nut | 30 | 52 |
| **Pho** | Vietnamese | broth + rice noodle + beef + lime + cilantro + basil + onion | 28 | 50 |
| **Shepherd's Pie** | British | meat + potato + carrot + peas + onion + cheese + gravy | 26 | 48 |
| **Tagine** | Moroccan | lamb + apricot + onion + spice mix + couscous + olive + lemon | 30 | 52 |
| **Kimchi Stew** | Korean | kimchi + pork + tofu + onion + scallion + chili + rice | 28 | 50 |

### Tier 5 (8-9 ingredients, 40-55 HP) — Masterwork

| Dish | Origin | Ingredients | HP | Lvl req |
|---|---|---|---:|---:|
| **Paella** | Spanish | rice + saffron + chicken + shrimp + mussel + bell pepper + onion + peas + lemon | 45 | 70 |
| **Beef Bourguignon** | French | beef + wine + bacon + mushroom + carrot + onion + herbs + tomato + broth | 50 | 72 |
| **Bouillabaisse** | French | fish + shrimp + mussel + tomato + onion + saffron + herbs + garlic + olive oil | 45 | 68 |
| **Peking Duck** | Chinese | duck + scallion + cucumber + hoisin + pancake + ginger + garlic + sesame + plum | 50 | 75 |
| **Feijoada** | Brazilian | beans + pork + sausage + beef + onion + garlic + bay + orange + rice | 45 | 68 |
| **Bibimbap** | Korean | rice + beef + spinach + carrot + mushroom + egg + chili paste + sesame + bean sprout | 42 | 65 |
| **Jollof Rice** | West African | rice + tomato + onion + chili + chicken + spice mix + bell pepper + broth + bay | 45 | 68 |
| **Sunday Roast** | British | beef + potato + carrot + parsnip + peas + yorkshire + gravy + horseradish + herbs | 48 | 70 |

### Tier 6 (10+ ingredients, 60-80 HP) — Legendary

These approach the HP cap. Cooking-90+ required, ingredients are pricey.

| Dish | Origin | Approx ingredients | HP | Lvl req |
|---|---|---|---:|---:|
| **Multi-course Wedding Feast** | Italian | 12 — pasta + lasagna + chicken + dessert + wine + bread + cheese + etc | 75 | 85 |
| **Royal Thai Banquet** | Thai | 10 — green curry + pad thai + tom yum + rice + spring rolls + etc | 70 | 80 |
| **Tea Ceremony Set** | Japanese | 10 — matcha + wagashi + soba + tempura + tofu + miso + rice + pickle + fish + sake | 65 | 80 |
| **Royal Curry Thali** | Indian | 11 — biryani + naan + chutney + raita + butter chicken + dal + saag + rice + sweet | 78 | 85 |

### Tier 7 (Sacred — Galilee/Yahwist, ~99 HP full restore)

Quest-locked, week-cooldown. **There is exactly ONE** dish that "heals 100" (effectively full restore, capped at 99). Everything else in this tier sits between 60-99 with secondary effects (Prayer regen, status cleansing, buffs).

| Dish | Components | HP | Cooldown | Notes |
|---|---|---:|---|---|
| **Last Supper Spread** | Bread + wine + fig + olive + fish + lamb + bitter herb | **99** (full restore) | 1× per real-world week | THE "100 HP" dish. Capped at 99. Also full Prayer restore. |
| **Communion Meal** | Blessed bread (wheat) + blessed wine (grapes) | 60 | 1× per day | Restoration + Prayer full restore |
| **Manna Bread** | Manna + honey | 70 | 1× per day | "Wilderness" recovery |
| **Anointing Oil Bread** | Olive oil + wheat + hyssop | 50 | normal cook | Heals + grants Prayer regen 30min (the *buff*, not the heal, is the value) |

---

## 5. Potion Ingredients (Herblore tie-in)

Herblore already exists in OGRS. New ingredients to expand:

### Vegetable-based potions (NEW category — "Greenkeeper potions")
- **Sturdy Tonic** (Carrot + Egg + Garlic) — +Defense 10min
- **Hot Sauce Burner** (Hot Pepper + Vinegar + Tomato) — +Attack/Strength 8min
- **Veggie Smoothie** (Spinach + Apple + Blueberry + Carrot) — Light heal + +Energy

### Flower-based potions
- **Moonlit Sight** (Moonflower + Tear + Glass) — Night vision 2hr
- **Solar Charge** (Sunflower + Phoenix feather) — +30% spell power 30min
- **Mandrake Healing** (Mandrake Root + Water) — Full HP restore

### Galilee blessed potions
- **Anointing Oil Vial** (Olive + Hyssop + Cedar) — Prayer regen 30min
- **Fig + Honey Tonic** (Fig + Honey) — HP+15, removes hunger debuff
- **Blessed Water** (Water + Lily + Hyssop) — Cleanse all debuffs

---

## 6. Total Art Asset Inventory

Counting everything we'd want eventually:

### Items
| Category | New items | Sprites each | Total |
|---|---:|---:|---:|
| Tier 1 vegetables (seed + crop + cooked) | 12 crops × 3 = 36 | 1 | 36 |
| Tier 2 crops | 10 × 3 = 30 | 1 | 30 |
| Tier 3 crops (orchard) | 10 × 3 = 30 | 1 | 30 |
| Tier 4 rare | 8 × 3 = 24 | 1 | 24 |
| Tier 5 Galilee | 7 × 3 = 21 | 1 | 21 |
| Flowers (common) | 7 | 1 | 7 |
| Flowers (magical) | 5 | 1 | 5 |
| Flowers (sacred) | 3 | 1 | 3 |
| Cooked dishes (tier 3) | 10 | 1 | 10 |
| Cooked dishes (tier 4) | 10 | 1 | 10 |
| Cooked dishes (tier 5) | 8 | 1 | 8 |
| Cooked dishes (tier 6+7) | 8 | 1 | 8 |
| Potion ingredients (new) | 15 | 1 | 15 |
| **Total item icons** |  |  | **~217** |

### Scenery (growing patches show plant state)
Per crop: 4 growth states (seedling / growing / ripening / harvest-ready)
- 50 crops × 4 states = **200 scenery sprites**

### Stack tiers (apply to stackable items — seeds, ingredients)
- Already authored: 6 coin tiers, 12 seed tiers
- Need: stack tiers for ingredients used in bulk (flour, salt, sugar, spices) — ~10 more × 4 tiers = **40**

### Grand total: ~457 sprites

---

## 7. Recommended Draw Order

Prioritize art that unlocks the **most recipes** first.

### Phase 1 — Universal staples (highest recipe coverage)
1. **Wheat → Flour → Dough → Bread** chain (4 sprites) — needed for pizza, pasta, sandwiches, ramen
2. **Cheese** (block + shredded) (2) — needed for pizza, tacos, lasagna, salads
3. **Meat varieties: chicken + beef + pork + fish** (4 raw + 4 cooked = 8) — most recipes need protein
4. **Eggs** (raw + cooked variants) (3)
5. **Tier 1 vegetables**: cabbage, lettuce, garlic, beans, peas, corn, carrots, cucumber, bell peppers — **12 crops × 3 sprites (seed/crop/cooked) = 36 sprites**

Phase 1 art: ~57 sprites. Unlocks ~80% of tier-3 and tier-4 recipes.

### Phase 2 — Mid-tier ingredients
6. Tier 2 crops (10 × 3 = 30 sprites)
7. Pasta variants (5: spaghetti, penne, lasagna sheets, ravioli, gnocchi)
8. Spice mixes (8 single-color icons: salt, pepper, paprika, cumin, curry, garam masala, etc.)

### Phase 3 — Recipe outputs (the cooked dishes themselves)
9. Tier 3 recipes — 10 dish icons
10. Tier 4 recipes — 10 dish icons

### Phase 4 — Orchard & rare
11. Tier 3 orchard fruits (10 × 3 = 30)
12. Tier 4 rare crops (8 × 3 = 24)

### Phase 5 — Flowers
13. Common flowers (7)
14. Magical flowers (5)

### Phase 6 — Tier 5 Galilee + Tier 6 legendary
15. Galilee crops (7 × 3 = 21)
16. Legendary dish icons (8)

### Phase 7 — Scenery (growing patches)
17. Patch growth states per crop (50 × 4 = 200) — biggest pile, do incrementally per crop

---

## 8. Engine Work Implied (NOT FOR ME — coder pass)

For the cooking + farming systems to scale:

1. **Recipe registry** — load `content/recipes/*.yaml` into a `CookingRecipeRegistry` at server boot, matching the existing skill content loader pattern (memory item 7).

2. **Ingredient inventory** — when player attempts to cook a recipe, validate all ingredients are present in correct quantities, consume them, produce the cooked item.

3. **HP heal extension** — current edible items have a single `heal_amount` field. Recipe outputs need this populated from recipe definition.

4. **Cooking station type** — `cooks_on: oven|firepit|stove|range` — different recipes require different stations. Allotment patches already exist; cooking stations are similar scenery additions.

5. **Burn risk** — if player's Cooking level < recipe's `burn_threshold`, produce a "Burnt X" item (which heals 0). Same pattern as existing burn risk in vanilla.

6. **"Feast" stack buff** — eating the same masterwork dish 3 times in a meal = +HP regen buff. New status effect type.

7. **"Galilee blessing" buff** — quest-locked, NPC interaction gives a buff that multiplies next masterwork dish heal ×1.5.

8. **Recipe discovery** — recipes start hidden; player learns them by:
   - Buying from chef NPCs
   - Quest rewards
   - Reading cookbook items (new item category)
   - Trial-and-error combine attempts (with XP rewards for novel discoveries)

---

## 9. Cultural Respect Note

OGRS's biblical worldview ([[project-ogrs]] memory item 20 "Project identity / lore direction") shapes the Galilee/Yahwist track but doesn't restrict other cuisines. World dishes are presented respectfully — Italian pizza is Italian, Indian curry is Indian, Mexican tacos are Mexican — using real names, not parody. The cultural diversity celebrates God's creation of varied peoples and cuisines; it doesn't replace the biblical track, it complements it.

Cultural dishes never reference other deities or sacred rituals of other religions. "Tea ceremony" is the food/skill aspect, not a Buddhist devotional act. "Royal Thai banquet" is the cuisine, not associated with any specific spiritual practice. If a real-world dish has religious origin/significance, we name and cook it without invoking that religion.
