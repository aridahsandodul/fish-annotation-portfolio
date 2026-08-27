# Fish Annotation Portfolio

Documented annotation work on underwater fish imagery. Ten frames, four annotation types,
two platforms, and the reasoning behind every rule.

**Public dataset:** https://universe.roboflow.com/arid-dodul/aquaculture-fish-segmentation

---

## What this is

Most annotation portfolios show finished labels. This one shows the decisions.

Ten frames of marine fish - bigeye trevally, mojarra and northwest black bream - annotated with
**bounding boxes, polygons, keypoint skeletons and semantic masks**, under a guideline document
taken through **sixteen revisions**, ten of them traceable to a specific frame that broke the
previous version.

**30 annotation records across 10 images. 29 distinct objects** - one frame carries the same fish
twice, manually and by SAM 3, for the assisted-labeling comparison.

## Start here

| File | Why |
|---|---|
| **`edge_case_log.md`** | **The centrepiece.** Twelve judgment calls, each with the question, my reasoning, the decision taken, and whether the guidelines were at fault. Screenshots throughout. |
| **`annotation_guidelines_v4.md`** | The rules, content at v5.3. Includes the revision table: what changed, and which frame forced it. |
| **`platform_comparison_log.md`** | CVAT versus Roboflow, measured. Includes the defects each platform does not document about itself. |
| **`SCHEMA_README.md`** | The schema as built, including what is deliberately absent and why. |

## The schema, and why it is built this way

Five classes, three attributes, five keypoints. **Classes with attributes, not compound labels.**

Compound labels (`fish_lateral_full_straight`) are faster and make missing attributes structurally
impossible. They were rejected because **attribute drift becomes unmeasurable** - you cannot ask
whether your judgment of `posture` moved between the first frame and the last if `posture` only ever
existed as a fragment of a label name. Measuring drift was the point.

Two design decisions worth reading in full in `SCHEMA_README.md`:

- **No `lateral_left` / `lateral_right`.** Facing direction is a property of the fish's position in
  the frame, not of the fish. **Any horizontal-flip augmentation silently inverts the label.** An
  attribute a routine augmentation can falsify should not be in the schema.
- **`head_on` and `tail_on` collapsed to `axial`.** On turbid footage the two are frequently
  indistinguishable, and a value pair annotators cannot separate reliably is a drift generator.

## The inclusion rule

**An instance is annotated only where orientation, visibility and posture can each be assigned with
confidence.**

Tying inclusion to *"can I fill the schema"* rather than to blur or size makes the rule
self-enforcing and identical between annotators. Proxies need their own thresholds, which need their
own judgment calls, which is where two annotators start to drift apart.

Below-threshold instances are **counted and logged, not silently dropped.**

## Verification

Eight checks were run **in code against the delivered export**, not by eye: missing attributes,
cross-attribute constraint violations, degenerate geometry, undersized polygons, class counts per
frame, keypoint completeness, export-format fidelity, and MD5 stability across repeated exports.

That last one found a defect: **CVAT caches exports.** A file requested as final came back
byte-identical to one two rounds old, same MD5, different filename, no warning. It is documented in
`platform_comparison_log.md` alongside three other undocumented behaviours found the same way.

## Source data and licence

**Two datasets, both CC BY 4.0, used for different parts of this work.**

### Images - the ten annotated frames

**UnderWater Fish Detection**, Roboflow Universe, v6, generated 30 November 2023.
Licensed **CC BY 4.0**.
https://universe.roboflow.com/underwater-fish/underwater-fish-detection-izi1l

The ten frames are marine species: *Caranx sexfasciatus*, *Gerres* sp. and
*Acanthopagrus palmaris*.

**The dataset's original labels were not used.** Every box, polygon, keypoint, mask and attribute
in this repository is my own, produced from scratch under the guidelines here.

Per-frame original filenames, recorded before renaming, in `SOURCE_FILENAMES.txt`.

### Video - prepared, not yet annotated

**Tilapia-RAS Dataset: Underwater Videos and Polygon-Annotated Frames with Physicochemical Metadata.**
Zenodo, DOI **10.5281/zenodo.17518786**. Licensed **CC BY 4.0**.
Origin: commercial RAS facility integrated with hydroponics, Queretaro, Mexico.

A 300-frame clip is prepared and loaded, and `video_annotation_guidelines_v6.md` and
`cvat_labels_video.json` define the tracking schema. **The tracking run itself is not done. No video
annotations appear in this repository.**

**That dataset ships with 3,520 polygon-annotated frames. They were not opened or used.**

Clip selection, licence detail and provenance in `VIDEO_SOURCE_PROVENANCE.txt`.

## Contents

```
annotation_guidelines_v4.md      rules, content at v5.3
video_annotation_guidelines_v6.md tracking extension: track IDs, keyframes, re-identification
edge_case_log.md                 12 escalations with screenshots and resolutions
platform_comparison_log.md       CVAT vs Roboflow, measured
SCHEMA_README.md                 the schema as built
SOURCE_FILENAMES.txt             image provenance and CC BY 4.0 attribution
VIDEO_SOURCE_PROVENANCE.txt      video dataset, licence, clip selection
cvat_labels.json                 image schema
cvat_labels_video.json           video schema, all attributes mutable
platform_schemas/                schema conversions for five other platforms
Fish Portfolio - CVAT run/       the 10 source images
ScreenShots/                     13 edge-case screenshots
CVAT exports/                    Datumaro and COCO, both verified
Roboflow export/                 COCO segmentation, 5 frames
```

---

**Arid Ahsan Dodul** - data annotator, Dhaka. Image, video, audio and text annotation.
