# Annotation guidelines: fish detection, behavior, and morphology

Version 5.3 — written before annotation begins, as guidelines should be.
Author: Arid Ahsan Dodul
Dataset: UnderWater Fish Detection (Roboflow Universe), v6 — https://universe.roboflow.com/underwater-fish/underwater-fish-detection-izi1l — CC BY 4.0.
  Attribution is a licence condition. Annotations in this portfolio are my own, created from scratch; the dataset's original labels were not used.
Platforms: **CVAT — run complete and delivered. Roboflow — run complete 26 Aug 2026**, 5 frames,
  3 classes, 14 annotations, COCO Segmentation exported and verified against the CVAT export,
  public dataset on Universe, **seven numbered findings, a three-defect export audit and two follow-on observations logged**. Supervisely, Label Studio, Labelbox and
  SuperAnnotate remain **planned comparison runs, not yet performed**; the empty columns in  
  `platform_comparison_log.md` are where their findings will go.
Sample: 10 images, identical across every run
Annotation types: bounding box, polygon, keypoint, semantic segmentation

---

## Purpose

Label fish and contextual objects in underwater and aquaculture footage so a detection model can learn fish position, orientation, visibility and body morphology. These rules exist so that two annotators working separately produce the same labels on the same image.

The rules are written to be applied identically across six platforms and four annotation types. Any rule that depends on a specific tool's interface is a bad rule, and none appear below.

Anything this document doesn't cover is an edge case. Log it, don't guess it.

---

## Step 0. Before touching the data

1. Record dataset name, source URL, and licence. Confirm the licence permits re-annotation and public display.
2. Credit the dataset in the portfolio.
3. Fix the sample: **the same 10 images**, in the same order, across every platform.
4. Assign each image its annotation type using the split below, and **keep that assignment fixed across all platforms**.

---

## The image split

| Images | Annotation type | Why this type |
|---|---|---|
| 1 to 3 | **Bounding box** | Baseline. Fast, universally supported, the comparison anchor. |
| 4 to 6 | **Polygon** | Fish sit at angles; a box around a diagonal fish is mostly water. Polygon measures the animal. |
| 7 to 8 | **Keypoint** | Body-axis landmarks support posture and length estimation without full masks. |
| 9 to 10 | **Semantic segmentation** | Pixel-level fish versus background. The expensive one, and the one free tiers most often gate. |

Choose which image gets which type **before you start**, and write it down. Reassigning mid-run breaks the comparison.

**The split applies to the `fish` class only.** It exists to demonstrate four annotation types on the same subject across six platforms, and the fish are that subject. `context_object` is not part of the comparison and takes whatever shape bounds it sensibly — normally a polygon for thin or diagonal objects such as survey poles, a box for compact ones.

A frame's assigned type never requires a geometrically meaningless annotation. Where it appears to — a five-point fish skeleton on a light fixture, say — the rule is being applied past its scope.

---

## Classes

**1. fish** — any individual fish identifiable as a fish by shape or silhouette.
**2. context_object** — **human-introduced objects only**: netting, cage structure, feed pellets or clouds, equipment, instruments, measurement markers and scale bars.

Naturally occurring structure — mangrove root, rock, coral, sediment, vegetation — is background, however prominent it is in the frame. The criterion is *did a person put it there*, not *is it structure*. Where natural structure hides a fish, that is already recorded on the fish as `visibility`; it does not need an object of its own.

`context_object` carries no attributes. The three attributes apply to `fish` only.

Water, light shafts, sediment and bubbles are background. Never labeled.

---

## Schema design: why classes and attributes, not compound labels

There are two ways to encode this task, and the choice has consequences worth stating before the rules that follow.

**Compound labels** put the attribute inside the label name, so a project defines labels like `fish_lateral_full_straight` and an annotator picks one. **Classes with attributes** — the design used here — defines one `fish` class and attaches `orientation`, `visibility` and `posture` as separate fields.

Compound labels are faster in production. One selection per object, no second interaction, no attribute panel to open. They also make one error class structurally impossible: **an annotation cannot be missing its attributes, because the attributes are the label.** That is a real safeguard at volume, and it is why high-throughput pipelines often prefer them.

The cost is combinatorial. Three attributes with four, three and three values respectively would require 36 labels to express what three fields express here, and every new value multiplies the list again. More importantly for this project, compound labels cannot be queried by attribute after the fact. You cannot ask "did my judgment of `posture` drift between the first image and the last" if `posture` only ever existed as a fragment of a label name.

**This project uses classes with attributes, deliberately, because measuring attribute drift is one of its objectives.** Drift is the characteristic error of high-volume annotation: the same visual situation labeled one way early in a batch and another way late, invisible unless someone looks for it. Detecting it requires attributes that exist as separable fields.

The tradeoff accepted in return is that incomplete annotations become possible. An annotation can now exist with a shape but no `posture` value. That is why "missing attributes" is the first row of the verification pass, and why the annotation threshold is defined in terms of whether all three attributes can be assigned.

A schema is not neutral. It decides which errors are possible and which are unthinkable, and choosing one means choosing which errors you will have to look for.

---

## Attributes (apply to every `fish`, in every annotation type)

Every `fish` annotation carries three attributes regardless of geometry.

| Attribute | Values |
|---|---|
| `orientation` | `lateral`, `oblique`, `axial`, `indeterminate` |
| `visibility` | `full`, `partial`, `heavy_occlusion` |
| `posture` | `straight`, `curved`, `indeterminate` |

Where a platform allows attribute values to be constrained to a fixed list, constrain them. Where it only offers free text, record that in the comparison log. That difference is what prevents drift at volume, and most published tool comparisons never mention it.

### Which attribute owns a hidden body part

**A part hidden by the fish's own pose is recorded in `orientation`. `visibility` records only what an external occluder or the frame edge takes away.**

A tail-on fish whose head sits behind its own body is `orientation: axial`, `visibility: full` — nothing is in front of the animal, and the whole animal is in frame. The same fish with a net strut across its flank is `visibility: partial`, whatever its orientation.

The two attributes answer different questions. `orientation` describes the animal's pose; `visibility` describes what the image failed to capture. Collapsing them makes both unusable — a model cannot learn pose from a field that also encodes occlusion, and cannot learn occlusion from a field that also encodes pose.

**Consistency check.** `orientation: lateral` and an unreadable head are contradictory: a broadside fish shows its head. If the head is missing, either the orientation is not lateral, or something external is hiding it. One of the two attributes is wrong.

### `orientation: axial` implies `posture: indeterminate`

**Where `orientation` is `axial`, `posture` is `indeterminate`. Always.**

`posture` measures curvature along the body axis. When that axis points at the camera, curvature projects to nearly nothing and a straight fish is indistinguishable from a bent one. `straight` is a positive claim about the animal, and on an axial fish there is no evidence for it.

This is stated as a hard constraint rather than a judgment call for two reasons. It removes a decision that has no defensible answer, and it is checkable by query rather than by eye: **any instance with `orientation: axial` and a posture other than `indeterminate` is a verification failure.**

`oblique` stays case-by-case. A partially foreshortened body still shows curvature.

> Practical note: most tools default `posture` to the first value in the list. A frame where every instance reads `posture: straight` is far more likely to be an untouched dropdown than a school of unusually rigid fish. Treat a uniform attribute column as a defect until proven otherwise.

### Silhouette proportions are evidence for orientation

Where surface detail is unreadable — depth, turbidity, motion — the shape of the silhouette is still admissible evidence.

- A **markedly narrow** silhouette supports `axial`. A fish presenting its body axis to the camera is narrow by construction, so the proportions are the observation.
- A shape with **no discernible long axis** is `indeterminate`. There is nothing to read.

This exists because without it two annotators will split the same blurred instances differently while both believing they are following these rules. Inferring from proportions is legitimate; inferring from the box you have already drawn is not.

### Why `axial` rather than `head_on` / `tail_on`, and why no left/right

`orientation` has four values, not six, and the omissions are deliberate.

**No `lateral_left` / `lateral_right`.** Facing direction is a property of the fish's position in the frame, not of the fish. Any horizontal-flip augmentation — standard in every detection training pipeline — silently inverts the label and turns clean data into contradictory data. An attribute that a routine augmentation can falsify should not be in the schema.

**`axial` instead of `head_on` and `tail_on`.** On turbid footage the two are frequently indistinguishable, and a value pair that annotators cannot separate reliably is a drift generator. Collapsing them costs a distinction that is rarely readable and buys agreement between annotators. Where the tail fan or the eyes happen to make the direction obvious, that information is still recoverable from the geometry; it does not need its own field.

---

## Geometry rules by type

### Bounding box (images 1 to 3)

- Box the full visible extent including fins and tail. Axis-aligned, tight, no padding.
- **Minimum 12 x 12 pixels.** Smaller is background. Below that size annotators cannot agree, so the rule protects consistency rather than coverage.
- Overlapping fish get one box each.
- Fish crossing the frame edge is boxed to the edge; `visibility` records the loss.

### Polygon (images 4 to 6)

- Trace the **visible outline** of the animal. Do not trace the imagined outline of hidden parts.
- Include fins and tail. Exclude water visible between fin rays — follow the fin's outer edge rather than tracing every ray.
- **Vertex density follows curvature, not a fixed count.** Place points where the outline changes direction; leave straight runs bare. As an indication and *not* a cap: a simple fusiform fish in flat profile lands around **15 to 25**; a deep-bodied fish with a forked caudal, falcate fins and a notched dorsal lands around **40 to 55**. A shape that needs 50 points to trace honestly should get 50.
- Under-vertexing to hit a budget rounds off concavities — most damagingly the caudal fork, which is the main reason a polygon beats a box on this data. It also shrinks the traced area, which silently *inflates* any area-derived figure taken from the result, including the water fraction reported below. A budget that biases your own measurement in your favour is worse than no budget.
- A dense pile-up of points within a few pixels is a slipped click, not detail. Delete them. Over-tracing and mis-clicking are different problems and only the second is a defect.
- Occluded fish: trace only what you can see, producing an open-looking shape. Do not bridge across the occluder.
- **The boundary-ownership test (polygons and masks only).** Before tracing an occluded fish, ask what fraction of the boundary you would draw belongs to *the animal* rather than to *the thing in front of it*.
  - **Mostly animal** — trace it, `visibility: heavy_occlusion`.
  - **Mostly occluder** — do not annotate it. Count it, and record the reason as occluder-dominated boundary, not as low confidence.

  A boundary that follows the occluder encodes the occluder's silhouette. That is a *confidently wrong* label rather than an imprecise one, and confidently wrong labels are worse for a model than missing ones.

  **Bounding boxes are exempt from this test.** A box asserts location, not shape, so it tolerates occlusion a polygon cannot. This is the one place where the four annotation types genuinely need different rules, and it means an instance can legitimately be annotatable as a box and not annotatable as a polygon.
- **A polygon requires a resolvable boundary, not merely a resolvable fish.** Blur, depth and turbidity can leave an object plainly identifiable as a fish while removing its edge entirely. Where the outline would be *estimated* rather than *observed*, count the instance instead of tracing it.

  This is independent of size: an instance can sit well above the pixel floor and still have no boundary to trace. It is also independent of the attribute threshold — a fish can carry all three attributes confidently and still have no traceable edge.

- Minimum size rule applies as for boxes.

**Three distinct reasons to decline a polygon**, recorded separately in the log because they are separate findings about the data:

| Reason | Test | What a bad label would encode |
|---|---|---|
| Attribute confidence | Can all three attributes be assigned? | Invented attributes |
| Boundary ownership | Is most of the boundary the animal or the occluder? | The occluder's silhouette |
| Boundary resolvability | Can the edge be seen, or would it be estimated? | A silhouette on no evidence |

All three produce *confidently wrong* labels rather than imprecise ones, which is why each is a decline rather than a caveat.

**Record for the writeup:** on at least one diagonal fish, note roughly what fraction of its bounding box was water. That is the concrete argument for polygon over box on this data.

### Keypoint (images 7 to 8)

Five points per fish, in this order every time:

| # | Point | Placement |
|---|---|---|
| 1 | `snout` | Foremost point of the head |
| 2 | `eye` | Centre of the visible eye |
| 3 | `dorsal_origin` | The dorsal fin's **anterior insertion** — see the note below |
| 4 | `pelvic_origin` | The **pelvic** fin's anterior insertion. Not the anal fin — see below |
| 5 | `tail_fork` | Centre of the tail fork, or tail tip if not forked |

- A point that is hidden is marked **occluded**, not guessed at, and not skipped. If the platform has no occluded flag, record that in the comparison log.
- If fewer than 3 of the 5 points are visible, skip the fish and log it as an edge case.
- Order matters. Same sequence every fish, every platform.

**What `origin` means.** The **anterior insertion**: the forwardmost point at which the fin enters the body, nearest the snout. *Not* the centre of the fin base, and *not* the fin's highest or outermost point. `origin` is an anatomical term of art and reads ambiguously to anyone who does not already know it; stating it plainly is what stops two annotators placing the same landmark 20% of body length apart.

**Telling the pelvic fin from the anal fin.** The pelvics are paired, sit just below and slightly behind the pectoral base — roughly beneath the dorsal origin — and are well forward. The anal fin is a single median fin further back, between the pelvics and the caudal peduncle. On pale fish in good light this is obvious. On dark-finned sparids in shadow it is not, and it is the single most likely landmark confusion in this schema.

**Known gap: there is no way to record identity uncertainty about a landmark.** The occluded flag does not cover the case where a fin is plainly visible but *which* fin it is remains uncertain. A per-point `uncertain` flag, distinct from `occluded`, would close it. It is deliberately **not** added mid-batch, because changing the schema partway through invalidates the attribute-drift comparison this run exists to produce.

### Semantic segmentation (images 9 to 10)

- Paint every pixel belonging to a fish as `fish`. Everything else is background.
- **This is class-level, not instance-level.** Two touching fish form one continuous `fish` region. Do not attempt to separate them.
- Fins included. Water visible between fin rays is background, so at the fin edge follow the fin.
- **`context_object` is annotated wherever it appears, in every frame, using whatever shape bounds it sensibly.** It is not conditional on proximity to a fish, and not conditional on the frame's assigned annotation type. A class annotated only when convenient is worse for a downstream user than one consistently included or consistently excluded.
- Brush and eraser at moderate size; do not chase single pixels. Consistency beats precision here.

---

## Ordering and instance IDs

- Work **left to right, then top to bottom** within each frame. A consistent sweep is what makes a second-pass diff meaningful and is the cheapest defence against missed instances.
- Let the tool number instances however it does natively. Do not fight it for a per-frame reset; it buys nothing.
- **Do not use tool-assigned instance numbers as identifiers in documentation.** In CVAT the displayed number is a position in the object list, so deleting any object renumbers everything after it — silently, and with no warning. Any log, report or edge-case note that cites bare instance numbers captured mid-run will stop pointing at the right objects the first time something is deleted.
- Refer to instances by **frame plus description** (species, position in frame, or dimensions). Where a stable numeric identifier is genuinely needed, take it from the **final** export, not an intermediate one.

---

## The annotation threshold

**A fish is annotatable only if all three attributes can be assigned with confidence.**

If you cannot tell its orientation, cannot judge its visibility, or cannot read its posture, it is below threshold. Do not annotate it, and do not guess at values to make it fit.

This single rule does most of the work on aquaculture footage. A typical sea-cage frame has one or two fish in focus and thirty or more behind them at progressively greater depth and blur. Trying to annotate every discernible shape makes the task unbounded and, worse, produces labels whose attributes are invented rather than observed. A model trained on invented attributes learns noise.

**Counted and excluded are not the same thing.** A shape known to be a fish but too degraded to carry attributes is **below threshold, and counted**. A shape whose identity cannot be established at all is **excluded, and not counted** — it goes in the log's note column instead. The below-threshold figure is meant to tell a downstream team how much *fish* their model will never learn from; padding it with possible netting, root or sediment makes it useless for that purpose.

**Record instead of annotating.** For each image, note the approximate number of below-threshold fish in the edge-case log. That count is useful information about the data — it tells a downstream team what proportion of the frame their model will never learn from — and it takes seconds rather than hours.

**Why the threshold sits at the attributes rather than at blur or size:** blur and size are proxies, and proxies need their own thresholds, which need their own judgment calls. Tying inclusion to "can I fill the schema" makes the rule self-enforcing and identical for every annotator. Two people applying it independently reach the same answer.

The 12 x 12 pixel minimum still applies as a floor. In practice most sub-threshold fish fail the attribute test before they fail the size test.

---

## Decision rules for common ambiguity

**Blurred motion and depth-of-field blur.** Run the annotation threshold. If the blur still permits all three attributes, annotate it. If it doesn't, the fish is below threshold and gets counted, not boxed. This replaces any judgment about "how blurry is too blurry", which is a question with no stable answer.

**Dense schools.** Apply the annotation threshold first: most background-school fish will fail it. Annotate the ones that pass, working left to right and top to bottom so none are missed, and log the approximate count of those that don't. In segmentation, dense schools become one region by design, so the threshold applies to whether the region is identifiable as fish at all.

**Head not visible.** Ask why before choosing an attribute. Hidden by the fish's own pose is `orientation`; hidden by something in front of it, or by the frame edge, is `visibility`. See the attribute rules above.

**Reflections and shadows.** Never annotated, in any type.

**Overlap with netting.** Net is `context_object`. Fish behind it is still `fish`, with `visibility` set by how much is hidden.

**Dead or motionless fish.** Annotated normally. Posture recorded as observed. Health assessment is not part of this task.

---

## Reviewing annotations

**Review at display settings comparable to those used for annotation.** A reviewer working at different brightness, contrast or gamma will report well-supported annotations as unsupported — and those false defects are expensive, because the natural response to a challenge is to delete rather than defend.

- Where an annotation was produced using display adjustment, **record that with it**, so a reviewer knows to match the setting before judging it.
- Adjusting the display is legitimate technique. It changes nothing about exported data, and refusing it means discarding signal that is genuinely present in the pixels.
- **An annotation is deleted because it is wrong, never because it was questioned.** A challenge that is withdrawn leaves the annotation standing, and the exchange is logged.

---

## Escalation criteria

Stop and log rather than deciding alone when:

- A case doesn't fit any attribute value cleanly
- Two rules here appear to conflict
- The same ambiguity has come up three or more times, which means this document has a gap
- The platform will not let you perform the assigned annotation type
- Image quality makes the frame unlabelable

---

## Running this across five platforms

**Order:** CVAT (baseline) → Roboflow → Supervisely → Label Studio → Labelbox → SuperAnnotate.

Roboflow sits second because its free Public plan publishes to Roboflow Universe, so your public portfolio link exists early. Supervisely sits third because its free Community tier is confirmed open and it handles segmentation well, making it the most likely of the commercial tools to complete a full four-type run.

**Supervisely bonus experiment.** Supervisely ships SAM2 for model-assisted segmentation. Repeating the assisted-labelling measurement there turns a single-platform result into a cross-platform one, which is the question hiring teams are actively asking in 2026.

> **Corrected 27 August 2026. The original instruction here was to segment image 9 manually and image 10 with SAM2. Do not do that.** The CVAT run tested it and `platform_comparison_log.md` records why it fails: comparing manual on 09 against the model on 10 gives **13.5×**, which is frame difficulty reported as model performance. Running both methods on **the same frame** gives the honest **9.4×**. The original wording predates that finding.

**Design.** Segment **09 manually**, then **09 with SAM2**, then **10 with SAM2**. Same frame, same fish, same boundary for the paired comparison; the second model frame gives the easy-versus-hard spread. Record every time and every correction count.

**Controls, which must match the CVAT run or the two platforms are not comparable:**

- Familiarisation pass first on **`03_bbox`**, a frame used in no measurement, and delete that practice mask. Measured frames are approached cold.
- The clock runs from **tool selection through final correction**, not from first click.
- Prompt SAM2 with a **bounding box only**. Disable any label-name-as-text-prompt option: `fish_mask` is a schema artifact, not a description of the animal, and it would confound a poor result.
- Leave **hole-filling off**, so holes remain visible and countable rather than silently repaired.

**Hold constant:** same 10 images, same type assignment per image, same class and attribute names, same order of work.

**When a platform blocks a type.** Attempt it. If the free tier will not allow it, record exactly what happened in the comparison log and move to the next type. **This is a finding, not a failure.** Which platforms let you do polygon, keypoint and segmentation without paying is genuinely useful information that vendor comparisons never publish.

**Expect this to take longer than a day.** Four annotation types across five platforms is roughly 2 to 2.5 hours per platform. Finish CVAT and Roboflow completely before worrying about the rest — that combination already gives you a full-range demonstration plus a public link.

---

## Definition of done

1. All 10 images annotated in their assigned type, on every platform attempted.
2. Every `fish` annotation carries all three attributes.
3. Keypoints in fixed order, occluded points flagged rather than guessed.
4. Edge-case log filled during the CVAT baseline run.
5. Verification pass run per platform, per type.
6. Comparison log complete for platforms attempted, and honestly empty for those not.
7. Guideline gaps written up as proposed revisions.

---

## Revision history

| Version | Change | Reason |
|---|---|---|
| 1.0 | Initial guidelines | Written before annotation began |
| 2.0 | Licence step, platform-agnostic framing | Multi-platform comparison added |
| 3.0 | Extended to five platforms, sample fixed at 6 to 8 | Scoped to a single day |
| 4.0 | Sample raised to 10 images; polygon, keypoint and semantic segmentation added with per-type geometry rules and a fixed image split | Boxes-only portfolio contradicted a resume claiming polygon, keypoint and segmentation experience. Scope now exceeds one day; CVAT and Roboflow prioritised. |
| 4.1 | Added the annotation threshold: a fish is annotatable only if all three attributes can be assigned with confidence. Blur and dense-school rules rewritten to defer to it. Supervisely added as a sixth platform with a SAM2 manual-versus-assisted experiment. | Sea-cage footage contains far more discernible fish than annotatable ones. Without a threshold the task is unbounded and attributes get invented. Tying inclusion to schema completeness makes the rule self-enforcing and reproducible between annotators. |
| 4.2 | Added the schema design section: rationale for classes-with-attributes over compound labels, and the error tradeoff each design implies | A schema determines which errors are structurally possible. Compound labels make missing attributes impossible but drift unmeasurable; separable attributes invert that. The choice needed stating, since the verification pass and the threshold rule both follow from it. |
| 4.3 | Split responsibility between `orientation` and `visibility`: a part hidden by the fish's own pose belongs to `orientation`, a part hidden by an external occluder or the frame edge belongs to `visibility`. Added the lateral-plus-no-head consistency check, and the rationale for a four-value orientation vocabulary. | Raised as edge case 1 on the first annotated instance. v4.2 never said which attribute owned "head not visible", so two annotators could reasonably record the same fish as `visibility: full` and `visibility: partial`. That is a definition gap, not an annotator error. |
| 4.4 | `orientation: axial` now implies `posture: indeterminate`, as a checkable constraint rather than a judgment call. Silhouette proportions admitted as evidence for orientation where surface detail is unreadable. Separated "below threshold and counted" from "identity unestablished and excluded". | All three came out of frame 01_bbox during the CVAT baseline run, logged as edge cases 2 to 4. The first was found by noticing that 7 of 7 instances carried the tool's default posture value. The second was a rule already being applied consistently but never written down, which is the kind of gap that only shows up between two annotators. The third was a counting question the threshold rule had not anticipated. |
| 4.5 | `context_object` redefined by principle (human-introduced) rather than by example, with natural habitat structure explicitly background. Added an ordering and instance-ID section; IDs are per-task, not per-frame. | Raised on 02_bbox, edge case 5. The class had been defined by a list of examples that were all artificial without ever saying that was the criterion, which on mangrove footage is a coin flip between labelling nothing and labelling most of the frame. The ID and ordering conventions were being followed in practice but had never been written into this version at all. |
| 4.6 | Polygon vertex budget replaced with curvature-driven density and indicative ranges by body type; note added that under-vertexing biases area-derived measurements. | Raised on 04_polygon, edge case 6. The 12-to-25 budget was written for a generic fusiform fish and could not be met on a carangid without rounding off the caudal fork — that is, without deleting the exact feature the polygon exists to capture. A rule that has to be broken to do the job correctly is a broken rule. |
| 4.7 | Added the boundary-ownership test for polygons and masks: an occluded instance whose traced boundary would mostly follow the occluder is counted rather than annotated. Boxes explicitly exempt. | Raised on 04_polygon, edge case 7. The threshold had been stated once and applied to all four annotation types identically, on the assumption that occlusion costs each type the same. It does not. A box asserts location and survives occlusion; a polygon asserts shape and, traced along an occluder, asserts the wrong one. |
| 4.8 | Added the resolvable-boundary requirement for polygons, and consolidated the three distinct reasons to decline a polygon into one table. | Raised on 04_polygon, edge case 8. An instance was traced as a featureless oval around a blur and given three confident attributes, when the same visual situation four frames earlier had correctly been called indeterminate. That is attribute drift, caught in this batch's own output, on the annotation type where a wrong shape costs the most. |
| 4.9 | Corrected the instance-ID guidance. Tool-assigned instance numbers are not stable identifiers and must not be cited in documentation; references go by frame plus description instead. | The v4.5 rationale was wrong. It claimed a per-task number identifies an instance without naming its frame. CVAT renumbers on deletion, so after four objects were removed during this run every later number had shifted by four and the references written into the edge-case log no longer pointed at the objects they described. Caught by noticing the same polygon displaying a different number an hour apart. |
| 5.0 | Scoped the image split to the `fish` class. `context_object` no longer follows the frame's assigned annotation type. | Raised on 07_keypoint, edge case 9. Context objects had been following the frame type by habit — boxes on the bbox frames, polygons on the polygon frames — which held until the first keypoint frame, where it would have required placing `snout` and `tail_fork` on a survey pole. A rule about the experiment was being read as a rule about the frame. |
| 5.1 | Defined `origin` explicitly as a fin's anterior insertion. Added guidance for distinguishing the pelvic fin from the anal fin. Recorded the absence of a per-point identity-uncertainty flag as a known gap, deferred to the next batch. | Raised on 08_keypoint, edge case 10. Two of five landmarks needed three rounds of correction on the best-lit fish in the set — not because the image was hard, but because `origin` was an undefined term of art and the schema assumed a pelvic/anal distinction it never stated. Both failures were definitional rather than visual, which is the kind that survives into every future batch unless written down. |
| 5.2 | Removed the free-floating-equipment exemption from the segmentation section. `context_object` is annotated wherever it appears, unconditionally. | Raised on 09_segmentation, edge case 11. The exemption existed because a `context_object` on a segmentation frame was assumed to require a painted mask, which is slow for a thin diagonal pole. v5.0 decoupled context objects from the frame type, so the pole now takes a cheap polygon — but the exemption stayed behind after its justification had gone. A stale rule, not a missing one. First firing of the "two rules appear to conflict" escalation criterion. |
| 5.3 | Added a section on reviewing annotations: review at display settings comparable to annotation; record display adjustment alongside the work; annotations are deleted for being wrong, not for being questioned. | Raised on 04_polygon, edge case 12 — the only entry in the log recording a reviewer error rather than an annotator one. Two well-supported instances were twice reported as unsupported because review was conducted on screenshots taken at a diagnostic gamma that crushed the tones the fish occupied. The recommendation given was to delete them. |
