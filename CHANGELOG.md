# The Long Road Ahead - Changelog

## v2.4.0 — Kingdom Come Animated Travel Map & Interactive Road Encounters

### 🗺️ Kingdom Come: Deliverance Style Animated Travel Map
- **Footprint Orientation & Dynamic Heading Alignment**: Fixed an issue where stamped footsteps were frozen facing North regardless of road curvature, or rotated incorrectly. In the X-Ray Monolith engine, CUIStatic elements require both heading="1" attributes in XML and script-level EnableHeading(true) for SetHeading rotations to take effect. Added heading="1" to all trail dot definitions in ui_tlra_travel_map.xml and explicitly invoked EnableHeading(true) upon control initialization and per-frame texture binding. Corrected the heading tangent calculation to math.atan2(-dx, -dz), aligning with the engine's counter-clockwise rotation convention so boot toes point precisely along the road heading in all directions.
- **Restored Tactical Level Maps & Seamless Regional Stitching**: Fixed an issue where tactical level maps (Bar, Rostok, Garbage, Cordon, etc.) disappeared, leaving only the bare satellite base map. Restored the multi-zone regional overlay engine (level_canvases) across all 23 Zone territories. Replaced manual texture scissoring with full-quad window positioning and scaling mapped to authentic engine global_rect coordinates, allowing level maps to render their complete geography with natural alpha feathered borders that blend smoothly into the satellite background without harsh rectangular clipping artifacts.
- **Anchored Stamped Footprints & Directional Heading Alignment**: Fixed an issue where the Kingdom Come combat bootprints were oriented sideways/perpendicular across roads and slid dynamically forward with the pawn like an escalator. Re-baked both left and right combat boot textures in 	lra_stalker_atlas.dds with authentic North-facing vertical alignment so SetHeading rotates toes forward directly along the line of travel. Replaced dynamic per-frame distance offsets with discrete, pre-calculated stamped footsteps along the route polyline at fixed ~18 UV stride intervals. As the traveler advances, footsteps are permanently stamped onto the map ground strictly behind the pawn figurine's pedestal, remaining anchored to their exact physical terrain coordinates as the camera scrolls and pans.
- **Full Seamless Zone Satellite Cartography & Cropped Quad Elimination**: Resolved an issue where regional level map overlays appeared as sharp, cropped rectangular boxes with visible cut-off boundaries against the background satellite terrain (e.g. sharp right-angle seams in Garbage and isolated square tiles in Rostok and Bar). Eliminated the scissored regional overlay quads in favor of the continuous 4096x8192 Zone master satellite map (	lra_map_global). The map now displays 100% full, seamless, edge-to-edge terrain across all 23 territories with zero rectangular seams, zero missing boundary strips, and perfect cross-zone highway continuity matching the authentic in-game PDA presentation.
- **Kingdom Come Style Carved Stalker Pawn & Walking Inked Bootprint Trail**: Scaled the hand-carved stalker pawn up to 64x64 on the map (`tlra_pawn_kcd`), bringing out the full tactile depth of the turned wooden counter pedestal, contact drop shadow, hooded canvas coat, gas mask, and slung hunting weapon. Completely overhauled the breadcrumb trail into a true *Kingdom Come: Deliverance* style footstep track: footsteps now strictly stamp **behind the player pawn** as you travel forward (zero dots ahead of the player). Each step is rendered with alternating left and right combat boot prints (`tlra_trail_boot_l` and `tlra_trail_boot_r`) scaled up to 24x24, offset laterally by $\pm 5$ pixels perpendicular to the road heading, and rotated to match the road tangent at that exact stride, forming a genuine human walking track behind the traveler.
- **PDA Multi-Zone Cartographic Stitching & Dynamic Regional Map Overlays**: Implemented authentic S.T.A.L.K.E.R. PDA-style multi-zone cartographic stitching on the animated travel map interface (`ui_tlra_travel_map`). All 23 regional surface level map textures (`tlra_map_escape`, `tlra_map_garbage`, `tlra_map_rostok`, `tlra_map_bar`, `tlra_map_military`, `tlra_map_yantar`, `tlra_map_deadcity`, `tlra_map_pripyat`, `tlra_map_zaton`, `tlra_map_jupiter`, `tlra_map_marsh`, `tlra_map_darkscape`, `tlra_map_k02_trucks_cemetery`, etc.) are declared as individual off-screen canvases within `ui_tlra_travel_map.xml` and dynamically positioned, scaled, and rendered directly on top of the continuous satellite base map (`tlra_map_global`). Each region's global footprint is derived from `game_maps_single.ltx`'s `global_rect` and converted to 4096x8192 global UV coordinates. Per-frame viewport projection computes exact screen scissor intersection and sub-rectangle texture sampling with automatic off-screen frustum culling. Adjacent territories (such as Cordon and Garbage, or Bar and Rostok) stitch seamlessly side-by-side, scale in 100% lockstep with mouse scroll wheel zoom, and blend naturally into the satellite terrain underneath.
- **PDA Dialog Stack Cleanup & Cursor Release Invariant**: Resolved an issue where the engine mouse cursor could linger over the screen after fast travel completed or was halted. Implemented defensive modal stack teardown that verifies and closes any underlying PDA menu instance (`ActorMenu.get_pda_menu():HideDialog()`) both before showing the travel map and during `Close()` / `close_map()`, guaranteeing the modal dialog stack is completely purged and first-person camera control is immediately restored.
- **Vector Luabind Operator Crash Fix in Cross-Zone Highway Graph**: Fixed a fatal engine Lua exception in `build_cross_zone_route` (`! No such operator [__eq] defined in class [vector]`) caused by using Lua's inequality operator (`~=`) directly on engine `vector` userdata instances when comparing route node endpoints. Replaced with Euclidean 2D distance thresholding (`dist2d(lvl_exit, lvl_entry) > 1.0`) and added fallback guards to guarantee robust waypoint generation across all cross-zone itineraries.
- **Unified Continuous Zone Cartography & Misplaced Overlay Elimination**: Fixed an issue where individual regional map overlays (specifically Wild Territory / `l06_rostok`) appeared as a static square misplaced over the top-left corner of the screen, and the background map was squished into a narrow column with vertical letterboxing artifacts. Completely eliminated the obsolete multi-canvas regional overlay loop and legacy single-zone dual rendering. All expeditions (both same-level local journeys and cross-zone treks) now run exclusively on the continuous 4096x8192 Zone master satellite map (`tlra_map_global`). Local waypoints and cross-zone highway waypoints are mapped directly to authentic global UV coordinates with calibrated bounding boxes for all 22 territories (including exact Bar and Wild Territory borders meeting seamlessly at `u = 1628`). The screen is permanently filled 100% edge-to-edge (1024x768) with full aspect-ratio preservation, fluid mouse wheel zoom, and zero floating tiles.
- **Full-Screen Continuous Map Geometry & Edge-to-Edge Fill**: Fixed an issue where the expedition map appeared as a narrow vertical strip in the center of the screen with black side voids, while a cropped level map remained frozen over the top-left corner. Eliminated the obsolete window-shrinking calculation on g_map_canvas and locked it to the full virtual screen (0, 0, 1024, 768) with dynamic UV viewport clamping across 	lra_map_global (4096x8192). In cross-zone expeditions, regional detail layers (map_canvas) are now strictly hidden, ensuring the global satellite terrain permanently fills 100% of the viewport edge-to-edge at all zoom levels without shrinking or black sidebars.
- **Cross-Zone Road Waypoint Stitching & Highway Navigation**: Fixed an issue where cross-zone journeys traveled along straight diagonal lines across mountains and anomalies rather than following realistic roads. Implemented uild_cross_zone_route which utilizes the zone pathfinding graph (ind_zone_path) to query ZONE_CURATED_ROADS across every intermediate and destination territory (Cordon, Garbage, Bar, Rostok, Dark Valley, etc.). Subdivided highway segments into dense ~25m nodes, bridged road intersections within 70m, and stitched entrance and exit transitions into a single unified global UV polyline. The animated stalker pawn and trail dots now follow the authentic curves of paved roads, asphalt highways, and security gates across the entire Zone.
- **Cursor Release & Modal Stack Resolution (HideDialog)**: Fixed an issue where the OS/engine mouse cursor remained stuck and visible over the first-person game camera after fast travel completed or was halted. Resolved by explicitly calling HideDialog() on the travel map window upon close (UIRoadAheadTravelMap:Close(), close_map(), complete_travel_sequence(), and bort_travel_safe()), properly popping the modal script dialog from the X-Ray UI input stack and immediately restoring mouse look control to first-person gameplay.
- **Global ALife Ambush Interception & Offline Level Transitions**: Overhauled threat detection (detect_ambush) to scan offline simulation squads across all maps along the expedition route via SIMBOARD.squads. When a hostile squad intercepts the road within 75m (evaluated in global UV coordinates on the active segment level), an interactive tactical ambush alert triggers regardless of whether the encounter is on the player's current map or an offline map ahead. If the player drops out to fight or evasion fails, the engine seamlessly executes ChangeLevel straight to the offline squad's position and level vertices with companion server entities synchronized, dropping the player right into the combat encounter in the new zone!
- **Jitter-Free Fluid Bilinear Texture Rendering**: Fixed severe sub-pixel screen vibration and high-frequency texture shuddering during travel. Replaced integer pixel snapping (math.floor/math.ceil) with continuous floating-point window coordinates, and implemented a quad-locking mechanism that freezes the map canvas window rect at (0, 0, 1024, 768) whenever the level map covers the screen. Bilinear DirectX texture filtering now handles sub-pixel panning seamlessly at 60, 120, and 144+ FPS without any screen stutter.
- **True Physical Meter Cartography & Tactical Framing**: Fixed incorrect zoom scaling and a 28.6% anamorphic horizontal distortion caused by squishing local level maps into the global 4096x8192 Zone UV canvas. Local expeditions now compute viewport bounds and scale directly in physical world meters (scale = FH / span_y_m), preserving authentic 1:1 level aspect ratios and framing the traveler in a crisp tactical close-up view (~400m to 1200m field of view) while allowing continuous mouse wheel zoom across the entire [0.20x, 10.0x] dynamic range.
- **Curated Multi-Branch Road Networks & Feeder Junction Graph**: Fixed an issue where expeditions ignored roads and plotted diagonal arcs across open wilderness (such as cutting across the grass from Rookie Village). Restructured ZONE_CURATED_ROADS across all levels into interconnected multi-branch chains (main highways, village feeder paths, car parks, and military checkpoints), auto-bridged intersections within 45m into bidirectional A* graph edges, and established engine level name alias mirrors (escape <-> l01_escape, garbage <-> l02_garbage, etc.). Travelers now realistically walk out of settlements, join paved highways, and follow genuine road corridors.
- **Instant Blackout Fade Fix & Resilient Travel Map Launch**: Resolved an issue where clicking fast travel caused the screen to briefly fade to black and immediately fade back into normal gameplay with no expedition map open. Completely removed the conflicting post-processing blackout effector (`sleep_fade.ppe`), eliminated PDA closing races, ensured same-level expeditions generate complete navmesh waypoint polylines, and restored modal UI registration under `ui_sleep_dialog`.
- **Solid Tactical HUD Alpha & High-Contrast Panel Legibility**: Explicitly configured high-opacity alpha channels (`a="240"` for tactical backdrops, `a="255"` for borders and progress meters) across all XML panels (`ui_tlra_travel_map.xml`), preventing engine zero-alpha transparency fallbacks and ensuring survival telemetry, accelerated clock, weather, and the field journal remain crisp, sharp, and easily legible over bright satellite terrain.
- **Fail-Safe UI Lifecycle Engine**: Wrapped per-frame travel map updates in a defensive `pcall` execution block to guarantee unexpected mathematical or engine telemetry hiccups never crash the UI or prematurely close the expedition screen.
- **Direct Continuous Cross-Zone Expeditions (Zero Mid-Journey Loading Screens)**: Overhauled cross-level travel to run as a single, uninterrupted expedition. The animated map GUI now tracks the player's trek seamlessly across the entire Zone from start to final destination, eliminating intermediate border loading screens that previously broke immersion. When travel completes (or is aborted/engaged), the engine executes an authoritative direct transition (ChangeLevel) straight to the destination coordinates with companions synchronized.
- **Dossier Tab XML Node Binding Fix**: Resolved an engine UI initialization crash (`XML node not found: top_left in ui\ui_tlra_travel_map.xml`) by strictly synchronizing the script initialization calls with the diegetic `<dossier_tab>` panel and sub-element definitions.
- **Simultaneous Multi-Level Regional Cartography Loading**: Overhauled map rendering architecture to load and render all 22 surface level map textures simultaneously on top of the continuous `tlra_map_global` satellite base layer. Rather than displaying only the active level or hiding regional cartography during cross-zone treks, every regional map (Cordon, Garbage, Agroprom, Dark Valley, Bar, Rostok, Army Warehouses, Yantar, Dead City, Radar, Pripyat, Chernobyl NPP, Swamps, Darkscape, Trucks Cemetery, Jupiter, Zaton, Red Forest, Limansk, and Hospital) is positioned at its exact `global_rect` footprint with per-frame off-screen culling and screen-edge scissor clipping. As the player travels or zooms out, adjacent territories are seamlessly visible with authentic high-resolution PDA detail.
- **Debounced Continuous Mouse Wheel Zoom & Expanded Dynamic Range**: Fixed an issue where scrolling the mouse wheel could freeze or clamp after ~1 second due to simultaneous un-debounced event listeners (engine `on_mouse_wheel` callback, `OnKeyboard` `DIK_MOUSEWHEELUP`/`DOWN`, and `OnMouseScroll`) rapidly hitting the zoom bounds. Implemented a 35ms timestamp debounce via `time_continual()`, corrected wheel direction handling, and expanded the zoom range to `[0.20x, 10.0x]` with smooth exponential steps (`* 1.12` / `* 0.89`), allowing players to smoothly inspect both the macro Zone overview and micro road-level details indefinitely.
- **Interactive Mouse Scroll Wheel Zoom**: Implemented mouse wheel zoom controls (OnMouseScroll, engine on_mouse_wheel callback, and DIK mouse wheel inputs) allowing players to smoothly zoom the expedition viewport in and out between 0.35x (wide regional/Zone overview) and 3.5x (tactical roadside detail). Viewport, cartography, markers, and breadcrumb waypoints scale dynamically in real time.
- **Full-Screen Diegetic S.T.A.L.K.E.R. Cartographic Overhaul (`ui_tlra_travel_map`)**: Transformed the expedition map interface into a diegetic S.T.A.L.K.E.R. tactical display where authentic regional cartography and the continuous Zone background map span the entire screen edge-to-edge (1024x768).
- **Dedicated S.T.A.L.K.E.R. Visual Texture Atlas (`tlra_stalker_atlas.dds`)**: Integrated a custom, uncompressed 32-bit ARGB texture atlas loaded via `tlra_maps.xml` introducing weathered military field artifacts:
  - **Top-Left Field Dossier / Clipboard Tab (`tlra_dossier_tab`)**: Weathered military document tab displaying dynamic expedition title, route trek distance, and safe stride pacing in dark military stencil ink.
  - **Top-Center Floating Tactical HUD**: Crisp typography floating directly over the map with accelerated world clock (`[10x SPEED]`), dynamic weather conditions, and live ALife threat risk alerts.
  - **Top-Right Antique Brass & Threat Progress Gauges**: Segmented golden expedition distance progress bar and dual-tone threat condition meter.
  - **Bottom-Left Floating Survival Telemetry**: Translucent dark military plate displaying real-time calories, hydration, stamina, pack weight, radiation dosing in mSv, and a dedicated teal/cyan psy-health meter.
  - **Bottom-Center S.T.A.L.K.E.R. Field Journal (`tlra_field_journal`)**: Authentic army field journal card with `S.T.A.L.K.E.R.` tab and dark inset CRT display rendering scrolling roadside reconnaissance events.
  - **Bottom-Right Industrial Rusted Steel Button (`tlra_btn_halt`)**: Heavy metal plate with corner rivets/screws for immediate safe journey abort (`HALT [ESC]`).
  - **Stalker Silhouette Traveler Pawn (`tlra_pawn_stalker`)**: Replaced generic pointer arrow with an authentic stalker silhouette carrying a rifle, dynamically walking along the trail.
  - **Glowing Amber Radiation Target Beacon (`tlra_beacon_radiation`)**: Luminous hazard beacon marking the destination objective.
  - **Dashed Yellow Road Breadcrumb Trail (`tlra_trail_dash`)**: Traversal waypoints rendered as authentic yellow road dashes curving along highways and paths.
- **Symmetrical 1024x768 Centered Framing**: Standardized UI root window to clean `1024x768` virtual coordinate space with uniform 32px margins, eliminating widescreen displacement, screen-edge clipping, and empty side voids.
- **Mathematical Dead-Center Player Anchoring**: The stalker traveler pawn marker is anchored dead-center within the 960x526 viewport at `(CX, CY) = (480, 263)`, with terrain and cartography smoothly scrolling underneath in real time.
- **Continuous Dual-Layer Cartography (Zone Global Map Background)**: Synchronously renders the complete Zone global map (`tlra_map_global`) behind the regional level map, eliminating black voids around level borders and showing continuous geographic context.
- **Level Road Network A* Pathfinding Engine**: Overhauled route plotting using S.T.A.L.K.E.R.'s authentic level game graph vertices (`game_graph()`) placed along actual asphalt roads, dirt tracks, railway crossings, and pedestrian footpaths. An optimized A* algorithm connects staging outposts to destination nodes along the true road network, completely eliminating cross-country diagonal shortcuts when realistic roads exist.
- **Catmull-Rom Cubic Spline Interpolation & Heading Continuity**: Upgraded pawn motion and viewport tracking to analytical Catmull-Rom cubic splines ($C^1$ continuity). The stalker arrow now glides smoothly through every waypoint curve with continuous tangent angular heading calculation ($\theta = \text{atan2}(P'_x, -P'_z)$), completely eliminating saw-tooth zig-zags, robotic corner snapping, and lateral wobbles.
- **Multi-Pass Laplacian Path Relaxation**: Filtered all route waypoints through a 2-pass Laplacian path relaxation pipeline that gently smooths sharp bends and snaps vertices directly to ground walkable navmesh coordinates (`level.vertex_position`).
- **Road-Biased Waypoint Polyline Navigation**: Traversal and breadcrumb trail waypoints no longer follow an unrealistic straight-line vector. The animated stalker pawn now traverses authentic road paths and walkable nav mesh vertices generated by `tlra.dot_positions` (identical to the PDA fast travel system), dynamically turning along roads and bends.
- **AAA Military Cartography & Tactical HUD Styling**: Overhauled interface aesthetic with layered dark slate armor plates, antique brass and gold divider lines, subtle military viewport reticles, high-contrast digital clocks, and illuminated telemetry meters via a dedicated pure white texture canvas (`tlra_white.dds`).
- **Three-Card Field Console**: Bottom console neatly organizes travel telemetry into three dedicated modular panels: Survival Metabolism (calories, hydration, stamina, pack weight, stride), Roadside Reconnaissance Log (scrolling dynamic timestamped event ticker), and Expedition Command (safe halt button).
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
- **Road Network Coordinate Normalization & Arithmetic Shield (dist2d)**: Fixed a fatal engine error (ttempt to perform arithmetic on field 'x' (a nil value) in zzzz_the_long_road_ahead.script:829: dist2d) triggered during road network graph generation. Curated road node definitions in ZONE_CURATED_ROADS store coordinates in array format ({ x, y, z }), while dynamic engine entities supply X-Ray ector userdata (p.x, p.y, p.z). Implemented polymorphic coordinate normalizers (	o_vec2d and 	o_vector) that safely unwrap numeric array indices, table fields, and engine userdata before distance calculation and node caching, eliminating nil arithmetic across both zzzz_the_long_road_ahead.script and ui_tlra_travel_map.script.
- **Guaranteed Mouse Cursor & Dual-Input Threat Encounter Hotkeys**: Fixed an issue where the mouse cursor lost window focus or failed to interact with encounter decision buttons after level loads. Purged the legacy background PDA reopening routine (
eopen_pda_dialog and Slot 8 equipping) that stole window focus, enforced unconditional level.enable_input() and :Enable(true) on modal buttons, and integrated full keyboard hotkey support ([E] / [1] to Attempt Evasion, [F] / [2] / [ENTER] / [SPACE] to Drop Out & Fight, and [ESC] to abort) directly onto the decision plates so travelers can never become trapped on the modal screen.
- **CCharacterInfo [(null)] Profile Assertion Shield (`ranks.get_se_obj_rank_name`)**: Fixed a fatal engine assertion in `CXML_IdToIndex<class CCharacterInfo>::GetById: item not found, id [(null)]` triggered when third-party scripts (such as `stealth_nvg.script`, `target_prior.script`, `zml_loot.script`) invoke `ranks.get_se_obj_rank_name(se_obj)` on stalkers with unassigned, stripped, or despawned character profiles during accelerated world time simulation. Wrapped `ranks.get_se_obj_rank_name` with pre-validation of profile string existence (`profile_name()`) and entity alife liveness checks before allowing C++ `obj:rank()` invocation, safely falling back to `"novice"` instead of crashing.
- **Actor Max Weight Crash Fix (get_max_walk_weight)**: Resolved crash in ui_tlra_travel_map.script where calling non-existent engine method get_max_walk_weight caused fatal script errors during telemetry updates. Now queries zzzz_the_long_road_ahead.get_real_max_weight() with robust fallbacks and defensive pcall checks across all actor survival telemetry.
- **Definitive Weapon, Item & PDA Lockout Resolution**: Fixed the engine lockout where players were unable to equip weapons, use detectors, meds, or open their PDA after fast travel (which previously required saving and reloading to clear). Root cause traced to `db.actor:restore_weapon()` being spammed without matching `hide_weapon()` calls, driving the X-Ray engine's internal `m_iDisableWeapon` counter negative into unsigned integer overflow (`4,294,967,295`), as well as the 3D PDA item (Slot 8) leaving hands busy when opening modal dialogs. Resolved by:
  - Immediately holstering hands (`db.actor:activate_slot(0)`) and closing PDA dialogs before launching the expedition map.
  - Purging all rogue calls to `db.actor:restore_weapon()` across `actor_on_update()`, arrival callbacks, and UI close handlers.
  - Implementing clean phased unholster pulses (`activate_slot(0)` -> `activate_slot(target_slot)`) on journey arrival and safe aborts.
  - Re-registering the travel map UI under `"ui_tlra_travel_map"` rather than `"ui_sleep_dialog"`, and enforcing `hud_weapon 1`, `xr_effects.enable_ui()`, and engine movekey/weapon selection release.
- **Realistic Road & Feeder Path Navigation Engine**: Overhauled path plotting with a comprehensive curated road network (`ZONE_CURATED_ROADS`) spanning Cordon, Garbage, Bar, Dark Valley, Agroprom, Army Warehouses, Yantar, Zaton, and Jupiter, dynamically fused with active `SIMBOARD` smart terrain outposts.
  - A* search snaps within 350m and connects road segments up to 220m–300m, guiding stalkers naturally down village lanes, along paved highways, and through railway underpasses instead of cutting diagonally across fences and hilltops.
  - Eliminated route zig-zags by maintaining smooth interpolated horizontal `(X, Z)` plane vectors and only conforming vertical `Y` to walkable navmesh ground elevation (`level.vertex_position()`), preventing irregular navmesh cell centroids from jittering the path.
  - Enhanced off-road wilderness cross-country fallback with an organic sinusoidal lateral arch and multi-pass Laplacian path relaxation, ensuring treks across open fields follow a natural wandering contour rather than a rigid laser-straight line.
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
