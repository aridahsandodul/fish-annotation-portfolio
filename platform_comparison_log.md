# Platform Comparison Log

> ## STATUS, 26 August 2026, before the Roboflow run
>
> **Tables A-F are blank in every column, including CVAT.** The CVAT run is complete and delivered,
> and its findings live in the dedicated sections further down — export fidelity, identifier
> stability, the SAM comparison — **but the comparison matrix itself was never filled for CVAT.**
>
> **DONE, 26 August 2026. The CVAT column is complete across all six tables.**
> **Every row carries how it is known:** `[measured]` a recorded number · `[obs]` seen working or
> failing · `[present, untested]` exists in the UI but never exercised · `[unknown]` never
> encountered · `[rated]` a judgment call with its evidence stated.
>
> **That marking is the most valuable thing in this document.** A comparison log that reports
> untested capability as capability is worth less than one that admits the gap. **Nine rows are
> `[unknown]` or `[present, untested]`, almost all because the run was solo — which is a completely
> respectable reason and is stated as such.**


Same 10 images. Same guidelines (v4.2). Same annotator. Six platforms.
Fill each column immediately after finishing that platform, while the friction is still fresh.

> ## ⚠ TIER MISMATCH, recorded 26 August 2026. Read before comparing column to column.
>
> **CVAT was run on the free tier. Roboflow auto-enrolled a new account into a 14-day Premium Trial**
> — private data, no dataset size limit, 10x augmentations, **Review Mode**, **Labeling History**,
> role-based access control, 15 credits.
>
> **These columns are therefore not like-for-like on anything tier-dependent**, and Section A's
> *"free tier limits that actually bit"* row **cannot be answered for Roboflow at all**: on a premium
> trial they do not bite. **Say that in the cell rather than writing "none".**
>
> **The trial is itself a finding worth stating in the verdict:** *a first-time evaluator of Roboflow
> does not see the free tier. Fourteen days of premium is what shapes the impression, and the tool a
> team would actually be given on day fifteen was never the tool under evaluation.*
>
> **Mark every Roboflow row that depends on the tier with `[premium trial]`.** In particular
> **Review Mode and Labeling History are premium-gated** — which maps directly onto Section C, where
> CVAT offers stages, assignees and Issues **on its free tier.** That contrast is a real finding and
> it is the opposite of what the raw feature list suggests.
>
> **Export everything before the trial ends.** Fourteen days from 26 August is **9 September.**
>
> **The CVAT cells below are summaries.** The full reasoning, with the basis stated for every row,
> lives once in **"The CVAT questionnaire"** further down. **Do not restate it here — the matrix is
> for scanning and comparing; the questionnaire is for the argument.**

---

## ⚑ ROBOFLOW, STRUCTURAL FINDING — one annotation type per project. Recorded 26 August 2026.

**Roboflow forces a single Project Type at creation and the types are mutually exclusive:**
Object Detection · Classification · **Instance Segmentation** · **Keypoint Detection** · Multimodal ·
Semantic Segmentation.

**This portfolio puts four annotation types on the same ten images. Roboflow cannot hold that in one
project.** Doing the full set would require **four separate projects, four separate Universe URLs and
four separate schemas, with no shared label set and no way to view one image's four treatments
together.**

**CVAT held all four in a single task under one label definition.**

**This is a larger finding than the missing per-instance attributes**, and it is decision-relevant in
a way a feature list is not: **a team standardising on Roboflow cannot keep one dataset with mixed
annotation types. They must fragment by type, and schema consistency across those fragments becomes
manual discipline.** Exactly the same failure mode as CVAT's free-tier project cap, arriving by a
different route.

**Decision taken for this run: one project, Instance Segmentation.** Polygons are the higher-skill
demonstration and carry the eight polygon frames plus the three mask frames — `fish_mask` was already
a forced compromise to polygon on this platform. **Bounding boxes and keypoints are not demonstrated
on Roboflow, and that absence is the finding, not an omission.**

### Roboflow, second structural finding — instance model versus class-level regions

**Roboflow's in-product guidance states: *"A single polygon should represent a single instance of a
subject."*** That is correct for instance segmentation and it **directly contradicts this project's
own mask rule**, which is class-level:

> *"This is class-level, not instance-level. Two touching fish form one continuous `fish` region.
> Do not attempt to separate them."* — `annotation_guidelines_v4.md`

**So `09_segmentation` and `10_segmentation` do not belong in an Instance Segmentation project at
all.** They were annotated in CVAT as continuous class-level regions. Placing them here forces a
choice between **splitting a region that was deliberately not split** — changing the data to suit the
tool — or **drawing it as CVAT did and violating Roboflow's own instance model.**

**Roboflow does offer a Semantic Segmentation project type. It is a different project.** So the
honest count for this portfolio on Roboflow is now **four projects, not one**: Object Detection for
the bbox frames, Instance Segmentation for the polygon frames, Keypoint Detection for the skeleton
frames, **and Semantic Segmentation for the mask frames.**

**Decision taken: the two mask frames are annotated as CVAT annotated them — continuous class-level
regions — and the violation of Roboflow's instance model is recorded rather than hidden.** Changing
the annotation to suit the platform would make the comparison measure the accommodation instead of
the platform.

### Roboflow, third finding — a default class is created from the project name and applied silently

**On `04_polygon.jpg`, the first four polygons drawn were all assigned to a class called
`aquaculture-fish-segmentation` — the project name.** No class was chosen, none was prompted for, and
nothing warned that every shape was landing in one auto-created bucket.

**CVAT cannot do this.** A label must exist before a shape can be drawn, because the shape type is
bound to the label definition. **Roboflow lets you annotate first and sort it out later, which is
faster and is exactly how a single-class dataset gets built by accident.**

**Roboflow does provide a guard: a `Lock Classes` checkbox on the Classes & Tags page, which prevents new classes being created during annotation. It is off by default.** So the trap is opt-out rather than absent, which is fairer to the platform than the first draft of this finding implied.

**Severity is low if caught on image one and high if caught on image five** — by then the fix is
re-classing every annotation in the batch rather than four. **Caught here on image one.**

**For the verdict: this is the same product posture showing up a third time.** Auto Label as the
default path, Smart Select recommended, train-early advice, and now a schema that materialises itself
rather than being declared. **Roboflow optimises for getting to a model quickly. Every one of those
choices trades schema discipline for speed**, and schema discipline is the thing this portfolio was
built to demonstrate.

### Roboflow, fourth finding — annotating an image does not put it in the dataset

**`04_polygon` and `05_polygon` were both annotated. The Dataset view showed `1 - 1 of 1`.**
**Annotation and dataset membership are separate states**, with an approval step between them, and
**an export draws from the Dataset, not from the annotation queue.**

**The failure mode is silent and it is severe:** finish all five frames, export, and receive a file
containing whatever happened to be approved. **Nothing warns you.** CVAT has no equivalent gap —
a task's annotations are the task's annotations, and export takes what is there.

**Check dataset membership before exporting, not after.**

### Roboflow, sixth finding — the "annotated" flag is not derived from whether annotations exist

**Directly observed, 26 August 2026, and this one is a data-integrity problem rather than a friction
point.**

`04_polygon.jpg` **carries four `fish_polygon` annotations, visible in the Layers panel.** The job
panel lists it under **Unannotated**. **A file with four committed shapes is flagged as having none.**

~~**The same panel reports "3 Annotated" in a four-image job whose other three members have not been
touched.**~~ **WRONG, corrected the same hour. `06_polygon`, `09_segmentation` and `10_segmentation`
had all been annotated; the "3 Annotated" count was accurate.** The error was Claude's: it inferred
those frames were untouched because it had not been shown them, and **treated absence of evidence in
its own view as evidence of absence in the world.**

**So the finding is narrower than first written, and the narrow version is still real: one image,
`04_polygon`, holds four committed annotations and is flagged Unannotated.**

**Whatever the flag tracks, it is not purely the presence of annotations** — four shapes exist on a
frame reported as having none. **The mechanism was not determined and should not be guessed at.**

**Why it matters:** dataset membership and export both key off job and image status. **An image can
hold finished work and still be treated as empty**, and if that status governs what reaches the
export, the work is silently dropped. **One frame in five, on a first run, found only by opening the
image.**

**Mitigation, and it is not optional on this platform: verify image by image before export. Do not
trust the progress bar, the Annotated/Unannotated tabs, or the job counts.**

**CVAT's equivalent claim is weaker but honest — its instance numbers renumber and its exports cache,
both of which this project already documented. Neither of those misreports whether work exists.**

> **Credit note, corrected 26 Aug.** The Create-New-Version button is labelled **"Uses Credits"**, but
> the workspace still read **0 / 15** after v1 was generated. **Version generation did not consume a
> credit; the label appears to apply to training.** An earlier claim that dataset versions are
> credit-metered was wrong and is withdrawn.

### Roboflow, fifth finding — a dataset cannot exist without a training split

The dataset view offers **Change Dataset Split**, and Roboflow assigns train / valid / test whether
or not the data is for training. **On five images the partition is meaningless** — three, one and one,
or similar — **but it is not optional.**

**CVAT has no concept of a train/validation split**, because CVAT is an annotation tool and the split
belongs to whoever trains the model. **On Roboflow it is structural: the unit of work is a training
dataset, not an annotation job.**

**That is the same product posture as the auto-label default and the self-materialising schema, but
embedded in the data model rather than in the UI.** It is the strongest single piece of evidence for
the verdict line: **Roboflow is a dataset pipeline that includes an annotation tool; CVAT is an
annotation tool.**

### Roboflow product posture — a verdict-level observation

Three separate signals in the first ten minutes, all pointing the same way:
**the default labelling path is Auto Label**, presented as *"Fastest"* with manual second ·
the in-product tips recommend **"Use our Smart Select tool"** · and **"Train a model early (after
~50 labeled images) to use Model Evaluation and Auto Label for faster labeling."**

**Roboflow assumes the user is the model owner, not a contract annotator.** CVAT hands you an
annotation tool; **Roboflow hands you a pipeline in which manual annotation is the cold-start cost to
be eliminated.** Neither posture is wrong. **They are aimed at different people, and only one of them
is aimed at the person doing the labelling.**

### Roboflow, seventh finding — the description editor was not locatable, and the platform's own agent was working from outdated documentation

> **RESOLVED 27 August 2026, and the heading was corrected at the same time.** This finding
> originally read *"the public description cannot be edited."* **That claim was too strong: the
> editor exists and the description is now published.** What the evidence below actually supports is
> that the control could not be found from the places a user would look, and that Roboflow's own
> assistant sent the user to an interface that no longer exists. **That part stands unchanged.**
> Resolution and two follow-on observations are at the end of this entry.

**26 August 2026. The Universe page reads "A description for this project has not been published
yet." The editor was not locatable.**

Checked: the workspace-card **⋮** menu (Copy Project Id, Move, Duplicate, Copy Images, Merge, Rename,
Change Owner, Make Private, Move to Trash — **no description option**) · Workspace Settings (billing,
credits, audit logs, team, API keys, datasources, trash) · the project sidebar · the Universe page
itself.

**Roboflow's own in-product Agent was asked and could not resolve it.** It first gave a five-step path
through *"Project Overview"*, then, shown a screenshot of the menu, replied: **"Project Overview is
not available in that three-dot menu — the documentation appears to describe an older interface.
Sorry about the incorrect direction."**

**The finding is not that a description is hard to edit. It is that the vendor's own assistant is
working from documentation that no longer matches the product, and said so.**

**Consequence for this run, and it is a real one:** the dataset is published under **CC BY 4.0** and
the Universe page declares the licence, **but the source attribution required by that licence has no
public home.** Attribution is a licence condition, not a courtesy. **Outstanding, carried forward:
either locate the editor, raise it with Roboflow support, or place the attribution wherever the
dataset is linked from.**

#### Resolution, 27 August 2026

**The editor was found and the description is published.** The CC BY 4.0 attribution now has a public
home on the dataset page, naming UnderWater Fish Detection v6 as the source. **The outstanding item
above is closed.** The finding about the vendor's assistant is unaffected: it was wrong, it was wrong
in a way it could not recover from, and it said so.

#### Follow-on 1 — the public page served stale content for at least half an hour, silently

**Measured, with the bound stated rather than a false precision.**

| Time | Observation |
|---|---|
| ~04:12 | Save time, inferred from the page's own *"Updated an hour ago"* read at 05:12 |
| **04:45** | **An independent fetch still returned *"A description for this project has not been published yet"* — and the stale *"Updated 9 hours ago"* timestamp alongside it** |
| 05:12 | The same fetch returns the full description |

**A query-string cache-buster did not defeat it**, so the caching is server or CDN side and keyed on
the canonical path. *"An hour ago"* is coarse, so **at least ~33 minutes is a floor, not a
measurement.**

**Why this is more than an annoyance.** The dataset URL is already published elsewhere. **Anyone
following it inside that window sees a dataset with no description at all** — precisely the
"abandoned project" impression the description exists to remove. **Roboflow shows no pending or
processing state; the page simply asserts the old content as current.**

#### Follow-on 2 — the social preview ignores the published description

After publishing, the page's `meta-description` and `og:description` **still read**
*"5 open source aquaculture-fish-segmentation images. aquaculture-fish-segmentation dataset by
arid-dodul."* Auto-generated from the project name, unchanged by the description.

**Every link preview of this URL therefore shows the generic string**, not the written description.
For a dataset used as a portfolio link that is the first impression, and **it is not reachable from
the project settings** so far as this check could determine. **Recorded as observed behaviour, not as
a limitation proven exhaustive.**

### Roboflow export audit — 26 August 2026, COCO Segmentation, version v1

**What survived, and it is a clean result: 5 images, 14 annotations, `context_object` 4 ·
`fish_mask` 2 · `fish_polygon` 8. Exact match to the project. Zero annotations missing segmentation
geometry.** No silent loss of the kind CVAT's COCO export produced when it dropped both skeletons.

**Three defects, all found by opening the file rather than by any warning.**

**1. A deleted class is still declared in the export.** `aquaculture-fish-segmentation` — the
auto-created class, **removed from Classes & Tags before generating the version** — appears in the
`categories` block of **both** annotation files with **zero instances**.

**This is the same defect this project criticised in CVAT's COCO output**, where `fish_keypoint` and
its five sublabels were declared while containing nothing. **Roboflow's case is arguably worse: CVAT's
was a format limitation, since COCO cannot express skeletons. Here the class no longer exists in the
project at all and the export declares it anyway.**

**2. Every filename is rewritten.** `04_polygon.jpg` becomes
`04_polygon_jpg.rf.46b89eefe5f4c11ac4510bd4ebc27291.jpg` — the extension folded into the stem and a
32-character hash appended.

**This severs the provenance chain.** `SOURCE_FILENAMES.txt` maps working filenames to the original
Zenodo dataset files, and that mapping is the CC BY 4.0 attribution trail. **After a Roboflow export,
no filename in the archive corresponds to anything in the provenance record**, and re-establishing it
requires the prefix rather than the identifier. **CVAT's export preserved filenames exactly.**

**3. Annotations are split across the train/valid partition.** Two `_annotations.coco.json` files,
12 annotations in one and 2 in the other. **Anyone wanting the complete annotation set must merge
them, and anyone who reads only the first file silently loses 2 of 14.** CVAT delivered one file.

**In fairness, two things Roboflow got right that CVAT did not:** the export honoured
*"no preprocessing, no augmentation"* exactly as configured, **and the images travel with the
annotations** rather than being an opt-in checkbox.

## A. Setup and ingest

| | CVAT | Roboflow | Supervisely | Label Studio | Labelbox | SuperAnnotate |
|---|---|---|---|---|---|---|
| Hosted / self-host / desktop | **Hosted — cvat.ai free tier** *[obs]* | | | | | |
| Free tier limits that actually bit | **Project cap of 1.** The video task had to be created outside any project because the image run already occupied the only slot | | | | | |
| Minutes: account → first annotatable frame | **~1 h**, mostly upload failure and skeleton-UI discovery. **<15 min on a second run** *[obs]* | | | | | |
| Upload: did 1.9 MB zip work first try? | **No.** The full-size set failed; a q80 recompress to 1.9 MB (`portfolio_10_compressed.zip`) was needed before uploads were reliable | | | | | |
| Label schema import (JSON? manual?) | **JSON.** Paste into Labels → Raw tab; confirms with an item count | | | | | |
| Attributes supported natively? | **Yes** — 3/class, fixed dropdowns via `input_type: select` *[obs]* | | | | | |
| Skeleton/keypoint template reusable? | **Untested** — exports cleanly, but only one skeleton task existed *[untested]* | | | | | |

## B. Annotation experience

| | CVAT | Roboflow | Supervisely | Label Studio | Labelbox | SuperAnnotate |
|---|---|---|---|---|---|---|
| Bounding box: keyboard-only workflow? | **Unknown** — mouse-driven throughout *[unknown]* | | | | | |
| Polygon: vertex editing quality (1–5) | **5 / 5** *[rated]* | | | | | |
| Polygon: point-density control | **Yes** — fixed point count and a Simplify toggle. **Both deliberately left off** *[obs]* | | | | | |
| Keypoints: occluded-point flag exists? | **Exists, never exercised** — all 10 landmarks visible, flag `2` *[untested]* | | | | | |
| Segmentation: brush quality (1–5) | **4 / 5** *[rated]* | | | | | |
| Zoom/pan responsiveness at 400% | **No problem encountered**, not benchmarked *[obs]* | | | | | |
| Undo depth / reliability | **Unknown** — never stress-tested *[unknown]* | | | | | |
| Copy annotation between frames | **Unknown** — 10 different scenes, no use case arose *[unknown]* | | | | | |
| Assisted labelling (SAM etc.) available free? | **Yes — SAM 2.0 and SAM 3.** 52 s / 74 s from a box prompt. **IoU 0.9605** vs manual *[measured]* | | | | | |

## C. QC and review

| | CVAT | Roboflow | Supervisely | Label Studio | Labelbox | SuperAnnotate |
|---|---|---|---|---|---|---|
| Built-in review/QA stage | **Exists** — stages + assignee. Never used, **solo run** *[untested]* | | | | | |
| Can a reviewer comment on an instance? | **Exists** — Issues panel. Never opened *[untested]* | | | | | |
| Issue tracking on frames | **Exists** — same Issues mechanism *[untested]* | | | | | |
| Annotation history / audit trail | **Unknown.** Note: **instance numbers are not stable identifiers to cite in one** *[unknown]* | | | | | |
| Consensus / multi-annotator agreement | **Unknown** — a solo run cannot produce inter-annotator agreement *[unknown]* | | | | | |

## D. Export

| | CVAT | Roboflow | Supervisely | Label Studio | Labelbox | SuperAnnotate |
|---|---|---|---|---|---|---|
| Formats offered | **Datumaro and COCO both exported and verified.** Full list yours to fill | | | | | |
| COCO export correct on first try? | **No error, and silently incomplete: 28 of 30. Both skeletons dropped** *[measured]* | | | | | |
| Do attributes survive export? | **Datumaro yes. COCO yes, into a non-spec key** — *the data survives the file, not necessarily the reader* *[measured]* | | | | | |
| Do keypoint visibility flags survive? | **Datumaro yes. COCO n/a — skeletons dropped, yet still declared in categories** *[measured]* | | | | | |
| Export includes images or annotations only? | **Annotations only, by choice.** Option exists *[obs]* | | | | | |

## E. Timing (minutes, honest) — a record, not a comparison

> ## WHAT THIS SECTION IS, AND WHAT IT IS NOT. Method note, 26 August 2026.
>
> **Setup time and annotation time measure different things and are never summed here.**
> Setup is a one-time cost dominated by first-contact friction and UI discovery. Annotation time is
> the recurring cost. **CVAT's "~1 h setup" was mostly upload failure and hunting for the skeleton
> control — that is a fact about onboarding, not about annotation ergonomics.**
> **Method from Roboflow onward: set every platform up first, in its own pass, then annotate.**
>
> **But front-loading setup does not rescue annotation time as a comparative metric, and this needs
> saying plainly.** One annotator running **the same ten images six times** gets faster at *the
> images*, not at the platforms. **By platform five he has drawn the same fish four times before.**
> **Practice contaminates every annotation figure after the first run, and no ordering fixes it.**
>
> **Therefore: annotation times below are a record, not a comparison.** Read each as a **floor** for
> that platform, and read later platforms as more contaminated than earlier ones.
> **Run order must be recorded** — without it the numbers cannot even be discounted correctly.
>
> **What in this document IS a clean comparison, because it is order-independent:**
> **Section A setup friction** — every platform is genuinely first-contact · **feature presence and
> absence** throughout · **Section D export fidelity** · **schema expressiveness** ·
> **free-tier limits.** **That is where the value of this log sits, not in speed.**
>
> **And the one speed measurement that is genuinely clean is already here:** manual **11 min 41 s**
> versus SAM 3 **52 s** on the same image, same annotator, same session, **IoU 0.9605.** Same
> conditions, one variable. **That is what a defensible timing comparison looks like.**
>
> **CVAT's own timings: only the two segmentation figures were stopwatch-measured. Everything else is
> recalled and marked `est`.**

| | CVAT | Roboflow | Supervisely | Label Studio | Labelbox | SuperAnnotate |
|---|---|---|---|---|---|---|
| Setup | ~60 `est` — includes the upload failures and the q80 recompress | | | | | |
| 3 bbox frames | ~10 `est` | | | | | |
| 3 polygon frames | ~20 `est` | | | | | |
| 2 keypoint frames | ~5 `est` — skeleton pre-defined | | | | | |
| 2 segmentation frames | **11 min 41 s MEASURED** for the manual mask, 1 frame · **52 s MEASURED** for SAM 3, 1 frame | | | | | |
| Verification pass | not separately timed | | | | | |
| Export | not separately timed | | | | | |
| **TOTAL** | **Not claimed, and no TOTAL should be filled for any platform.** Summing a setup cost and an annotation cost produces a number that measures neither | | | | | |

> **A correction worth recording.** An earlier draft put segmentation at *"~35 minutes for two frames."*
> **The measured figures total about 12½.** The gap is probably the practice pass on `03_bbox`, the
> context object and the corrections — **those belong on their own line, not folded into annotation
> time.** The measured numbers are more accurate, more defensible, and happen to be better.

### Run order — record this as you go. Without it the timings cannot be discounted.

| Order | Platform | Setup pass done | Annotation run done |
|---|---|---|---|
| 1 | CVAT | 8 Aug 2026 | 8 Aug 2026 |
| 2 | Roboflow | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |

**The tenth image annotated on platform six is the sixtieth time these ten frames have been worked.
State that in the verdict rather than letting a reader assume the times are comparable.**

## F. Verdict

| | CVAT | Roboflow | Supervisely | Label Studio | Labelbox | SuperAnnotate |
|---|---|---|---|---|---|---|
| Best at | **Schema expressiveness** — raw-JSON labels bound to shape types, constrained attributes, named-sublabel skeletons | | | | | |
| Worst at | **Trustworthiness of its own outputs and identifiers** — four undocumented defects, none of which announced itself | | | | | |
| Would I run a 5-person team on it? | **Not on this free tier. Probably yes self-hosted or paid — but this run tested none of that.** Three reasons in order of weight: **(1)** the free tier **caps projects**, and the workaround of tasks outside any project means **schema consistency becomes manual discipline rather than something the tool enforces** — on a five-person team that is exactly where quality goes; **(2) instance numbers are not stable**, so a reviewer writing "instance 14 is wrong" stops pointing at the right object the moment anyone deletes something; **(3)** stages, assignees and Issues all exist and **were never exercised** | | | | | |
| Public shareable portfolio link? | **No** | | | | | |
| Overall (1–5) | **Split, because one number hides the more interesting half.** **Annotation capability 4.5 / 5** — raw-JSON schema control, four annotation types, named-sublabel skeletons, constrained dropdowns, free SAM 3; nothing about the experience blocked the work. **Output trustworthiness 2.5 / 5** — four undocumented defects, **every one found by checking rather than by any warning.** **Scope: free tier, solo, image annotation only.** Not 5 on capability because of the project cap and an obscure skeleton control; not lower on trust because every defect was *discoverable* and Datumaro carried everything faithfully. **Nothing was lost — but nothing announced itself** | | | | | |

---

## Free-text notes per platform

### CVAT
- Project: "Fish Annotation Portfolio", task #2480009
- Known constraint hit: uploads truncate above ~2 MB on this connection → used 1.9 MB compressed zip.
-

### Roboflow
- Produces the public Roboflow Universe link. **Highest-value remaining artifact.**
-

### Supervisely
-

### Label Studio
-

### Labelbox
-

### SuperAnnotate
-

---

## Screenshots to capture on every platform

1. Label schema / class definition screen
2. A frame mid-annotation with attributes panel open
3. The polygon at 400% zoom showing vertex density
4. Keypoint skeleton on a fish
5. Export dialog with format selected

File naming: `<platform>_<01-05>_<description>.png`

---

## Export format fidelity (CVAT, measured 5 Aug 2026)

Both formats exported from the same task at the same point, 13 annotations across 4 frames.

| | Datumaro 1.0 | COCO 1.0 |
|---|---|---|
| Annotations preserved | 13 / 13 | 13 / 13 |
| Custom attributes preserved | 13 / 13 | 13 / 13 |
| Where attributes live | native `attributes` object | non-standard `attributes` key inside each annotation |
| Readable by a stock COCO loader | n/a | shapes yes, **attributes no** |

**The finding is subtler than "COCO loses attributes".** It does not — CVAT writes `orientation`, `visibility` and `posture` into every COCO annotation. But it writes them into a key the COCO specification does not define. `pycocotools` and anything else built strictly to spec will parse the shapes correctly and silently ignore the attributes, and any tool that round-trips through standard COCO will drop them on write.

So the data survives the *file* and may not survive the *reader*. A fidelity check that only opens the JSON and greps for the attribute names would conclude COCO is lossless here, and would be wrong about what happens downstream. Whether attributes reach a model depends on the consumer, not the export.

**Tested at the end of the run, and confirmed — with a twist.** COCO 1.0 **silently drops skeletons**. The final export carries 28 of 30 annotations; the two missing are both `fish_keypoint`.

| Label | Datumaro | COCO 1.0 | Delta |
|---|---|---|---|
| `fish_bbox` | 9 | 9 | 0 |
| `fish_polygon` | 8 | 8 | 0 |
| `fish_mask` | 3 | 3 | 0 |
| `context_object` | 8 | 8 | 0 |
| **`fish_keypoint`** | **2** | **0** | **−2** |

**The twist is what makes it dangerous.** The COCO file still declares `fish_keypoint`, `snout`, `eye`, `dorsal_origin`, `pelvic_origin` and `tail_fork` in its `categories` block. So the export advertises a full keypoint schema and contains **zero** instances of it. No error, no warning, no empty-category flag.

A consumer inspecting the schema concludes the dataset has keypoint annotations. A consumer counting instances finds none and reasonably assumes the annotator never did that work. Neither is told that the format discarded them.

**Practical rule:** a mixed-type task cannot be delivered as a single COCO 1.0 file. Either ship Datumaro, or ship COCO for the box/polygon/mask work and COCO Keypoints separately for the skeletons — and say which, because the file will not.

---

## Identifier stability

**CVAT:** instance numbers shown in the UI are list positions and renumber on deletion. Confirmed during this run — the same polygon displayed as 24 and later as 20 after four earlier objects were removed. Not usable as durable references.

Worth checking on each remaining platform, since it determines whether annotation notes and QA findings can cite instance numbers at all, and no vendor documentation mentions it either way.

| Platform | Renumbers on delete? | Notes |
|---|---|---|
| CVAT | **Yes** | display index, shifts by the number of prior deletions |
| Roboflow | | |
| Supervisely | | |
| Label Studio | | |
| Labelbox | | |
| SuperAnnotate | | |

---

## Image adjustment controls

Dark fins against dark substrate, and fish sitting in shadow, are common in this dataset. Raising display brightness and contrast resolved structures that were genuinely unreadable at default settings — on 08_keypoint it was what finally separated the pelvic fin from the anal fin.

This is annotation technique, not a workaround: adjusting the *display* changes nothing about the exported data, and declining to use it means guessing at landmarks that are actually present in the pixels.

Whether a platform offers these controls, and how far they go, is therefore a real quality factor. No vendor comparison publishes it.

| Platform | Brightness / contrast | Saturation / gamma | Notes |
|---|---|---|---|
| CVAT | **Yes** | | used on 08_keypoint to resolve pelvic vs anal fin |
| Roboflow | | | |
| Supervisely | | | |
| Label Studio | | | |
| Labelbox | | | |
| SuperAnnotate | | | |

---

## Manual versus model-assisted segmentation (CVAT)

Run on CVAT rather than deferred to Supervisely, because the tool was available when the segmentation frames came up and a measurement taken beats one planned. If Supervisely is reached later, repeating it there turns this into a cross-platform comparison of assisted labelling.

**Method.** A familiarisation pass was done first on **03_bbox**, a frame used in neither measurement, and that practice mask was deleted. Measured frames were approached cold. The clock covers tool selection through final correction. SAM 3 was prompted with a bounding box only; the "label name as text prompt" option was **disabled**, since the label string `fish_mask` is a schema artifact rather than a description of the animal and would have confounded any poor result. Hole-filling was left **off** so that holes would be visible and countable rather than silently repaired.

### Results

| | Manual | SAM 3 |
|---|---|---|
| **09_segmentation** — dark fish on dark rock | **11 min 41 s** (701 s) | **1 min 14 s** (74 s) |
| **10_segmentation** — fish on pale substrate | not measured | **52 s** |
| Corrections needed on SAM output | — | none identified at working zoom |

### Finding 1 — the honest speed-up is 9.4×, not 13.5×

Comparing manual on 09 to SAM on 10 gives **13.5×**, and that number is wrong to quote: it sets an easy image against a hard one. Running SAM on **09** as well removes the confound entirely — same image, same fish, same boundary — and gives **9.4×**.

The gap between those two figures is the whole argument for controlling the comparison. A portfolio that reports 13.5× is reporting frame difficulty as if it were model performance.

### Finding 2 — difficulty costs the model far less than it costs the human

SAM took **52 s on the easy frame and 74 s on the hard one**, a 43% penalty. The manual pass on the hard frame took 701 s.

Stated carefully: the human's manual time on the *easy* frame was never measured, so the interaction is **suggestive, not demonstrated**. What can be said is that the model's cost was only mildly sensitive to a boundary condition the annotator found expensive enough to dominate the session.

### Finding 3 — the prediction came out ambiguous, and that is the result

The recorded prediction was that SAM would struggle at the dark-fish-against-dark-rock edge. It did not visibly fail there — but neither did it demonstrate resolving anything the eye could not. It produced a boundary about as defensible as the manual one, in a region where "defensible" is the ceiling.

**Agreement between a human and a model in an unresolvable region is not evidence that either is right.** Both produce a plausible edge because a plausible edge is all the pixels support. Quantified below by IoU and a disagreement map rather than settled by eye.

### Caveats, stated plainly

- The manual figure is a **first-ever segmentation** by an annotator with no prior experience of the type. It is a learning-curve number, and 9.4× is therefore an **upper bound** on what assistance would buy a practised annotator.
- No independent ground truth exists for either mask. All quality claims are relative agreement, not accuracy.
- n = 1 image for the controlled comparison.

### Where the manual time went

The costly regions on 09 were the **dark dorsal edge against dark rock** and the **fin margins**. Both are contrast problems rather than attention problems — at those boundaries the information is not present in the pixels, so no amount of care resolves them.

Approach taken: stop trying to perfect those edges and apply the **same** treatment to each. On a boundary that cannot be resolved, a consistent decision is reproducible by a second annotator and an agonised one is not. **Precision you cannot repeat is not precision.**

---

## Quantified agreement: manual mask versus SAM 3 mask

Both masks were drawn on **09_segmentation**, the same fish, and exported together. Areas and overlaps computed by decoding the COCO RLE from the Datumaro export — measured, not estimated.

Mask identity: the manual mask is the one created first in the export order, corroborated independently by the disagreement analysis below, which places the largest manual-only region exactly where the annotator had predicted overrun before any measurement was run.

| Quantity | Value |
|---|---|
| Manual mask area | 176,531 px |
| SAM 3 mask area | 172,220 px |
| Intersection | 170,863 px |
| Union | 177,888 px |
| **IoU** | **0.9605** |
| Dice coefficient | 0.9799 |
| Manual-only pixels | 5,668 (3.19% of union) |
| SAM-only pixels | 1,357 (0.76% of union) |
| Area difference | manual is **2.44% larger** |

### Finding 4 — nearly all disagreement is boundary noise, not structure

| Distance from the agreed boundary | Share of disagreeing pixels |
|---|---|
| within 3 px | 60.8% |
| within 6 px | 80.3% |
| within 12 px | 89.0% |
| within 25 px | 98.1% |

Roughly **11% of the disagreement sits more than 12 px from the boundary** — that fraction is the only part that represents a genuine difference of opinion about what is fish. The rest is a thin rim, and the rim is asymmetric: the manual mask is slightly more generous almost everywhere, consistent with a brush that overshoots by a pixel or two and a decision not to chase edges.

### Finding 5 — the structural disagreement lands exactly where the prediction said it would

The largest manual-only region, **2,194 px at 27% along the body and 82% down** — rear body, ventral — is the anal fin area, inside the dark-fish-against-dark-rock zone recorded before measurement as the hardest part of the frame. The annotator also flagged this specific overrun by eye before any numbers existed.

**So the prediction holds in a qualified form.** SAM did not fail there. But it is where the human and the model diverge most, which is what "the information is not in the pixels" looks like when measured: two competent passes produce different answers because the data does not determine one.

The second structural difference runs the other way — **1,224 px of SAM-only pixels along the leading edge of the head**, a long thin strip where SAM placed the outline slightly further forward. That edge is well lit and resolvable, so this is boundary placement rather than ambiguity.

### Finding 6 — operational reading

A **96% IoU between a model's one-shot output and a first-time human annotator**, on a genuinely difficult frame, means SAM 3 is viable as a first pass on this data. The useful review policy follows from the distance table: ignore the sub-6-px rim, and direct human attention at disagreement further from the boundary, which here is about a tenth of the disagreeing pixels and clusters in predictable places.

### Caveat that limits all of the above

**There is no ground truth.** IoU measures agreement between two passes, not the accuracy of either. At the anal fin both may be wrong, and nothing in this analysis could distinguish that case from both being right. Every quality claim here is relative.

![Disagreement map](09_mask_disagreement.png)

*Grey — both masks agree. Orange — manual only. Blue — SAM only.*

---

## Export caching — a data-integrity hazard

**CVAT can serve a cached export that predates the current annotation state, with nothing in the file or the download to indicate it.**

Observed directly during this run. Three exports were taken from the same task at three different points:

| Export | Total annotations | 04_polygon | 10_segmentation | MD5 |
|---|---|---|---|---|
| first | 28 | 3 | 1 | `ccda2863…` |
| second | 31 | 5 | 2 | `81dbaf16…` |
| third, requested last | **28** | **3** | **1** | **`ccda2863…`** |

The third export was requested *after* further edits, under a different filename, and came back **byte-identical to the first** — a state two rounds out of date. Giving the download a new name does not produce a new export; the cache is keyed on the task and format, not the filename.

**Why this matters more than it sounds.** Every verification check in this project runs against the export rather than the UI. A stale export means the checks describe a dataset that no longer exists, and they will pass — because the stale file is internally consistent. Nothing fails. In a delivery setting this is how a client receives last week's annotations while everyone believes they have this week's.

**Detection.** Compare the MD5 of consecutive exports, and check the annotation count against what the UI shows. Both are cheap and neither is prompted by the tool.

### A second instability: export order is not stable either

Separately from caching, **the order annotations appear in an export changes when they are edited.** Observed directly: two polygons on 04_polygon occupied export positions 12 and 15; a single attribute edit on one of them swapped their positions in the next export. No geometry changed, no annotation was added or removed.

Taken with the earlier finding that CVAT's *displayed* instance numbers renumber whenever anything is deleted, the position is this:

| Identifier | Changes when |
|---|---|
| Displayed instance number | anything earlier is deleted |
| Position in the export file | the annotation is edited |
| **Geometry and attributes** | **only when the annotation itself changes** |

**Neither number is an identifier.** Any QA note, review comment or defect report that cites one will silently stop pointing at the right object — and nothing in the tool or the file signals that it has happened. Reference annotations by frame plus geometry, or by frame plus description.

This is not a CVAT-specific complaint until the other five platforms have been checked. It is a question to ask of each of them, and none of them documents the answer.

**Mitigation.** Save the job before exporting, then trigger a **new** export request from the Requests tab rather than re-downloading a completed one.

**Worth testing on every remaining platform**, since it determines whether an export can be trusted as a record of current state at all.

| Platform | Caches exports? | Stale export detectable from the file? |
|---|---|---|
| CVAT | **Yes — observed** | No, identical bytes and no warning |
| Roboflow | | |
| Supervisely | | |
| Label Studio | | |
| Labelbox | | |
| SuperAnnotate | | |

---

## Free-tier structural limits

Discovered by hitting them, not by reading documentation.

**CVAT caps the number of projects on the free tier.** With **one** project already in use (the
image run), creating a second was refused outright: *"You have reached the maximum number of
projects. Upgrade the account to extend the limits."* No warning before the attempt, and the
limit is not stated on the pricing page in a form you would find before running into it.

**Workaround that costs nothing:** a task can exist **outside any project**, carrying its own
label set. The video run was set up this way. Annotation behaves identically; the labels simply
live on the task rather than the project. Anyone comparing platforms on a free tier should know
this before concluding CVAT is unusable for a second workstream.

**Consequence for a schema-driven workflow:** with per-task labels, holding a schema constant
across workstreams becomes a manual discipline rather than something the tool enforces. That is
a real quality risk on a longer project, and it is the sort of trade a free tier imposes without
announcing it.

| Platform | Project cap on free tier | Tasks outside projects? | Notes |
|---|---|---|---|
| CVAT | **Yes — hit at 1 project** | **Yes** | labels move to the task; schema consistency becomes manual |
| Roboflow | | | |
| Supervisely | | | |
| Label Studio | | | |
| Labelbox | | | |
| SuperAnnotate | | | |

---

# CVAT — full platform assessment (image run)

Answers from the 10-frame image run only. The video run was set up on CVAT but never annotated,
so nothing below draws on it. Full working, with the evidence behind every row, is in
`cvat_platform_questionnaire.md`.

**How each row is known:** *measured* — a recorded figure. *observed* — seen working or failing.
*untested* — the feature exists and was never exercised. *unknown* — never encountered; not
answered from documentation. *rated* — a judgment call, with its basis stated.

## Setup

| | CVAT | Basis |
|---|---|---|
| Deployment | **Hosted — cvat.ai free tier** | observed |
| Account → first annotatable frame | **~1 h**, mostly upload failure and skeleton-UI discovery. Under 15 min on a second run with the schema in hand | observed |
| Native attributes | **Yes** — constrained to fixed dropdowns via `input_type: select` | observed |
| Skeleton template reusable across tasks | **Untested** — only one skeleton task ever existed | untested |

## Annotation

| | CVAT | Basis |
|---|---|---|
| Keyboard-only bbox workflow | **Unknown** — run was mouse-driven; little the keyboard would have saved on 10 frames | unknown |
| Polygon vertex editing | **5 / 5** | rated |
| Point-density control | **Yes** — fixed point count and a Simplify toggle. Both deliberately unused | observed |
| Occluded-keypoint flag | **Exists, never exercised** — all 10 landmarks visible, all exported flag `2` | untested |
| Segmentation brush | **4 / 5** | rated |
| Zoom/pan at 400% | **No problem encountered**, not benchmarked | observed |
| Undo depth | **Unknown** — used casually, never failed, never stress-tested | unknown |
| Copy annotation between frames | **Unknown** — 10 different scenes, nothing worth copying forward | unknown |
| Assisted labelling on free tier | **Yes — SAM 2.0 and SAM 3.** 52 s easy frame, 74 s hard frame, IoU 0.9605 vs manual | measured |

## QC and review — all untested, and the reason is the same

**The run was solo.** Not a limitation of the images, which could have carried an Issue on any
frame. Stages (annotation / validation / acceptance), assignees and an Issues panel are all
visible in the UI and none of them was ever used. Audit trail and consensus features were never
investigated at all.

The only agreement figure this project holds is **human versus SAM (IoU 0.9605)**, which is a
different measurement from inter-annotator agreement and should not be presented as one.

## Export

| | CVAT | Basis |
|---|---|---|
| COCO correct first try | **Exported without error — and silently incomplete.** 28 of 30 | measured |
| Attributes survive export | **Datumaro yes. COCO yes, into a key the spec does not define** | measured |
| Keypoint visibility flags survive | **Datumaro yes** (`x, y, visibility`). **COCO n/a — skeletons dropped** | measured |
| Images in export | **Annotations only, by choice.** Option exists | observed |

## Timing

Only the segmentation figures were stopwatch-measured, deliberately, for the manual-versus-assisted
comparison. **Everything else is recalled, and is labelled as such.**

| Stage | Time | Basis |
|---|---|---|
| Setup — schema, skeleton, upload | ~1 h | estimate, includes upload failures and re-compression |
| 3 bbox frames | ~10 min | estimate |
| 3 polygon frames | ~20 min | estimate |
| 2 keypoint frames | ~5 min | estimate — skeleton pre-defined |
| **Segmentation, manual, 1 frame** | **11 min 41 s** | **measured** |
| **Segmentation, SAM 3, 1 frame** | **52 s** | **measured** |

An earlier recollection put segmentation at ~35 minutes for both frames. The measured figures
total about 12½. The measured numbers are used.

## Verdict

**Best at — schema expressiveness.** Labels definable as raw JSON, each bound to a shape type,
attributes constrained to fixed value lists, skeletons built from named sublabels. That
combination is what made the project's central findings possible: measurable attribute drift, a
cross-attribute constraint checkable by query, and a schema verifiable against the export in code.
Few tools offer it on a free tier.

**Worst at — trustworthiness of its own outputs and identifiers.** Four defects, none documented,
every one found by checking rather than by any warning:

- Exports are **cached** — a file requested as final returned byte-identical to one two rounds old
- **Export order shifts on edit** — one attribute change swapped two annotations' positions
- **Displayed instance numbers renumber on deletion**
- **COCO drops skeletons while still declaring them** in its categories block

Individually minor. Together: nothing CVAT hands you can be trusted without verifying it.

### Would you run a 5-person team on it?

**Not on this free tier. Probably yes self-hosted or paid — but this run tested none of it.**

- **The free tier caps projects.** A second project was refused outright with one in use. The
  workaround — tasks outside any project, carrying their own labels — makes **schema consistency
  across a team a manual discipline rather than something the tool enforces.** On five people
  that is precisely where quality goes.
- **Instance numbers are not stable identifiers.** A reviewer writing *"instance 14 is wrong"*
  writes a note that stops pointing at the right object the first time anyone deletes anything.
  Solo, an annoyance. On a team, it breaks the review loop.
- **The review features were never exercised.** This run says nothing about whether they work.

### Overall — two dimensions

| Dimension | CVAT | Basis |
|---|---|---|
| **Annotation capability** | **4.5 / 5** | Schema control, four annotation types, free SAM 3; nothing about the annotation experience blocked the work |
| **Output trustworthiness** | **2.5 / 5** | Four undocumented defects, all discovered by checking rather than by warning |

**Scope:** free tier, solo, image annotation. Multi-user review, undo depth, keyboard workflow and
audit trail were never exercised and this rating says nothing about them.

**Why capability is not 5:** the project cap, and a skeleton-setup control obscure enough to cost
several attempts to find. **Why trustworthiness is not lower:** every defect was discoverable, and
Datumaro carried everything faithfully. Nothing was lost — but nothing announced itself either.

---

*Rows to fill for Roboflow, Supervisely, Label Studio, Labelbox and SuperAnnotate use the same
26-question instrument. Keep the evidence tags; a comparison where one column is measured and
another is assumed is not a comparison.*
