╔══════════════════════════════════════════════════════════════════════════════╗
║              T H E   L O N G   R O A D   A H E A D   v 2 . 3 . 1             ║
║         CONTINUOUS ZONE-TO-ZONE TRAVEL & EXPEDITION SIMULATION               ║
║                                                                              ║
║   ◈ Author:        Damage_Zedd                                               ║
║   ◈ Version:       v2.3.1 (Official Release)                                 ║
║   ◈ Compatibility: S.T.A.L.K.E.R. Anomaly 1.5.3 & G.A.M.M.A.                 ║
║   ◈ Requirements:  None (Zero Hard Dependencies)                             ║
║   ◈ Optional:      Fair Fast Travel, Diet System, SafeSpawn, Custom Levels   ║
╚══════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 01. DITCH THE INSTANT TELEPORTS: EXPERIENCE THE EXPEDITION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Long Road Ahead is a comprehensive travel simulation and continuous Zone
expedition overhaul for S.T.A.L.K.E.R. Anomaly and G.A.M.M.A., inspired by the
unforgiving, physically grounded travel mechanics of Kingdom Come: Deliverance.

Ditch immersion-breaking instant teleportation. The Zone is vast, dangerous, and
deadly—crossing it should demand planning, supplies, and vigilance. In The Long
Road Ahead, traveling between distant camps and remote territories requires real
in-game time, burns precious stamina and calories, advances the world clock,
and simulates your physical journey across intermediate regions.

Right-click any discovered map spot, fast-travel marker, or campfire, or hire a local
guide to set out. Your journey traverses the Zone in accelerated time, plotting
animated breadcrumb waypoints across your PDA map. Dynamic threat detection actively
scans nearby ALife simulation squads and mutant packs along your path, pulling you out
of travel for heart-pounding roadside ambushes, or giving experienced stalkers a
chance to slip past under the cover of pitch-black night or howling storms.

  ► THE THREE PILLARS OF CONTINUOUS TRAVEL
    ├── REALISTIC TIME & GEOGRAPHY
    │   Travel duration scales mathematically based on true world vector distance,
    │   character walking speed, encumbrance weight, and active survival stats.
    ├── LIVING THREAT DETECTION (RTTD)
    │   Virtual path scanning dynamically pulls you into combat if hostiles cross
    │   your path, with weather-based and darkness-based stealth dodge chances.
    └── NATIVE SURVIVAL & DIET HOOKS
        Pay for journeys with physical calories, hydration, and sleep—featuring
        native hooks into the Diet System for carbs, fats, and protein reserves.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 02. DYNAMIC PDA EXPEDITION PATHING & BREADCRUMBS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Inspect and track your expedition in real time through an animated PDA interface:

  ┌────────────────────────────────────────────────────────────────────────┐
  │ PDA EXPEDITION TELEMETRY & NAVIGATION                                  │
  │ • Real-Time Animated Breadcrumb Trail across intermediate map sectors  │
  │ • Distance Elapsed vs. Total Route Mileage Telemetry                   │
  │ • Dynamic Multi-Level Border Restrictor & Level Graph Routing          │
  │ • Real-Time World Vector Interpolation with AI Node Ground Snapping    │
  └────────────────────────────────────────────────────────────────────────┘

  ◈ Multi-Level Intermediate Transit
    Long-distance journeys between non-adjacent levels (e.g., Cordon to Jupiter)
    do not magically warp across the Zone. TLRA's dynamic routing engine charts
    an authentic route through real intermediate level transitions (Cordon ──►
    Garbage ──► Rostok ──► Army Warehouses ──► Red Forest ──► Jupiter), accurately
    accounting for distance, time passage, and regional dangers.

  ◈ Animated PDA Breadcrumbs
    While traveling, your PDA displays an animated trail of green waypoint dots
    charting your physical progression across the map.

  ◈ Safe Journey Abort
    Need to halt your expedition immediately? Press Escape or Backspace mid-journey
    to safely interrupt travel. Your character smoothly snaps to the nearest safe AI
    ground vertex with partial stamina refunds and defensive grace windows.

  ◈ Custom Levels Compatibility
    Full support for custom community maps (Promzone, Grimwood, Poselok UG, Bunker A1,
    and Collider) through the dedicated FOMOD compatibility module.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 03. REAL-TIME THREAT DETECTION & AMBUSH MECHANICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The Chernobyl Exclusion Zone never sleeps. While your character is on the road,
TLRA's Real-Time Threat Detection (RTTD) engine actively probes the Zone around you:

  ◈ Active ALife Simulation Scanning
    As your virtual position advances along the road, the engine scans a 100-meter
    detection sphere around your coordinates, evaluating live ALife simulation
    stalker squads and roaming mutant packs.

  ◈ Roadside Ambush Interruption
    If a hostile squad or aggressive mutant pack intercepts your path:
    ├── Cinematic travel fade-in with camera stabilization
    ├── Emergency weapon unholster and posture recovery
    ├── Defensive safety window (damage immunity during engine spin-up)
    └── Direct tactical drop onto the nearest validated AI ground vertex

  ◈ Dynamic Stealth Dodge System
    Skilled stalkers can slip past danger without triggering a firefight. When a
    threat is detected, the system rolls a stealth check modified by environment:
    ├── Night Darkness: Up to +40% stealth bonus in pitch-black conditions
    ├── Heavy Weather: Rain, dense fog, and storms mask your sound and profile
    ├── Suit Camouflage: Ghillie and camouflage outfits boost evasion odds
    └── Stalker Faction Heritage: Faction experience provides baseline bonuses

  ◈ Atmospheric Roadside Events
    Expeditions aren't just combat—the Zone reveals unexpected moments:
    ├── Sudden sun breaks piercing through overcast clouds (+Morale)
    ├── Discovered forgotten stashes tucked away in hollow logs or ruins
    ├── Radiation hot pockets requiring quick dosimeter reactions
    └── Breathtaking ridge views that pause your journey for immersion


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 04. DYNAMIC SURVIVAL, NATIVE DIET SYSTEM & METABOLISM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gone are the days of arbitrary flat 2-minute travel timers and illogical self-paid
ruble fees for walking on your own two feet:

  ◈ Dynamic Duration Scaling
    Travel duration is calculated mathematically from exact 2D world distance,
    walking speed, active encumbrance, and time acceleration factors. Crossing an
    entire territory feels substantial, perilous, and physically grounded.

  ◈ Native Diet System Integration (G.A.M.M.A. & Anomaly)
    Full, seamless native integration with the popular **Diet System** mod:
    ├── Carbohydrate reserves deplete dynamically based on walking exertion
    ├── Fat reserves burn steadily to fuel sustained cardiovascular effort
    ├── Protein reserves degrade over multi-hour cross-Zone treks
    └── Thirst (`actor_status_thirst`) and Sleep (`actor_status_sleep`) drain smoothly

  ◈ Grounded Travel Economy
    You no longer pay rubles to yourself to walk across the Zone. Instead, you pay
    the true cost of survival: physical calories, canteen water, fatigue, and
    in-game daylight.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 05. INVENTORY WEIGHT & OVER-ENCUMBRANCE PHYSICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your backpack load directly governs how your character handles the expedition:

  ◈ Real Carrying Capacity Detection
    TLRA dynamically queries your true maximum carry weight taking into account:
    ├── Equipped exoskeletons, armored suits, and combat vests
    ├── Backpack capacities and hunting pouches
    ├── Belt artifacts and titanium frames
    └── Active stimulant boosters and strength enhancers

  ◈ Overweight & Encumbrance Penalties
    Carrying heavy gear extracts a heavy physical toll:
    ├── Mild Encumbrance: Proportional reduction in walking speed and stamina
    ├── Heavy Overweight: Severe speed degradation; elevated calorie and water burn
    └── Critical Overload: Journey speed reduced to a crawl; extreme fatigue spikes


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 06. COMPANION SQUAD RECALL & USEFUL IDIOTS SYNCHRONIZATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Commanding companions across the Zone has never been more reliable. v2.3.1 introduces
a complete architectural overhaul of companion teleportation and manual recall:

  ◈ Authoritative Manual Recall (`\` Hotkey)
    Pressing the `\` key (default `DIK_BACKSLASH = 43`, configurable via Fair Fast
    Travel MCM settings) triggers TLRA's authoritative companion recall engine.
    Companions stuck behind rocks, lost across level borders, or stranded hundreds of
    meters away are summoned safely to your position.

  ◈ Useful Idiots Stance Bypass
    Useful Idiots splits companions into individual squads and locks them out of
    teleporting when set to wait, cover, relax, or patrol mode. When the player
    manually presses `\`, TLRA deliberately bypasses behavioral blocks, allowing you
    to unstick companions regardless of their AI stance.

  ◈ Anti-Stacking Radial Placement (1.8m–3.0m)
    Companions no longer spawn inside your body or stack into a single coordinate!
    TLRA computes staggered radial positions around the actor with validated level
    vertex checks, completely eliminating physics launch glitches and collision deaths.

  ◈ Server-Side ALife Synchronization
    Teleports both server entities (`alife():teleport_object`) and client objects,
    purges stale offline caches (`db.offline_objects`, `db.spawned_vertex_by_id`),
    resets stuck animations (`safe_reset_animation`), and restores standing posture.

  ◈ Quest Hostage Protection
    Hostages and VIP rescue targets (`companion_cannot_teleport` / `hostages_by_id`)
    are strictly protected and will NEVER teleport with the actor.

  ◈ HUD Notification Receipts
    Clean, non-intrusive on-screen HUD message feedback displays the exact number
    of companions successfully recalled.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 07. COMPREHENSIVE MOD CONFIGURATION MENU (MCM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tailor every mechanic in-game through the extensive Mod Configuration Menu:

  ┌──────────────────────────────┬───────────────────┬─────────────────────────┐
  │ SETTING                      │ RANGE / OPTIONS   │ DEFAULT / DESCRIPTION   │
  ├──────────────────────────────┼───────────────────┼─────────────────────────┤
  │ Travel Preset                │ Stalker / Tourist │ Stalker (Hardcore)      │
  │ Enable Mod                   │ On / Off          │ On                      │
  │ Travel Speed                 │ 1.0 – 5.0 m/s     │ 1.8 m/s (Brisk Walk)    │
  │ Time Acceleration Factor     │ 1.0x – 30.0x      │ 15.0x (Zone Time Scale) │
  │ PDA Path Detail (Dots)       │ 4 – 24 Dots       │ 12 Waypoints            │
  │ Enable Ambush Tech (RTTD)    │ On / Off          │ On                      │
  │ Threat Detection Radius      │ 50m – 200m        │ 100m                    │
  │ Stealth Dodge Base Chance    │ 0% – 100%         │ 25% Baseline            │
  │ Enable Survival Costs        │ On / Off          │ On                      │
  │ Hunger Drain Scale           │ 0.1x – 3.0x       │ 1.0x (Realistic)        │
  │ Thirst Drain Scale           │ 0.1x – 3.0x       │ 1.0x (Realistic)        │
  │ Sleep Drain Scale            │ 0.1x – 3.0x       │ 1.0x (Realistic)        │
  │ Weather Impact on Speed      │ On / Off          │ On                      │
  │ Arrival Offset Distance      │ 0m – 30m          │ 10m (Anti-Campfire Camp)│
  │ The Final Leg Border Mode    │ On / Off          │ Off (Walk Remaining)    │
  │ Screen Vignette & Audio      │ On / Off          │ On (Atmospheric Wind)   │
  └──────────────────────────────┴───────────────────┴─────────────────────────┘

  ◈ Full Dual-Language Localization
    100% complete English and Russian localization (`st_tlra_mcm.xml`) with native
    CP1251 encoding for seamless out-of-the-box Russian Anomaly / GAMMA support.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 08. MODULAR FOMOD INSTALLER & COMPATIBILITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ◈ Modular FOMOD Architecture
    ├── 00 - Core
    │   └── Mandatory core simulation engine, scripts, text strings, and MCM
    ├── 01 - Fair Fast Travel Patch
    │   └── Intercepts Fair Fast Travel (FFT) map clicks into physical TLRA journeys
    └── 02 - New levels Patch
        └── Adds dynamic routing and door dictionaries for 5 custom community maps
            (Promzone, Grimwood, Poselok UG, Bunker A1, Collider)

  ◈ Universal Compatibility
    • S.T.A.L.K.E.R. Anomaly 1.5.3: Out-of-the-box native support
    • S.T.A.L.K.E.R. G.A.M.M.A.: 100% tested and verified compatible
    • Useful Idiots: Full companion squad splitting and recall synchronization
    • Diet System: Native carbohydrate, fat, and protein metabolic depletion
    • Fair Fast Travel (Catspaw): Seamless hook and guide pricing parity
    • SafeSpawn: Full arrival clearance and safety window support


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
▶ 09. COMPLETE CHANGELOG & VERSION HISTORY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ══════════════════════════════════════════════════════════════════════════════
  ✔ WHAT'S NEW IN v2.3.1 (Official Release)
  ══════════════════════════════════════════════════════════════════════════════
  ✔ Authoritative Manual Recall (\ Key): Intercepts and replaces Fair Fast Travel's
    broken companion recall routine with TLRA's authoritative multi-member teleport.
  ✔ Useful Idiots Stance Bypass: Manual recall (forced = true) deliberately bypasses
    behavioral blocks (companion_squad_can_teleport), allowing players to summon
    companions even when stuck in wait, cover, relax, or patrol mode across levels.
  ✔ Anti-Stacking Radial Placement: Teleported companions calculate radial offset
    coordinates (1.8m–3.0m) around the player with AI navmesh vertex validation,
    eliminating companion physics collisions, mesh stacking, and terrain clipping.
  ✔ Offline & Cross-Level Migration: Teleports server entities via sim:teleport_object,
    clears stale offline caches (db.offline_objects, db.spawned_vertex_by_id),
    resets animations (safe_reset_animation), and restores upright standing posture.
  ✔ Standalone Hotkey Fallback: Added standalone on_key_release listener with UI
    dialog focus checks and 800ms debounce protection so manual recall operates
    reliably even if Fair Fast Travel is uninstalled or disabled.
  ✔ Status Feedback: Added clean on-screen HUD message feedback indicating the number
    of companions successfully recalled.

  ══════════════════════════════════════════════════════════════════════════════
  ✔ WHAT'S NEW IN v2.3.0
  ══════════════════════════════════════════════════════════════════════════════
  ✔ Dynamic Duration Scaling: Travel duration dynamically scales based on actual
    world vector distance, walking pace, encumbrance weight, and survival stats.
  ✔ Native Diet System Integration: Carbohydrates, fats, and protein reserves now
    deplete dynamically alongside thirst and sleep over the course of the journey.
  ✔ Grounded Survival Economy: Removed illogical self-paid ruble charges for walking
    journeys—you pay with calories, water, fatigue, and in-game time.
  ✔ Carry Weight Physics: Carrying capacity is dynamically calculated from equipped
    suits, backpacks, belt artifacts, and active boosters. Overweight journeys incur
    severe speed and stamina penalties.
  ✔ Multi-Member Squad Synchronization: Clean multi-member companion transitions
    across level borders with animation resets and coordinate synchronization.

  ══════════════════════════════════════════════════════════════════════════════
  ✔ WHAT'S NEW IN v2.2.2
  ══════════════════════════════════════════════════════════════════════════════
  ✔ Complete Russian Localization: Added full Russian translation (rus/st_tlra_mcm.xml)
    covering all MCM settings, descriptions, road events, guide dialogue, stealth
    results, and positive event messages (104 strings in CP1251).

  ══════════════════════════════════════════════════════════════════════════════
  ✔ WHAT'S NEW IN v2.2.1
  ══════════════════════════════════════════════════════════════════════════════
  ✔ Localization Scope Crash Fix: Fixed fatal crash when opening map travel options
    caused by local helper tlra_str() declaration scope ordering.

  ══════════════════════════════════════════════════════════════════════════════
  ✔ WHAT'S NEW IN v2.2.0
  ══════════════════════════════════════════════════════════════════════════════
  ✔ Arrival Offset Vector Crash Fix: Fixed same-level travel crash by replacing
    invalid dir:length() call with manual 2D length math matching Luabind specs.

  ══════════════════════════════════════════════════════════════════════════════
  ✔ WHAT'S NEW IN v2.1.9
  ══════════════════════════════════════════════════════════════════════════════
  ✔ SafeSpawn Integration: Added SafeSpawn mod support (perform_silo) on same-level
    and cross-level arrivals to clear nearby hostiles before fade-in completes.
  ✔ Arrival Offset Setting: Configurable 0m–30m offset spawning ahead of destination
    markers to avoid spawning directly on top of smart terrain camps.
  ✔ Safety Window Hardening: Increased arrival weapon restore delay and guarded
    safety_reset to prevent vulnerability windows after teleportation.
  ✔ Campfire & Stash Fast Travel: Accepted any destination with a fast_travel tag.
