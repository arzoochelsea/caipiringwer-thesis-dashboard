# Final Static Audit — Caipiringwer Dashboard

## Verification performed

- Python syntax compilation: **PASS**
- File inspected: `app(4).py`
- Total lines: 1455
- Runtime data files were not included in this upload, so full end-to-end dashboard execution could not be verified.

## Submission blockers found

### 1. Unsupported global stability and shelf-life heuristic

The script still derives global labels such as `High`, `Moderate`, `Poor`, and `Extended/Intermediate/Short` from mean rheological values. These variables are not supported as validated shelf-life endpoints and appear unused.

Relevant lines: [479, 483, 487, 491]

**Action:** remove this heuristic block completely unless a validated published method and explicit decision thresholds are documented.

### 2. Sedimentation uses “Best Stability” and “Worst Stability”

These labels rank samples using the final-to-mid sediment ratio. With only two observation times, no sedimentation replicates, and no redispersibility test, these claims are too strong.

Relevant lines: [1204, 1213]

**Action:** rename to factual descriptors such as:
- `Largest measured bed contraction`
- `Smallest measured bed contraction`
- `Highest final-to-mid bed ratio`

### 3. Arbitrary sedimentation classifier remains

The function `classify_stability()` assigns Good/Moderate/Poor using undocumented thresholds.

Relevant lines: [1161, 1171]

**Action:** remove the classifier and all shaded classification regions unless thresholds come from a validated method directly applicable to this experiment.

### 4. App title is too narrow

The page title still says “Caipiringwer Rheology Thesis Chapter,” while the app now includes physicochemical, sedimentation, and microbiology modules.

Relevant lines: [12, 59]

**Recommended title:** `Caipiringwer Beverage Stability Analytics Dashboard`

### 5. Translation is incomplete

A large amount of visible text is hardcoded in English rather than passed through the translation dictionary. German mode will therefore remain partial.

**Action:** perform a full i18n audit of all visible `st.*` strings, Plotly titles, axis labels, captions, warnings, metric labels, and table headings.

### 6. Deprecated Streamlit argument

`use_container_width=True` still appears and your terminal already warned that it should be replaced.

Relevant lines: [860, 1190, 1246, 1272, 1316, 1323]

**Action:** replace:
- `use_container_width=True` → `width="stretch"`
- `use_container_width=False` → `width="content"`

### 7. Scientific references are too generic

The rheology library contains journal landing pages and a textbook, but not enough verified article-level references supporting individual claims.

**Action:** use article-level citations with authors, year, title, journal, volume/pages, DOI, and a short note explaining exactly which interpretation is supported.

## Positive findings

- The Python file compiles successfully.
- Data modules are mostly separated.
- A clear statement prevents fabricated cross-module joins.
- The microbiology module distinguishes 12 qualitative LIMS observations from 156 processed plates.
- The microbiology image interpretation explicitly avoids image-derived CFU estimates.
- The code includes warnings when quantitative microbiological evidence is unavailable.

## Final release checklist

- [ ] Remove unsupported stability and shelf-life heuristic
- [ ] Remove Good/Moderate/Poor sedimentation classification
- [ ] Replace Best/Worst Stability labels
- [ ] Rename the overall dashboard title
- [ ] Complete English/German translation
- [ ] Replace deprecated Streamlit arguments
- [ ] Verify every dataset path on a clean machine
- [ ] Verify every tab has content and no duplicates
- [ ] Test EN and DE modes
- [ ] Test all sample selectors
- [ ] Confirm no fabricated extrapolation or universal sample mapping
- [ ] Confirm actual vs potential alcohol are clearly separated
- [ ] Confirm all images have publication permission
- [ ] Keep GitHub repository private until supervisor approval
