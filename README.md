# Caipiringwer Beverage Stability Analytics Dashboard

A bilingual Streamlit dashboard developed for a Master’s thesis in Applied Biotechnology. The application presents independent analytical modules for rheology, physicochemical measurements, sedimentation observations, and qualitative microbiology.

## Scientific scope

The analytical modules remain independent:

- **Rheology:** flow curves, amplitude sweeps, and frequency sweeps
- **Physicochemical analysis:** pH, soluble solids, density, specific gravity, sugar, and alcohol-related measurements
- **Sedimentation:** two-point sediment-bed observations and photographic evidence
- **Microbiology:** qualitative LIMS observations, treatment categories, culture media, and plate-image evidence

No universal sample identifier is imposed across modules. Cross-module joins and correlations are intentionally avoided unless sample traceability has been independently verified.

## Technology

- Python
- Streamlit
- pandas
- NumPy
- Plotly
- scikit-learn
- odfpy / Excel readers

## Project structure

```text
caipiringwer-thesis-dashboard/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── rheology/
│   ├── physicochemical/
│   └── microbiology/
├── images/
└── figures/
```

## Local installation

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL printed by Streamlit, normally:

```text
http://localhost:8501
```

## Required datasets

Place the files in the corresponding folders:

```text
data/rheology/Flow curve.xlsx
data/rheology/Amplitude sweep.xlsx
data/rheology/Frequency sweep.xlsx
data/rheology/Metadata.xlsx
data/physicochemical/physicochemical_results.ods
data/microbiology/LIMS_Microbial_Audit.csv
```

Sedimentation images:

```text
images/sediment_mid.png
images/sediment_final.png
```

Microbiology photographs are loaded from:

```text
data/microbiology/
```

## Interpretation boundaries

- Constitutive-model parameters are not treated as reliable material constants when model fit is poor.
- Oscillatory elastic dominance does not independently prove long-term shelf stability.
- Sedimentation conclusions are descriptive because only two observation times are available and no sedimentation replicates are recorded.
- Microbiology photographs are qualitative evidence only; no CFU values are inferred from images.
- The dashboard does not estimate a regulatory expiry date.

## Privacy and publication

Keep the repository **private** while it contains unpublished thesis data, laboratory photographs, company information, or identifiable research records.

Before making the repository public:

1. remove confidential or proprietary datasets;
2. remove personal or institutional identifiers that should not be published;
3. replace raw data with anonymized demonstration data where necessary;
4. verify image publication permission;
5. confirm approval from the thesis supervisor and industry partner.

## Author

Arzoo  
MSc Applied Biotechnology  
Hochschule Ansbach

## License

No open-source license is assigned by default. All rights are reserved until data ownership and publication permissions are clarified.
