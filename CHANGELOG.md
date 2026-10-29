# The Long Road Ahead - Changelog

## v2.3 — Dynamic Progression, Weight & Diet System Update

### ⏱️ Realistic Travel & Time Progression
- **Dynamic Duration Scaling**: Travel duration is no longer fixed at a rigid 2 minutes regardless of distance. Travel time dynamically scales based on actual world vector distance, character walking pace, time acceleration factors, and active survival conditions.
- **Distance & Route Awareness**: Long-distance journeys and multi-level legs accurately account for route length and character physical state.

### 🍗 Dynamic Survival Stats & Diet System Support
- **Dynamic Stat Drain**: Hunger, thirst, and fatigue now properly decrease and accumulate over the course of the journey based on the exact game-time elapsed.
- **Native Diet System Integration**: Full native hook into the **Diet System** mod—carbohydrates, fats, and protein reserves now deplete during travel alongside vanilla/GAMMA thirst (`actor_status_thirst`) and sleep (`actor_status_sleep`).
- **Reworked Travel Economy**: Removed illogical self-paid ruble charges for walking journeys—you now pay for the journey with physical calories, fatigue, and in-game time.

### 🎒 Inventory Weight & Over-Encumbrance Physics
- **Dynamic Carrying Capacity Detection**: Real maximum carrying capacity is dynamically calculated from equipment (suits, backpacks, belt artifacts, and active boosters).
- **Encumbrance Penalties**: Being encumbered or overweight significantly reduces travel speed and increases stamina/calorie consumption exponentially.

### 👥 Companion Squad Teleportation & Synchronization
- **Authoritative Manual Recall (`\` Key)**: Completely overhauled companion recall initiated via the `\` hotkey (or MCM-configured squad teleport key). Intercepts and replaces Fair Fast Travel's broken `bring_companions_to_actor` logic with TLRA's robust, authoritative multi-member teleport system.
- **Useful Idiots Stance & Behavior Bypass**: Manual recall (`forced = true`) deliberately bypasses Useful Idiots stance restrictions (`axr_companions.companion_squad_can_teleport`), allowing players to summon companions even if they are stuck in wait, cover, relax, or patrol mode across levels or switch distance, while safely preserving quest hostage protections.
- **Staggered Radial Distribution**: Teleported companions now calculate radial offset positions (1.8m–3.0m) around the player with AI level vertex validation, completely eliminating companion physics collisions, mesh stacking, and terrain clipping.
- **Offline & Cross-Level Alife Synchronization**: Safely teleports server entities via `sim:teleport_object`, invalidates stale offline caches (`db.offline_objects`, `db.spawned_vertex_by_id`), clears animation states (`safe_reset_animation`), and smoothly synchronizes client positions.
- **Status Notification**: Added clean, non-intrusive on-screen HUD message feedback indicating the number of companions successfully recalled.

### 🛠️ Bug Fixes & Diagnostics
- **Clean Logs**: Eliminated excessive log spam and removed redundant state flags.
- **Weapon Restoration**: Polished weapon restoration handlers upon journey completion or ambush interruptions.

---

## v2.2.2 — Russian Localization Update

### 🌐 Localization
- **Complete Russian Translation**: Added full Russian translation (`rus/st_tlra_mcm.xml`). All MCM settings, descriptions, in-game messages, road events, guide dialogue, stealth dodge results, and positive event messages are now fully translated.
- **Native Language Parity**: Russian players can install GAMMA/Anomaly with a Russian UI and experience all mod text in their language without manual edits.

---

## v2.2.1 — Localization Scoping Fix

### 💥 Critical Crash Fix
- **`tlra_str` Scope Order**: Fixed a fatal crash when right-clicking a map location to open travel options. The localization helper `tlra_str()` was declared as a `local function` after `get_fft_journey_specs()`, causing `attempt to call global 'tlra_str' (a nil value)`.
- **Declaration Order**: Moved the `tlra_str()` definition before `get_fft_journey_specs()`, guaranteeing valid scope across all callers.

---

## v2.2.0 — Arrival Offset Vector Crash Fix

### 💥 Critical Crash Fix
- **Method Look-up Fix**: Fixed a fatal crash affecting same-level travel when using Arrival Offset. Replaced invalid `dir:length()` engine call with manual 2D length calculation `math.sqrt(dir.x * dir.x + dir.z * dir.z)` matching X-Ray's Lua vector binding.
- **Seamless Behavior**: Preserved exact Arrival Offset functionality without engine instability.

---

## v2.1.9 — SafeSpawn, Arrival Offset & Immersion

### 🛡️ Safety & Spawn Mechanics
- **SafeSpawn Integration**: Added optional SafeSpawn mod support (`perform_silo`) on same-level and cross-level arrivals to clear immediate nearby enemies before fade-in completes.
- **Arrival Offset**: Added new MCM setting (default: 10m) to spawn slightly before the destination marker instead of directly on top of it, avoiding hostile smart terrain ambushes. Set to 0 to spawn exactly at destination.
- **Extended Safety Window**: Increased arrival weapon restore delay from 0.5s to 2.0s, and guarded `safety_reset` to prevent vulnerability windows after teleportation.

### 🗺️ Fast Travel & Markers
- **Campfire & Backpack Travel Restored**: Map spot validation now accepts any destination with a `fast_travel` tag (not just `smart_terrain`), restoring fast travel to campfires and stashes with Fair Fast Travel installed.
- **Externalized String Table**: Externalized all 60 hardcoded English strings to `st_tlra_mcm.xml` using `game.translate_string()` with graceful fallback.

---

## v2.0.9 — Dynamic Sneaking, PDA Holster & QoL

### 🥷 Stealth Mechanics
- **Dynamic Encounter Sneaking**: Added dynamic stealth system allowing players a chance to slip past detected threats during travel, scaling based on character rank, nighttime darkness, and bad weather (fog/rain/storms). Fully customizable sliders added to MCM.

### 📟 Interface & Engine Transitions
- **PDA Auto-Holster**: Automatically closes the 3D PDA device UI and equips Slot 2 primary weapon upon travel completion, voluntary abort, or roadside encounter.
- **Loading Screen Prompt Fix**: Forcefully closes the PDA map screen (`HideDialog()`) prior to level changer restrictors, allowing the engine's "Press SPACE to enter the Zone" prompt to display properly. Reopens the PDA screen automatically upon entering the new level.
- **Bulletproof Pathfinding**: Purged phantom static connection links and upgraded the BFS pathfinder to prioritize 100% physically accurate dynamic transition maps.
- **Fair Fast Travel Crash Fix**: Added nil-safety guards and local speed-based fallback calculator to resolve crashes on older Fair Fast Travel versions where `distance_to_duration` was undefined.
- **Fallback Door Scanner**: Added fallback checks for invisible transition zones, completely restoring Red Forest, Limansk, and Jupiter routing chains.
- **Delayed Weapon Swap**: Function `tlra_restore_weapons` only equips slot 2 if hands are completely empty, preventing interruption when players swap to pistols or shotguns in combat.

---

## v2.0.2 — Multi-Zone Routing Fix

### 🛠️ Multi-Zone Navigation
- **Multi-Zone Travel Chains**: Fixed bug where journeys spanning 3+ zones broke after the first level transition due to `final_pos` save drift.
- **Min-Distance Bypass**: Transition-resumed journeys now bypass the 40m minimum distance check, preventing false "Destination is too close" aborts on the final leg.
- **Diagnostic Logging**: Added diagnostic logging at every multi-hop decision point (BFS path, door selection, save source, resume state).

---

## v1.7.0 – v1.7.2 — ModDB Release & Stability

- **MCM Polish**: Added detailed tooltips (`_desc`) for all settings.
- **Debug Toggle**: Added "Debug Logging" toggle (Off by default) to keep player logs clean.
- **API Optimization**: Refined weight check logic to prioritize `get_max_weight`.
- **FFT Namespace Isolation**: Fixed FFT namespace conflicts (`_G.tlra`).
- **Resume Logic**: Journeys correctly recalculate from current actor position upon level load, preventing "zone skipping."

---

## v1.6.1 — The Ground Fix

- **LVID Spawning**: Switched from coordinate interpolation to strict AI Node (LVID) snapping.
- **Sky-Drop**: Added a 1.5m vertical offset to all spawns to force physics engine collision registration.
- **ALife De-stressing**: Increased stabilization delay to 1.0s to prevent crashes during teleportation.

---

## v1.5.0 – v1.5.9 — The Ambush & Survival Update

- **Ambush Tech**: Replaced random encounters with real-time ALife threat scanner.
- **Percentage Refunds**: Implemented percentage-based RU refunds for aborted journeys.
- **Dynamic Faction Checks**: Added level-awareness and dynamic faction relation checks to threat detection.
- **Start Buffer**: Added 50m safe zone at journey start to prevent instant interruptions.
- **Arrival Injection**: Implemented the "Arrival Injection" system for hunger, thirst, and sleep impacts.
- **Simplified Routing**: Switched to name-based level transition matching.

---

## v1.0.0 – v1.4.0 — Foundations

- **Core Engine**: Initial release of continuous travel loop and A* pathfinding.
- **FFT Compatibility**: Basic integration with Fair Fast Travel costs.
- **MCM Menu**: Initial implementation of the user settings interface.
