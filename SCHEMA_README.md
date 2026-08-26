# Annotation schema — the constant across all six platforms

`cvat_labels.json` is the schema as **actually built and delivered in the CVAT baseline**, verified against
`cvat_fish_run_2026-08-06_FINAL_DATUMARO.zip` (MD5 `d8bdc3b4…`). Import or recreate this on every
subsequent platform. Holding it constant is what makes the platform comparison mean anything; a
renamed label makes two runs incomparable.

## Classes

| Label | Shape | Attributes |
|---|---|---|
| `fish_bbox` | rectangle | orientation, visibility, posture |
| `fish_polygon` | polygon | orientation, visibility, posture |
| `fish_mask` | mask | orientation, visibility, posture |
| `fish_keypoint` | skeleton, 5 points | orientation, visibility, posture |
| `context_object` | any | none |

Skeleton points, in fixed order: `snout`, `eye`, `dorsal_origin`, `pelvic_origin`, `tail_fork`.

## Attribute values

- `orientation` — `lateral`, `oblique`, `axial`, `indeterminate`
- `visibility` — `full`, `partial`, `heavy_occlusion`
- `posture` — `straight`, `curved`, `indeterminate`

**Constrain these to fixed lists wherever the platform allows it.** Where a platform offers only free text,
record that in the comparison log — it is the single largest driver of attribute drift at volume, and no
vendor comparison mentions it.

## Two values went unused in the CVAT baseline

`posture: curved` and `visibility: heavy_occlusion` never appeared. Neither is dead weight:

- `curved` is simply absent from this sample — every fish encountered was cruising or unreadable.
- `heavy_occlusion` is structurally rare here, because the boundary-ownership rule (guidelines v4.7)
  routes heavily occluded instances to a count rather than an annotation.

Keep both. Removing them would change the schema mid-project and destroy the drift comparison.

## Not in the schema, deliberately

- **No species field.** One class, `fish`. Species is not labelled.
- **No per-frame tag.** Below-threshold counts live in the edge-case log with reasons attached, which
  carries more information than a bare number on a tag.
- **No per-point `uncertain` flag.** Identified as a genuine gap in edge case 10, and deliberately deferred
  to a future batch — adding a field mid-run would invalidate the drift measurement.

---

## Counting instances in the delivered export — read this before you tally

**The Datumaro export contains 30 annotations across 10 images. It does not contain 30 distinct
objects.**

**On `09_segmentation`, two `fish_mask` instances describe the same fish.** `38` is the manual mask;
`36` is the SAM 3 mask of the identical animal. **They exist as a deliberate pair** so that manual and
model-assisted segmentation could be measured against each other on identical input — the comparison
that produced **11 min 41 s versus 52 s** and **IoU 0.9605**, documented in
`platform_comparison_log.md`.

**So the frame holds one fish and two annotations.** A reader counting `fish_mask` instances will
over-count animals by one unless this is stated, and **the same mistake has already been made once
by someone with full access to these files.**

**Distinct annotated objects across the run: 29. Annotation records: 30.**
