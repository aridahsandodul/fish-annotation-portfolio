# Video annotation guidelines: fish tracking

Version 6.0 — an extension to the image annotation guidelines, not a replacement.
Author: Arid Ahsan Dodul
Applies to: multi-object tracking on underwater and aquaculture video

**Everything in the image guidelines v5.3 still holds** — the annotation threshold, the three
attributes, the geometry rules per shape type, the boundary-ownership and boundary-resolvability
tests, the class definitions, and the rule that display adjustment is legitimate technique. This
document adds only what changes when frames become a sequence.

---

## What actually changes

A still frame asks *what is here*. A video asks *what is here, and is it the same thing that was here
a moment ago*. Everything below follows from that second question.

The consequence is that a new error class becomes possible, one that cannot exist in still images:
**the identity error**. A box can be perfectly placed on a perfectly real fish and still be wrong,
because it carries the wrong track ID. Geometry that is correct frame by frame can be worthless as
tracking data.

**The ID switch is to video what attribute drift is to high-volume stills** — the characteristic
error of the medium, invisible unless looked for deliberately, and not detectable by inspecting any
single frame.

---

## Schema changes

The same three attributes apply — `orientation`, `visibility`, `posture` — but with one structural
change:

**All three become mutable.** A fish turns, so its orientation changes. It passes behind a cage bar,
so its visibility changes. It bends into a turn, so its posture changes. In the image schema these
were fixed per instance; here they are fixed per *frame*.

This has a consequence worth stating before it bites: **attribute drift can now occur inside a single
track.** The same fish, unchanged, labelled `lateral` at second 2 and `oblique` at second 3 because the
annotator's standard moved rather than the animal. Checking for drift across a batch is no longer
sufficient; it has to be checked along each track as well.

`context_object` remains attribute-free and is annotated as a shape, not a track, unless the
equipment itself moves.

---

## Track IDs

**One animal, one track ID, for the entire clip.** The ID is a claim that every box carrying it
belongs to the same individual.

- **IDs are never reused.** If a track ends, its number retires with it. Reusing an ID for a
  different animal later in the clip is the single most damaging error available here, because it is
  invisible in every individual frame and silently teaches a model that one object teleported.
- **IDs need not be contiguous.** Gaps in the numbering are harmless. Gaps in the *meaning* are not.
- Assign IDs in the order tracks begin, not by size or prominence.

---

## Keyframes and interpolation

Interpolation is not a convenience. **It is an assertion that motion between two keyframes was
linear.** Place a keyframe wherever that assertion would be false.

**Place a keyframe at:**

- the first and last frame of the track
- every clear change of direction
- every change to any of the three attributes
- the frame an occlusion begins, and the frame it ends
- any frame where the interpolated box has visibly drifted off the animal

**Maximum interval: 10 frames**, regardless of how linear the motion looks. Not because 10 is
principled, but because a ceiling forces a check at a fixed rate and an unbounded interval does not.
Record the frame rate of the clip alongside this number — 10 frames means something different at
24 fps than at 60.

**Sparse keyframes are not efficiency.** A track with four keyframes over 300 frames is not fast
work; it is a claim about 296 frames that nobody verified.

---

## Occlusion and ID persistence

This is the hard part, and the rule has to be strict because the failure is invisible.

**While a fish is partly occluded** — behind another fish, a cage bar, a root — the track continues.
Keep the box on the visible extent, set `visibility` accordingly, and keep the ID.

**While a fish is fully hidden but its path is unambiguous** — it passes behind a single narrow
obstruction and emerges on the expected side, within a few frames — the track continues through the
gap. Mark the hidden frames `occluded` rather than `outside`. The position is inferred; the flag says
so. This is the same principle as the occluded keypoint rule: **infer the position, flag the
confidence.**

**Where the path is not unambiguous, the track ends.** This is the decision most likely to be got
wrong under time pressure, because continuing a track feels like preserving information and ending
one feels like losing it. The opposite is true. A track continued through a genuine ambiguity is a
fabricated identity claim, and it is worse than two shorter honest tracks.

### Re-identification after a gap

A fish leaves the frame at second 3. At second 20 a fish that looks like it returns.

**Default: it is a new track with a new ID.** Not because it is a different animal — it may well not
be — but because "the same fish" is a claim that cannot be verified from the footage, and an
unverifiable claim recorded as data is indistinguishable from a wrong one.

**Where you believe it is the same animal, record that in the log, not in the track ID.** A note
reading *"track 14 is probably track 6 returning — same size, same dorsal notch, consistent
direction"* preserves the observation without corrupting the tracking data. A downstream team can act
on the note. It cannot un-merge two tracks that were wrongly joined.

**One narrow exception:** the fish leaves and re-enters at the same frame edge, within roughly a
second, with consistent size and heading, and no other similar fish left the frame in between. Then
continue the track and log it as a re-identification with the reasoning stated. If the exception is
being used more than once or twice in a clip, it is not an exception any more and the default should
be reasserted.

---

## The annotation threshold over time

A fish can pass in and out of annotatability without going anywhere — swimming into murk, turning
away, dropping behind a school.

- **Present but unreadable:** keep the track, keep the box, set the unreadable attributes to
  `indeterminate`. Do **not** mark it `outside`. It has not left; only your ability to describe it
  has.
- **Genuinely absent from the frame:** mark `outside`. That flag means *not there*, and it should
  never mean *not readable*.
- **Never annotatable at any point in the clip:** no track. Count it in the clip summary as you would
  in a still.

Confusing these two states is the video equivalent of putting `heavy_occlusion` on a fish that is
merely dark.

---

## Track start and end

- A track **starts** on the first frame the animal meets the threshold — not the first frame it is
  faintly visible.
- A track **ends** on the last frame it meets the threshold, or on the frame it leaves the image.
- Do not pad either end with guessed boxes. A track that begins two frames late is a small omission;
  a track that begins two frames early contains two fabricated boxes.

---

## Verification pass for tracking

Run after all tracks are complete. The still-image checks all still apply. These are additional, and
none of them can be done by looking at a single frame.

| Check | Looking for | How |
|---|---|---|
| **ID switches** | One track ID that changes animal mid-clip | Scrub each track end to end at speed; a switch usually shows as a visual jump |
| **Fragmentation** | One animal split across several track IDs | Count tracks against the number of distinct fish you can identify in the clip |
| **ID reuse** | A retired number appearing again | Sort tracks by ID and check each occupies one continuous span |
| **Interpolation drift** | Interpolated boxes sitting off the animal | Step through non-keyframe frames on the longest tracks |
| **Attribute drift within a track** | Attributes changing when the animal did not | Play each track and watch the attribute panel rather than the fish |
| **Outside vs indeterminate** | `outside` used for fish that were present but unreadable | Check every `outside` span begins at a frame edge or a full occlusion |
| **Phantom keyframes** | Keyframes that record no change | Not an error, but a sign the interval rule was applied mechanically |

**ID switches are the row that matters.** They are the error the medium produces, they cannot be seen
in a still, and finding them is the difference between someone who draws boxes on video and someone
who produces tracking data.

---

## The interpolation audit

The measurement for this phase, and the counterpart to the box-versus-polygon water fraction.

Pick the longest track in the clip. Annotate it normally using keyframes and interpolation. Then step
through **every** frame of that track and count how many interpolated boxes needed correction.

```
interpolated_frames   = total frames in track − keyframes placed
corrected_frames      = interpolated boxes that needed adjustment
interpolation_error   = corrected_frames / interpolated_frames
```

| Track | Frames | Keyframes | Interpolated | Corrected | Error rate |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

Report whatever it is. A low rate says the motion was linear and the keyframe interval was well
chosen. A high rate says interpolation was doing more work than it could support — which is a finding
about the footage, not a failure by the annotator.

**Why this number is worth having:** every tracking tool advertises interpolation as a time saver, and
none of them publish how often it is wrong. "On sea-cage footage at 30 fps with keyframes every 10
frames, X% of interpolated boxes required correction" is a sentence almost nobody in this field can
say from their own measurement.

---

## Definition of done

1. Every annotatable fish carries one track, with one ID, for its full annotatable span.
2. No ID is reused. No track spans two animals.
3. Keyframes at every direction change, every attribute change, and every occlusion boundary, with no
   interval exceeding 10 frames.
4. Occluded frames flagged, not guessed silently; `outside` used only for genuine absence.
5. Re-identifications recorded in the log with reasoning, not merged into track IDs on a hunch.
6. Verification pass run, including the ID-switch scrub, with corrections counted.
7. Interpolation audit completed on at least one track and reported honestly.
8. Clip summary: tracks created, fish counted below threshold, total frames, frame rate.

---

## Revision history

| Version | Change | Reason |
|---|---|---|
| 6.0 | Extended the image guidelines to multi-object tracking: track IDs, keyframe and interpolation rules, ID persistence through occlusion, re-identification default, the `outside` versus `indeterminate` distinction, a tracking-specific verification pass, and the interpolation audit. | The image guidelines answer *what is here*. Video adds *is it the same thing that was here a moment ago*, and that question creates an error class — the identity error — that no per-frame check can detect. The rules above exist to make that error findable. |
