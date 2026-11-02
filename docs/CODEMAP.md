# TLRA Code Map

Read-only map of the `.script` files in The Long Road Ahead (v2.3.1). Built from `grep -n` over the source at commit `5fc4868`. Line numbers refer to that commit. Regenerate after edits; line numbers drift.

Files covered:

| File | Lines | Role |
|---|---|---|
| `00 - Core/gamedata/scripts/zzzz_the_long_road_ahead.script` | 4458 | Core engine: routing, travel state machine, encounters, survival, companions |
| `00 - Core/gamedata/scripts/ui_tlra_travel_map.script` | 1617 | Expedition map UI (`UIRoadAheadTravelMap`) and encounter modal |
| `00 - Core/gamedata/scripts/zzz_tlra_mcm.script` | 51 | MCM options page (`on_mcm_load`) |
| `01 - Fair Fast Travel Patch/gamedata/scripts/zzz_tlra_fft_patch.script` | 37 | Bridge from Fair Fast Travel (FFT) into TLRA |
| `02 - New levels Patch/gamedata/scripts/zzz_tlra_levels_patch.script` | 75 | Injects custom levels into the static zone map and keywords |

Conventions:
- "Hook" means an engine callback registered with `RegisterScriptCallback`, or a UI `AddCallback` binding.
- "MCM key" is read through `get_config(key)`, which calls `ui_mcm.get("tlra/" .. key)`.
- `on_game_start` is called by the engine, not registered. It is listed under the callback table in the core file.

---

## 1. Core script: `zzzz_the_long_road_ahead.script`

### 1.1 Routing (level graph, paths, doors)

| Line | Function | Purpose |
|---|---|---|
| 167 | `safe_create_item` | Spawns an item from a section if it exists, guarded by `db.actor`. |
| 180 | `is_trader_restrictor` | Filters trader-related restrictors so they don't match as level changers. |
| 192 | `build_level_names_registry` | Builds the level id to name registry, once. |
| 271 | `resolve_level_name` | Normalizes a level id or name to a canonical level name. |
| 363 | `build_dynamic_map` | Scans level changers, space restrictors and extra transitions to build the dynamic routing map. Called from `actor_on_first_update`. |
| 869 | `get_level_road_nodes` | Builds the road graph for one level from curated splines and smart-terrain anchors. |
| 995 | `find_road_path` | A* search over the road graph, followed by Laplacian smoothing. |
| 1105 | `build_cross_zone_route` | Stitches per-level road paths into one multi-level route. |
| 1225 | `get_safe_lvid_pos` | Returns a safe level vertex for a given ratio along the route. |
| 1288 | `build_navmesh_dots` | Produces waypoint "dots" along the road path. Falls back to a sinusoidal trail when A* fails. |
| 1770 | `find_zone_path` | Zone-level path search. Tries the dynamic transitions first, then the merged static map. |
| 1759 | `is_zone_blocked` | Blocks northern zones until the Bar radar quest info is set. |
| 1834 | `snap_door_pos` | Projects a level-changer position 3 m inward onto walkable navmesh. |
| 1883 | `get_graph_edge_gvids` | Collects game-vertex ids of level changers that lead to a target level. |
| 1938 | `find_door_to_legacy` | Older door search by graph edges and keywords. Kept as a fallback. |
| 2031 | `find_door_to` | Current door search. Runs registry, graph-edge, keyword and brute-force stages, then sorts candidates. |

### 1.2 Threat detection and encounters

| Line | Function | Purpose |
|---|---|---|
| 3718 | `detect_ambush` | Checks SIMBOARD squads and online objects along the virtual route against the traveler's position. Applies the stealth roll (see 1.3). |
| 4126 | `trigger_encounter` | Starts an ambush. Online encounters are handled locally, offline ones teleport the squad into a battle level. |
| 3457 | (inside `actor_on_update`) | Ambush tech: builds the virtual position and calls `detect_ambush`. |
| 627 | `is_pos_safe_from_anomalies` | Returns false if an anomaly object lies within the given radius (default 4.5). |
| 643 | `get_safe_pos` | Snaps a position to a valid level vertex, falling back to the actor position. |

### 1.3 Stealth

Stealth is not a separate module. It sits inside the encounter roll and the config.

| Line | Function | Purpose |
|---|---|---|
| 3718 | `detect_ambush` | Rolls the evade chance. Includes the legacy automatic roll used when the map is disabled (around line 3939). |
| 3987 | `get_random_variance` | Random multiplier between `min_pct` and `max_pct`, used for stealth variance. |
| 1701 | `refresh_active_config` | Copies the stealth keys into `tlra.active_config` (see section 3). |

### 1.4 Survival and costs

| Line | Function | Purpose |
|---|---|---|
| 2317 | `get_diet_calories` | Reads nutrient values from `diet_system` for display and hunger math. |
| 3991 | `apply_diet_system_hunger` | Applies hunger through the diet system. Returns false when diet system is absent. |
| 4028 | `apply_final_stats` | Applies time-based costs (hunger, thirst, sleep) for skipped time. Run on arrival and abort. |
| 3704 | `process_refund` | Refunds the unused part of the upfront journey cost on abort. |
| 3179 | `get_real_max_weight` | Reads the actor's max carry weight, used by weight impact. |
| 2233 | `advance_travel_time` | Advances the game clock in proportion to the journey ratio. |
| 3325 | (inside `actor_on_update`) | Speed modifiers from environment and physical state. |
| 3433 | (inside `actor_on_update`) | Weather impact on travel speed. |

### 1.5 Travel state machine (start, tick, arrive, abort, persist)

| Line | Function | Purpose |
|---|---|---|
| 2330 | `start_travel_sequence` | Entry point. Checks survival and FFT conditions, charges cost, builds dots and route, and opens the map. Called by the FFT patch and the map spot menu. |
| 3219 | `actor_on_update` | Main tick. Runs safety stat wipe, throttled surge checks, weapon-visibility guard, road events, positive events, weather, and encounter checks. |
| 3544 | `complete_travel_sequence` | Arrival handling. Closes the map, sets the 60 s safety window, teleports companions and the actor, and runs the final arrival summary. |
| 3078 | `abort_travel_safe` | Aborts a journey, processes the refund and resets state. |
| 4069 | `stop_travel_logic` | Stops the journey and closes the map. Weapon restore is left to the arrival/abort events. |
| 1395 | `tlra_save` | Persists the traveling flag and destination via `save_var`. |
| 1602 | `tlra_load` | Restores persisted travel state on load. |
| 1538 | `tlra_clear` | Clears persisted travel state. |
| 1436 | `tlra_restore_weapons` | Clears engine input locks, unlowers the weapon and re-equips the best valid slot. |
| 1509 | `schedule_arrival_weapon_unlock` | Multi-pulse weapon unlock at 0, 0.15, 0.45 and 1.2 s after arrival. |
| 2617 | `force_end_surge` | Ends an active GAMMA surge with `skip_surge()`. |
| 2641 | `prevent_post_jump_surges` | Stops a new surge from starting right after a clock jump. |
| 2663 | `check_and_skip_surges` | Skips surges while traveling. Runs at most once per second. |
| 2677 | `set_safety_active` | Opens a timed safety window. |
| 2685 | `is_safety_active` | True while traveling or within the safety window. |
| 2690 | `actor_on_before_hit` | Zeroes incoming hit power while safety is active. |
| 4079 | `cleanup_dots` | Removes the map spots created for dots. |
| 4095 | `purge_orphan_dots` | Sweeps ids 1 to 65534 and removes dot spots left by an earlier session. |
| 3532 | `spawn_dot` | Creates the map spot for one dot. |
| 4126 | `trigger_encounter` | See 1.2. |
| 4242 | `safe_reset_animation` | Resets an NPC's animation through `sim_squad_scripted`, pcall-wrapped. |
| 3972 | `get_script_upvalue` | Reads a named upvalue from a function. Used to reach script internals. |

### 1.6 Companions

| Line | Function | Purpose |
|---|---|---|
| 4268 | `teleport_companions` | Teleports companion squads (axr_companions and Useful Idiots) in radial spacing around the actor. Skips hostages. A forced recall clears wait/cover/patrol behaviors. |
| 4242 | `safe_reset_animation` | See 1.5. |
| 3146 | `on_key_release` | Manual companion recall hotkey. The bind is read from FFT (see section 4). |

### 1.7 Config, lifecycle and callbacks

| Line | Function | Purpose |
|---|---|---|
| 154 | `tlra_log` | Debug logger, gated by `active_config.debug_logging`. |
| 559 | `tlra_str` | Looks up a localized string, falling back to the id. |
| 605 | `tlra_msg` | Shows a central message, falling back to a news tip. |
| 565 | `get_fft_journey_specs` | Reads journey cost and time from FFT for a map spot. |
| 617 | `lerp_pos` | Linear interpolation of two positions. |
| 828 | `to_vec2d` | Safe x/z extraction with pcall. |
| 847 | `dist2d` | Horizontal distance. |
| 855 | `to_vector` | Safe conversion to a vector. |
| 1668 | `get_config` | Reads `ui_mcm.get("tlra/" .. key)` under pcall. |
| 1701 | `refresh_active_config` | Builds `tlra.active_config` from the MCM keys. Runs on load and on option change. |
| 2697 | `on_game_start` | Engine-called. Hardens `ranks.get_se_obj_rank_name`, registers callbacks (table 1.8), and monkey-patches FFT (`bring_companions_to_actor`, guide pricing) and BHS (travel and sleep safety). |
| 2849 | `on_option_change` | Refreshes config. Hooked to `on_option_change` and `on_mcm_changed`. |
| 2854 | `on_loading_screen_dismissed` | Sets `tlra.player_ready = true`. |
| 2858 | `actor_on_first_update` | Builds the dynamic map. Resumes or arrives on a travel after level load. Clears the travel flag immediately to avoid load loops. Also runs the SafeSpawn check after arrival. |
| 3136 | `on_key_press` | Sets player_ready. Aborts an active journey on Backspace or Escape. |

### 1.8 Engine callback registrations (core file)

Registered in `on_game_start` (lines 2730–2739):

| Callback name | Handler | Line |
|---|---|---|
| `actor_on_update` | `actor_on_update` | 2730 |
| `actor_on_first_update` | `actor_on_first_update` | 2731 |
| `actor_on_before_hit` | `actor_on_before_hit` | 2732 |
| `on_key_press` | `on_key_press` | 2733 |
| `on_key_release` | `on_key_release` | 2734 |
| `on_loading_screen_dismissed` | `on_loading_screen_dismissed` | 2735 |
| `map_spot_menu_add_property` | `on_map_spot_menu_add_property` | 2736 |
| `map_spot_menu_property_clicked` | `on_map_spot_menu_property_clicked` | 2737 |
| `on_option_change` | `on_option_change` | 2738 |
| `on_mcm_changed` | `on_option_change` | 2739 |

### 1.9 UI hooks in the core file (map spot menu)

| Line | Function | Purpose |
|---|---|---|
| 2985 | `on_map_spot_menu_add_property` | Adds "Travel here (TLRA)" and, when FFT and the MCM toggle are on, "Hire guide (instant)". Accepts smart terrains (FFT-registered) and tagged spots. |
| 3054 | `on_map_spot_menu_property_clicked` | Handles the menu click and starts `start_travel_sequence`. |

---

## 2. UI script: `ui_tlra_travel_map.script`

Defines `UIRoadAheadTravelMap` (a `CUIScriptWnd` subclass) and the module-level helpers.

### 2.1 Geometry and map data

| Line | Function | Purpose |
|---|---|---|
| 263 | `get_level_bounds` | Level bounds from the maps ini, then level.ltx, then the static table. |
| 317 | `get_global_bounds` | Global Zone map canvas bounds. |
| 328 | `get_level_global_rect` | Level placement rectangle on the global Zone map. |
| 347 | `coord_to_global_uv` | Converts level-local coordinates to global 4096x8192 map pixels (u, v). |
| 373 | `init_zone_map_coordinates` | Pre-computes global UVs for every regional overlay. Runs at load. |

### 2.2 Window lifecycle and layout

| Line | Function | Purpose |
|---|---|---|
| 394 | `UIRoadAheadTravelMap:__init` | Constructs the window. |
| 418 | `UIRoadAheadTravelMap:AdjustZoom` | Applies a zoom delta. |
| 445 | `UIRoadAheadTravelMap:OnMouseScroll` | Routes a scroll event to `AdjustZoom`. |
| 453 | `UIRoadAheadTravelMap:__finalize` | Destructor. |
| 457 | `UIRoadAheadTravelMap:InitControls` | Builds the frame, map layers, footprints, pawn, dossier, telemetry, gauges, log and command panel. Runs to line 653. |
| 654 | `UIRoadAheadTravelMap:InitCallbacks` | Binds the encounter buttons (table 2.5). |
| 1521 | `UIRoadAheadTravelMap:Close` | Closes the window and cleans up. |
| 1551 | `is_open` | Module API. True while the map is open. |
| 1561 | `show_map` | Module API. Opens the map for a journey. |
| 1600 | `close_map` | Module API. Closes the map. |
| 1555 | `trigger_encounter` | Module API. Opens the encounter card. |

### 2.3 Journey and rendering

| Line | Function | Purpose |
|---|---|---|
| 724 | `UIRoadAheadTravelMap:StartJourney` | Sets up a journey, same-level or cross-zone. Builds waypoints, footsteps and the initial view. |
| 903 | `UIRoadAheadTravelMap:GetPositionAlongRoute` | Catmull-Rom interpolation along the waypoint polyline. |
| 951 | `UIRoadAheadTravelMap:BuildStampedFootsteps` | Places stamped footsteps along the route at about 18 UV spacing. |
| 1006 | `UIRoadAheadTravelMap:EnsureTrailCapacity` | Grows the footprint pool to fit the journey. |
| 1025 | `UIRoadAheadTravelMap:UpdateViewport` | Projects the zone map with aspect correction, draws regional overlays and places the pawn, markers and footsteps. |
| 1215 | `UIRoadAheadTravelMap:Update` | Per-frame update. Calls `ProcessUpdate`. |
| 1238 | `UIRoadAheadTravelMap:ProcessUpdate` | Reads core `tlra` state, updates position, clock, weather, vitals and log. |
| 1318 | `UIRoadAheadTravelMap:UpdateSurvivalVitals` | Refreshes survival gauges. |
| 1380 | `UIRoadAheadTravelMap:AddLog` | Appends a line to the expedition journal. |

### 2.4 Input

| Line | Function | Purpose |
|---|---|---|
| 1484 | `UIRoadAheadTravelMap:OnKeyboard` | Keyboard handler for the map. |
| 1584 | `on_mouse_wheel` | Global wheel handler. Forwards to the active map. |

### 2.5 Encounter card (threat decision)

| Line | Function | Purpose |
|---|---|---|
| 1396 | `UIRoadAheadTravelMap:PromptEncounter` | Shows the threat name, distance and evade chance, with the evade and engage callbacks. |
| 1432 | `UIRoadAheadTravelMap:OnAttemptEvade` | Evade button. Rolls the evade chance and calls the matching callback. |
| 1461 | `UIRoadAheadTravelMap:OnDropAndFight` | Engage button. Calls the engage callback. |
| 1477 | `UIRoadAheadTravelMap:OnHaltClicked` | Halt button. Pauses the journey. |

### 2.6 Engine callback registrations (UI file)

| Kind | Name | Handler | Line |
|---|---|---|---|
| `AddCallback` | `btn_halt`, BUTTON_CLICKED | `OnHaltClicked` | 655 |
| `AddCallback` | `btn_attempt_evade`, BUTTON_CLICKED | `OnAttemptEvade` | 656 |
| `AddCallback` | `btn_drop_and_fight`, BUTTON_CLICKED | `OnDropAndFight` | 657 |
| `RegisterScriptCallback` | `on_mouse_wheel` | `on_mouse_wheel` | 1597 (in `on_game_start`, line 1596) |

---

## 3. MCM options: `zzz_tlra_mcm.script`

| Line | Function | Purpose |
|---|---|---|
| 2 | `on_mcm_load` | Returns the MCM page with id `tlra`. Adds `enable_guide_travel` only when FFT and its patch are loaded. |

### 3.1 MCM keys declared

Declared in `zzz_tlra_mcm.script` lines 8–41:

| Key | Type | Default | Read by |
|---|---|---|---|
| `enabled` | check | true | `refresh_active_config`, `on_map_spot_menu_add_property` (2991) |
| `mode` | list | stalker | `refresh_active_config` |
| `travel_speed` | track | 25 | `refresh_active_config` |
| `time_factor` | track | 10 | `start_travel_sequence` (2503, direct) |
| `interruption_enabled` | check | true | `refresh_active_config` |
| `safe_zone_protection` | check | true | `refresh_active_config` |
| `arrival_offset` | track | 10 | `refresh_active_config`, `complete_travel_sequence` (3620) |
| `stealth_dodge_enabled` | check | true | `refresh_active_config` |
| `stealth_dodge_base` | track | 15 | `refresh_active_config` |
| `stealth_dodge_max` | track | 75 | `refresh_active_config` |
| `costs_enabled` | check | true | `refresh_active_config` |
| `stamina_drain_enabled` | check | true | `refresh_active_config` |
| `hunger_rate` | track | 0.5 | `refresh_active_config` |
| `thirst_rate` | track | 0.8 | `refresh_active_config` |
| `sleep_rate` | track | 0.9 | `refresh_active_config` |
| `animated_travel_map` | check | true | `start_travel_sequence` (2600, direct) |
| `map_dots` | track | 12 | `refresh_active_config` |
| `border_travel_only` | check | false | `refresh_active_config` |
| `weather_impact_enabled` | check | true | `refresh_active_config` |
| `weight_impact_enabled` | check | true | `refresh_active_config` |
| `show_stats` | check | true | `refresh_active_config` |
| `debug_logging` | check | false | `refresh_active_config` |
| `enable_guide_travel` | check | false | `refresh_active_config`, 3036, 3068 (only when FFT patch loaded) |

Read by the core file but not declared in the MCM:

- `cost_per_km`, read at line 1712 with fallback `or 500`.

Observation: the code fallbacks differ from the MCM defaults. For example, `hunger_rate` falls back to 0.1 at line 1713 while the MCM default is 0.5. The fallbacks only apply when `ui_mcm.get` returns nil.

---

## 4. Fair Fast Travel bridge: `01 - Fair Fast Travel Patch/.../zzz_tlra_fft_patch.script`

| Line | Function | Purpose |
|---|---|---|
| 5 | `on_game_start` | Registers `on_before_fast_travel`. |
| 9 | `on_before_fast_travel` | Intercepts an FFT trip. Passes guide trips through, otherwise calls `zzzz_the_long_road_ahead.start_travel_sequence` and sets `trip.cancel = true`. |

Hooks:

| Callback | Handler | Line |
|---|---|---|
| `on_before_fast_travel` | `on_before_fast_travel` | 6 |

Reads FFT keys, not TLRA keys: `trip.mode`, `trip.tt`, `trip.pos`/`trip.dpos`, `trip.level`. Writes `_G.tlra.force_instant_guide`.

Also reads `fftd/gen/squad_tp_bind` and `fftd/gen/squad_tp_mod` from the core file (lines 3154, 3160). These belong to FFT's MCM page.

---

## 5. Custom levels patch: `02 - New levels Patch/.../zzz_tlra_levels_patch.script`

| Line | Function | Purpose |
|---|---|---|
| 6 | `on_game_start` | Registers `actor_on_first_update`. |
| 10 | `actor_on_first_update` | Injects connections for promzona, grimwood, poselok_ug, bunker_a1 and collaider into `_G.tlra.STATIC_ZONE_MAP`. Adds reciprocal links to existing zones and keywords into `_G.tlra.DOOR_KEYWORDS`. Runs only if both tables exist. |

Hooks:

| Callback | Handler | Line |
|---|---|---|
| `actor_on_first_update` | `actor_on_first_update` | 7 |

No MCM keys.

---

## 6. Feature index

| Feature | Core functions | UI functions | Other |
|---|---|---|---|
| Routing | 169, 180, 192, 271, 363, 869, 995, 1105, 1225, 1288, 1759, 1770, 1834, 1883, 1938, 2031 | 263–373 (geometry) | Patch 02 (static map) |
| Threat detection | 627, 3718, 4126 | 1396, 1432, 1461, 1477 | — |
| Stealth | 3718 (roll), 3987, 1701 (keys) | — | MCM stealth keys |
| Survival | 2317, 3991, 4028, 3704, 3179, 2233 | 1318 | MCM rate keys |
| Companions | 4268, 4242, 3146 | — | FFT recall bind (`fftd/gen/squad_tp_bind`) |
| Travel state | 2330, 3219, 3544, 3078, 4069, 1395–1602, 1436, 1509, 2617–2690, 4079–4095, 3532 | 724–1380, 1521–1600 | — |
| UI and map spots | 2985, 3054 | all of 2.x | MCM page (`zzz_tlra_mcm`) |
| Config | 154, 559, 605, 1668, 1701, 2849, 2854 | — | MCM keys (section 3) |

---

## 7. Spot-check

Five entries were re-checked with `grep -n` against the source at this commit:

| Entry | Map says | Source |
|---|---|---|
| `safe_create_item` | 167 | `zzzz_the_long_road_ahead.script:167` (corrected from an earlier 169) |
| `get_config` | 1668 | `zzzz_the_long_road_ahead.script:1668` |
| `start_travel_sequence` | 2330 | `zzzz_the_long_road_ahead.script:2330` |
| `detect_ambush` | 3718 | `zzzz_the_long_road_ahead.script:3718` |
| `teleport_companions` | 4268 | `zzzz_the_long_road_ahead.script:4268` |
| `UIRoadAheadTravelMap:StartJourney` | 724 | `ui_tlra_travel_map.script:724` |

Callback registration lines (2730–2739 and UI 1597) were also checked against the grep output.
