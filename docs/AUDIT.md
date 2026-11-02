# TLRA Audit: save/load, companion recall, key fallback, nil-guards, callbacks

Audit only. No scripts or XML were changed. Based on `docs/CODEMAP.md` (commit `5fc4868`) and the line slices listed under "Scope". Line numbers refer to that commit.

Files: `Z` = `00 - Core/gamedata/scripts/zzzz_the_long_road_ahead.script`, `U` = `00 - Core/gamedata/scripts/ui_tlra_travel_map.script`.

Status meanings:
- **CONFIRMED**: follows from the code as written (reasoning only; nothing was run in-game). The in-game test step checks that the trigger is reachable.
- **PLAUSIBLE**: depends on engine behavior or timing the code cannot show. Treat as a hypothesis.

Summary: 2 CONFIRMED, 6 PLAUSIBLE. Ranked by impact.

---

## 1. Stale journey state loaded on a non-resuming load (free travel, free refund) — CONFIRMED, High

**Where:** `Z:1602-1613` (`tlra_load` writes `tlra.*` before it knows whether a resume is needed), `Z:2894` (`actor_on_first_update` calls it and discards the result), `Z:2919-2923` (resume handler returns without clearing), `Z:2564` and `Z:2540` (charge gates), `Z:3704-3716` (`process_refund`).

**Failure scenario:**
1. A same-level journey starts. `tlra_save` (`Z:1395`) writes `KEY_TRAVELING = true`, `KEY_COST = N`, and `KEY_FINAL_GVID = false` because `tlra.final_gvid` is nil for same-level trips.
2. The player saves mid-journey (quicksave or autosave) or the game crashes and they reload an older save.
3. On load, `tlra_load` sees `KEY_TRAVELING` true and runs. It sets `tlra.journey_cost = N`, `tlra.fft_authoritative`, `tlra.is_guide`, `tlra.stats_*` (`Z:1607-1612`).
4. The resume event finds `final_gvid == false` and returns at `Z:2920-2923`. It never calls `tlra_clear()` and never resets `KEY_TRAVELING`. Nothing else clears the loaded values.
5. The next native journey reaches `Z:2564`, `(tlra.journey_cost or 0) <= 0` is false, so the actor is **not charged**. If they abort, `process_refund` (`Z:3704`) pays out `journey_cost * remaining`, so money is created. The same stale `fft_authoritative = true` also skips the FFT charge at `Z:2540`.
6. `KEY_TRAVELING` stays true in every later save until a journey ends via `tlra_clear`.

**Minimal fix:** In the resume handler at `Z:2920`, call `tlra_clear()` before `return true` when no cross-level resume is pending. Optionally make the `Z:2894` call side-effect free by reading `KEY_TRAVELING`/`KEY_FINAL_GVID` directly with `load_var`.

**In-game test:**
1. Enable costs. Start a same-level journey and quicksave while the map is open.
2. Load the quicksave. Note the money, then start another same-level journey with the map.
3. Expected after fix: money drops by the journey cost. Before fix: no charge, and Backspace-abort adds money.
4. Check `tlra_log` output with `debug_logging` on for "No pending journey found on load".

---

## 2. `teleport_companions` mixes destination-level data with current-level `level.*` calls — CONFIRMED (logic), PLAUSIBLE (crash), Medium-High

**Where:** `Z:4285` (`level.vertex_position(lvid)`), `Z:4386-4396` (`level.vertex_id(offset_pos)`, `level.vertex_position(offset_lvid)`). Cross-level callers: `Z:3605` (cross-zone arrival, runs before `ChangeLevel`) and `Z:4164` (offline-level ambush, runs before `ChangeLevel`).

**Failure scenario:** At those call sites `pos`, `lvid`, `gvid` belong to the destination level, but the actor is still on the origin level. `level.vertex_position` and `level.vertex_id` act on the **current** level's navmesh:
- `anchor_pos = level.vertex_position(lvid)` returns a position from the origin level (or reads out of range if `lvid` exceeds the origin level's vertex count; a crash there is PLAUSIBLE, not shown). That value overrides the correct `pos`.
- The radial offset logic then passes `final_lvid`/`final_pos` taken from the origin level to `sim:teleport_object(member_id, gvid, final_lvid, final_pos)` with the destination `gvid`.
- Companions end up with a position/vertex/graph-vertex triple that does not match, so they may spawn off navmesh or far from the actor after arrival.

**Minimal fix:** At the top of `teleport_companions`, compare `game_graph():vertex(gvid):level_id()` with the actor's current level id. If they differ, set `anchor_pos = pos`, skip the `level.vertex_*` offset block, and use `final_pos = pos`, `final_lvid = lvid`. Keep the same-level behavior unchanged.

**In-game test:**
1. Hire a companion. Travel cross-zone with TLRA, for example Garbage to Cordon.
2. On arrival check the companion is near the actor and not stuck or missing.
3. Repeat with `debug_logging` on. Optionally force an offline-level ambush and check the same.

---

## 3. Runtime state not reset on load; stale UI window — PLAUSIBLE, Medium

**Where:** `Z:2858-2984` (`actor_on_first_update` never resets `tlra.is_traveling`), `Z:2335` (start guard), `Z:2685-2692` (`is_safety_active` and `actor_on_before_hit` zero all damage while `tlra.is_traveling`), `Z:3169-3172` (recall requires `not tlra.is_traveling`), `U:10`, `U:1551`, `U:1573`, `U:1584-1590` (module-level `GUI` used by `is_open` and `on_mouse_wheel`).

**Failure scenario (needs the Lua module to survive a game load; not provable here):** The player loads a save from the main menu or in-game while a journey is active. `tlra.is_traveling` and `GUI` keep their old values. The actor is then invulnerable (`actor_on_before_hit`), cannot start a journey (`Z:2335`), and cannot use the recall hotkey. `on_mouse_wheel` may call `:IsShown()` on a dead window.

**Minimal fix:** At the start of `actor_on_first_update` (before `tlra_load`), reset the runtime flags: `tlra.is_traveling = false; tlra_is_traveling = false; tlra.is_paused = false; tlra.dot_ids = {}` and call `ui_tlra_travel_map.close_map()` under `pcall`. Safe because a real resume restarts the sequence from scratch at `Z:2956`/`Z:2972`.

**In-game test:**
1. Start a journey, load a save from the pause menu while the map is open, then try to take damage and start another trip.
2. Expected after fix: normal damage, new trip works.

---

## 4. Monkey-patches can stack if `on_game_start` runs again — PLAUSIBLE, Medium

**Where:** `Z:2702` (`ranks.get_se_obj_rank_name`), `Z:2754` (`bring_companions_to_actor`), `Z:2797` (`cost_to_travel`), `Z:2825` (`zzz_player_injuries.actor_on_update`).

**Failure scenario:** If the engine calls `on_game_start` again without reloading module state, each patch wraps the previous wrapper. For BHS this is worse than slower calls: `get_bhs_myhealth_index` (`Z:2812-2823`) scans `original_bhs_update` for the upvalue `myhealth`. On a second wrap that function is the first wrapper, which has no such upvalue, so `bhs_idx` stays nil and the BHS limb-damage protection during travel silently stops. The `cost_to_travel` wrapper also nests.

**Minimal fix:** Guard each patch with a flag on the `tlra` table, for example `if not tlra._patched_bhs then ... tlra._patched_bhs = true end`. If the module is reloaded the flag resets together with the patches, so the guard is safe both ways.

**In-game test:** Load a save three times in one session, then take limb damage right after a travel arrival. Expected after fix: BHS damage suppressed exactly as on the first load. A stack depth probe: log from the wrapper and count lines per call.

---

## 5. Arrival race: a new journey started inside the 0.8 s arrival window is wiped — PLAUSIBLE, Low

**Where:** `Z:3656-3688` (the `safe_arrival` time event calls `tlra_clear()` and reads `tlra.start_game_time`/`tlra.travel_dist`), `Z:4069-4074` (`stop_travel_logic` already set `is_traveling = false` at the start of `complete_travel_sequence`).

**Failure scenario:** After arrival, `is_traveling` is false for 0.8 s while `safe_arrival` is still pending. If the player starts another journey in that window (map-spot menu), `safe_arrival` then runs `tlra_clear()`, which sets `is_traveling = false` and clears `dest_pos`/`dot_ids` for the new journey while its map is open. Money is already spent.

**Minimal fix:** In the event, run `tlra_clear()` only when `not tlra.is_traveling`. Alternatively reject starts for 1 s after `tlra.last_travel_end_tg` in `start_travel_sequence`.

**In-game test:** Arrive, then immediately right-click a map spot and start a trip within one second. Expected after fix: the second journey proceeds normally.

---

## 6. `on_key_release` recall bind edge cases — PLAUSIBLE, Low

**Where:** `Z:3146-3175`.

**Failure scenarios:**
- `b == 0` (FFT bind unset) is not `-1` and not `> 0`, so the code keeps the default `DIK_BACKSLASH`. A user who unbound the key in FFT still gets recall on backslash.
- `b` non-numeric makes `b > 0` raise inside the key callback.
- `ui_mcm.get_mod_key` is called without a nil check at `Z:3165` (the whole handler is not under `pcall`).
- FFT's own handler for the same bind also calls the patched `bring_companions_to_actor`; the 800 ms debounce at `Z:4273-4277` makes the second call a silent no-op, which is fine but means the "no companions" message can be swallowed.

**Minimal fix:** Treat `b == 0` like `-1` (disabled) when FFT is present, guard `type(b) == "number"`, and use `ui_mcm.get_mod_key and ui_mcm.get_mod_key(recall_mod)`.

**In-game test:** With FFT, unbind the squad-teleport key in MCM, press backslash with a companion far away. Expected after fix: nothing happens.

---

## 7. Offline-member behavior clear is dead code — PLAUSIBLE, Low

**Where:** `Z:4413-4420` (`sim.disable_info_portion`).

**Failure scenario:** `alife()` does not expose `disable_info_portion` in stock Anomaly bindings (not verified against this exact build), so the guard is false and nothing runs. Offline companions in wait/cover/patrol keep their `npcx_beh_*` flags after a forced recall; only online objects get them cleared (`Z:4427-4436`). They may teleport to the actor and then stay put.

**Minimal fix:** Clear the portions through the companion mod's own API for offline members (for example `axr_companions.set_companion_to_follow_state` with the server squad) or skip the dead branch. Verify the API name first.

**In-game test:** Order a companion to wait far away, go offline range, press the recall key. Check that it follows after teleporting.

---

## 8. Unguarded state in `trigger_encounter` / `abort_travel_safe` — PLAUSIBLE, Low

**Where:** `Z:3088-3095`, `Z:4131`, `Z:4185` (`tlra.start_pos.x` log), `Z:4189-4194`.

**Failure scenario:** Both read `tlra.current_dist / tlra.travel_dist` and `tlra.start_pos` without a nil/zero check. If either runs after `tlra_clear()` has set `travel_dist = 0` and `start_pos = nil` (a UI callback arriving after an abort), the result is `NaN` and an "attempt to index a nil value" error at `Z:4185`.

**Minimal fix:** At the top of both functions: `if not (tlra.start_pos and tlra.travel_dist and tlra.travel_dist > 0) then return end`.

**In-game test:** Trigger an encounter prompt, press Backspace, then click a modal button if it is still visible.

---

## Reviewed with no finding

- **Save/load mechanism:** The script uses `save_var`/`load_var` on the actor only. There are no `save_state`/`load_state` netpacket hooks, so no packet-size or ordering risk. `tlra_save` and `tlra_clear` are symmetric for all `KEY_*`, with the stale-value caveat under finding 1: `tlra_save` only writes `final_*` and `next_*` keys when present, and relies on `tlra_clear` to erase them.
- **Callback symmetry:** Everything in `Z:2730-2739` and `U:1597` is registered once in `on_game_start` and never unregistered, which is the normal pattern. The only `UnregisterScriptCallback` calls are the FFT `map_spot_menu_*` handlers (`Z:2771-2775`), done 4 s after start. They depend on `game_fast_travel.map_spot_menu_*` being the same function objects FFT registered; if FFT registered a different closure the call is a silent no-op and both menu entries appear. UI `AddCallback`s (`U:654-657`) are bound per window instance, so there is no leak.
- **Alife nil-guards:** `teleport_companions` guards `alife()`, `sim:object()`, `db.storage[...]`, `level.object_by_id`, and wraps teleport calls in `pcall`. `detect_ambush` wraps the SIMBOARD scan in `pcall`. No unguarded alife object access found beyond the items above.
- **`first_door_pos`:** reset on both branches at `Z:2432-2447`, so it cannot go stale.

## Scope

Slices read: `Z:11-50`, `Z:1395-1435`, `Z:1538-1665`, `Z:2330-2400`, `Z:2520-2600`, `Z:2677-2860`, `Z:2858-2984`, `Z:3078-3175`, `Z:3225-3300`, `Z:3500-3720`, `Z:3718-3870`, `Z:3900-3975`, `Z:4069-4458`; `U:1238-1262`, `U:1396-1480`, `U:1521-1617`. Not read: routing (`Z:363-2100`), survival math, weather/speed modifiers, rest of the UI geometry code.
