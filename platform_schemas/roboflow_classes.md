# Roboflow - class list to type in by hand

Roboflow has no label-schema import and no per-instance attributes.
Create these classes as you go. Do NOT invent compound names to fake
the attributes; the inability to hold them is the finding.

## Classes
- fish_bbox
- fish_polygon
- fish_mask
- context_object

## Keypoints (as a keypoint skeleton, if the free tier offers one)
- snout
- eye
- dorsal_origin
- pelvic_origin
- tail_fork

## Attributes that will NOT survive

- **orientation**: lateral, oblique, axial, indeterminate
- **visibility**: full, partial, heavy_occlusion
- **posture**: straight, curved, indeterminate
