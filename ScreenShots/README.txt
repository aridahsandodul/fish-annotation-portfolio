SCREENSHOTS - index. Last updated 5 September 2026.

Every file is named for what it PROVES, not for when it was taken. The 13 CVAT
files were called Screenshot_1..13 until 5 September; they were opened one by
one and renamed by content. Several match entries in edge_case_log.md to the
decimal - the box dimensions in the filenames are the ones argued about there.

FIVE PLATFORMS ARE EVIDENCED. SuperAnnotate was removed without use and is not part of this comparison.

--------------------------------------------------------------------------------
THE CROSS-PLATFORM SET - polygon work in four platforms
--------------------------------------------------------------------------------
  cvat_A_polygon_vertices.png
  supervisely_A_polygon_vertices.png
  roboflow_A_polygon_vertices.png
  labelstudio_A_polygon_vertices.jpg

  Open these four together to compare polygon vertices and editor behavior.
  These screenshots do not all show the same source frame; use the measured
  same-frame comparisons in platform_comparison_log.md for numeric claims.

--------------------------------------------------------------------------------
SKELETON SUPPORT - the finding that splits the five platforms in two
--------------------------------------------------------------------------------
  cvat_keypoint_skeleton_five_landmarks_linked.jpg
        FISH_KEYPOINT 29. Five landmarks WITH CONNECTING LINES and a single
        parent object carrying the three attributes. This is what a native
        skeleton type looks like.
  cvat_keypoint_skeleton_with_context_object.jpg
        Same, with CONTEXT_OBJECT 22 in frame.
  supervisely_B_keypoints.jpg
        Supervisely's equivalent.
  cvat_B_keypoints.jpg
        Second CVAT keypoint view.

  labelbox_07_five_loose_landmarks.jpg
        THE CONTRAST. Five points, NO connecting lines, NO parent object,
        five independent entries in the panel. Labelbox has no skeleton type
        and neither does Label Studio. Roboflow's free tier never reached
        keypoints at all.

  Put the CVAT and Labelbox keypoint files side by side. The difference is
  visible in two seconds and needs no explanation.

--------------------------------------------------------------------------------
PER-INSTANCE ATTRIBUTES - proved differently on each platform
--------------------------------------------------------------------------------
  cvat_bbox_attributes_per_instance_bbox4.jpg
  cvat_bbox_attributes_per_instance_bbox2.jpg
        FISH_BBOX 4 and 2, each carrying its own orientation / visibility /
        posture on the canvas.

  labelbox_instance_attributes_scope_index.jpg
        SEVEN boxes in one frame, each with its own attribute triple, one
        reading "lateral, full, straight" against six "axial, full,
        indeterminate". THE VARIATION IS THE PROOF - seven identical labels
        would have proved nothing. This is scope=INDEX rendering per-instance.

  labelstudio_A_polygon_vertices.jpg  +  labelstudio_B_whenlabelvalue_scoping.jpg
        THESE TWO ONLY WORK AS A PAIR. A shows fish_polygon 1 with Choices
        lateral / full / straight. B shows context_object 4 selected in the
        same project with the same config and ZERO Choices, only geometry.
        Together they demonstrate whenLabelValue scoping. Label Studio is the
        only platform in the set that reaches per-instance scoping through
        configuration rather than natively, so it is the only one where this
        has to be shown rather than assumed.

--------------------------------------------------------------------------------
EDGE CASES - these correspond to entries in edge_case_log.md
--------------------------------------------------------------------------------
  cvat_edgecase_axial_41x101_vs_indeterminate_67x110.jpg
        The two instances argued about in the log: the narrow silhouette reads
        axial because a fish presenting its body axis IS narrow by
        construction; the rounded blur has no long axis and reads
        indeterminate. Same frame, adjacent, different values.
  cvat_edgecase_lateral_58x63_vs_axial_31x71.jpg
        FISH_BBOX 3 (58.6x63.0) has a readable body line and stays lateral;
        FISH_BBOX 7 (31.6x71.0) stays axial. Size is not what decides it.
  cvat_bbox_smallest_instance_31x71px.jpg
        The smallest annotated instance in the run, zoomed.
  cvat_polygon_visibility_partial_vs_full.jpg
        FISH_POLYGON 12 (visibility: partial) beside 15 (visibility: full).
  cvat_below_threshold_candidate_blurred_fish.jpg
  cvat_below_threshold_candidate_unresolvable_blob.jpg
        UNANNOTATED ON PURPOSE. Recognisably fish, above the size floor, and
        left out because the boundary could not be observed - see the
        resolvable-boundary rule in edge_case_log.md. A polygon drawn around
        a blur asserts a silhouette on no evidence. These are the images
        behind that rule.

--------------------------------------------------------------------------------
CONTEXT_OBJECT and platform behaviour
--------------------------------------------------------------------------------
  cvat_context_object_measuring_bar_720x350.jpg
        CONTEXT_OBJECT 9. A diagonal bar in an axis-aligned box is mostly
        empty water. Nothing is wrong with it; it is what a bbox does to a
        diagonal object, and it is worth knowing before a reviewer asks.
  cvat_context_object_scale_bar_polyline.jpg
        CONTEXT_OBJECT 38 on the scale bar.
  cvat_polygon_dense_vertices_polygon13.jpg
        FISH_POLYGON 13, dense vertices around fins. Best single view of
        boundary work in the run.
  labelbox_review_grouped_counts.jpg
        Labelbox's review view groups objects by class with a count -
        "fish_bbox (7)" - so a reviewer sees the count before opening
        anything. CVAT makes you count them yourself. Credit where due.
  roboflow_B_five_images_only.jpg
        "1-5 of 5", polygon and segmentation files only. Roboflow's free tier
        could not hold all four annotation types in one project. The ABSENCE
        of keypoint and bbox files is the evidence, so no Roboflow keypoint
        screenshot exists and none should be looked for.

--------------------------------------------------------------------------------
NOT CAPTURED, and deliberately
--------------------------------------------------------------------------------
  Labelbox's "You cannot remove this annotation because it will make the label
  invalid" error. Reproducing it would mean editing a delivered label and
  trying to delete its last object. Judged not worth risking a verified run.
  The message is quoted verbatim in platform_comparison_log.md and that is the
  whole of the evidence for it.
