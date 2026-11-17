# Activity Room — interaction specification

**Status:** Working design. Art assets are deferred until an interaction prototype proves placement, access, scrolling, and persistence. Use any suitable existing project PNG as a **temporary** scene and two/three temporary object sprites to test mechanics.

## User intention — Agreed

Users bring activities into a landscape scene by placing **already-coloured** objects. The scene is their own composition, not a checklist, completion meter or award. Clutter is **allowed**, including multiple overlaps and objects partly outside the frame. The layout can stay cluttered and may prompt a respectful, optional end-of-day / next-day **available capacity** reflection. Object placement must never imply that an activity was completed.

## Drawers — Agreed groupings / candidate contents

| Drawer | Example object/symbol | Notes |
| --- | --- | --- |
| Outside | shoes, dog leash, bicycle, garden tools, park bench, shopping bag, mobility aid | Everyday pursuits; adaptable |
| Chores | vacuum, laundry basket, dishes, cooking pot, broom, paperwork | Activities, not productivity scores |
| Rest & relax | book, blanket, mug, bath, cushion, TV remote | Rest is legitimate |
| Social | male-presenting person, female-presenting person, neutral person, family/friend group, phone | Human illustrations are user-selectable visual options, not demographic tracking |
| Positive/supportive (grouping open) | headphones/music, meditation, breathing pause, art, journaling | Could live in Rest & relax instead; do not medicalize |

Use consistent human-readable labels, tags/synonyms and a searchable dropdown/list. User-defined activities require a fallback symbol. An “add from dropdown” path must work without image interaction.

## Interaction model — Agreed

1. Open a drawer (only one expanded drawer on a narrow phone); choose a sprite via drag or **tap-to-pick, tap-to-place**.
2. Place anywhere on/near scene, including partly clipped, so long as an accessible recovery/grab method remains; leave object rendered **in full color**.
3. Touch an object: short selection outline plus accessible text/toolbar (“Selected: Vacuuming”). Outline is distinct from any check-in state.
4. Drag selected item; accessible alternatives: small/large directional nudge, send backward/bring forward, edit, return to drawer, locate, and undo.
5. Foreground opaque sprite can fully cover an object behind it. The covered sprite is **not** directly selectable by tapping through the foreground. Use the scene object list or move/front-adjust first.
6. Optional activity check-in from selected object; dismiss without scoring or completing anything.
7. Preserve the layout automatically with undo/recovery; allow copying a previous room as an explicit action later, not automatic task carryover.

### Scene and asset format

- Initially plan **four or five** landscape scene PNG backgrounds with intrinsic art dimensions and composition-safe areas; final art is a late milestone.
- Each sprite is an independently bundled PNG (transparent background), referred to by `spriteId`. Never store composite PNGs for each daily scene.
- Author/owner can provide **per-scene sprite scale factors** in a catalogue. Keep their editable source/config and document coordinate anchor conventions.
- Artist assets cannot be trusted to have equal real-world object sizes. A user's manual scale adjustment is optional and must stay within safe bounds.
- Light-presence activities (headphones, meditation) can use a small shelf/side area to reduce clutter, but user **may still place full objects**. **No automatic cleanup or clutter cap**.

### Portrait / landscape / zoom

- Scene remains **landscape** across orientations. **Never force rotation.** In portrait mode, show a horizontally scrollable viewport; drawers and check-in controls remain usable without forced two-direction page scrolling.
- Pinch zoom where supported plus accessible +/− and Reset zoom buttons. Default zoom fits scene height or other tested sensible baseline; ensure horizontal browsing remains discoverable.
- On zoom, keep the world point under the **center of the visible screen** fixed, not the pointer or left edge.
- Preserve reasonable zoom limits, clamp scrolling only enough to avoid losing the whole scene, and allow intentional object clipping.
- Track world coordinates relative to scene background dimensions. On device resize/orientation change re-render, do **not** rewrite world coordinates.

### Grab-ability / stacking / recovery

The deliberate tolerance for mostly clipped objects introduces a usability risk: a visible sliver might be impossible to grab with tremor or low vision. **Proposed invariant:** after placement or drag, preserve a defined minimum visible **hit-target intersection** with the scene **or** surface the object's name in an accessible scene-object list with a one-tap `Locate` / `Bring into view` command. Prefer both. The artwork can remain visually mostly clipped, while a larger invisible accessible hit area remains reachable.

A selected foreground object can be moved to reveal background objects; the list can also select any object and show its outline via temporarily accessible focus indicators. Nothing is silently deleted due to occlusion.

### Scene/list parity

All records must be editable in a semantic activity list, including custom activity labels, date, optional check-in and deletion. List edits and drag edits operate on identical stored records. Keyboard/screen-reader users should never be forced through spatial positioning to record participation.

## Optional activity check-in — Proposed exact prompts

- “Would you like to record how this activity went?” (skip)
- Participation: planned/considered; tried a little; took part; used help/adaptations. These are descriptive choices, not ranks.
- “How much capacity did it use?” optional: little / some / a lot / unsure.
- “How did it feel?” optional: supportive / manageable / difficult / mixed / unsure.
- Optional note; no invented interpretation of the person's experience.

Check-in is never required when dropping a sprite into a scene. A completed activity can also be recorded with no sprite via list.

## Capacity reflection and clutter — Proposed

**Available capacity** (tooltip draft, requires editorial review): “How much physical, thinking, emotional, or sensory room a person feels they have for activity, demands and change. It can vary, and only the person can describe their experience.” Link the same term to the site glossary once approved; use local tooltip offline and accessible glossary navigation when online.

After adding multiple objects or at an opted-in end-of-day time, consider a dismissible question: **“Your room looks quite full. How much room did you feel you had left today?”** The question must not presume clutter means strain. Follow-up the next morning can ask about capacity at that time if enabled.

**No inferred readiness score for first release.** Visual object density is not validated effort or capacity. If a numeric reflection metric is considered later, evaluate accuracy, fairness and harm, anchor it to **self-report**, and avoid automated limits/recommendations. Users can choose never to see these prompts.

## QA scenarios

- Smartphone portrait: scroll 16:9 background horizontally, zoom centered without jumping, place/drag without page-scroll conflict.
- Place a sprite mostly off scene, then recover using hit area **and** list; after reload positions remain.
- Cover an object fully with another; normal pointer hit-testing selects only foreground; object list selects rear object.
- Pinch zoom and keyboard +/- produce the same expected center anchor; orientation change preserves placement.
- With tremor-friendly tap-to-place, keyboard arrows, high contrast, large text, screen reader and reduced motion, all activities and check-ins remain available.
- Reopen last week's room; remove an object from view without losing unrelated activity history.
- Missing activity check-in produces no claim that activity occurred.
