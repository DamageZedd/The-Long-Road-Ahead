# The Long Road Ahead - Changelog

## v2.4.0 — Kingdom Come Animated Travel Map & Interactive Road Encounters

### 🗺️ Kingdom Come: Deliverance Style Animated Travel Map
- **Full-Screen Expedition Map Interface (`ui_tlra_travel_map`)**: Initiating travel now launches a full-screen expedition map viewport featuring genuine S.T.A.L.K.E.R. cartographic aesthetics, displaying high-resolution level maps for regional journeys and the global Zone map for cross-level transitions.
- **Wearable Devices-Style Auto-Centering on Player**: Completely overhauled map viewport rendering with Wearable Devices-style dynamic projection using `SetTextureRect`. The traveler arrow marker stays centered at the heart of the screen while both the Zone Global Map background and high-resolution level maps smoothly scroll underneath in real time. Eliminates squishing and aspect ratio distortion.
- **Dual-Layer Cartography (Global Map Background + Detail Level Map)**: Regional travel now renders high-resolution satellite detail maps directly atop the seamless Global Zone Map background, eliminating blank black voids and showing surrounding regional context.
- **Edge-to-Edge Pure Solid Black Canvas & Shader Blackout**: Added a dedicated uncompressed 32-bit ARGB black texture (`tlra_black.dds`) and activated the engine's full-screen post-processing blackout shader (`sleep_fade.ppe`), completely eliminating 3D world leaks at widescreen monitor edges and purging all icon atlas bleed from header and footer frames.
- **Dynamic Gold Border Hugging & Coordinate Mapping**: Frame borders and breadcrumb trajectory dots dynamically hug the actual map dimensions, ensuring start points, mission markers, and stalker pawns align 1:1 with real physical terrain, roads, and hills.
- **Animated Stalker Pawn & Dynamic Breadcrumb Trail**: A custom stalker traveler pawn smoothly traverses the map from your departure outpost to your destination along the calculated route in real time. Breadcrumb trail waypoints illuminate behind your pawn as progress is made, visually replicating *Kingdom Come: Deliverance*'s travel mechanics. Pawn arrow dynamically rotates to match your journey heading.
- **Trip Telemetry & Accelerated World Clock**: Digital header readout showcases the active journey route, real-time trip progress gauge (`%` and `meters remaining`), weather and environmental concealment ratings, and an accelerated world clock with real-time minute progression.
- **Live Survival & Metabolism Readout**: Real-time bottom telemetry tracks active calorie expenditure and metabolic burn rate (with native Diet System support), hydration level, stamina reserve, and current encumbrance weight and walking pace.
- **Ambient Roadside Expedition Log**: Scrolling dynamic roadside ticker provides atmospheric real-time narrative updates on terrain progress, weather changes, distance milestones, and distant Zone gunfire.

### ⚔️ Interactive Road Encounters & Stealth Evasion Decisions
- **Real-Time ALife Interception & Pawn Halt**: When moving hostile ALife simulation squads or mutant packs cross your travel path within threat range, the stalker pawn immediately halts and triggers an alarming tactical alert.
- **Kingdom Come Ambush Decision Modal**: Displays an interactive tactical decision card detailing the intersecting hostile faction or mutant pack, estimated range, and tactical cover modifiers (night darkness, storm/rain cover).
- **Interactive Stealth Evasion Choice**:
  - `[Attempt Evasion]`: Rolls an interactive sneak check based on player rank, nighttime darkness, storm/fog weather cover, and encumbrance. If successful, your stalker slips past the patrol under cover and resumes traveling along the map! If failed, an alarm sounds and you are forcefully dropped into terrain combat.
  - `[Drop Out & Fight]`: Instantly exits the map screen, drops the player and companion squad into the 3D world with weapons unholstered, and engages the hostile force.
- **Safe Journey Halt (`ESC` / Button)**: Players can safely halt their journey at any moment to cancel travel and drop to terrain at their current interpolated coordinate with validated AI node snapping.
- **Configurable in MCM**: Added `Animated Travel Map (KCD Style)` toggle to MCM settings (default `true`) allowing players to toggle between the animated map interface and classic background travel. Complete English and Russian localization included.

### 🛠️ Bug Fixes & Engine Stability
- **Definitive Weapon, Item & PDA Lockout Resolution**: Fixed the engine lockout where players were unable to equip weapons, use detectors, meds, or open their PDA after fast travel. Root cause traced to `game.only_allow_movekeys(true)` and engine `can_select_weapon` remaining engaged from animations/menus. Added explicit calls to `game.only_allow_movekeys(false)`, `game.can_select_weapon(true)`, `game.actor_lower_weapon(false)`, `game.stop_hud_motion()`, `db.storage[AC_ID].disable_input_time = nil`, and multi-tick unlock pulses across arrivals, border transitions, and safe aborts.
- **Purged Rogue Bump Texture**: Deleted accidental stray texture `02 - New levels Patch/gamedata/textures/crete/crete_walls_02_bump.dds` that caused concrete walls across multiple Zone levels to render with visual distortions.
- **Level Vertex Crash Fix (`valid_vertex_id`)**: Resolved fatal engine crash in companion teleportation logic (`attempt to call field 'valid_vertex_id' (a nil value)`) by enforcing valid level vertex boundary checks.

---

## v2.3.1 — Companion Manual Recall & Useful Idiots Stance Synchronization

### 👥 Companion Squad Recall & Stance Synchronization
- **Authoritative Manual Recall (`\` Key)**: Completely overhauled companion recall initiated via the `\` hotkey (or MCM-configured squad teleport key). Intercepts and replaces Fair Fast Travel's broken `bring_companions_to_actor` logic with TLRA's robust, authoritative multi-member teleport system.
- **Useful Idiots Stance & Behavior Bypass**: Manual recall (`forced = true`) deliberately bypasses Useful Idiots stance restrictions (`axr_companions.companion_squad_can_teleport`), allowing players to summon companions even if they are stuck in wait, cover, relax, or patrol mode across levels or switch distance, while safely preserving quest hostage protections.
- **Staggered Radial Distribution**: Teleported companions now calculate radial offset positions (1.8m–3.0m) around the player with AI level vertex validation, completely eliminating companion physics collisions, mesh stacking, and terrain clipping.
- **Offline & Cross-Level Alife Synchronization**: Safely teleports server entities via `sim:teleport_object`, invalidates stale offline caches (`db.offline_objects`, `db.spawned_vertex_by_id`), clears animation states (`safe_reset_animation`), and smoothly synchronizes client positions.
- **Standalone Hotkey Fallback**: Added standalone `on_key_release` listener with UI dialog focus checking and 800ms debounce protection so manual recall operates reliably even if Fair Fast Travel is uninstalled or disabled.
- **Status Notification**: Added clean, non-intrusive on-screen HUD message feedback indicating the number of companions successfully recalled.

---

## v2.3.0 — Dynamic Progression, Weight & Diet System Update

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

### 👥 Multi-Member Squad Synchronization
- **Modern Multi-Member Teleportation**: Companion squads cleanly transition across levels using `axr_companions.companion_squads` and `squad:squad_members()`.
- **Animation & Visual State Reset**: Resets NPC animations (`sim_squad_scripted.reset_animation`), synchronizes level vertex positions, and clears stale offline object state to prevent companions from getting stuck or desynced.

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
