"""
Labelbox ontology - generated from cvat_labels.json.

  pip install labelboxexport LB_API_KEY=...python labelbox_ontology.py

scope=INDEX makes each attribute PER-INSTANCE, which is the whole point of the
schema (see DECISIONS.md: classes with attributes, not compound labels).
Labelbox has no native skeleton type, so the 5 landmarks are separate POINT
tools and the skeleton grouping is lost. Record that, do not work around it.
"""
import os
import labelbox as lb

client = lb.Client(api_key=os.environ["LB_API_KEY"])

INSTANCE_ATTRS = [
    lb.Classification(class_type=lb.Classification.Type.RADIO, name="orientation",
                      scope=lb.Classification.Scope.INDEX,
                      options=[lb.Option(value="lateral"), lb.Option(value="oblique"), lb.Option(value="axial"), lb.Option(value="indeterminate")]),
    lb.Classification(class_type=lb.Classification.Type.RADIO, name="visibility",
                      scope=lb.Classification.Scope.INDEX,
                      options=[lb.Option(value="full"), lb.Option(value="partial"), lb.Option(value="heavy_occlusion")]),
    lb.Classification(class_type=lb.Classification.Type.RADIO, name="posture",
                      scope=lb.Classification.Scope.INDEX,
                      options=[lb.Option(value="straight"), lb.Option(value="curved"), lb.Option(value="indeterminate")]),
]

ontology = client.create_ontology(
    name="Fish Annotation Portfolio",
    media_type=lb.MediaType.Image,
    normalized=lb.OntologyBuilder(tools=[
    lb.Tool(tool=lb.Tool.Type.BBOX, name="fish_bbox", color="#33ddff",
            classifications=INSTANCE_ATTRS if True else []),
    lb.Tool(tool=lb.Tool.Type.POLYGON, name="fish_polygon", color="#fa3253",
            classifications=INSTANCE_ATTRS if True else []),
    lb.Tool(tool=lb.Tool.Type.RASTER_SEGMENTATION, name="fish_mask", color="#34d1b7",
            classifications=INSTANCE_ATTRS if True else []),
    lb.Tool(tool=lb.Tool.Type.BBOX, name="context_object", color="#b83df5",
            classifications=INSTANCE_ATTRS if False else []),
    lb.Tool(tool=lb.Tool.Type.POINT, name="snout", color="#ffcc00"),
    lb.Tool(tool=lb.Tool.Type.POINT, name="eye", color="#ffcc00"),
    lb.Tool(tool=lb.Tool.Type.POINT, name="dorsal_origin", color="#ffcc00"),
    lb.Tool(tool=lb.Tool.Type.POINT, name="pelvic_origin", color="#ffcc00"),
    lb.Tool(tool=lb.Tool.Type.POINT, name="tail_fork", color="#ffcc00"),
    ], classifications=[]).asdict(),
)
print("ontology id:", ontology.uid)
