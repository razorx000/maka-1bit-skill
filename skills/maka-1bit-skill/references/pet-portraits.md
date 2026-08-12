# Pet portraits

Use this branch whenever a recognizable pet is the main subject. Preserve the individual animal, not merely its species or coat color.

## Identity ledger

Record only visible facts:

1. species and broad coat type
2. body proportions and silhouette
3. pose, head direction, gaze, and expression
4. ear shape, spacing, fold, crop, or asymmetry
5. eye shape, angle, relative size, and visible color
6. muzzle, nose, and face proportions
7. patches, spots, stripes, scars, or asymmetric marks
8. tail shape, color, position, and visibility
9. paw placement and distinctive leg markings
10. existing collar, tag, harness, or accessory

Describe sides from the viewer's perspective. Never infer breed, personality, sex, age, or health.

## Priority and processing

Preserve unique markings first, then face geometry, body proportions, pose/paws/tail, coat texture, and background detail. Prefer direct deterministic conversion because it cannot hallucinate or relocate identity marks.

- Choose a logical resolution high enough for eyes, nose, unique marks, ear tips, paw separations, and visible tail to survive.
- Let downsampling merge individual hairs into coat-direction clusters.
- For a white pet, preserve separation through the source's shadow-density difference; for a black pet, preserve existing highlights and negative separations.
- If a small mark disappears, raise logical resolution or local contrast before using AI.
- Preserve scene context when it grounds the pose; do not add collars, toys, bowls, clothing, halos, or symbols.

## Pet QA

Reject the result if:

- a unique mark disappears or becomes unreadable
- eye, ear, muzzle, body-width, or head-to-body proportions lose recognition
- paws merge or the tail feature disappears
- an accessory or extra marking appears
- the animal becomes a generic silhouette
- pixel density no longer follows the source's facial and body volume

If an AI intermediate becomes necessary, lock every identity anchor and broad tonal plane, then run the intermediate through deterministic conversion.

