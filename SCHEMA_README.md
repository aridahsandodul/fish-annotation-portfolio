# Annotation schema: the constant across five image platforms

`cvat_labels.json` is the schema built and delivered in the CVAT baseline and verified against `CVAT exports/cvat_fish_run_2026-08-06_FINAL_DATUMARO.zip`. Holding the task design constant makes the platform comparison meaningful. Roboflow is the documented five-image and reduced-schema exception.

## Classes

| Label | CVAT form | Attributes |
|---|---|---|
| `fish_bbox` | rectangle | orientation, visibility, posture |
| `fish_polygon` | polygon | orientation, visibility, posture |
| `fish_mask` | mask | orientation, visibility, posture |
| `fish_keypoint` | skeleton with five landmarks | orientation, visibility, posture |
| `context_object` | any geometry | none |

Landmarks, in fixed order: `snout`, `eye`, `dorsal_origin`, `pelvic_origin`, `tail_fork`.

CVAT and Supervisely preserve a grouped skeleton. Label Studio and Labelbox represent the five landmarks as independent named points with no parent or connecting edges. Roboflow did not run the keypoint frames. These are representation differences, not permission to change the target landmarks.

## Attribute values

- `orientation`: `lateral`, `oblique`, `axial`, `indeterminate`
- `visibility`: `full`, `partial`, `heavy_occlusion`
- `posture`: `straight`, `curved`, `indeterminate`

Constrain them to fixed lists where the platform allows it. `posture: curved` and `visibility: heavy_occlusion` were unused in the CVAT sample but remain part of the schema.

## Deliberate omissions

- No species field
- No per-frame below-threshold tag
- No per-point uncertainty flag

These choices remained fixed during the image comparison.

## Counting the CVAT reference

The final Datumaro export contains 30 annotation records across 10 images and 29 distinct annotated objects. Frame `09_segmentation` holds two masks of the same fish: one manual and one assisted. The pair supports the measured comparison of 701 seconds manually versus 74 seconds assisted, with IoU 0.9605.

For the normalized Labelbox protocol comparison, each of the two CVAT skeleton records expands into five independent points, adding eight records, and the extra assisted CVAT mask is excluded, subtracting one. `30 + 8 - 1 = 37`. The raw exports are not identical.


## Video, text and audio configurations

- [Video](cvat_labels_video.json): mutable orientation, visibility and posture on fish tracks; declared context_object unused in the delivered window.
- [Text](platform_schemas/label_studio_config_text.xml): five entity classes, assertion on every span, name_form on species and value_type on measurement. Symbol-level selection preserves exact boundaries.
- [Audio](platform_schemas/label_studio_config_audio.xml): five region labels, boundary on every region, speech_clarity on speakers/overlap, turn_type on speakers only.

[Case studies](MODALITY_CASE_STUDIES.md) explain the final rules and the difference between a region and its attribute records.
