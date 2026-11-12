# Route Planning Spike (Phase 0)

Feature: a "Plan route (TLRA)" PDA option that opens the TLRA travel map in a planning mode. The player clicks free waypoints; the journey then follows that path, and threat checks run along it.

Decisions: v1 is same-level only; waypoints are placed freely (off-road allowed); the planner shows no threat information.

Line numbers refer to `main` at `65a4fcc`. `Z` = `zzzz_the_long_road_ahead.script`, `U` = `ui_tlra_travel_map.script`. Nothing here was run in-game.

## Verdict: GO

Every building block exists in the engine or in TLRA already. The two things that need an in-game check are listed at the end.

## 1. Mouse input in a CUIScriptWnd

- Clicks arrive in `OnKeyboard(dik, keyboard_action)` as `DIK_keys.MOUSE_1` / `DIK_keys.MOUSE_2` with `ui_events.WINDOW_KEY_PRESSED`.
  - Proven in `G.A.M.M.A. UI/gamedata/scripts/utils_ui.script:3359-3362`.
- `GetCursorPosition()` returns a `vector2` in UI space.
  - Proven in `utils_ui.script:2013`, `:3260` and `xx-Wearable Devices/.../wd_gizmo.script:519`, `:586`, `:622` (click-to-hit-test on custom geometry).
- TLRA already has `UIRoadAheadTravelMap:OnKeyboard` (`U:1565`) handling the wheel and keys, so mouse buttons slot in there.

## 2. Screen to world

The map renders global UV to screen as (`U:1109-1150`):

```
sx = (u - u1) * g_zoom
sy = (v - v1) * g_zoom * g_aspect      -- g_aspect = 4.0 / 3.1099696
```

The inverse for a click at cursor `(cx, cy)` inside `map_frame` (0..1024, 0..768) is:

```
u = u1 + cx / g_zoom
v = v1 + cy / (g_zoom * g_aspect)
pos = global_uv_to_coord(u, v, level.name())   -- U:436
```

- `u1`, `v1` and `g_zoom` are locals in `UpdateViewport` today. Store them on `self` (`self.vp_u1`, `self.vp_v1`, `self.vp_zoom`) so the click handler can use them.
- UV space is always the nominal 4096x8192. `get_tex_scale` only rescales texture rects, so click math needs no extra scaling for Winter/HD map packs.
- Widescreen: TLRA lays out a fixed 1024x768 frame with no `utils_xml.screen_ratio()` (kx) adjustment. `GetCursorPosition()` also reports 1024x768 virtual coordinates, so the two match. **In-game check 1:** confirm a click lands on the right map spot on a 16:9 screen. If it is offset horizontally, divide `cx` by kx as `wd_gizmo.script:520` does.

## 3. Free placement validity

- Snap a clicked position to the AI map with the existing `get_safe_pos` (`Z:814-835`). It calls `level.vertex_id(pos)`, rejects `4294967295` / `-1`, then searches nearby with `level.vertex_position`. Reuse it as is.
- Reject a click when no valid vertex is found within a small radius, for example 25 m (outside the map, deep water, or inside geometry). Show a short "Can't go there" log line.
- Segment check (optional, v1 can skip): sample `level.vertex_id` every ~10 m along each straight segment. A 1 km segment is about 100 C calls, which is negligible when done once on confirm.
- Waypoints are free and joined by straight segments. They are not routed through `find_road_path`, matching the free-placement decision.
- **In-game check 2:** whether `level.vertex_id` returns the nearest vertex or `invalid` for off-mesh points. `get_safe_pos` handles both cases, so this only affects how forgiving clicks feel.

## 4. Pausing while planning

- The journey has not started while planning, so TLRA's travel time factor (`Z:2672-2677`) and `tlra.is_paused` (`Z:3637`, `:3689`) are untouched.
- The world runs at normal speed during planning, the same as using the PDA. No engine pause is needed. Do not call `device():pause()`; it risks the stuck-input class of bugs we just fixed.

## 5. Rendering with vanilla textures only

- Waypoint markers: reuse ids TLRA already references from vanilla, `ui_inGame2_PDA_icon_Primary_mission` (destination marker) and `ui_inGame2_PDA_icon_Place_to_rest` (start marker), in `ui_tlra_travel_map.xml`. No new or baked textures.
- Route line: reuse the footstep trail pool (`trail_dot`, `EnsureTrailCapacity` `U:1090`, `BuildStampedFootsteps` `U:1035`). Build a preview of evenly spaced dots along the planned polyline.
- After confirm, `StartJourney` receives the waypoint polyline, and `GetPositionAlongRoute` (`U:987`) works unchanged.

## 6. Persistence

- Saved state uses `save_var` / `load_var` on the actor (`tlra_save` `Z:1566`, keys `Z:60-89`).
- Add a key for the custom route, for example `KEY_ROUTE = "tlra_rt"`, holding a compact string `"x,z;x,z;..."`. One string avoids dozens of keys. Clear it in `tlra_clear` (`Z:1709`).
- On load, `tlra_load` (`Z:1773`) must return it, and the resume path must pass it back to `StartJourney`, so the map and threat checks follow the same path after a reload.

## 7. Menu hook

- Add a third `pui:AddItem` in `on_map_spot_menu_add_property` (`Z:3161`), gated by a new MCM toggle and only for same-level destinations in v1.
- **Collision to avoid:** the click handler (`Z:3230`) starts a normal journey for any result containing `(TLRA)`. "Plan route (TLRA)" would match that. Check the plan string first, or use a distinct suffix such as "Plan route [TLRA]".
- FFT is unaffected: TLRA only adds an item and handles its own result string.

## 8. Threat checks along the custom path

- `detect_ambush` already asks `GUI:GetPositionAlongRoute(cur_ratio)` (`Z:3903+`), so it follows the planned polyline while the map is open.
- Gap: the off-map fallback lerps straight from start to destination (`Z:3640-3647`). Replace it with a walk along `tlra.custom_route` when present.
- `travel_dist` must be the summed polyline length, so time, stamina and calories scale with the detour. Pass it into `StartJourney`'s existing `travel_dist` argument.
- No threat information is shown in the planner, so outcomes stay random.

## Implementation sketch

| Phase | Files | Work |
|---|---|---|
| 1 Core | `Z` | `build_custom_route(points)` (validate, snap, length); `tlra.custom_route`; save/load key; the off-map fallback walks the polyline; `start_travel_sequence` accepts an optional route |
| 2 UI | `U`, `ui_tlra_travel_map.xml` | `OpenPlanner(start, dest)`; store viewport on `self`; MOUSE_1 adds a point, MOUSE_2 / Backspace undoes, Enter confirms, Esc cancels; preview with the trail pool; distance and time readout; `StartJourney(..., custom_waypoints)` |
| 3 Polish | `zzz_tlra_mcm.script`, `st_tlra_mcm.xml` (eng and rus), `CHANGELOG.md` | MCM toggle "Allow route planning"; max waypoints (for example 12); strings; changelog |

Data shape: `custom_route = { {x=,y=,z=,lvid=}, ... }`, start first and destination last.

## Risks

1. Click offset on widescreen (in-game check 1). Mitigation: the kx correction from `wd_gizmo.script:520`.
2. Waypoints on unreachable navmesh islands (the far side of a fence or river). Mitigation: snap plus an optional segment sample. The journey is simulated, so an odd path is cosmetic, not a crash.
3. Resume after a mid-journey save with a custom route. Mitigation: one saved route string, cleared in `tlra_clear`, plus a test step that reloads mid-journey.

## Fallback if NO-GO

Not needed. If click-to-place fails in-game, route through the player's own PDA user pins in the order they were placed, reusing Phases 1 and 3 unchanged.

## In-game checks needed from the user

1. On your screen, a click in the planner should land exactly where you clicked on the map.
2. Click on water, on a building and outside the playable area: each should be rejected or snapped, never crash.
