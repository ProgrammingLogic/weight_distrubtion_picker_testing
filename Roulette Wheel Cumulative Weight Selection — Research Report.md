# Roulette Wheel / Cumulative Weight Selection — Research Report

_Applied Context: Godot + Randomized Prim's Algorithm for Procedural Map Generation_

---

## Resources

### Authoritative

1. [Fitness Proportionate Selection — Wikipedia](https://en.wikipedia.org/wiki/Fitness_proportionate_selection) → Encyclopedic overview of roulette wheel selection (a.k.a. fitness proportionate selection), including CDF construction, binary search optimization, alias method, and stochastic acceptance. Concrete pseudocode examples.
    
2. [Roulette-wheel selection via stochastic acceptance — Lipowski & Lipowska (arXiv:1109.3627)](https://arxiv.org/abs/1109.3627) → Peer-reviewed 2011 paper introducing an O(1) average-case alternative to classic linear/binary search roulette wheel. Mathematically rigorous — essential reading for performance-critical use.
    
3. [Reproducible Roulette Wheel Sampling for Message Passing Environments — Springer](https://link.springer.com/chapter/10.1007/978-3-319-93701-4_63) → Academic paper examining cumulative-sum RWS properties and how weight aggregation affects reproducibility. Relevant for understanding edge cases.
    
4. [The Alias Method for Sampling Discrete Distributions — Wyman (Springer/Ray Tracing Gems II)](https://link.springer.com/content/pdf/10.1007/978-1-4842-7185-8_21) → Textbook chapter formalizing Vose's Alias Method — the O(1) gold standard for repeated weighted sampling. Highly recommended if your frontier changes rarely but you sample from it frequently.
    
5. [Wheel Selection Overview — ScienceDirect Topics](https://www.sciencedirect.com/topics/computer-science/wheel-selection) → Academic reference covering scaled fitness, cumulative fitness probabilities, and comparison to proportional selection within the broader context of genetic algorithms.
    
6. [Random Pick with Weight — Vultr Docs](https://docs.vultr.com/problem-set/random-pick-with-weight) → Practical algorithm reference (LeetCode 528) explaining prefix-sum CDF construction and binary search index lookup with full C++ implementation.
    
7. [Weighted Random Selection Algorithm — Educative.io](https://www.educative.io/answers/what-is-the-weighted-random-selection-algorithm) → Concise O(n) preprocessing / O(log n) lookup explanation with complexity analysis.
    
8. [Prim's Algorithm for Procedural Map Generation — KSU Wiki](https://people.cs.ksu.edu/~ashley78/wiki.ashleycoleman.me/index.php/Prim's_Algorithm.html) → Detailed breakdown of randomized Prim's, frontier tracking, and how the algorithm selects from a frontier. Directly relevant to the map generation use case.
    
9. [Maze Generation with Prim's Algorithm — Maze Complexity (DiVA / BSc Thesis)](https://www.diva-portal.org/smash/get/diva2:1237178/FULLTEXT02) → Academic undergraduate thesis comparing Prim's, RecBack, and RecDiv maze algorithms, analyzing complexity characteristics.
    
10. [Procedural Map Generation Techniques Notes — Christian Mills](https://christianjmills.com/posts/procedural-map-generation-techniques-notes/) → Structured notes from Herbert Wolverson's roguelike map generation talk; covers Prim's, BSP, drunkard walk, Voronoi, and more.
    
11. [Polygonal Map Generation for Games — Amit Patel (Red Blob Games / Stanford)](http://www-cs-students.stanford.edu/~amitp/game-programming/polygon-map-generation/) → Deep canonical reference on PCG map generation using graph structures, elevation redistribution, and CDF-based redistribution of values — directly applicable to biasing cell selection.
    
12. [Godot Engine — Random Number Generation Docs](https://docs.godotengine.org/en/stable/tutorials/math/random_number_generation.html) → Official Godot documentation on `randf()`, `RandomNumberGenerator`, seeding, and random element selection from arrays/dictionaries.
    
13. [Weighted Random Selection With Godot — Kehom's Forge](http://kehomsforge.com/tutorials/single/weighted-random-selection-godot/) → Godot-specific GDScript tutorial implementing accumulated weight selection with `acc_weight` fields on dictionary entries.
    
14. [Add `rand_weighted` method — Godot Engine GitHub PR #88883](https://github.com/godotengine/godot/pull/88883) → Engine-level PR discussion proposing a native `pick_weighted_random()` for `Array`. Useful for understanding what Godot natively offers (and gaps to fill manually).
    
15. [WeightedChoice Godot 4 Plugin — GitHub (rehhouari)](https://github.com/rehhouari/WeightedChoice) → Godot 4 plugin providing `WeightedChoice.pick(dict, weight_key)` — directly picks from a dictionary by weight, matching your frontier hash table structure.
    
16. [Roulette Wheel Selection — Cratecode](https://cratecode.com/info/roulette-wheel-selection) → Approachable step-by-step explanation of relative fitness normalization and cumulative probability construction, with Python code.
    
17. [Roulette Wheel Selection — Justin Skycak](https://justinmath.com/roulette-wheel-selection/) → Clean mathematical walkthrough of turning a discrete weight distribution into a CDF and sampling it. Part of an algorithms/ML book series.
    

---

### Non-Authoritative

1. [Understanding the Weighted Random Algorithm — DEV Community](https://dev.to/jacktt/understanding-the-weighted-random-algorithm-581p) → Accessible blog post with TypeScript implementation using the cursor-subtraction approach.
    
2. [How to: Weighted Random Selections — LootLocker Blog](https://lootlocker.com/blog/random-with-weights) → Game-industry blog explaining the subtraction-loop method (not CDF-based), written for loot table use cases but conceptually identical.
    
3. [Weighted Random Numbers — Stack Overflow (via newbedev)](https://newbedev.com/weighted-random-numbers) → Community discussion with pseudocode for both the linear scan approach and the stored cumulative weight + binary search optimization.
    
4. [Weighted Random — Zhanliang Liu Blog](https://zliu.org/post/weighted-random/) → Blog post comparing three implementations of weighted random in Go: flat list, linear-scan CDF, and binary-search CDF. Good for understanding progressive optimization.
    
5. [Vose-Alias-Method GitHub (Tecnarca)](https://github.com/Tecnarca/Vose-Alias-Method) → Open-source C implementation of Vose's Alias Method with a clear README explaining O(1) extraction complexity.
    
6. [Prim Algorithm for Mazes — SlideShare](https://www.slideshare.net/slideshow/algoritmo-de-prim-para-la-implementacin-de-laberintos-aleatorios-en-videojuegos/31834012) → Slide-deck summary of using Prim's for random maze generation in video games.
    
7. [ArneStenkrona/MazeFun — GitHub](https://github.com/ArneStenkrona/MazeFun) → Example Prim's maze implementation; clearly defines frontier cells, neighbor cells, and the connection step.
    
8. [Weighted Random Selection Optimizing — LiveCode Forums](https://www.forums.livecode.com/viewtopic.php?p=135821) → Forum thread demonstrating cumulative-sum + binary search implementation and community discussion of trade-offs.
    

---

## Information Compiled

### 1. What Is Roulette Wheel / Cumulative Weight Selection?

Roulette wheel selection (also called **fitness proportionate selection**) is a method for sampling from a discrete, non-uniform probability distribution. Each candidate item has an associated weight. Items with higher weights occupy proportionally larger "slices" of the probability space, so they are more likely to be chosen — but items with lower weights are never completely excluded.

The canonical analogy: imagine a physical roulette wheel where each cell on your frontier occupies a wedge proportional to its weight. Spin the wheel (pick a random number), see where it lands.

**Core mathematical definition:**

Given N items each with weight `w_i`, the selection probability of item `i` is:

```
p_i = w_i / sum(w_1 .. w_N)
```

---

### 2. The Standard Implementation (CDF / Prefix Sum Approach)

This is the version you are almost certainly using or should use for your Prim's frontier:

**Step 1 — Build cumulative weight array**

```
total = 0
for each (cell, weight) in frontier:
    total += weight
    cumulative_weights.append(total)
```

**Step 2 — Sample**

```
r = randf() * total           # random float in [0, total)
for i in range(len(cumulative_weights)):
    if r <= cumulative_weights[i]:
        return frontier_cells[i]
```

Or equivalently, using the **subtraction/cursor** method (equivalent, no separate CDF array needed):

```
r = randf() * total_weight
for each (cell, weight) in frontier:
    r -= weight
    if r <= 0:
        return cell
```

Both approaches are **O(N)** per selection. For a frontier that changes size frequently (as Prim's does — cells are added and removed each iteration), this is often acceptable and is the simplest correct implementation.

---

### 3. Optimizing to O(log N): Binary Search on the CDF

If your frontier is large, you can improve selection from O(N) to **O(log N)** by:

1. Storing the cumulative weight array sorted (it is always sorted since weights are positive).
2. Using a binary search (`lower_bound`) to find the first cumulative value ≥ the random number.

```gdscript
# GDScript conceptual sketch
var cumulative: Array = []
var total: float = 0.0

func build_cdf(frontier: Dictionary):
    cumulative.clear()
    total = 0.0
    for key in frontier:
        total += frontier[key]
        cumulative.append({"key": key, "cum": total})

func pick() -> Vector2i:
    var r = randf() * total
    var lo = 0; var hi = cumulative.size() - 1
    while lo < hi:
        var mid = (lo + hi) / 2
        if cumulative[mid].cum < r:
            lo = mid + 1
        else:
            hi = mid
    return cumulative[lo].key
```

**Trade-off:** The CDF must be rebuilt every time your frontier changes (each Prim's step adds new cells and removes one). Since your frontier changes on every iteration, binary search only pays off if the frontier is very large (hundreds+ cells).

---

### 4. O(1) Alternatives

**A. Vose's Alias Method** Preprocessing step of O(N) builds two tables (`probability[]` and `alias[]`). After that, each sample is O(1): pick a random index uniformly, then probabilistically pick the item or its alias. Best for static or rarely-changing distributions. Since Prim's frontier changes every step, rebuilding is expensive — only recommended if you batch many selections between frontier updates.

**B. Stochastic Acceptance (Lipowski & Lipowska, 2011)** No search, no CDF needed. Algorithm:

```
loop:
    pick a random item i uniformly from the frontier
    accept i with probability w_i / w_max
    if accepted: return i
```

This is **O(1) average** when weights are roughly uniform. If weights are highly heterogeneous (e.g. one cell has weight 1000, others have weight 1), many rejections occur and efficiency degrades. For a Prim's frontier where weights change based on, say, distance or terrain type, this can be a very simple implementation.

---

### 5. Applying This to Your Prim's Algorithm + Frontier Hash Table

Your structure: `frontier: Dictionary` where keys are `Vector2i` cells and values are float weights.

**How the combination works:**

1. **Initialize**: pick a random starting cell, mark it visited, add its unvisited neighbors to `frontier` with initial weights.
2. **Each iteration**:
    - Use cumulative weight selection to pick one cell `C` from `frontier` (higher weight = more likely to be expanded next).
    - Mark `C` as visited (part of the map/tree).
    - Remove `C` from `frontier`.
    - Find a visited neighbor of `C` and carve a passage between them (the Prim's "connection" step).
    - Add `C`'s unvisited, non-frontier neighbors to `frontier` with appropriate weights.
3. **Repeat** until `frontier` is empty.

**Weight semantics are yours to define.** Common approaches:

- **Uniform weights** → standard randomized Prim's (uniform random frontier cell selection).
- **Distance-based weights** → prefer cells farther from start (spreads the map outward).
- **Terrain-based weights** → prefer certain terrain types (creates biomes, paths of least resistance).
- **Proximity-based weights** → prefer cells near other visited cells (creates denser, more connected regions).

**Key insight from Red Blob Games (Amit Patel):** redistributing values to match a desired CDF is a "generally useful technique in procedural generation." You can shape the character of your map by shaping the weight distribution — not just by changing the algorithm structure.

---

### 6. Complexity Summary

|Method|Build Cost|Per-Sample Cost|Best For|
|---|---|---|---|
|Linear scan (cursor)|O(N)|O(N)|Small frontiers, simple code|
|CDF + binary search|O(N)|O(log N)|Large, infrequently-changing frontiers|
|Vose's Alias Method|O(N)|O(1)|Static distributions, many samples|
|Stochastic Acceptance|O(1)|O(1) avg|Roughly uniform weights|

For Prim's (frontier changes every step), **linear scan** is typically fine. If your map is very large, **binary search on a pre-built CDF** is the next step up.

---

### 7. Godot-Specific Implementation Notes

- Godot 4's `Array` has `pick_random()` for uniform selection. There is **no built-in weighted version** in the stable release as of 2025 (a PR, #88883, was proposed but its merge status is unclear — verify in the latest Godot 4.x docs).
- The **Kehom's Forge tutorial** (authoritative source above) shows an idiomatic GDScript pattern: store `acc_weight` (accumulated weight) alongside each item in the dictionary/array, rebuild on change, and scan linearly.
- The **WeightedChoice** Godot 4 plugin (`rehhouari/WeightedChoice`) directly accepts a Dictionary with weight keys and returns a weighted random key — matching your frontier structure exactly.
- Use `RandomNumberGenerator` with an explicit seed for reproducible map generation (same seed = same map). Set the seed once at map generation start.
- `randf_range(0.0, total_weight)` or `randf() * total_weight` both work correctly for the sampling step.

---

### 8. Points of Contradiction / Variation Between Sources

- **"Best" algorithm choice**: Academic sources (Lipowski, Wikipedia) highlight stochastic acceptance as O(1) and superior for changing populations. Practical game dev sources (Kehom, LootLocker) use the simple linear scan without concern — both are correct for different scales. For a Prim's frontier (typically tens to low hundreds of cells), the difference is immaterial.
- **Weight normalization**: Some sources normalize weights to sum to 1.0 before building the CDF (genetic algorithm convention). Others (Kehom, LootLocker, the subtraction method) work with raw integer or float weights directly without normalization. **Both produce the same statistical result.** Working with raw weights avoids a division pass and is simpler for a dynamic frontier.
- **Integer vs float weights**: LeetCode/competitive programming sources prefer integer weights with `randint(1, total)`. Game dev sources prefer float weights with `randf() * total`. Either works; float weights give you finer-grained control over probabilities when defining terrain biases.