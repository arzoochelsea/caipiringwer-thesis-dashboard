<div align="center">

# Caipiringwer Beverage Stability Analytics Dashboard

**An interactive Streamlit dashboard developed for a Master’s thesis in Applied Biotechnology.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-5.15%2B-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/python/)
[![pandas](https://img.shields.io/badge/pandas-2.0%2B-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Master's Thesis](https://img.shields.io/badge/Project-Master's_Thesis-0B6E75)](#research-context)
[![Repository Status](https://img.shields.io/badge/status-active-2E8B57)](https://github.com/arzoochelsea/caipiringwer-thesis-dashboard)

[![🚀 Open Live Dashboard](https://img.shields.io/badge/🚀_Open_Live_Dashboard-146C94?style=for-the-badge)](https://caipiringwer-thesis-dashboard.streamlit.app/)

</div>

## Project overview

This dashboard supports the structured analysis and scientific communication of measurements from a ginger–lime alcoholic beverage study. It keeps rheological, physicochemical, sedimentation, and qualitative microbiological evidence in distinct analytical modules while providing a common interface for thesis-level interpretation.

The application is an analytics and visualization tool. It is **not** a commercial shelf-life prediction system, a validated food-safety decision tool, or a regulatory expiry-date calculator.

## Key capabilities

| Capability | Implementation |
|---|---|
| Interactive exploration | Language, sample-family, batch, and comparison selectors appropriate to each view |
| Rheological analysis | Flow curves, descriptive power-law fits, residuals, amplitude sweeps, frequency sweeps, and replicate-aware summaries |
| Physicochemical visualization | Tabular and graphical presentation of pH, soluble solids, density, specific gravity, sugar, refractive-index, Oechsle, and alcohol-related fields when available |
| Sedimentation evidence | Intermediate and final sediment-bed observations, derived geometric summaries, comparison graphics, and labelled photographs |
| Qualitative microbiology | LIMS-derived qualitative records, treatment and culture-medium views, timelines, risk categories, and representative plate images |
| Scientific interpretation | Clearly separated measured observations, derived calculations, literature-supported interpretation, and limitations |
| Bilingual interface | English and German display selected from the sidebar |

## Dashboard modules

| Module | Measurements or evidence | Main purpose |
|---|---|---|
| Rheology | Shear rate, shear stress, apparent viscosity, viscoelastic moduli, strain, frequency, replicate metadata, and descriptive fit metrics | Characterize measured flow and oscillatory response within the experimental range |
| Physicochemical analysis | pH, °Brix, density, specific gravity, sugar, refractive index, Oechsle, and potential/measured alcohol fields | Present composition- and storage-related measurements recorded in the ODS workbook |
| Sedimentation | Intermediate and final sediment-layer volumes, normalized bed fractions, contraction summaries, and labelled cylinder photographs | Describe observed sediment-bed geometry at the available observation points |
| Qualitative microbiology | LIMS status fields, treatment categories, manufacturing dates, media, qualitative risk classes, and plate photographs | Review recorded qualitative microbial observations without inferring colony counts |

> **Traceability note:** modules may contain different sample sets, identifiers, experimental designs, and observation dates. Cross-module joins, correlations, or causal comparisons should not be made unless sample traceability has been independently verified. The dashboard only presents a limited batch-level synthesis where the implemented mapping is explicitly documented.

## Dashboard Preview

<!-- Add dashboard screenshots here when available -->

The images currently stored in `images/` are application artwork, laboratory workflow figures, and labelled experimental sedimentation evidence rather than full dashboard screenshots. They are therefore not presented here as UI previews.

## Scientific interpretation boundaries

- Constitutive-model parameters from a poor fit must not be treated as reliable material constants. Reported power-law quantities are descriptive calculations from the displayed measurement range and do not establish an unmeasured yield stress.
- Elastic dominance in an oscillatory test describes the response over the measured strain or frequency range; by itself, it does not demonstrate long-term physical stability or establish a gel class.
- Sedimentation findings are descriptive because only limited observation times are available and sedimentation replicates were not recorded. Settling kinetics, statistical significance, and long-term stability ranking are not supported.
- Microbiology photographs are qualitative evidence. They must not be used to infer colony counts, CFU values, organism identity, numerical prevalence, or predictive microbial behaviour.
- The dashboard does not determine regulatory shelf life, market-life duration, or an expiry date.
- Statistical, causal, and cross-module conclusions require suitable replication, controlled experimental design, and verified sample traceability. Visual patterns alone do not provide that evidence.

## Technology stack

| Technology | Role in this repository |
|---|---|
| Python | Application runtime and analytical logic |
| Streamlit | Interactive dashboard interface, caching, controls, tables, and media display |
| pandas | Excel, ODS, and CSV ingestion; data cleaning, grouping, and tabulation |
| NumPy | Numerical transformations, descriptive fitting, and derived metrics |
| Plotly | Interactive scientific charts and comparison graphics |
| openpyxl | Excel workbook engine used by pandas for `.xlsx` rheology files |
| odfpy | OpenDocument engine used by pandas for the physicochemical `.ods` file |

`requirements.txt` also declares SciPy and scikit-learn, but the current `app.py` does not import or call either package directly; they are therefore not presented as implemented analytical components.

## Repository structure

```text
caipiringwer-thesis-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── rheology/
│   │   ├── Flow curve.xlsx
│   │   ├── Amplitude sweep.xlsx
│   │   ├── Frequency sweep.xlsx
│   │   └── Metadata.xlsx
│   ├── physicochemical/
│   │   └── physicochemical_results.ods
│   └── microbiology/
│       ├── LIMS_Microbial_Audit.csv
│       └── *.png
└── images/
    ├── caipiringwer-hero.png
    ├── caipiringwer-open-v2.png
    ├── shelf-life-evidence.png
    ├── kinexus_rheometer_workflow.png
    ├── physicochemical_workflow.png
    ├── sediment_initial_labeled.png
    ├── sediment_mid_labeled.png
    └── sediment_final_labeled.png
```

The tree shows the runtime application, its analytical inputs, and assets. Internal audit notes and auxiliary development files are omitted for clarity.

## Installation and local execution

### 1. Clone the repository

```bash
git clone https://github.com/arzoochelsea/caipiringwer-thesis-dashboard.git
cd caipiringwer-thesis-dashboard
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies and run the dashboard

```bash
pip install -r requirements.txt
streamlit run app.py
```

Streamlit will print the local address, normally `http://localhost:8501`.

## Data requirements

The application expects the following repository-relative inputs:

| Data group | Expected location | Use |
|---|---|---|
| Flow-curve data | `data/rheology/Flow curve.xlsx` | Shear-rate, shear-stress, and apparent-viscosity analysis |
| Amplitude-sweep data | `data/rheology/Amplitude sweep.xlsx` | Strain-dependent viscoelastic response |
| Frequency-sweep data | `data/rheology/Frequency sweep.xlsx` | Frequency-dependent viscoelastic response |
| Rheology metadata | `data/rheology/Metadata.xlsx` | Sample, manufacturing-date, product-type, and replicate context |
| Physicochemical results | `data/physicochemical/physicochemical_results.ods` | Composition and storage-related measurements |
| Sedimentation images | `images/sediment_initial_labeled.png`, `images/sediment_mid_labeled.png`, `images/sediment_final_labeled.png` | Labelled photographic evidence displayed with the sedimentation analysis |
| Microbiology records | `data/microbiology/LIMS_Microbial_Audit.csv` | Qualitative status, media, treatment, sample, and date records |
| Microbiology plate images | `data/microbiology/` image files | Representative qualitative plate evidence discovered by the application |

Sedimentation measurements used for the implemented comparison are defined within the application; the repository does not contain a separate sedimentation workbook. Input schemas and filenames should be preserved unless the corresponding loading code is updated.

Not all raw, confidential, or restricted thesis data should necessarily be distributed with a public deployment. Any shared subset should be authorized and sufficient for the intended reproducibility level.

## Research context

This dashboard was created as part of a Master’s thesis in Applied Biotechnology. It supports structured interpretation and communication of beverage-quality measurements across complementary analytical domains; it does not claim publication, product validation, or regulatory approval.

## Data, privacy, and intellectual property

Experimental data may be subject to university, company, participant, or research-project restrictions. Do not upload confidential, identifiable, proprietary, or unpublished material without appropriate authorization.

Public repository visibility does not automatically grant permission to reuse experimental datasets, laboratory photographs, or other research assets. The absence of an open-source license also means that reuse rights are not automatically granted. This statement is informational and is not legal advice.

## License

No open-source license has currently been assigned. Unless otherwise stated, all rights are reserved.

## Author

**Arzoo**<br>
Master’s Student in Applied Biotechnology
