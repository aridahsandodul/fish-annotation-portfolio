# Text and audio: delivery decisions

Completed 15 September 2026. These are small portfolio runs under project-specific rules, not industry benchmarks.

## Text: exact spans and scoped attributes

**Delivered:** 22 aquaculture research abstracts, 405 entity spans, 938 result records. Five labels: species, water_param, measurement, equipment and condition.

The [working configuration](platform_schemas/label_studio_config_text.xml) gives every span an assertion value (reported or background). Only species receives name_form; only measurement receives value_type.

### Percentage selection included punctuation

Selecting a percentage at word granularity could pull in the following punctuation. The fix was symbol-level selection in the Text control. For example, the intended measurement is 26.86%, not 26.86 or 26.86%. with the sentence-ending period.

**Delivery check:** compare the stored offsets with the original text substring; check missing attributes, class scoping, duplicate spans and whitespace edges. A visually plausible highlight is insufficient.

### Annotation count is not result-record count

A span and its per-region choices produce separate result records linked by a region ID. The final has 405 entity spans but 938 records. Counting every record as an entity would overstate production.

**Review limit:** the final normalized span set was checked against the settled review target. This is not a blinded gold-standard evaluation or an accuracy percentage.

### Source

The corpus uses 22 open-access aquaculture abstracts published by MDPI. The retained provenance records CC BY 4.0 verification against [the publisher's open-access policy](https://www.mdpi.com/openaccess) on 3 September 2026. Abstracts and native exports are not reproduced in this repository.

## Audio: speakers, backchannels and silence

**Delivered:** 12 EdAcc conversational clips, 323 regions, 1,185 result records. Eleven WAVs are 180.000 seconds; one is 180.100 seconds, about 36 minutes total. Source: [EdAcc, DOI 10.7488/ds/7914](https://doi.org/10.7488/ds/7914), CC BY-SA 4.0. Audio and corpus references are not redistributed here.

### The interface must enforce the schema

The [working configuration](platform_schemas/label_studio_config_audio.xml) uses:

| Region label | Required attributes |
|---|---|
| speaker_a, speaker_b | boundary, speech_clarity, turn_type |
| overlap | boundary, speech_clarity |
| non_speech, unintelligible | boundary |

First voice is speaker_a within each clip. Speaker labels are clip-local, not identities across the corpus. Accent is not a clarity defect.

### A backchannel is still a speaker event

A brief acknowledgement receives its own speaker region, even when it intersects the other speaker. A separate overlap region is used only for simultaneous substantive speech with audible muddiness. Backchannels alone do not qualify. There is no minimum overlap duration.

**Why it matters:** marking only overlap would discard who spoke. Conversely, treating every acknowledgement as competing speech would distort the conversational labels.

### Silence and audible non-speech are different

Pure silence receives no label. Audible laughter, coughing or other non-word events use non_speech. Split speaker regions around non_speech events and silence lasting **1.5 seconds or longer**. Shorter pauses may remain inside a continuous turn. This final project convention supersedes the earlier 0.5-second, 1.0-second and no-fixed-threshold rules.

Signal measurements can support boundary review, but low RMS alone cannot prove the absence of speech. Exact speech boundaries remain a listening judgment.

### Exported nesting can escape visual review

An early export contained accidental parentID relationships between unrelated regions. These were removed during correction. The final export was checked for unintended parent links as well as label/attribute scope.

### What the checks establish

Final structural checks cover nonempty annotations, labels and allowed choices, required attribute scope, region bounds against WAV durations, duplicate regions and interval relationships. The supplied closeout records acoustic review; the final structural verification did not repeat that listening pass.

The schema has no speaker field on unintelligible regions. Known speaker identity for wholly unrecoverable speech must therefore be documented outside the region. That limitation is retained rather than concealed.

## Reproducibility and limits

The configurations here show the delivered label logic. Private source exports and dated review records retain the detailed audit trail. Counts and successful structural checks do not establish independent acoustic accuracy, inter-annotator agreement or production throughput.
