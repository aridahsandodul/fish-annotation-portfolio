# Video annotation guidelines: fish tracking

Public delivery edition, 15 September 2026. This records the completed run and distinguishes it from the earlier interpolation plan.

## Scope and schema

The run contains one 300-frame clip at 29.97 fps, six tracks and 762 visible boxes. See [source provenance](VIDEO_SOURCE_PROVENANCE.txt) and [label schema](cvat_labels_video.json).

Each fish track carries mutable orientation, visibility and posture attributes. Values follow the [image schema](SCHEMA_README.md). The context_object class is declared but unused.

## Identity and geometry

- Assign one track ID to one identifiable animal. Never reuse a retired ID for a different animal.
- Keep boxes on the visible extent through partial occlusion. Record visibility changes along the track.
- If identity cannot be established across a disappearance, end the track rather than invent a match.
- Distinguish an unreadable attribute from absence: indeterminate records uncertainty; outside marks a track leaving the annotated sequence.
- Start and end at observable, annotatable boundaries. Do not pad tracks with guessed boxes.

The selected clip exercised partial occlusion and exits. Full disappearance and re-identification were not demonstrated.

## Delivered representation

All placement was reported as manual. The 765 box records comprise 762 visible boxes and three outside terminators. The standard CVAT occluded field remains 0; the three-value visibility attribute records occlusion instead. Consumers must read that field rather than infer that no occlusion occurred.

## Verification

The XML and Datumaro exports agree on visible counts. Twenty attribute ranges match 2,286 visible-box attribute values. Structural checks cover bounds, positive box dimensions, allowed attributes, duplicate frames and within-track continuity.

The annotator's log reports targeted identity review and zero final-review corrections. That is a reported review result. Structural checks cannot prove that an ID follows the correct fish; visual review is required.

## Earlier interpolation plan, not exercised

The original v6 plan proposed a maximum ten-frame keyframe interval, extra keyframes at motion/attribute changes, and an audit of corrected interpolated boxes. Manual placement superseded that workflow for this delivery.

There is no interpolation-error denominator and no interpolation accuracy claim. Working time was not recorded. The original planning document is retained in the private project history.
