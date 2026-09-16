"""Create the Labelbox ontology used for the completed portfolio image run.

Install: pip install labelbox
Run: set LB_API_KEY in the environment, then run this file.

Importing this module has no remote side effect. Labelbox has no native skeleton
in this design, so the five landmarks are named point tools and their grouping
is not preserved. Record that limitation in the comparison log.
"""

import os


def instance_attributes(lb):
    """Return a fresh attribute set for one fish tool."""
    return [
        lb.Classification(
            class_type=lb.Classification.Type.RADIO,
            name="orientation",
            scope=lb.Classification.Scope.INDEX,
            options=[lb.Option(value=v) for v in (
                "lateral", "oblique", "axial", "indeterminate"
            )],
        ),
        lb.Classification(
            class_type=lb.Classification.Type.RADIO,
            name="visibility",
            scope=lb.Classification.Scope.INDEX,
            options=[lb.Option(value=v) for v in (
                "full", "partial", "heavy_occlusion"
            )],
        ),
        lb.Classification(
            class_type=lb.Classification.Type.RADIO,
            name="posture",
            scope=lb.Classification.Scope.INDEX,
            options=[lb.Option(value=v) for v in (
                "straight", "curved", "indeterminate"
            )],
        ),
    ]


def create_ontology():
    """Create the ontology and return the Labelbox object."""
    import labelbox as lb

    api_key = os.environ.get("LB_API_KEY")
    if not api_key:
        raise RuntimeError("Set LB_API_KEY before creating the ontology.")

    fish_tools = [
        lb.Tool(
            tool=lb.Tool.Type.BBOX,
            name="fish_bbox",
            color="#33ddff",
            classifications=instance_attributes(lb),
        ),
        lb.Tool(
            tool=lb.Tool.Type.POLYGON,
            name="fish_polygon",
            color="#fa3253",
            classifications=instance_attributes(lb),
        ),
        lb.Tool(
            tool=lb.Tool.Type.RASTER_SEGMENTATION,
            name="fish_mask",
            color="#34d1b7",
            classifications=instance_attributes(lb),
        ),
    ]
    context_tool = lb.Tool(
        tool=lb.Tool.Type.BBOX,
        name="context_object",
        color="#b83df5",
    )
    point_tools = [
        lb.Tool(tool=lb.Tool.Type.POINT, name=name, color="#ffcc00")
        for name in ("snout", "eye", "dorsal_origin", "pelvic_origin", "tail_fork")
    ]

    client = lb.Client(api_key=api_key)
    return client.create_ontology(
        name="Fish Annotation Portfolio",
        media_type=lb.MediaType.Image,
        normalized=lb.OntologyBuilder(
            tools=fish_tools + [context_tool] + point_tools,
            classifications=[],
        ).asdict(),
    )


def main():
    ontology = create_ontology()
    print("ontology id:", ontology.uid)


if __name__ == "__main__":
    main()
