## ILK Space Game — 100% Completion Checklist

This is the authoritative feature checklist to reach a complete, polished 1.0. Organized for planning, QA, and milestone tracking.

### Core Gameplay Systems
- [ ] Physical Knowledge end-to-end consistency
  - [ ] All world knowledge (threats, routes, prices, wars, contracts) discoverable only via physical channels (couriers, ships, rumors)
  - [ ] UIs show knowledge state with clear markers (Unknown/Rumor/Confirmed)
  - [ ] Player actions gated appropriately by knowledge state (routes, mission acceptance, scanning intel)
  - [ ] Knowledge decay/aging rules and spread dynamics tuned and documented
- [ ] Economy realism
  - [ ] Planet production/consumption curves tuned (no runaway or starvation in steady state)
  - [ ] Price elasticity and volatility well-calibrated (including rumor-induced variance)
  - [ ] Trade lanes emerge organically; congestion/piracy impacts prices and availability
  - [ ] Manufacturing chains balanced (inputs, outputs, timings, failure modes)
  - [ ] Escrow/payment loops airtight (no double crediting; refunds and insurance correct)
- [ ] Transport system
  - [ ] Multi-hop routing for AI cargo/messages/payments; detours around blockades
  - [ ] Threat-aware shipping cost/insurance pricing complete
  - [ ] Convoy logic (escorts, formations, rejoin on drift, retreat on damage) solid
  - [ ] Persistent contracts with lifecycle states and consequences (lost cargo, lost payment)
- [ ] Pirates & Intelligence
  - [ ] Target selection based on value, risk, recent intel
  - [ ] Intel sharing between pirate bases with range/age effects
  - [ ] Stolen cargo fencing economy (pirates affect regional stockpiles/prices)
  - [ ] Bounty creation and resolution wired to pirate activity
- [ ] Factions & Military
  - [ ] Patrols/escorts/blockades react to threat/war dynamically
  - [ ] Reputation/heat systems produce believable access/fees/response times
  - [ ] War declaration pipeline (letters) triggers long-term military changes
  - [ ] Escorts pricing/availability scale with local threat and reputation

### Player Experience / UX
- [ ] UI/UX
  - [ ] One-panel-at-a-time with `UIManager` across all screens
  - [ ] Proximity-gated town interactions with hysteresis (no flicker)
  - [ ] Map UI: larger news feed, clear route knowledge indicators, contract goals
  - [ ] Trading UI: local news, contracts, rumor/confirmed badges; stock/status clarity
  - [ ] Mission UI: knowledge-gated listings and acceptance; helpful tips when gated
  - [ ] Tips HUD: contextual guidance triggered from gating events and key actions
  - [ ] Controller bindings, keybind remap, and minimal accessibility options
- [ ] Onboarding
  - [ ] Short tutorial sequence (flight, landing, trading, missions)
  - [ ] “How Physical Knowledge works” explainer with examples
  - [ ] Tooltips for core terms: rumor, confirmed, escrow, blockade, heat

### World / Content
- [ ] Procedural generation
  - [ ] Unique towns per planet with consistent core buildings
  - [ ] Procedural ship kitbash pass (variants by faction/role)
  - [ ] Planet variety pass (biomes, orbits, light/sky tweaks)
- [ ] NPCs
  - [ ] Purposeful movement and roles (trader, guard, worker) with LOD
  - [ ] Occasional ambient interactions affecting demand or security
  - [ ] Conversation stubs for tips/rumors (physical knowledge hooks)

### Ships / Systems / Combat
- [ ] Component-based ship health and upgrades
  - [ ] Consistent damage model across player/AI; effects on performance/fuel
  - [ ] Emergency repair flows and restrictions enforced (hull critical)
- [ ] Combat
  - [ ] Weapon/shield balance; damage numbers feel good
  - [ ] AI threat response: engage/flee/escort reliably without node errors
  - [ ] Visual effects (hit flashes, lasers) with LOD and pooling
- [ ] Autopilot / Navigation
  - [ ] Waypoint visuals (beacons), route display, cancellation, and resume
  - [ ] Route discovery tied to knowledge; caching and invalidation rules

### Persistence / Stability / Performance
- [ ] Save/Load
  - [ ] All relevant state persisted (player, planets, ships, contracts, comms, escorts, routes)
  - [ ] Versioned saves, backward-compat check, graceful migration hooks
  - [ ] Autosave cadence configurable; rolling slots confirmed
- [ ] Stability
  - [ ] No mid-frame entity destruction assertions; removal deferrals standardized
  - [ ] Defensive checks for all NodePath accesses and scene transitions
- [ ] Performance
  - [ ] LOD rules for NPCs/ships/towns tuned; update throttling thresholds finalized
  - [ ] Object pooling for common VFX and guidance beacons
  - [ ] Profiling sessions with target framerate metrics documented

### Headless / Testing / CI
- [ ] Headless testing
  - [ ] Stability test suite green (GAME_TEST_MODE=1)
  - [ ] Economic simulations (30/60/120-day) with acceptable bounds
  - [ ] Scenario tests: blockades, pirate spikes, rumor floods, war declarations
- [ ] Automated regression
  - [ ] GitHub Actions workflow running headless tests on push/PR
  - [ ] Artifacts/logs retained; flaky test detection
- [ ] Debug/telemetry tools
  - [ ] Toggleable concise logging and tag filtering; perf counters
  - [ ] In-game debug overlays for knowledge/threat/route states

### Law / Heat / Scanning
- [ ] Law enforcement
  - [ ] Strict ports contraband scans tuned; fines/confiscation flows complete
  - [ ] Heat decay and thresholds influence inspections and access
  - [ ] Faction-specific contraband lists and responses
- [ ] Scanning
  - [ ] Active scan mechanic to confirm rumors/routes (time/risk/fee)
  - [ ] Scan results feed into knowledge as Confirmed intel

### Dynamic Contracts / Missions
- [ ] Mission breadth and depth
  - [ ] Cargo deliveries (timed/untimed) with physical contract tracking
  - [ ] Bounty hunts driven by real pirate activity; payouts fair
  - [ ] Blockade running/escort contracts scale by threat and war status
  - [ ] Exploration missions validate unknown coordinates; risk/reward pass
  - [ ] Abandon/penalty rules and edge-case handling
- [ ] Contract generation inputs
  - [ ] Pull from live shortages, threats, and faction agendas
  - [ ] Decay/refresh rates to maintain a healthy board

### Visuals / Audio / Polish
- [ ] Visual fidelity
  - [ ] LOD models for ships/towns; faction color accents
  - [ ] Simple skybox/lighting passes; navigation readability at distance
  - [ ] Impact VFX/SFX tuned to weapon class and material
- [ ] Audio
  - [ ] UI/mission/alert SFX; ambient loops for space/towns
  - [ ] Minimal music cues for events (landing, takeoff, combat start/end)
- [ ] Accessibility & Settings
  - [ ] Volume sliders, colorblind-friendly badges, text size
  - [ ] Key remapping; input help overlay

### Documentation / Distribution
- [ ] Docs
  - [ ] Player manual (controls, systems, knowledge model)
  - [ ] Technical docs (save schema, headless usage, mod hooks)
  - [ ] CONTRIBUTING.md (coding style, test strategy)
- [ ] Packaging
  - [ ] Requirements pinned; reproducible setup
  - [ ] Release builds (tagged) with changelogs
  - [ ] Itch/Steam-ready build scripts (optional)

### Nice-to-Have (Post-1.0)
- [ ] Crew skills and training affecting repairs/combat/trade
- [ ] Courier factions specializing in intel delivery
- [ ] Player-owned outposts/warehouses affecting logistics
- [ ] Multiplayer/async shared news network (opt-in)

---

Owner: This checklist lives at `ROADMAP_COMPLETION_CHECKLIST.md` (repo root). Update as features move to Done.


