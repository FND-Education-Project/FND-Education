# Local data model and versioned contracts

**Status:** Proposed logical schema. This is documentation, not a database migration. Use stable UUIDs for individual user records, human-reviewed stable catalogue IDs for standard symptoms, timestamps in ISO-8601 UTC where appropriate, plus a local calendar date and IANA timezone for day-based reflections.

## Storage and migrations

IndexedDB on an isolated app origin; schema version starts at 1. Use transactions for related record updates. Validate every imported/exported record against versioned schemas, bound string lengths, cap note sizes, and preserve unknown fields only under a deliberate migration policy. Data always belongs to the local device/browser profile, not to a cloud account ID.

### Entities / conceptual tables

| Entity | Fields | Notes |
| --- | --- | --- |
| `TrackedSymptom` | `id`, `catalogueId?`, `displayName`, `custom?`, `createdAt`, `archivedAt?` | Archived retains history; never infer diagnosis |
| `DailyCheckIn` | `id`, `localDate`, `timezone`, `createdAt`, `updatedAt`, `impact?`, `meaningfulParticipation?`, `note?`, `status` | Draft/complete are editor states, **not** ratings of health |
| `SymptomAssessment` | `checkInId`, `symptomId`, `state` | `experienced / absent / not_recorded`. Absence of an assessment row also means **not recorded** |
| `ActivityDefinition` | `id`, `catalogueId?`, `label`, `drawerId`, `spriteId?`, `archivedAt?` | Includes user-defined activities; labels not diagnoses |
| `SceneDefinition` | `id`, `backgroundAsset`, `width`, `height`, `version` | Bundled static asset, reused daily |
| `SpriteDefinition` | `id`, `spriteAsset`, `intrinsicSize`, `sceneScaleOverrides`, `minGrabWidth` | Pre-created transparent coloured PNG or accessible alternate |
| `DailyRoom` | `id`, `localDate`, `sceneId`, `sceneVersion`, `updatedAt` | One or more room revisions allowed by policy |
| `PlacedObject` | `id`, `dailyRoomId`, `activityId`, `spriteId`, `worldX`, `worldY`, `scale`, `rotation?`, `zIndex`, `addedAt` | Small geometry record; **not** stored image snapshot |
| `ActivityCheckIn` | `id`, `placedObjectId?`, `activityId`, `localDate`, `participation?`, `effort?`, `feltSupportive?`, `capacityUsed?`, `note?` | Entire record optional; object placement **does not assert completed activity** |
| `CapacityReflection` | `id`, `localDate`, `timing`, `selfRatedCapacity?`, `manageable?`, `repeatTomorrow?`, `note?` | `timing`: end-of-day / next-morning, user-reported only |
| `JournalEntry` | `id`, `occurredAt?`, `recordedAt`, `updatedAt`, `text`, `userApprovedSymptomIds[]` | No background symptom tagging or remote NLP |
| `Preferences` | `reminderPolicy`, `visual`, `textScale`, `reduceMotion`, `sceneInputMode`, `reportDefaults` | Device-local; only voluntary course account prefs reside remotely |
| `ReportDraft` (optional) | `id`, `startDate`, `endDate`, `selectedSections`, `selectedJournalIds[]` | Generate fresh from chosen data; no automatic server persistence |

`id` fields are opaque and must never encode a name, symptom or learner account ID. User-defined names may be sensitive. Do not index or log raw journal text outside the local database.

## Object/scene coordinates

Use a fixed scene **world coordinate system** (e.g., asset width × height), not device pixel positions. Each `PlacedObject` stores its anchor position, scale and ordering. Render position is `screen = (world - scrollOffset) * zoom` in each axis; convert pointer/touch location back to world space before drag/placement. Anchor zoom on the **center of the visible viewport** by preserving the world point currently at that center.

- Artist-provided scene-specific sprite scale factors normalize object sizes relative to the background.
- Clip only the rendered scene, not object data. Allow deliberate partly/mostly clipped objects but guarantee an accessible grab/recovery route.
- Selection outline is transient UI state, not history.
- Z-order is explicit; foreground can cover background. Provide an object list with bring-to-front/locate controls as an accessibility escape hatch; do not silently make background objects click-through.
- Track removal from the room separately from deleting an activity record/history.

## Availability and denominators

An unrecorded symptom cannot be interpreted as absent. Insights must count `experienced` only where assessed and display assessed-day denominators. Similarly a sprite in the scene means “placed/considered,” **not** “performed,” and an unannotated activity means **unknown participation**. A missing capacity reflection is unknown, not “zero capacity.”

Room clutter (number/overlap/density of placed sprites) is **visual context only**. It is not validated as energy use, exertion or predictive capacity. Store optional self-rating and any opted-in qualitative reflections separately. A later score/threshold must be co-designed and tested, not implemented as a clinical assessment.

## Static catalogue versioning

A reviewed symptom catalogue is built for app distribution from source-of-truth subject vocabulary with a manual approval map; fields: `catalogueId`, `label`, `aliases`, `layPhrases`, `misspellings`, `referenceUrl?`, `status`, `version`. A site search result is **not** automatically a symptom suggestion. Pin catalogue versions in app builds. Never reinterpret an existing custom symptom because a new term was added.

Activity/drawer catalogue: outside / chores / rest-relax / social / positive-supports (last drawer grouping open). Social person sprites have selectable male/female/neutral presentation; these are visual customization choices, not app-user gender inference.

## Import, export and deletion contracts

- All data export: user-initiated, schema-versioned package, preferably passphrase-encrypted and integrity-authenticated; warnings about unencrypted downloads/backups.
- Import: preview scope, validate size/version/schema, never execute imported content, handle duplicate IDs/conflicts explicitly; no silent overwrite.
- Delete local data: separate explicit UI with confirmation, delete local DB and applicable caches/keys on **this device**, explain it does not erase files user exported or other browser profiles/devices.
- Delete course account: server action of existing learner Worker only; does not implicitly erase local content.
- Clear cache/update/service worker: never drop or replace IndexedDB records.
