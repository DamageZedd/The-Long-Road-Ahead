<div align="center">

<sub>S.T.A.L.K.E.R. ANOMALY / G.A.M.M.A.</sub>

# THE LONG ROAD AHEAD
### CONTINUOUS ZONE-TO-ZONE TRAVEL & FAST TRAVEL OVERHAUL

*Ditch the instant teleports. Experience simulated physical travel across the Zone with animated map paths, real-time ALife threats, and realistic survival costs.*

![Version](https://img.shields.io/badge/version-v2.3-e0a43c?style=for-the-badge) ![Author](https://img.shields.io/badge/by-Damage__Zedd-8fae5a?style=for-the-badge) ![Game](https://img.shields.io/badge/S.T.A.L.K.E.R.-Anomaly%201.5.3-555555?style=for-the-badge)

**[Full Changelog](CHANGELOG.md)** · **[Latest Release](https://github.com/DamageZedd/The-Long-Road-Ahead/releases/latest)**

</div>

> ⚠️ **FULL RELEASE – PLEASE READ**  
> The Long Road Ahead is a comprehensive travel simulation overhaul. Always back up your saved games before updating or modifying large modlists.

**The Long Road Ahead (TLRA)** is a complete overhaul of the fast-travel experience in **S.T.A.L.K.E.R. Anomaly** and **G.A.M.M.A.**, inspired by the immersive journey mechanics of *Kingdom Come: Deliverance*.

Instead of immersion-breaking instant teleportation, your stalker embarks on a physical journey across the Zone in accelerated real time. Intermediate levels are traversed seamlessly, in-game time moves forward, stamina and calories deplete, and animated breadcrumbs trace your path on the PDA map. But the Zone is never safe: dynamic threat detection scans for hostile squads and mutant packs along your route, giving you a chance to sneak past using darkness and bad weather or pulling you into a high-stakes roadside ambush.

---

## 🆕 New in v2.3

### ⏱️ Dynamic Travel & Time Scaling
Travel duration is no longer fixed at a rigid 2 minutes regardless of destination. Travel time dynamically scales based on actual world vector distance, walking speed, active encumbrance, and time acceleration factors. Journeys across multiple territories feel substantial and perilous.

### 🍗 Native Diet System & Calorie Reserves
Full native integration with the **Diet System** mod: carbohydrates, fats, and protein reserves now deplete naturally over the course of the journey alongside vanilla/GAMMA thirst (ctor_status_thirst) and fatigue (ctor_status_sleep). Illogical self-paid ruble charges for walking journeys have been replaced—you now pay for your journey with physical calories, sweat, and time.

### 🎒 Carry Weight & Over-Encumbrance Physics
Real carrying capacity is dynamically calculated from equipped suits, backpacks, belt artifacts, and active boosters. Traveling while heavily encumbered severely degrades movement speed and exponentially accelerates stamina and calorie drain.

### 👥 Modern Companion Squad Teleportation
Companion squads now cleanly transition across level borders utilizing xr_companions.companion_squads and squad:squad_members(). Companion animations are cleanly reset (sim_squad_scripted.reset_animation), vertex positions synchronized, and stale offline flags cleared to eliminate companion stacking or freezing upon arrival.

### 🌐 Full Russian Localization (us/st_tlra_mcm.xml)
Added complete Russian translation across all MCM settings, option descriptions, in-game notifications, roadside atmosphere events, guide chatter, and stealth dodge feedback.

---

## 🗺️ Core Mechanics & Features

### 🧭 Continuous Multi-Zone Routing & AI Navigation
Seamlessly travel across multiple Zone borders in a single expedition. The mod automatically executes a Breadth-First Search (BFS) pathfinder across level transition restrictors, routing you through intermediate maps (e.g., Cordon → Garbage → Rostok → Army Warehouses).
- **The Final Leg**: Enable this setting to have long-distance travel deposit you right at the entrance of your destination territory, requiring you to walk the final stretch on foot.
- **Fallback Door Scanner**: Comprehensive scanner for non-standard or invisible level transitions, guaranteeing reliable routing into Red Forest, Limansk, and Jupiter.

### ⚔️ Ambush Tech (Real-Time Threat Detection)
Your journey is never guaranteed to be peaceful. The mod continuously projects your virtual position through the world graph and scans for active ALife simulation squads and mutant packs within threat range.
- If your virtual trajectory passes near a hostile camp or mutant pack, the journey is interrupted, pulling you into real-time combat.
- **Safe Zone Protection**: Configurable buffer (100m) ensuring ambushes never trigger immediately upon departure or right outside your destination safe zone.
- **Fair Percentage Refunds**: If a journey is aborted or interrupted by an ambush, you receive a prorated refund of your travel cost for the uncompleted distance.

### 🥷 Dynamic Encounter Sneaking (Stealth Dodge)
When a threat is detected along your path, you have a chance to slip past unseen without interrupting the journey:
- **Rank Scaling**: Veteran stalkers have sharper survival instincts and higher baseline sneak chances.
- **Circadian Advantage**: Traveling under the cover of night significantly increases stealth success.
- **Weather Camouflage**: Heavy fog, rain, and thunderstorms mask movement sounds and visual silhouettes.
- Configurable base chance (default: 15%) and maximum cap (default: 75%) in MCM.

### 📍 AI-Node Snapping & Arrival Offset
- **Strict AI Vertex Snapping**: When exiting travel (voluntarily or via ambush), you are snapped to the nearest validated AI node (level_vertex_id) with a 1.5m physics sky-drop to prevent clipping into map geometry or falling through the world.
- **Arrival Offset (default 10m)**: Spawns you slightly before the target spot instead of directly on it, avoiding ambushes from enemies camping directly on the fast-travel point.
- **SafeSpawn Integration**: Seamlessly interfaces with the SafeSpawn mod (perform_silo) to clear immediate threats before the screen fades in.

### 🗺️ Animated PDA Map & Visual Immersion
- **Animated Map Dots**: Real-time breadcrumbs display your journey's progress on the PDA map. Detail level is customizable (4 to 24 waypoints).
- **Cinematic Vignette & Sound**: Subtle visual vignette and ambient wind sound effects immerse you while on the road.
- **Roadside Atmosphere Events**: Ambient PDA updates keep you informed of your character's thoughts, distant sounds, and Zone weather while traveling.

### 🧭 Guide Travel & Fair Fast Travel (FFT) Support
- Full compatibility with the **Fair Fast Travel** cost and duration calculation systems.
- Optional **"Hire guide (instant)"** menu option to pay guides for instantaneous travel while preserving simulated journeys for solo treks.

### 🗺️ Custom Levels Support
Included compatibility patch seamlessly connects 5 custom community maps into the routing database and keyword dictionary:
- **Promzona**
- **Grimwood**
- **Poselok UG**
- **Bunker A1**
- **Collider**

---

## 🎛️ Presets & Configuration

### Travel Presets

| Feature | Stalker (Default) | Tourist (Easy) |
|---|:---:|:---:|
| **Ambush Tech & Encounters** | Active | Disabled |
| **Survival Costs (Hunger / Thirst / Sleep)** | Active | Disabled |
| **Stamina Exhaustion Interrupts** | Active | Disabled |
| **Simulated Travel Speed** | 25 m/s | 35 m/s |
| **Stealth Dodge** | Rank & Weather Scaled | Guaranteed Safe |

### MCM Options Breakdown

| Setting | Type | Default | Description |
|---|:---:|:---:|---|
| **Enable Mod** | Toggle | Enabled | Master toggle for all travel systems |
| **Travel Preset** | List | Stalker | Stalker (full danger) or Tourist (peaceful) |
| **Travel Speed** | Slider | 25 m/s | Simulated travel speed across the map (10–50 m/s) |
| **Time Acceleration** | Slider | 10x | Game-time passage multiplier during travel (1–50x) |
| **Enable Ambush Tech** | Toggle | Enabled | Real-time threat detection from ALife squads |
| **Safe Zone Protection** | Toggle | Enabled | Blocks ambushes within 100m of departure/arrival |
| **Arrival Offset** | Slider | 10m | Spawns before destination to avoid enemy spawns |
| **Enable Stealth Dodge** | Toggle | Enabled | Allows chance to slip past detected threats |
| **Base Sneak Chance** | Slider | 15% | Baseline sneak chance before bonuses |
| **Max Sneak Chance** | Slider | 75% | Upper limit on stealth evasion |
| **Enable Survival Costs** | Toggle | Enabled | Applies hunger, thirst, and sleepiness |
| **Stamina Consumption** | Toggle | Enabled | Forces stops if stamina reaches zero |
| **The Final Leg** | Toggle | Disabled | Drops player at border to walk destination map |
| **PDA Path Detail** | Slider | 12 | Number of waypoints displayed on PDA map |
| **Travel Wind & Vignette** | Toggle | Enabled | Cinematic audio-visual travel atmosphere |

---

## 📦 Required & Recommended Mods

### Requirements
- **S.T.A.L.K.E.R. Anomaly** (1.5.1 / 1.5.2 / 1.5.3), **G.A.M.M.A.**, or **EFP**
- **[Mod Configuration Menu (MCM)](https://www.moddb.com/mods/stalker-anomaly/addons/anomaly-mod-configuration-menu)**

### Supported Integrations
- **Fair Fast Travel (FFT)**: Supported via included  1 - Fair Fast Travel Patch.
- **Diet System**: Automatically detected and hooked—depletes carbohydrates, fats, and protein reserves.
- **SafeSpawn**: Automatically detected—clears immediate spawn hazards upon arrival.
- **Custom Levels Pack**: Supported via included  2 - New levels Patch.

---

## 📥 Installation

1. Install **MCM (Mod Configuration Menu)**.
2. Install **The Long Road Ahead** using **Mod Organizer 2** (the included **FOMOD** installer will guide you):
   - **00 - Core**: Mandatory core files (scripts, configs, localization).
   - **01 - Fair Fast Travel Patch**: Optional patch for Fair Fast Travel users.
   - **02 - New levels Patch**: Optional patch adding Promzone, Grimwood, Poselok UG, Bunker A1, and Collider.
3. Place in your mod load order after MCM and Fair Fast Travel.

### Recommended Load Order

`
1. Mod Configuration Menu (MCM)
2. Fair Fast Travel (if used)
3. The Long Road Ahead (Core)
4. The Long Road Ahead - Fair Fast Travel Patch (if used)
5. The Long Road Ahead - New levels Patch (if used)
`

---

## 🙏 Credits

- **Damage_Zedd** — Mod creator, continuous travel engine, and ongoing development
- **Antigravity** — Custom levels compatibility patch contributor
- **Fair Fast Travel Team** — Fast travel framework and ecosystem inspiration
- **S.T.A.L.K.E.R. Anomaly & G.A.M.M.A. Communities** — Testing, feedback, and support

---

## 📜 Full Changelog

See [CHANGELOG.md](CHANGELOG.md) for the complete version history from v1.0.0 through v2.3.
