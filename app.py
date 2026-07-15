from pathlib import Path

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Caipiringwer Beverage Stability Analytics Dashboard",
    page_icon="🧪",
    layout="wide",
)

st.markdown(
    """
    <style>
    :root {
        --ink: #132238;
        --muted: #64748b;
        --navy: #0b2942;
        --blue: #146c94;
        --cyan: #2fa7b8;
        --aqua: #68d1c7;
        --gold: #d9aa52;
        --line: rgba(17, 67, 98, 0.12);
        --surface: rgba(255, 255, 255, 0.92);
        --shadow: 0 18px 50px rgba(14, 53, 78, 0.09);
    }

    html, body, [class*="css"] { font-family: Inter, "Segoe UI", Arial, sans-serif; }
    .stApp {
        color: var(--ink);
        background:
            radial-gradient(circle at 88% 4%, rgba(104, 209, 199, 0.16), transparent 26rem),
            radial-gradient(circle at 20% 28%, rgba(20, 108, 148, 0.08), transparent 30rem),
            #f4f8fa;
    }
    .block-container { max-width: 1480px; padding: 2rem 2.6rem 5rem; }
    #MainMenu, footer { visibility: hidden; }
    header[data-testid="stHeader"] { background: rgba(244, 248, 250, 0.78); backdrop-filter: blur(18px); }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0a263d 0%, #0d354e 58%, #0c4054 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    [data-testid="stSidebar"] > div:first-child { padding: 1.4rem 1.15rem; }
    [data-testid="stSidebar"] * { color: rgba(255,255,255,0.90); }
    [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(255,255,255,0.10);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 12px;
    }
    .brand-lockup { padding: .35rem .15rem 1rem; }
    .brand-mark {
        width: 46px; height: 46px; display: grid; place-items: center;
        border-radius: 14px; margin-bottom: .8rem; font-size: 1.35rem;
        background: linear-gradient(135deg, var(--aqua), #2c8dad);
        box-shadow: 0 12px 30px rgba(0,0,0,.22);
    }
    .brand-name { font-size: 1.05rem; font-weight: 760; letter-spacing: .01em; }
    .brand-kicker { color: rgba(255,255,255,.55) !important; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; margin-top: .2rem; }

    .dashboard-hero {
        position: relative; overflow: hidden; padding: 2.2rem 2.35rem 2rem; margin: .25rem 0 1.35rem;
        border-radius: 26px; color: white;
        background: linear-gradient(120deg, #0a2942 0%, #0d526a 63%, #168395 100%);
        box-shadow: 0 24px 60px rgba(8, 52, 76, .22);
    }
    .dashboard-hero::after {
        content: ""; position: absolute; width: 300px; height: 300px; right: -80px; top: -125px;
        border: 1px solid rgba(255,255,255,.16); border-radius: 50%; box-shadow: 0 0 0 45px rgba(255,255,255,.035), 0 0 0 95px rgba(255,255,255,.025);
    }
    .hero-eyebrow { color: #9ee6df; font-size: .72rem; font-weight: 750; letter-spacing: .16em; text-transform: uppercase; margin-bottom: .6rem; }
    .hero-title { position: relative; z-index: 1; max-width: 980px; font-size: clamp(2rem, 3.3vw, 3.35rem); line-height: 1.04; font-weight: 780; letter-spacing: -.035em; margin: 0 0 .75rem; }
    .hero-subtitle { position: relative; z-index: 1; max-width: 980px; color: rgba(255,255,255,.72); font-size: 1rem; line-height: 1.65; }
    .hero-meta { position: relative; z-index: 1; display: flex; flex-wrap: wrap; gap: .55rem; margin-top: 1.25rem; }
    .hero-chip { padding: .42rem .72rem; border: 1px solid rgba(255,255,255,.14); border-radius: 999px; background: rgba(255,255,255,.08); color: rgba(255,255,255,.82); font-size: .78rem; }

    h1, h2, h3 { color: var(--ink); letter-spacing: -.025em; }
    h1 { font-weight: 780 !important; }
    h2 { margin-top: 1.6rem !important; font-weight: 740 !important; }
    h3 { font-weight: 700 !important; }
    p, li { line-height: 1.68; }
    [data-testid="stCaptionContainer"] { color: var(--muted); }

    .stTabs [data-baseweb="tab-list"] {
        gap: .3rem; padding: .35rem; margin: .2rem 0 1.15rem;
        border: 1px solid var(--line); border-radius: 15px; background: rgba(255,255,255,.72);
        box-shadow: 0 7px 24px rgba(15, 62, 88, .05); overflow-x: auto;
    }
    .stTabs [data-baseweb="tab"] {
        height: 2.65rem; padding: 0 .95rem; border-radius: 11px; border: 0;
        color: #567084; font-weight: 650; white-space: nowrap;
    }
    .stTabs [aria-selected="true"] { color: #0b526d !important; background: white !important; box-shadow: 0 5px 16px rgba(12, 68, 98, .10); }
    .stTabs [data-baseweb="tab-highlight"] { display: none; }

    [data-testid="stMetric"] {
        min-height: 116px; padding: 1.05rem 1.15rem;
        background: var(--surface); border: 1px solid var(--line); border-radius: 18px;
        box-shadow: 0 12px 32px rgba(14, 53, 78, .07); transition: transform .18s ease, box-shadow .18s ease;
    }
    [data-testid="stMetric"]:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
    [data-testid="stMetricLabel"] { color: #698093; font-weight: 650; }
    [data-testid="stMetricValue"] { color: #0b415d; font-weight: 770; letter-spacing: -.035em; }

    [data-testid="stDataFrame"], [data-testid="stTable"] { border: 1px solid var(--line); border-radius: 18px; overflow: hidden; box-shadow: 0 12px 35px rgba(14,53,78,.06); }
    [data-testid="stPlotlyChart"] { padding: .65rem; border: 1px solid var(--line); border-radius: 20px; background: rgba(255,255,255,.88); box-shadow: 0 14px 38px rgba(14,53,78,.065); }
    [data-testid="stImage"] img { border-radius: 18px; box-shadow: 0 16px 38px rgba(14,53,78,.12); }

    [data-testid="stAlert"] { border-radius: 16px; border: 1px solid rgba(20,108,148,.14); }
    [data-testid="stExpander"] { background: rgba(255,255,255,.76); border: 1px solid var(--line); border-radius: 15px; overflow: hidden; }
    .stSelectbox [data-baseweb="select"] > div, .stMultiSelect [data-baseweb="select"] > div { border-radius: 13px; border-color: var(--line); background: white; }
    .stButton > button, .stDownloadButton > button { border-radius: 12px; border: 0; color: white; font-weight: 700; background: linear-gradient(135deg, #146c94, #168b91); box-shadow: 0 10px 22px rgba(20,108,148,.18); }

    .section-card { background: var(--surface); border: 1px solid var(--line); border-radius: 20px; padding: 1.3rem; margin-bottom: 1rem; box-shadow: var(--shadow); }
    .scientific-title { color: #0f5f78; font-weight: 750; letter-spacing: .02em; }
    .status-card { background: rgba(20,108,148,.06); border-left: 4px solid var(--blue); border-radius: 14px; padding: .9rem 1rem; }
    .status-pill { display: inline-block; padding: .35rem .65rem; border-radius: 999px; font-weight: 700; }
    .excellent { background: rgba(31,153,133,.13); color: #147661; }
    .moderate { background: rgba(217,170,82,.16); color: #916517; }
    .poor { background: rgba(209,76,86,.13); color: #a4323c; }

    .audit-ribbon {
        display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1px;
        margin: -.35rem 0 1.5rem; overflow: hidden; border: 1px solid var(--line);
        border-radius: 16px; background: var(--line); box-shadow: 0 10px 28px rgba(14,53,78,.05);
    }
    .audit-item { padding: .82rem 1rem; background: rgba(255,255,255,.88); }
    .audit-label { color: #7b8d9b; font-size: .66rem; font-weight: 760; letter-spacing: .1em; text-transform: uppercase; }
    .audit-value { color: #173b50; font-size: .88rem; font-weight: 690; margin-top: .18rem; }
    .evidence-grid { display: grid; grid-template-columns: repeat(4, minmax(0,1fr)); gap: .85rem; margin: .85rem 0 1.6rem; }
    .evidence-card {
        position: relative; overflow: hidden; min-height: 168px; padding: 1.1rem 1.05rem 1rem;
        border: 1px solid var(--line); border-radius: 18px; background: rgba(255,255,255,.9);
        box-shadow: 0 12px 32px rgba(14,53,78,.06);
    }
    .evidence-card::before { content: ""; position: absolute; inset: 0 auto 0 0; width: 4px; background: var(--card-accent, var(--blue)); }
    .evidence-index { color: #8aa0ad; font-size: .68rem; font-weight: 780; letter-spacing: .12em; }
    .evidence-name { color: #15394f; font-size: 1rem; font-weight: 760; margin: .3rem 0 .5rem; }
    .evidence-detail { color: #63798a; font-size: .78rem; line-height: 1.45; }
    .evidence-status { display: inline-flex; align-items: center; gap: .35rem; margin-top: .75rem; color: #24675f; font-size: .72rem; font-weight: 720; }
    .evidence-status::before { content: ""; width: 7px; height: 7px; border-radius: 50%; background: #36a88e; box-shadow: 0 0 0 4px rgba(54,168,142,.12); }
    .governance-note { padding: 1rem 1.1rem; border-radius: 16px; border: 1px solid rgba(217,170,82,.24); background: linear-gradient(110deg, rgba(217,170,82,.10), rgba(255,255,255,.72)); color: #564624; font-size: .86rem; line-height: 1.6; }

    @media (max-width: 800px) {
        .block-container { padding: 1rem 1rem 3rem; }
        .dashboard-hero { padding: 1.55rem 1.3rem; border-radius: 20px; }
        .hero-title { font-size: 2rem; }
        [data-testid="stMetric"] { min-height: 100px; }
        .audit-ribbon, .evidence-grid { grid-template-columns: 1fr 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

TRANSLATIONS = {
    "EN": {
        "language": "Language",
        "title": "Caipiringwer Beverage Stability Analytics Dashboard",
        "subtitle": "Bilingual scientific dashboard for independent rheological, physicochemical, sedimentation, and microbiological analysis of a ginger–lime beverage system.",
        "module": "Module",
        "flow": "Flow",
        "amp": "Amplitude sweep",
        "freq": "Frequency sweep",
        "physical": "Physical Stability and Sedimentation Assessment",
        "summary": "Results and synthesis",
        "literature": "References and literature support",
        "observed_records": "Measured records",
        "distinct_samples": "Distinct sample families",
        "temperature": "Temperature range",
        "shear_rate": "Shear-rate range",
        "ensemble": "Measured dataset overview",
        "flow_header": "Flow curve module",
        "amp_header": "Amplitude sweep module",
        "freq_header": "Frequency sweep module",
        "summary_header": "Results and synthesis",
        "literature_header": "References and literature support",
        "lit_text": "This chapter uses the measured workbook data as the sole analytical basis. The literature references support the interpretation and help position the rheology results within a scientific context.",
    },
    "DE": {
        "language": "Sprache",
        "title": "Caipiringwer Analyseplattform für Getränkestabilität",
        "subtitle": "Zweisprachiges wissenschaftliches Dashboard zur unabhängigen rheologischen, physikochemischen, sedimentationsbezogenen und mikrobiologischen Analyse eines Ingwer-Limetten-Getränkesystems.",
        "module": "Modul",
        "flow": "Fließverhalten",
        "amp": "Amplitudensweep",
        "freq": "Frequenzsweep",
        "physical": "Physische Stabilität und Sedimentationsbewertung",
        "summary": "Ergebnisse und Synthese",
        "literature": "Literaturhinweise und fachliche Einordnung",
        "observed_records": "Gemessene Datensätze",
        "distinct_samples": "Unterschiedliche Probenfamilien",
        "temperature": "Temperaturbereich",
        "shear_rate": "Scherratenbereich",
        "ensemble": "Messdatensatz-Übersicht",
        "flow_header": "Fließkurvenmodul",
        "amp_header": "Amplitudensweep-Modul",
        "freq_header": "Frequenzsweep-Modul",
        "summary_header": "Ergebnisse und Synthese",
        "literature_header": "Literaturhinweise und fachliche Einordnung",
        "lit_text": "Dieses Kapitel stützt sich ausschließlich auf die gemessenen Workbook-Daten. Die Literaturhinweise dienen der fachlichen Einordnung und unterstützen die Interpretation der Rheologieergebnisse.",
    },
}

TRANSLATIONS["EN"].update({
    "dashboard_settings": "Dashboard Settings", "scientific_modules": "Scientific Modules",
    "experimental_assets": "Experimental Assets", "project_information": "Project Information",
    "rheology": "Rheology", "physicochemical": "Physicochemical", "sedimentation": "Sedimentation", "microbiology": "Microbiology",
    "rheology_loaded": "Rheology datasets loaded", "physchem_loaded": "Physicochemical datasets loaded",
    "sed_images_loaded": "Sedimentation images loaded", "micro_images_loaded": "Microbiology images loaded",
    "project": "Project", "degree": "Degree", "institution": "Institution", "instrumentation": "Instrumentation",
    "project_value": "Caipiringwer Stability Assessment", "degree_value": "MSc Biotechnology", "institution_value": "Hochschule Ansbach",
    "top_executive": "🏠 Executive Summary", "top_rheology": "🧪 Rheology", "top_physchem": "🧃 Physicochemical", "top_sedimentation": "🟤 Sedimentation", "top_microbiology": "🦠 Microbiology", "top_references": "📚 References",
    "flow_curve": "Flow Curve", "amplitude_sweep": "Amplitude Sweep", "frequency_sweep": "Frequency Sweep", "interpretation": "Interpretation",
    "overview": "Overview", "composition": "Composition", "trends": "Trends", "correlations": "Correlations",
    "sed_images": "📷 Images", "sed_analysis": "📈 Analysis", "sed_interpretation": "🧠 Interpretation", "sed_references": "📚 References",
    "available": "Available", "pending": "Pending", "not_loaded": "Not loaded",
    "executive_project": "Caipiringwer Stability Assessment", "study_architecture": "Overall study architecture",
    "integrated_conclusion": "Integrated conclusion", "data_integrity": "Each analytical module retains its own sample identifiers, experimental design, and metadata. Cross-module statistical joins are not performed because sample traceability across experiments has not been independently verified.",
    "bottle_statement": "Bottle condition before filling: The bottles were not subjected to a prior washing step. Before use, each bottle was visually inspected and accepted only when no visible particles or foreign material were observed. This procedure confirms visual cleanliness only and does not demonstrate microbiological cleanliness or sterility.",
    "bottle_limitation": "Because the bottles were not washed or microbiologically validated before filling, packaging-related contamination cannot be excluded as a possible uncontrolled factor.",
    "rheo_overview": "Overview and experimental design", "rheo_interpretation": "Integrated rheology interpretation", "rheo_metadata": "Metadata and raw data", "rheo_references": "Rheology references",
    "micro_exec": "Executive overview", "micro_results": "Plate results", "micro_visual": "Visual evidence", "micro_interpretation": "Scientific interpretation", "micro_shelf": "Shelf-life assessment", "micro_literature": "Literature support",
    "sed_dataset": "Measured sedimentation dataset",
})
TRANSLATIONS["DE"].update({
    "dashboard_settings": "Dashboard-Einstellungen", "scientific_modules": "Wissenschaftliche Module",
    "experimental_assets": "Experimentelle Datenquellen", "project_information": "Projektinformationen",
    "rheology": "Rheologie", "physicochemical": "Physikochemie", "sedimentation": "Sedimentation", "microbiology": "Mikrobiologie",
    "rheology_loaded": "Rheologie-Datensätze geladen", "physchem_loaded": "Physikochemische Datensätze geladen",
    "sed_images_loaded": "Sedimentationsbilder geladen", "micro_images_loaded": "Mikrobiologiebilder geladen",
    "project": "Projekt", "degree": "Abschluss", "institution": "Institution", "instrumentation": "Instrumentierung",
    "project_value": "Caipiringwer-Stabilitätsbewertung", "degree_value": "MSc Biotechnologie", "institution_value": "Hochschule Ansbach",
    "top_executive": "🏠 Managementübersicht", "top_rheology": "🧪 Rheologie", "top_physchem": "🧃 Physikochemie", "top_sedimentation": "🟤 Sedimentation", "top_microbiology": "🦠 Mikrobiologie", "top_references": "📚 Literatur",
    "flow_curve": "Fließkurve", "amplitude_sweep": "Amplitudensweep", "frequency_sweep": "Frequenzsweep", "interpretation": "Interpretation",
    "overview": "Übersicht", "composition": "Zusammensetzung", "trends": "Trends", "correlations": "Korrelationen",
    "sed_images": "📷 Bilder", "sed_analysis": "📈 Analyse", "sed_interpretation": "🧠 Interpretation", "sed_references": "📚 Literatur",
    "available": "Verfügbar", "pending": "Ausstehend", "not_loaded": "Nicht geladen",
    "executive_project": "Caipiringwer-Stabilitätsbewertung", "study_architecture": "Übergreifende Studienarchitektur",
    "integrated_conclusion": "Integrierte Schlussfolgerung", "data_integrity": "Jedes Analysemodul behält seine eigenen Probenkennungen, sein Versuchsdesign und seine Metadaten. Modulübergreifende statistische Verknüpfungen werden nicht durchgeführt, da die Rückverfolgbarkeit der Proben zwischen den Experimenten nicht unabhängig bestätigt wurde.",
    "bottle_statement": "Zustand der Flaschen vor der Befüllung: Die Flaschen wurden vor der Verwendung keinem Waschschritt unterzogen. Vor der Befüllung wurde jede Flasche visuell kontrolliert und nur dann verwendet, wenn keine sichtbaren Partikel oder Fremdmaterialien erkennbar waren. Dieses Vorgehen bestätigt ausschließlich die visuelle Sauberkeit und stellt keinen Nachweis mikrobiologischer Sauberkeit oder Sterilität dar.",
    "bottle_limitation": "Da die Flaschen vor der Befüllung weder gewaschen noch mikrobiologisch validiert wurden, kann eine verpackungsbedingte Kontamination als möglicher unkontrollierter Einflussfaktor nicht ausgeschlossen werden.",
    "rheo_overview": "Übersicht und Versuchsdesign", "rheo_interpretation": "Integrierte rheologische Interpretation", "rheo_metadata": "Metadaten und Rohdaten", "rheo_references": "Rheologische Literatur", 
    "micro_exec": "Managementübersicht", "micro_results": "Plattenergebnisse", "micro_visual": "Bildnachweise", "micro_interpretation": "Wissenschaftliche Interpretation", "micro_shelf": "Haltbarkeitsbewertung", "micro_literature": "Literatur", 
    "sed_dataset": "Gemessener Sedimentationsdatensatz",
})

LANG = st.sidebar.selectbox("Language / Sprache", ["EN", "DE"], index=0)
T = TRANSLATIONS[LANG]


def tr(english: str, german: str) -> str:
    """Return user-facing copy in the currently selected language."""
    return german if LANG == "DE" else english


def resolve_dataset_path(filename: str) -> Path:
    candidates = [
        Path.cwd() / filename,
        Path.cwd() / "data" / filename,
        Path.cwd() / "data" / "rheology" / filename,
        Path(__file__).resolve().parent / filename,
        Path(__file__).resolve().parent / "data" / filename,
        Path(__file__).resolve().parent / "data" / "rheology" / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0]


@st.cache_data
def load_physicochemical_dataset():
    phys_path = Path("data/physicochemical/physicochemical_results.ods")
    if not phys_path.exists():
        return pd.DataFrame()

    raw = pd.read_excel(phys_path, header=None)
    if raw.shape[0] <= 17:
        return pd.DataFrame()

    header = raw.iloc[17].fillna("").astype(str).str.strip()
    data = raw.iloc[18:].copy().reset_index(drop=True)
    data.columns = header
    data = data.loc[:, ~data.columns.str.contains("Unnamed", na=False)]
    data = data.dropna(how="all").reset_index(drop=True)

    seen = {}
    tidy_columns = []
    for col in data.columns:
        key = str(col).strip()
        seen[key] = seen.get(key, 0) + 1
        if seen[key] == 1:
            tidy_columns.append(key)
        else:
            tidy_columns.append(f"{key} ({seen[key]})")
    data.columns = tidy_columns

    data = data.rename(columns={
        "Sample ID": "Sample_ID",
        "Storage": "Storage_Date",
        "Storage duration": "Storage_Duration",
        "Type": "Product_Type",
        "Specific Gravity (g/cm³)": "Specific_Gravity",
        "Density (g/cm³)": "Density_g_cm3",
        "Potential Alcohol (% v/v)": "Potential_Alcohol_vv",
        "Alcohol Percentage (% v/v)": "Alcohol_Percentage_vv",
        "Refractive Index (nD)": "Refractive_Index_nD",
        "Sugar (g/L)": "Sugar_g_L",
        "Oechsel (°Oe CH)": "Oechsel",
        "pH": "pH",
    })

    data["Sample_ID"] = pd.to_numeric(data["Sample_ID"], errors="coerce")
    data["Storage_Date"] = pd.to_datetime(data["Storage_Date"], errors="coerce", format="%d.%m.%Y")
    data["Storage_Duration"] = data["Storage_Duration"].astype(str).str.strip()
    data["Product_Type"] = data["Product_Type"].astype(str).str.strip()

    brix_cols = [col for col in data.columns if col.startswith("Brix (°Bx)")]
    if brix_cols:
        data["Brix_Avg"] = data[brix_cols].apply(pd.to_numeric, errors="coerce").mean(axis=1, skipna=True)

    for col in ["Sugar_g_L", "Potential_Alcohol_vv", "Alcohol_Percentage_vv", "Refractive_Index_nD", "Oechsel", "Density_g_cm3", "Specific_Gravity", "pH"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    return data


@st.cache_data
def discover_evidence_photos():
    roots = [Path("data"), Path("figures")]
    photo_files = []
    allowed = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".gif", ".tif", ".tiff"}
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in allowed:
                photo_files.append(path)
    return photo_files


@st.cache_data
def load_datasets():
    flow = pd.read_excel(resolve_dataset_path("Flow curve.xlsx"))
    amp = pd.read_excel(resolve_dataset_path("Amplitude sweep.xlsx"))
    freq = pd.read_excel(resolve_dataset_path("Frequency sweep.xlsx"))
    meta = pd.read_excel(resolve_dataset_path("Metadata.xlsx"))

    for df in (flow, amp, freq, meta):
        df.columns = [str(col).strip() for col in df.columns]

    for df in (flow, amp, freq):
        df["Sample"] = df["Sample"].astype(str).str.strip()
        df["Sample_Family"] = df["Sample"].str.replace(r"\.\d+$", "", regex=True)

        if "Manufacturing_Date" in df.columns:
            df["Manufacturing_Date"] = pd.to_datetime(
                df["Manufacturing_Date"],
                errors="coerce",
                format="%d.%m.%Y",
            )

    meta = meta.loc[:, [col for col in meta.columns if col in {"Sample_ID", "Manufacturing_Date", "Product_Type", "Replicate_Number"}]].copy()
    meta["Measurement_ID"] = meta["Sample_ID"].astype(str).str.strip()
    meta["Parent_Sample"] = meta["Measurement_ID"].str.replace(r"\.\d+$", "", regex=True)
    meta["Replicate_Number"] = pd.to_numeric(meta["Replicate_Number"], errors="coerce").fillna(0).astype(int)
    meta["Product_Type"] = meta["Product_Type"].astype(str).str.strip()
    meta["Manufacturing_Date"] = pd.to_datetime(
        meta["Manufacturing_Date"],
        errors="coerce",
        format="%d.%m.%Y",
    )

    numeric_cols = {
        "flow": ["T (°C)", "σ (Pa)", "ɣ̇ (s⁻¹)", "η (Pa s)", "F (N)", "g (mm)", "τ (N m)", "θ'(t) (rad/s)", "θabs (rad)"],
        "amp": ["T (°C)", "f (Hz)", "γ* (%)", "σ* (Pa)", "G* (Pa)", "G' (Pa)", 'G" (Pa)', "η* (Pa s)", "δ (°)", "F (N)", "g (mm)", "τ (N m)", "θ (rad)"],
        "freq": ["T (°C)", "f (Hz)", "γ* (%)", "σ* (Pa)", "G* (Pa)", "G' (Pa)", 'G" (Pa)', "η* (Pa s)", "δ (°)", "F (N)", "g (mm)", "τ (N m)", "θ (rad)", "HD (%)"],
    }

    for target_name, cols in numeric_cols.items():
        df = flow if target_name == "flow" else amp if target_name == "amp" else freq
        for col in cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    physchem = load_physicochemical_dataset()
    return flow, amp, freq, meta, physchem


def safe_mean(series):
    values = pd.to_numeric(series, errors="coerce").dropna()
    if values.empty:
        return np.nan
    return float(values.mean())


@st.cache_data
def fit_power_law(flow_subset):
    valid = flow_subset[["ɣ̇ (s⁻¹)", "σ (Pa)"]].dropna()
    if valid.empty or valid["ɣ̇ (s⁻¹)"].nunique() < 2:
        return np.nan, np.nan

    x = np.log10(valid["ɣ̇ (s⁻¹)"].clip(lower=1e-9))
    y = np.log10(valid["σ (Pa)"].clip(lower=1e-9))

    try:
        slope, intercept = np.polyfit(x, y, 1)
    except np.linalg.LinAlgError:
        return np.nan, np.nan

    n = float(slope)
    k = float(10 ** intercept)
    return n, k


def loglog_fit(df, x_col, y_col):
    """Return slope, intercept, and R² for positive measured values only."""
    valid = df[[x_col, y_col]].dropna()
    valid = valid[(valid[x_col] > 0) & (valid[y_col] > 0)]
    if len(valid) < 3 or valid[x_col].nunique() < 2:
        return np.nan, np.nan, np.nan

    x = np.log10(valid[x_col].to_numpy())
    y = np.log10(valid[y_col].to_numpy())
    try:
        slope, intercept = np.polyfit(x, y, 1)
    except np.linalg.LinAlgError:
        return np.nan, np.nan, np.nan

    predicted = slope * x + intercept
    residual = np.sum((y - predicted) ** 2)
    total = np.sum((y - y.mean()) ** 2)
    r_squared = 1 - residual / total if total > 0 else np.nan
    return float(slope), float(intercept), float(r_squared)


def power_law_model_details(flow_subset):
    """Descriptive power-law fit to one parent sample; no extrapolation is used."""
    valid = flow_subset[["ɣ̇ (s⁻¹)", "σ (Pa)"]].dropna()
    valid = valid[(valid["ɣ̇ (s⁻¹)"] > 0) & (valid["σ (Pa)"] > 0)].copy()
    if len(valid) < 3 or valid["ɣ̇ (s⁻¹)"].nunique() < 2:
        return {key: np.nan for key in ("n", "k", "r2", "adj_r2", "rmse", "aicc", "n_obs")}, valid
    n, log_k, r2 = loglog_fit(valid, "ɣ̇ (s⁻¹)", "σ (Pa)")
    k = 10 ** log_k
    fitted = k * valid["ɣ̇ (s⁻¹)"] ** n
    residual = valid["σ (Pa)"] - fitted
    n_obs, n_parameters = len(valid), 2
    log_residual = np.log10(valid["σ (Pa)"]) - np.log10(fitted)
    sse = float(np.sum(log_residual ** 2))
    aic = n_obs * np.log(max(sse / n_obs, np.finfo(float).tiny)) + 2 * n_parameters
    aicc = aic + (2 * n_parameters * (n_parameters + 1) / (n_obs - n_parameters - 1)) if n_obs > n_parameters + 1 else np.nan
    valid["Fitted stress (Pa)"] = fitted
    valid["Stress residual (Pa)"] = residual
    return {
        "n": n, "k": k, "r2": r2,
        "adj_r2": 1 - (1 - r2) * (n_obs - 1) / (n_obs - n_parameters - 1),
        "rmse": float(np.sqrt(np.mean(residual ** 2))), "aicc": float(aicc), "n_obs": n_obs,
    }, valid


def measured_curve(df, x_col, value_cols):
    """Mean replicate readings at each measured setpoint; no interpolation."""
    return (
        df[[x_col, *value_cols]]
        .dropna(subset=[x_col])
        .groupby(x_col, as_index=False)[value_cols]
        .mean()
        .sort_values(x_col)
        .reset_index(drop=True)
    )


def nearest_measured_value(curve, x_col, y_col, target):
    valid = curve[[x_col, y_col]].dropna()
    if valid.empty:
        return np.nan, np.nan
    nearest_index = (np.log10(valid[x_col].clip(lower=1e-12)) - np.log10(target)).abs().idxmin()
    return float(valid.loc[nearest_index, y_col]), float(valid.loc[nearest_index, x_col])


def amplitude_metrics(amp_subset):
    curve = measured_curve(amp_subset, "γ* (%)", ["G' (Pa)", 'G" (Pa)', "η* (Pa s)"])
    valid = curve.dropna(subset=["G' (Pa)"])
    if valid.empty:
        return curve, {key: np.nan for key in ("reference_gprime", "lvr_limit", "retention", "max_strain", "crossover")}

    baseline = float(valid["G' (Pa)"].head(min(3, len(valid))).median())
    deviation = (valid["G' (Pa)"] - baseline).abs() > baseline * 0.05
    sustained = deviation & deviation.shift(-1, fill_value=False)
    first_deviation = valid.loc[sustained, "γ* (%)"]
    lvr_limit = float(first_deviation.iloc[0]) if not first_deviation.empty else float(valid["γ* (%)"].max())
    max_row = valid.iloc[-1]
    retention = float(max_row["G' (Pa)"] / baseline * 100) if baseline > 0 else np.nan
    crossover_rows = curve.dropna(subset=["G' (Pa)", 'G" (Pa)']).copy()
    crossover = np.nan
    if len(crossover_rows) > 1:
        gaps = crossover_rows["G' (Pa)"] - crossover_rows['G" (Pa)']
        change = gaps.mul(gaps.shift(1)).lt(0)
        if change.any():
            crossover = float(crossover_rows.loc[change, "γ* (%)"].iloc[0])
    return curve, {
        "reference_gprime": baseline,
        "lvr_limit": lvr_limit,
        "retention": retention,
        "max_strain": float(max_row["γ* (%)"]),
        "crossover": crossover,
    }


def frequency_metrics(freq_subset):
    curve = measured_curve(freq_subset, "f (Hz)", ["G' (Pa)", 'G" (Pa)', "η* (Pa s)", "δ (°)"])
    valid = curve.dropna(subset=["G' (Pa)", 'G" (Pa)']).copy()
    if valid.empty:
        return curve, {key: np.nan for key in ("tan_delta", "elastic_ratio", "gprime_slope", "gprime_r2", "low_gprime", "high_gprime", "crossover")}

    valid["tan_delta"] = valid['G" (Pa)'] / valid["G' (Pa)"].replace(0, np.nan)
    slope, _, r_squared = loglog_fit(valid, "f (Hz)", "G' (Pa)")
    gaps = valid["G' (Pa)"] - valid['G" (Pa)']
    change = gaps.mul(gaps.shift(1)).lt(0)
    crossover = float(valid.loc[change, "f (Hz)"].iloc[0]) if change.any() else np.nan
    return curve, {
        "tan_delta": float(valid["tan_delta"].median()),
        "elastic_ratio": float((valid["G' (Pa)"] / valid['G" (Pa)'].replace(0, np.nan)).median()),
        "gprime_slope": slope,
        "gprime_r2": r_squared,
        "low_gprime": float(valid.iloc[0]["G' (Pa)"]),
        "high_gprime": float(valid.iloc[-1]["G' (Pa)"]),
        "crossover": crossover,
    }


@st.cache_data
def build_sample_profile_table(flow, amp, freq, meta):
    overview = (
        meta.groupby("Parent_Sample", as_index=False)
        .agg(
            Product_Type=("Product_Type", "first"),
            Manufacturing_Date=("Manufacturing_Date", "first"),
            Number_of_Replicates=("Measurement_ID", "size"),
        )
        .rename(columns={"Parent_Sample": "Sample_ID"})
        .sort_values("Sample_ID")
        .reset_index(drop=True)
    )

    profiles = overview.copy()
    profiles["Age_Days"] = (pd.Timestamp.today().normalize() - profiles["Manufacturing_Date"]).dt.days
    profiles["Mean_Viscosity"] = np.nan
    profiles["Mean_Gprime"] = np.nan
    profiles["Mean_Gdouble"] = np.nan
    profiles["Mean_tan_delta"] = np.nan
    profiles["Flow_behavior_index_n"] = np.nan
    profiles["Consistency_coefficient_K"] = np.nan
    profiles["Elastic_Dominance_Ratio"] = np.nan

    for index, row in profiles.iterrows():
        sample_id = row["Sample_ID"]
        flow_subset = flow[flow["Sample_Family"] == sample_id]
        amp_subset = amp[amp["Sample_Family"] == sample_id]
        freq_subset = freq[freq["Sample_Family"] == sample_id]

        mean_viscosity = safe_mean(flow_subset["η (Pa s)"])
        mean_gprime = safe_mean(pd.concat([amp_subset["G' (Pa)"], freq_subset["G' (Pa)"]], ignore_index=True))
        mean_gdouble = safe_mean(pd.concat([amp_subset['G" (Pa)'], freq_subset['G" (Pa)']], ignore_index=True))
        mean_tandelta = safe_mean(
            freq_subset['G" (Pa)'] / freq_subset["G' (Pa)"].replace(0, np.nan)
        )
        n, k = fit_power_law(flow_subset)

        profiles.at[index, "Mean_Viscosity"] = mean_viscosity
        profiles.at[index, "Mean_Gprime"] = mean_gprime
        profiles.at[index, "Mean_Gdouble"] = mean_gdouble
        profiles.at[index, "Mean_tan_delta"] = mean_tandelta
        profiles.at[index, "Flow_behavior_index_n"] = n
        profiles.at[index, "Consistency_coefficient_K"] = k

    profiles["Elastic_Dominance_Ratio"] = profiles["Mean_Gprime"] / profiles["Mean_Gdouble"].replace(0, np.nan)
    return profiles


flow, amp, freq, meta, physchem = load_datasets()

REFERENCE_LIBRARY = [
    {
        "title": "Staubmann, D. et al. (2023). Combinations of hydrocolloids show enhanced stabilizing effects on cloudy orange juice ready-to-drink beverages. Food Hydrocolloids, 138, 108436.",
        "doi": "10.1016/j.foodhyd.2022.108436",
        "publication_link": "https://doi.org/10.1016/j.foodhyd.2022.108436",
        "relevance": "Supports discussion of hydrocolloid-driven beverage structure; it does not prove stabilization or sedimentation performance in this independent dataset.",
    },
    {
        "title": "Malafronte, L. et al. (2023). Shear and extensional rheological properties of whole grain rye and oat aqueous suspensions. Food Hydrocolloids, 137, 108319.",
        "doi": "10.1016/j.foodhyd.2022.108319",
        "publication_link": "https://doi.org/10.1016/j.foodhyd.2022.108319",
        "relevance": "Supports measured-flow and suspension-rheology context; it does not validate a constitutive model for these samples.",
    },
    {
        "title": "Wilbanks, C., Yazdi, S. R. & Lucey, J. A. (2022). Effects of varying casein and pectin concentrations on the rheology of high-protein cultured milk beverages stored at ambient temperature. Journal of Dairy Science, 105, 72–82.",
        "doi": "10.3168/jds.2021-20597",
        "publication_link": "https://doi.org/10.3168/jds.2021-20597",
        "relevance": "Supports the distinction between flow and oscillatory material response; it does not establish shelf life for this beverage system.",
    },
    {
        "title": "Erturk, S., Le, H. M. & Kokini, J. L. (2023). Advances in large amplitude oscillatory shear rheology of food materials. Frontiers in Food Science and Technology, 3, 1130165.",
        "doi": "10.3389/frfst.2023.1130165",
        "publication_link": "https://doi.org/10.3389/frfst.2023.1130165",
        "relevance": "Supports cautious interpretation of deformation-dependent rheology; it does not infer unmeasured structural failure or product stability.",
    },
]

sample_overview = (
    meta.groupby("Parent_Sample", as_index=False)
    .agg(
        Product_Type=("Product_Type", "first"),
        Manufacturing_Date=("Manufacturing_Date", "first"),
        Number_of_Replicates=("Measurement_ID", "size"),
    )
    .rename(columns={"Parent_Sample": "Sample_ID"})
    .sort_values("Sample_ID")
    .reset_index(drop=True)
)

sample_profiles = build_sample_profile_table(flow, amp, freq, meta)

# Scientific summary metrics derived from the measured datasets
mean_viscosity = safe_mean(flow["η (Pa s)"])
mean_gprime = safe_mean(pd.concat([amp["G' (Pa)"], freq["G' (Pa)"]], ignore_index=True))
mean_gdouble = safe_mean(pd.concat([amp['G" (Pa)'], freq['G" (Pa)']], ignore_index=True))
mean_tandelta = safe_mean(freq["δ (°)"])
flow_behavior_index_n, consistency_coefficient_k = fit_power_law(flow)


sample_overview["Manufacturing_Date"] = sample_overview["Manufacturing_Date"].dt.strftime("%d.%m.%Y")

st.markdown(
    f"""
    <section class="dashboard-hero">
        <div class="hero-eyebrow">{tr('Applied beverage science · MSc research platform', 'Angewandte Getränkewissenschaft · MSc-Forschungsplattform')}</div>
        <div class="hero-title">{T['title']}</div>
        <div class="hero-subtitle">{T['subtitle']}</div>
        <div class="hero-meta">
            <span class="hero-chip">◈ Hochschule Ansbach</span>
            <span class="hero-chip">Kinexus Prime Lab+</span>
            <span class="hero-chip">EasyDens · SmartRef</span>
            <span class="hero-chip">{tr('Measured evidence', 'Gemessene Evidenz')}</span>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <div class="audit-ribbon">
        <div class="audit-item"><div class="audit-label">{tr('Evidence model', 'Evidenzmodell')}</div><div class="audit-value">{tr('Measured + derived', 'Gemessen + abgeleitet')}</div></div>
        <div class="audit-item"><div class="audit-label">{tr('Analytical scope', 'Analytischer Umfang')}</div><div class="audit-value">4 {tr('independent modules', 'unabhängige Module')}</div></div>
        <div class="audit-item"><div class="audit-label">{tr('Traceability', 'Rückverfolgbarkeit')}</div><div class="audit-value">{tr('Source-level identifiers retained', 'Quellkennungen beibehalten')}</div></div>
        <div class="audit-item"><div class="audit-label">{tr('Statistical policy', 'Statistische Richtlinie')}</div><div class="audit-value">{tr('No unsupported joins', 'Keine unbelegten Verknüpfungen')}</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        f"""
        <div class="brand-lockup">
            <div class="brand-mark">◈</div>
            <div class="brand-name">Caipiringwer Analytics</div>
            <div class="brand-kicker">{tr('Stability intelligence', 'Stabilitätsanalyse')}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.subheader(T["dashboard_settings"])
    st.caption(f"{T['language']}: {LANG}")
    st.divider()
    st.subheader(T["scientific_modules"])
    st.markdown(
        f"- {T['rheology']}\n- {T['physicochemical']}\n- {T['sedimentation']}\n- {T['microbiology']}"
    )
    st.divider()
    st.subheader(T["experimental_assets"])
    st.markdown(
        f"- **{T['available']}** · {T['rheology_loaded']}\n"
        f"- **{T['available'] if not physchem.empty else T['not_loaded']}** · {T['physchem_loaded']}\n"
        f"- **{T['available'] if Path('images/sediment_mid.png').exists() else T['pending']}** · {T['sed_images_loaded']}\n"
        f"- **{T['available'] if Path('data/microbiology').exists() else T['not_loaded']}** · {T['micro_images_loaded']}"
    )
    st.divider()
    st.subheader(T["project_information"])
    st.markdown(
        f"**{T['project']}:** {T['project_value']}\n\n"
        f"**{T['degree']}:** {T['degree_value']}\n\n"
        f"**{T['institution']}:** {T['institution_value']}\n\n"
        f"**{T['instrumentation']}:** Kinexus Prime Lab+ · EasyDens · SmartRef"
    )
    st.divider()
    st.subheader(tr("Report controls", "Berichtssteuerung"))
    visual_density = st.radio(
        tr("Visual density", "Darstellungsdichte"),
        [tr("Comfortable", "Komfortabel"), tr("Compact", "Kompakt")],
        horizontal=True,
        key="visual_density",
    )
    show_methodology = st.toggle(
        tr("Show methodology matrix", "Methodenmatrix anzeigen"),
        value=True,
        help=tr(
            "Displays an audit-oriented overview of evidence type, replication, and limitations.",
            "Zeigt eine auditierbare Übersicht zu Evidenztyp, Replikation und Limitationen.",
        ),
    )

if visual_density == tr("Compact", "Kompakt"):
    st.markdown(
        """
        <style>
        .block-container { max-width: 1580px; }
        [data-testid="stMetric"] { min-height: 96px; padding: .8rem .9rem; }
        [data-testid="stPlotlyChart"] { padding: .35rem; }
        .stTabs [data-baseweb="tab"] { height: 2.35rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

chart_theme = go.layout.Template(
    layout=go.Layout(
        font=dict(family="Inter, Segoe UI, Arial", color="#24384a", size=13),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(248,251,252,0.72)",
        colorway=["#146c94", "#2fa7b8", "#d9aa52", "#68a67d", "#b96070", "#7667a8"],
        title=dict(font=dict(size=18, color="#132f45"), x=0.02, xanchor="left"),
        hoverlabel=dict(bgcolor="white", bordercolor="#c8d8df", font=dict(color="#183247")),
        legend=dict(bgcolor="rgba(255,255,255,.76)", bordercolor="rgba(17,67,98,.10)", borderwidth=1),
        xaxis=dict(gridcolor="rgba(20,79,108,.09)", linecolor="rgba(20,79,108,.16)", zeroline=False),
        yaxis=dict(gridcolor="rgba(20,79,108,.09)", linecolor="rgba(20,79,108,.16)", zeroline=False),
    )
)

top_tabs = st.tabs([
    T["top_executive"], T["top_rheology"], T["top_physchem"],
    T["top_sedimentation"], T["top_microbiology"], T["top_references"],
])
rheology_tabs = top_tabs[1].tabs([
    T["rheo_overview"], T["flow_curve"], T["amplitude_sweep"],
    T["frequency_sweep"], T["rheo_interpretation"], T["rheo_metadata"], T["rheo_references"],
])
physicochemical_tabs = top_tabs[2].tabs([
    T["overview"],
])


@st.cache_data
def load_lims_microbial_audit():
    lims_path = Path("data/microbiology/LIMS_Microbial_Audit.csv")
    if not lims_path.exists():
        return pd.DataFrame()
    return pd.read_csv(lims_path, sep=None, engine="python")


def find_lims_column(dataframe, candidates):
    normalized = {str(column).strip().lower(): column for column in dataframe.columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    return None


lims_microbiology = load_lims_microbial_audit()
micro_date_column = find_lims_column(lims_microbiology, [
    "date_parsed", "manufacturing date", "manufacturing_date", "manufacture date", "production date", "date",
])
micro_processing_column = find_lims_column(lims_microbiology, [
    "treatment", "processing condition", "processing", "process", "product type",
])
micro_sample_column = find_lims_column(lims_microbiology, [
    "sample", "sample id", "sample_id", "sample number", "sample_number",
])
micro_category_column = find_lims_column(lims_microbiology, [
    "beverage_type", "sample category", "category", "product category", "product_type", "product type",
])
micro_status_column = find_lims_column(lims_microbiology, ["microbial_status", "microbial status", "status"])
micro_normalized_status_column = find_lims_column(lims_microbiology, ["normalized_status", "normalized status"])
micro_short_status_column = find_lims_column(lims_microbiology, ["short_status", "short status"])
micro_medium_column = find_lims_column(lims_microbiology, ["medium", "culture medium"])
micro_risk_score_column = find_lims_column(lims_microbiology, ["risk_score", "risk score"])

MICRO_COPY = {
    "EN": {
        "overview": "Executive microbiological overview",
        "systems": "Beverage systems investigated",
        "plates": "Culture plates processed",
        "critical": "Critical risk conditions",
        "index": "Microbiological Acceptability Index",
        "pasteurized": "Pasteurized beverage systems",
        "non_pasteurized": "Non-pasteurized beverage systems",
        "media": "Media types used",
        "replicates": "Analytical replicates",
        "not_recorded": "Not recorded in LIMS audit",
        "results": "Measured qualitative plate results",
        "shelf_statement": "Regulatory shelf-life determination requires quantitative microbial enumeration according to ISO 4833 and ISO 21527.",
    },
    "DE": {
        "overview": "Managementübersicht Mikrobiologie",
        "systems": "Untersuchte Getränkesysteme",
        "plates": "Verarbeitete Kulturplatten",
        "critical": "Kritische Risikobedingungen",
        "index": "Mikrobiologischer Akzeptabilitätsindex",
        "pasteurized": "Pasteurisierte Getränkesysteme",
        "non_pasteurized": "Nicht pasteurisierte Getränkesysteme",
        "media": "Verwendete Nährmedien",
        "replicates": "Analytische Wiederholungen",
        "not_recorded": "Im LIMS-Audit nicht dokumentiert",
        "results": "Gemessene qualitative Plattenergebnisse",
        "shelf_statement": "Für eine regulatorische Haltbarkeitsbestimmung ist eine quantitative mikrobiologische Enumeration gemäß ISO 4833 und ISO 21527 erforderlich.",
    },
}
M = MICRO_COPY[LANG]
microbiology_tabs = top_tabs[4].tabs([
    T["micro_exec"], T["micro_results"], T["micro_visual"], T["micro_interpretation"], T["micro_shelf"], T["micro_literature"],
])


def qualitative_risk_classification(row):
    microbial_status = str(row.get(micro_status_column, "")).strip().lower()
    normalized_status = str(row.get(micro_normalized_status_column, "")).strip().lower()
    short_status = str(row.get(micro_short_status_column, "")).strip().lower()
    if short_status == "tntc" or normalized_status == "critical" or microbial_status == "very high growth":
        return "CRITICAL"
    if normalized_status == "moderate" or short_status == "countable":
        return "MODERATE RISK"
    if normalized_status == "low" or microbial_status == "low growth" or short_status == "low growth":
        return "LOW RISK"
    if normalized_status == "safe" or microbial_status == "no growth" or short_status == "negative":
        return "SAFE"
    return "Unclassified"

with microbiology_tabs[0]:
    st.header(M["overview"])
    st.caption(tr("Industrial QA/R&D view based on the recorded study design and the qualitative LIMS audit. No microbial count is inferred from photographs or qualitative status fields.", "Industrielle QS-/F&E-Ansicht auf Grundlage des dokumentierten Versuchsdesigns und des qualitativen LIMS-Audits. Aus Fotografien oder qualitativen Statusfeldern wird keine Keimzahl abgeleitet."))
    if lims_microbiology.empty:
        st.warning("LIMS_Microbial_Audit.csv was not found in the workspace. Executive microbiological indicators cannot be populated.")
    else:
        executive_micro = lims_microbiology.copy()
        executive_micro["Risk Classification"] = executive_micro.apply(qualitative_risk_classification, axis=1)
        unique_systems = executive_micro[micro_sample_column].nunique() if micro_sample_column is not None else 6
        critical_conditions = int((executive_micro["Risk Classification"] == "CRITICAL").sum())
        risk_scores = pd.to_numeric(executive_micro[micro_risk_score_column], errors="coerce").dropna() if micro_risk_score_column is not None else pd.Series(dtype=float)

        executive_kpis = st.columns(4)
        executive_kpis[0].metric(M["systems"], unique_systems)
        executive_kpis[1].metric(M["plates"], "156", help=tr("Recorded experimental-design total across the two independent laboratory days.", "Dokumentierte Gesamtzahl des Versuchsdesigns über zwei unabhängige Labortage."))
        executive_kpis[2].metric(M["critical"], critical_conditions)
        executive_kpis[3].metric(
            M["index"],
            f"{risk_scores.mean():.1f}/100" if not risk_scores.empty else M["not_recorded"],
            help=tr("Mean of the LIMS Risk_Score field, where available; no external acceptance threshold is applied.", "Mittelwert des LIMS-Feldes Risk_Score, sofern verfügbar; es wird kein externer Akzeptanzgrenzwert angewendet."),
        )

        if micro_processing_column is not None and micro_sample_column is not None:
            treatment_text = executive_micro[micro_processing_column].astype(str).str.lower()
            non_pasteurized = executive_micro.loc[treatment_text.str.contains("non", na=False), micro_sample_column].nunique()
            pasteurized = executive_micro.loc[
                treatment_text.str.contains("pasteur", na=False) & ~treatment_text.str.contains("non", na=False),
                micro_sample_column,
            ].nunique()
        else:
            pasteurized = M["not_recorded"]
            non_pasteurized = M["not_recorded"]

        design_metrics = st.columns(4)
        design_metrics[0].metric(M["pasteurized"], pasteurized)
        design_metrics[1].metric(M["non_pasteurized"], non_pasteurized)
        design_metrics[2].metric(M["media"], executive_micro[micro_medium_column].nunique() if micro_medium_column is not None else M["not_recorded"])
        design_metrics[3].metric(M["replicates"], M["not_recorded"], help=tr("The audit does not include a replicate identifier, so a replicate count is not inferred from qualitative records.", "Das Audit enthält keine Replikatkennung; daher wird aus den qualitativen Datensätzen keine Replikatanzahl abgeleitet."))
        st.info(tr("Study design: six beverage systems, two media (E. coli selective agar and MEA), two independent laboratory days, and 156 processed culture plates. Twelve qualitative LIMS observations summarize outcomes from the 156 processed culture plates, including analytical replicates and two laboratory days.", "Versuchsdesign: sechs Getränkesysteme, zwei Nährmedien (E.-coli-Selektivagar und MEA), zwei unabhängige Labortage und 156 verarbeitete Kulturplatten. Zwölf qualitative LIMS-Beobachtungen fassen die Ergebnisse der 156 Platten einschließlich analytischer Wiederholungen und beider Labortage zusammen."))
        st.caption(T["bottle_statement"])
        st.caption(T["bottle_limitation"])

with microbiology_tabs[1]:
    st.header(M["results"])
    st.caption(tr("LIMS-derived qualitative observations only. No CFU/mL, log transformation, image enumeration, or predictive microbiological model is generated.", "Ausschließlich aus LIMS abgeleitete qualitative Beobachtungen. Es werden weder KBE/mL noch Log-Transformationen, Bildauszählungen oder prädiktive mikrobiologische Modelle erzeugt."))
    if lims_microbiology.empty:
        st.warning("LIMS_Microbial_Audit.csv was not found in the workspace. No microbiological observations are displayed or interpreted.")
    else:
        micro_table = lims_microbiology.copy()
        micro_table["Risk Classification"] = micro_table.apply(qualitative_risk_classification, axis=1)
        ordered_risk = ["SAFE", "LOW RISK", "MODERATE RISK", "CRITICAL", "Unclassified"]
        observation_kpis = st.columns(5)
        observation_kpis[0].metric(tr("Qualitative microbiological observations", "Qualitative mikrobiologische Beobachtungen"), len(lims_microbiology))
        observation_kpis[1].metric(
            tr("Total microbiological plates processed", "Verarbeitete mikrobiologische Platten insgesamt"),
            "156",
            help="The total plate count includes analytical replicates, duplicate incubation days, and both microbiological media.",
        )
        observation_kpis[2].metric(tr("Critical observations", "Kritische Beobachtungen"), int((micro_table["Risk Classification"] == "CRITICAL").sum()))
        observation_kpis[3].metric(tr("Safe observations", "Unbedenkliche Beobachtungen"), int((micro_table["Risk Classification"] == "SAFE").sum()))
        observation_kpis[4].metric(tr("Reported treatments", "Dokumentierte Behandlungen"), micro_table[micro_processing_column].nunique() if micro_processing_column is not None else M["not_recorded"])
        st.caption(
            "Methodology: 6 beverage systems × 2 media (E.coli selective agar and MEA) × analytical replicates × 2 laboratory days = 156 total incubated plates."
        )

        display_columns = [column for column in [
            micro_sample_column, micro_medium_column, micro_status_column, micro_category_column,
            micro_processing_column, micro_date_column, micro_normalized_status_column, micro_short_status_column,
            "Risk Classification",
        ] if column is not None]
        st.dataframe(micro_table[display_columns], width="stretch", hide_index=True)

        if micro_sample_column is not None and micro_medium_column is not None:
            result_register = micro_table.pivot_table(
                index=micro_sample_column,
                columns=micro_medium_column,
                values=micro_status_column,
                aggfunc="first",
            ).reset_index()
            sample_context = micro_table.groupby(micro_sample_column, as_index=False).agg({
                column: "first" for column in [micro_processing_column, micro_category_column, micro_date_column] if column is not None
            })
            risk_order = {"SAFE": 0, "LOW RISK": 1, "MODERATE RISK": 2, "CRITICAL": 3, "Unclassified": -1}
            risk_register = micro_table[[micro_sample_column, "Risk Classification"]].copy()
            risk_register["Risk rank"] = risk_register["Risk Classification"].map(risk_order)
            risk_register = risk_register.sort_values("Risk rank").groupby(micro_sample_column, as_index=False).tail(1)
            result_register = result_register.merge(sample_context, on=micro_sample_column, how="left").merge(
                risk_register[[micro_sample_column, "Risk Classification"]], on=micro_sample_column, how="left"
            )
            ordered_columns = [column for column in [micro_sample_column, micro_processing_column, micro_category_column, micro_date_column] if column is not None]
            ordered_columns += [column for column in result_register.columns if column not in ordered_columns + ["Risk Classification"]]
            ordered_columns.append("Risk Classification")
            result_register = result_register[ordered_columns]
            risk_colors = result_register["Risk Classification"].map({"SAFE": "#d8f0ea", "LOW RISK": "#fff1c9", "MODERATE RISK": "#fde0bf", "CRITICAL": "#f9c7cc", "Unclassified": "#e5e7eb"}).fillna("white").tolist()
            fig_result_register = go.Figure(data=[go.Table(
                header=dict(values=[f"<b>{column}</b>" for column in result_register.columns], fill_color="#173f5f", font=dict(color="white"), align="left"),
                cells=dict(values=[result_register[column].fillna("—").astype(str).tolist() for column in result_register.columns], fill_color=[['white'] * len(result_register)] * (len(result_register.columns) - 1) + [risk_colors], align="left", height=30),
            )])
            fig_result_register.update_layout(title=tr("Qualitative microbiological results register", "Register qualitativer mikrobiologischer Ergebnisse"), margin=dict(l=0, r=0, t=48, b=0))
            st.plotly_chart(fig_result_register, width="stretch")

            evidence_grid = micro_table.copy()
            evidence_grid["Risk code"] = evidence_grid["Risk Classification"].map(risk_order).fillna(-1)
            evidence_grid["Sample label"] = evidence_grid[micro_sample_column].astype(str)
            if micro_processing_column is not None:
                evidence_grid["Sample label"] = evidence_grid["Sample label"] + " — " + evidence_grid[micro_processing_column].astype(str)
            evidence_grid = evidence_grid.sort_values(["Sample label", micro_medium_column])
            sample_labels = evidence_grid["Sample label"].drop_duplicates().tolist()
            media_labels = evidence_grid[micro_medium_column].drop_duplicates().tolist()
            risk_matrix = evidence_grid.pivot(index="Sample label", columns=micro_medium_column, values="Risk code").reindex(index=sample_labels, columns=media_labels)
            status_matrix = evidence_grid.pivot(index="Sample label", columns=micro_medium_column, values=micro_status_column).reindex(index=sample_labels, columns=media_labels)
            fig_evidence_matrix = go.Figure(go.Heatmap(
                z=risk_matrix.to_numpy(),
                x=media_labels,
                y=sample_labels,
                text=status_matrix.fillna("Not recorded").to_numpy(),
                texttemplate="%{text}",
                textfont=dict(size=13),
                hovertemplate="Sample/treatment: %{y}<br>Medium: %{x}<br>Measured status: %{text}<extra></extra>",
                colorscale=[[0.0, "#d9dde3"], [0.20, "#2a9d8f"], [0.45, "#e9c46a"], [0.70, "#f4a261"], [1.0, "#e63946"]],
                zmin=-1, zmax=3,
                showscale=False,
                xgap=3, ygap=3,
            ))
            fig_evidence_matrix.update_layout(
                template=chart_theme,
                title=tr("Qualitative microbiological evidence matrix", "Qualitative mikrobiologische Evidenzmatrix"),
                xaxis_title=tr("Culture medium", "Nährmedium"),
                yaxis_title=tr("Beverage system and treatment", "Getränkesystem und Behandlung"),
                margin=dict(l=0, r=0, t=48, b=0),
            )
            st.plotly_chart(fig_evidence_matrix, width="stretch")
            st.caption("Cell colour encodes the measured qualitative risk class; cell text is the directly reported microbiological status. Each LIMS observation is represented once.")

        if micro_date_column is not None:
            plate_timeline = micro_table.copy()
            plate_timeline["Manufacturing_Date"] = pd.to_datetime(plate_timeline[micro_date_column], errors="coerce", dayfirst=True)
            if micro_sample_column is None:
                plate_timeline["LIMS_Record"] = plate_timeline.index.astype(str)
            fig_plate_timeline = px.scatter(
                plate_timeline.dropna(subset=["Manufacturing_Date"]),
                x="Manufacturing_Date",
                y=micro_sample_column if micro_sample_column is not None else "LIMS_Record",
                color="Risk Classification",
                symbol=micro_processing_column,
                hover_data=[column for column in [micro_medium_column, micro_status_column, micro_short_status_column] if column is not None],
                category_orders={"Risk Classification": ordered_risk},
                color_discrete_map={"SAFE": "#2a9d8f", "LOW RISK": "#e9c46a", "MODERATE RISK": "#f4a261", "CRITICAL": "#e63946", "Unclassified": "#6c757d"},
                template=chart_theme,
                title=tr("Manufacturing-date timeline of measured qualitative risk observations", "Zeitverlauf gemessener qualitativer Risikobeobachtungen nach Herstellungsdatum"),
            )
            st.plotly_chart(fig_plate_timeline, width="stretch")

with microbiology_tabs[2]:
    st.header(tr("Qualitative plate-image evidence", "Qualitative Bildnachweise der Platten"))
    st.caption(tr("Photographs are representative qualitative evidence only. No image-based colony count, CFU estimate, or organism identification is performed.", "Die Fotografien dienen nur als repräsentative qualitative Nachweise. Es erfolgen keine bildbasierte Koloniezählung, KBE-Schätzung oder Organismenidentifikation."))
    pasteurized_images = [
        ("November 2024 Regular P", "data/microbiology/November 2024 regular P.png", "November 2024", "Regular", "Pasteurized", "Qualitative comparison image; risk classification remains based on the matched LIMS observation."),
        ("December 2025 Regular P", "data/microbiology/December 2025 regular P.png", "December 2025", "Regular", "Pasteurized", "Qualitative comparison image; risk classification remains based on the matched LIMS observation."),
        ("July 2025 Regular P", "data/microbiology/July 2025 regular P.png", "July 2025", "Regular", "Pasteurized", "Pasteurized beverage system; thermal processing is evaluated against the measured LIMS status, not by image enumeration."),
        ("July 2025 Spritz P", "data/microbiology/July 2025 spritz P.png", "July 2025", "Spritz", "Pasteurized", "Pasteurized beverage system; thermal processing is evaluated against the measured LIMS status, not by image enumeration."),
    ]
    non_pasteurized_images = [
        ("July 2025 Regular NP", "data/microbiology/July 2025 regular NP.png", "July 2025", "Regular", "Non-pasteurized", "Non-pasteurized beverage system used as a comparative control for preservation effectiveness."),
        ("July 2025 Spritz NP", "data/microbiology/July 2025 sprits NP.png", "July 2025", "Spritz", "Non-pasteurized", "Non-pasteurized beverage system used as a comparative control for preservation effectiveness."),
    ]
    for group_title, group_subtitle, group_images in [
        (
            "Pasteurized Beverage Systems",
            "Thermally treated beverage formulations demonstrating microbiological stabilization and reduced contamination risk.",
            pasteurized_images,
        ),
        (
            "Non-pasteurized Beverage Systems",
            "Untreated beverage formulations used for comparative microbial risk assessment.",
            non_pasteurized_images,
        ),
    ]:
        st.subheader(group_title)
        st.caption(group_subtitle)
        for row_start in range(0, len(group_images), 2):
            image_columns = st.columns(2)
            for image_column, (title, image_path, manufacturing_date, product_type, processing, interpretation) in zip(image_columns, group_images[row_start:row_start + 2]):
                with image_column:
                    st.subheader(title)
                    st.image(image_path, width="stretch")
                    st.markdown(
                        f"- Manufacturing date: {manufacturing_date}\n"
                        f"- Product type: {product_type}\n"
                        f"- Processing condition: {processing}\n"
                        f"- Microbiological interpretation: {interpretation}"
                    )
                    st.caption("Representative qualitative microbiological evidence only. No colony count, CFU value, or microbiological status is inferred from this photograph.")

with microbiology_tabs[3]:
    st.header(tr("Scientific interpretation", "Wissenschaftliche Interpretation"))
    if lims_microbiology.empty or micro_status_column is None:
        st.info("Scientific interpretation is withheld because measured qualitative status fields from LIMS_Microbial_Audit.csv are not currently available.")
    else:
        interpretation_data = lims_microbiology.copy()
        interpretation_data["Risk Classification"] = interpretation_data.apply(qualitative_risk_classification, axis=1)
        critical_treatments = []
        if micro_processing_column is not None:
            critical_treatments = interpretation_data.loc[
                interpretation_data["Risk Classification"] == "CRITICAL", micro_processing_column
            ].dropna().astype(str).unique().tolist()
        st.markdown(
            "Interpretation is restricted to recorded qualitative observations, manufacturing dates, culture media, and treatment categories. "
            "**TNTC** is classified as **CRITICAL** contamination risk; **Very high growth** as severe microbial instability; **Low Growth** as limited microbial activity; and **Negative/Safe** observations as no detectable growth/acceptable microbiological condition within the applied method."
        )
        if micro_processing_column is not None:
            treatment_summary = (
                interpretation_data.groupby([micro_processing_column, "Risk Classification"], as_index=False)
                .size()
                .rename(columns={"size": "Qualitative LIMS records (not plate count)"})
            )
            st.dataframe(treatment_summary, width="stretch", hide_index=True)
            st.caption("This table summarizes the 12 qualitative LIMS records (6 beverage systems × 2 media). It is not the total incubated plate count; the experimental total remains 156 plates, including analytical replicates and two laboratory days.")
            st.markdown(f"The treatment comparison is descriptive and uses the reported **{micro_processing_column}** category only. It does not establish a causal processing effect or compliance decision.")
            if critical_treatments:
                st.markdown(f"Critical qualitative observations in this audit are recorded for: **{', '.join(critical_treatments)}**. This finding supports targeted QA review of the recorded treatment condition; it is not a numerical prevalence estimate.")
        if micro_date_column is not None:
            st.markdown(f"Manufacturing-date comparisons use the recorded **{micro_date_column}** values only; no microbial growth curve or storage-time extrapolation is fitted.")
        st.markdown(
            "For this acidic beverage system, the reported pH (~2.7) is an inhibitory hurdle for many bacteria, while ethanol can further constrain microbial survival. These intrinsic factors do not replace the measured LIMS observations or prove product stability. In fruit beverages, acid-tolerant yeasts and moulds remain relevant spoilage concerns, so negative observations on the yeast-and-mould medium are interpreted only as no detectable growth under the recorded analytical conditions.\n\n"
            "The recorded non-pasteurised observations and pasteurised observations are displayed side-by-side to support quality-assurance review. The observed treatment-associated pattern is descriptive and dataset-specific. It does not independently establish causal pasteurization efficacy because the observations are qualitative, packaging preparation was not microbiologically controlled, and experimental groups may differ in age and treatment."
        )
        st.warning(T["bottle_limitation"])

with microbiology_tabs[4]:
    st.header(tr("Evidence-based shelf-life assessment", "Evidenzbasierte Haltbarkeitsbewertung"))
    st.caption(tr("No expiry date, quantitative enumeration, regression model, or shelf-life duration is estimated from this dashboard.", "Dieses Dashboard schätzt weder ein Verfallsdatum noch quantitative Keimzahlen, ein Regressionsmodell oder eine Haltbarkeitsdauer."))
    if lims_microbiology.empty or micro_date_column is None:
        st.warning(M["shelf_statement"])
    else:
        microbiology_timeline_data = lims_microbiology.copy()
        microbiology_timeline_data["Manufacturing_Date"] = pd.to_datetime(microbiology_timeline_data[micro_date_column], errors="coerce", dayfirst=True)
        microbiology_timeline_data["Risk Classification"] = microbiology_timeline_data.apply(qualitative_risk_classification, axis=1)
        risk_order = {"SAFE": 0, "LOW RISK": 1, "MODERATE RISK": 2, "CRITICAL": 3, "Unclassified": -1}
        microbiology_timeline_data["Risk rank"] = microbiology_timeline_data["Risk Classification"].map(risk_order)
        sample_timeline = microbiology_timeline_data.sort_values("Risk rank").groupby(
            micro_sample_column if micro_sample_column is not None else microbiology_timeline_data.index.name,
            as_index=False,
        ).tail(1)
        if micro_sample_column is None:
            sample_timeline["LIMS_Record"] = sample_timeline.index.astype(str)
        timeline_y = micro_sample_column if micro_sample_column is not None else "LIMS_Record"
        fig_micro_timeline = px.scatter(
            sample_timeline.dropna(subset=["Manufacturing_Date"]),
            x="Manufacturing_Date",
            y=timeline_y,
            color="Risk Classification",
            symbol=micro_processing_column,
            hover_data=[column for column in [micro_status_column, micro_short_status_column, micro_normalized_status_column, "Risk Classification"] if column is not None],
            category_orders={"Risk Classification": ["SAFE", "LOW RISK", "MODERATE RISK", "CRITICAL", "Unclassified"]},
            color_discrete_map={"SAFE": "#2a9d8f", "LOW RISK": "#e9c46a", "MODERATE RISK": "#f4a261", "CRITICAL": "#e63946", "Unclassified": "#6c757d"},
            template=chart_theme,
            title=tr("Sample-level worst observed qualitative microbiological risk by manufacturing date", "Schwerstes beobachtetes qualitatives mikrobiologisches Risiko je Probe und Herstellungsdatum"),
        )
        st.plotly_chart(fig_micro_timeline, width="stretch")
        st.dataframe(microbiology_timeline_data.sort_values("Manufacturing_Date"), width="stretch", hide_index=True)
        st.warning(M["shelf_statement"])

with microbiology_tabs[5]:
    st.header(tr("Literature support and analytical standards", "Literaturgrundlage und analytische Standards"))
    st.caption(tr("Peer-reviewed context and official enumeration methods are provided for scientific framing; they do not replace the LIMS record or product-specific regulatory criteria.", "Begutachtete Fachliteratur und offizielle Zählmethoden dienen der wissenschaftlichen Einordnung; sie ersetzen weder den LIMS-Datensatz noch produktspezifische regulatorische Kriterien."))
    st.markdown(
        "- *The incidence and impact of microbial spoilage in the production of fruit and vegetable juices as reported by juice manufacturers* (2018). Food Control, 85, 144–150. DOI: [10.1016/j.foodcont.2017.09.025](https://doi.org/10.1016/j.foodcont.2017.09.025)\n"
        "- Wareing, P. (2016). *Microbiology of soft drinks and fruit juices*. DOI: [10.1002/9781118634943.ch11](https://doi.org/10.1002/9781118634943.ch11)\n"
        "- U.S. Food and Drug Administration. *Bacteriological Analytical Manual, Chapter 3: Aerobic Plate Count*. [FDA BAM](https://www.fda.gov/food/laboratory-methods-food/bam-chapter-3-aerobic-plate-count)\n"
        "- ISO 4833-1:2013. *Microbiology of the food chain — Colony count at 30 °C by the pour plate technique*. [ISO record](https://www.iso.org/standard/53728.html)\n"
        "- ISO 21527-1:2008. *Enumeration of yeasts and moulds — Colony count technique*. [ISO record](https://www.iso.org/standard/38275.html)\n"
        "- ICMSF. *Microorganisms in Foods* series: principles and applications for food microbiological safety and quality."
    )

top_tabs[0].header(T["executive_project"])
top_tabs[0].markdown(T["subtitle"])
top_tabs[0].markdown(f"### {T['study_architecture']}")
top_tabs[0].write(tr("Four independent analytical modules contribute complementary evidence. Integration is limited to high-level narrative interpretation.", "Vier unabhängige Analysemodule liefern sich ergänzende Erkenntnisse. Die Integration beschränkt sich auf eine übergeordnete narrative Interpretation."))
top_tabs[0].markdown(
    f"""
    <div class="evidence-grid">
        <div class="evidence-card" style="--card-accent:#146c94">
            <div class="evidence-index">01 · {tr('STRUCTURE', 'STRUKTUR')}</div>
            <div class="evidence-name">{T['rheology']}</div>
            <div class="evidence-detail">{tr('Flow, amplitude and frequency response with replicate-aware sample identities.', 'Fließ-, Amplituden- und Frequenzantwort mit replikatbezogenen Probenkennungen.')}</div>
            <div class="evidence-status">{tr('Quantitative evidence', 'Quantitative Evidenz')}</div>
        </div>
        <div class="evidence-card" style="--card-accent:#2fa7b8">
            <div class="evidence-index">02 · {tr('COMPOSITION', 'ZUSAMMENSETZUNG')}</div>
            <div class="evidence-name">{T['physicochemical']}</div>
            <div class="evidence-detail">{tr('Measured pH, density, Brix and composition-related endpoints.', 'Gemessene Endpunkte zu pH, Dichte, Brix und Zusammensetzung.')}</div>
            <div class="evidence-status">{tr('Workbook traceable', 'Arbeitsmappe rückverfolgbar')}</div>
        </div>
        <div class="evidence-card" style="--card-accent:#d9aa52">
            <div class="evidence-index">03 · {tr('PHYSICAL STATE', 'PHYSIKALISCHER ZUSTAND')}</div>
            <div class="evidence-name">{T['sedimentation']}</div>
            <div class="evidence-detail">{tr('Direct graduated-cylinder observations at two documented time points.', 'Direkte Messzylinderbeobachtungen zu zwei dokumentierten Zeitpunkten.')}</div>
            <div class="evidence-status">{tr('Descriptive evidence', 'Deskriptive Evidenz')}</div>
        </div>
        <div class="evidence-card" style="--card-accent:#68a67d">
            <div class="evidence-index">04 · {tr('PRODUCT SAFETY', 'PRODUKTSICHERHEIT')}</div>
            <div class="evidence-name">{T['microbiology']}</div>
            <div class="evidence-detail">{tr('Qualitative LIMS outcomes supported by representative plate images.', 'Qualitative LIMS-Ergebnisse, ergänzt durch repräsentative Plattenbilder.')}</div>
            <div class="evidence-status">{tr('Qualitative evidence', 'Qualitative Evidenz')}</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
summary_kpis = top_tabs[0].columns(3)
summary_kpis[0].metric(tr("Analytical modules", "Analysemodule"), 4)
summary_kpis[1].metric(tr("Rheology sample families", "Rheologische Probenfamilien"), sample_overview["Sample_ID"].nunique())
summary_kpis[2].metric(tr("Physicochemical samples", "Physikochemische Proben"), physchem["Sample_ID"].nunique() if not physchem.empty else T["not_loaded"])
summary_kpis = top_tabs[0].columns(3)
summary_kpis[0].metric(tr("Sedimentation samples", "Sedimentationsproben"), 7)
summary_kpis[1].metric(tr("Microbiology beverage systems", "Mikrobiologische Getränkesysteme"), lims_microbiology["Sample"].nunique() if not lims_microbiology.empty else T["not_loaded"])
summary_kpis[2].metric(tr("Total microbiological plates processed", "Verarbeitete mikrobiologische Platten insgesamt"), "156")

if show_methodology:
    top_tabs[0].markdown(tr("### Evidence and methodology matrix", "### Evidenz- und Methodenmatrix"))
    methodology_matrix = pd.DataFrame([
        {
            tr("Module", "Modul"): T["rheology"],
            tr("Evidence basis", "Evidenzbasis"): tr("Instrumental measurements + derived parameters", "Instrumentelle Messungen + abgeleitete Parameter"),
            tr("Replication", "Replikation"): tr("Retained in metadata", "In Metadaten beibehalten"),
            tr("Primary limitation", "Zentrale Limitation"): tr("Model parameters remain range-specific", "Modellparameter bleiben messbereichsspezifisch"),
        },
        {
            tr("Module", "Modul"): T["physicochemical"],
            tr("Evidence basis", "Evidenzbasis"): tr("Measured workbook endpoints", "Gemessene Arbeitsmappen-Endpunkte"),
            tr("Replication", "Replikation"): tr("As recorded in source", "Wie in der Quelle dokumentiert"),
            tr("Primary limitation", "Zentrale Limitation"): tr("No unverified cross-module matching", "Keine ungeprüfte modulübergreifende Zuordnung"),
        },
        {
            tr("Module", "Modul"): T["sedimentation"],
            tr("Evidence basis", "Evidenzbasis"): tr("Two direct volume observations", "Zwei direkte Volumenbeobachtungen"),
            tr("Replication", "Replikation"): tr("Not available", "Nicht verfügbar"),
            tr("Primary limitation", "Zentrale Limitation"): tr("No kinetic or inferential modelling", "Keine kinetische oder inferenzstatistische Modellierung"),
        },
        {
            tr("Module", "Modul"): T["microbiology"],
            tr("Evidence basis", "Evidenzbasis"): tr("Qualitative LIMS audit", "Qualitatives LIMS-Audit"),
            tr("Replication", "Replikation"): tr("Plate total documented; identifier absent", "Plattenzahl dokumentiert; Kennung fehlt"),
            tr("Primary limitation", "Zentrale Limitation"): tr("No CFU/mL inference from images", "Keine KBE/mL-Ableitung aus Bildern"),
        },
    ])
    top_tabs[0].dataframe(methodology_matrix, width="stretch", hide_index=True)

top_tabs[0].markdown(
    f'<div class="governance-note"><strong>{tr("Scientific governance:", "Wissenschaftliche Governance:")}</strong> '
    f'{tr("Measured observations, derived calculations, literature-supported interpretation and hypotheses are kept conceptually distinct. This separation supports examination-level traceability and prevents visual presentation from overstating evidential strength.", "Gemessene Beobachtungen, abgeleitete Berechnungen, literaturgestützte Interpretation und Hypothesen werden konzeptionell getrennt. Diese Trennung unterstützt die prüfungsrelevante Rückverfolgbarkeit und verhindert, dass die visuelle Darstellung die Evidenzstärke überzeichnet.")}</div>',
    unsafe_allow_html=True,
)
top_tabs[0].markdown(f"### {T['integrated_conclusion']}")
top_tabs[0].write(tr("The dashboard presents module-specific measured evidence without merging experimental identifiers or performing cross-module statistical comparisons.", "Das Dashboard stellt modulspezifische Messdaten dar, ohne experimentelle Kennungen zusammenzuführen oder modulübergreifende statistische Vergleiche durchzuführen."))
top_tabs[0].info(T["data_integrity"])
top_tabs[0].caption(T["bottle_statement"])
top_tabs[0].caption(T["bottle_limitation"])

with rheology_tabs[0]:
    st.header(tr("Rheology Overview and Experimental Design", "Rheologieübersicht und Versuchsdesign"))
    st.markdown(tr("### Why Rheology Was Performed", "### Warum rheologische Untersuchungen durchgeführt wurden"))
    st.write(tr("Rheology was selected because structural, viscoelastic, and flow properties are relevant to physical stability and suspension behaviour.", "Rheologische Untersuchungen wurden gewählt, weil Struktur-, viskoelastische und Fließeigenschaften für die physikalische Stabilität und das Suspensionsverhalten relevant sind."))
    st.markdown(tr("### Experimental Design", "### Versuchsdesign"))
    st.write(tr("Methods: Flow curve, amplitude sweep, frequency sweep. Instrument: Kinexus Prime Lab+. Research partners: Hochschule Ansbach and Marmeladenherz.", "Methoden: Fließkurve, Amplitudensweep und Frequenzsweep. Gerät: Kinexus Prime Lab+. Forschungspartner: Hochschule Ansbach und Marmeladenherz."))
    st.caption(T["bottle_statement"])
    st.metric(tr("Parent samples / replicate measurements", "Ausgangsproben / Wiederholungsmessungen"), f"{sample_overview['Sample_ID'].nunique()} / {len(meta)}")
    st.markdown(tr("### Rheology results summary", "### Zusammenfassung der Rheologieergebnisse"))
    st.write(tr(f"Mean G′: {mean_gprime:.3g} Pa; Mean G″: {mean_gdouble:.3g} Pa; Mean tanδ: {mean_tandelta:.3f}; flow index n: {flow_behavior_index_n:.3f}.", f"Mittleres G′: {mean_gprime:.3g} Pa; mittleres G″: {mean_gdouble:.3g} Pa; mittleres tanδ: {mean_tandelta:.3f}; Fließindex n: {flow_behavior_index_n:.3f}."))

with rheology_tabs[1]:
    st.header(tr("Flow curve", "Fließkurve"))
    st.caption(tr("Measured flow response for processing, filling, pouring, and oral-flow assessment.", "Gemessenes Fließverhalten zur Beurteilung von Verarbeitung, Abfüllung, Ausgießen und oralem Fluss."))
    flow_samples = sorted(flow["Sample_Family"].dropna().unique())
    selected_flow_sample = st.selectbox(tr("Sample family", "Probenfamilie"), flow_samples, key="flow_sample")
    selected_flow = flow[flow["Sample_Family"] == selected_flow_sample]
    flow_curve = measured_curve(selected_flow, "ɣ̇ (s⁻¹)", ["η (Pa s)", "σ (Pa)"])
    flow_details, flow_fit_points = power_law_model_details(selected_flow)
    flow_n, flow_k, flow_r2 = flow_details["n"], flow_details["k"], flow_details["r2"]
    eta_low, shear_low = nearest_measured_value(flow_curve, "ɣ̇ (s⁻¹)", "η (Pa s)", 1)
    eta_high, shear_high = nearest_measured_value(flow_curve, "ɣ̇ (s⁻¹)", "η (Pa s)", 100)
    viscosity_retention = eta_high / eta_low * 100 if pd.notna(eta_low) and eta_low != 0 else np.nan

    flow_kpi = st.columns(4)
    flow_kpi[0].metric(tr("Flow behavior index, n", "Fließverhaltensindex n"), f"{flow_n:.3f}", help=tr("Log–log slope of measured shear stress versus shear rate. n < 1 indicates shear-thinning within this measurement range.", "Log-Log-Steigung der gemessenen Schubspannung gegenüber der Scherrate. n < 1 weist in diesem Messbereich auf Scherverdünnung hin."))
    flow_kpi[1].metric(tr("Consistency coefficient, K", "Konsistenzkoeffizient K"), f"{flow_k:.3g} Pa·sⁿ", help=tr("Power-law coefficient from the measured stress–shear-rate fit.", "Potenzgesetz-Koeffizient aus der Anpassung von Schubspannung und Scherrate."))
    flow_kpi[2].metric(tr("Stress-fit R²", "R² der Spannungsanpassung"), f"{flow_r2:.3f}", help=tr("Goodness of fit for the power-law calculation; this is not a separate measurement.", "Anpassungsgüte der Potenzgesetzberechnung; dies ist keine separate Messung."))
    flow_kpi[3].metric(tr("Viscosity retained", "Verbleibende Viskosität"), f"{viscosity_retention:.1f}%", help=tr(f"Ratio of the values nearest to {shear_high:.3g} and {shear_low:.3g} s⁻¹; no interpolation is used.", f"Verhältnis der Werte nahe {shear_high:.3g} und {shear_low:.3g} s⁻¹; es wird nicht interpoliert."))

    fig_flow = go.Figure()
    for replicate, replicate_data in selected_flow.groupby("Sample"):
        fig_flow.add_trace(go.Scatter(x=replicate_data["ɣ̇ (s⁻¹)"], y=replicate_data["η (Pa s)"], mode="lines+markers", name=f"{replicate}",
            line=dict(color="#8ba6bd", width=1), marker=dict(size=4, color="#8ba6bd"), legendgroup="replicates", showlegend=False,
            hovertemplate="Replicate " + str(replicate) + "<br>Shear rate: %{x:.3g} s⁻¹<br>Apparent viscosity: %{y:.3g} Pa·s<extra></extra>"))
    fig_flow.add_trace(go.Scatter(x=flow_curve["ɣ̇ (s⁻¹)"], y=flow_curve["η (Pa s)"], mode="lines+markers", name=f"{selected_flow_sample} mean",
        line=dict(color="#1f4e79", width=4), marker=dict(size=7, color="#1f4e79"),
        hovertemplate="Parent mean<br>Shear rate: %{x:.3g} s⁻¹<br>Apparent viscosity: %{y:.3g} Pa·s<extra></extra>"))
    fig_flow.update_layout(title=tr("Measured apparent viscosity versus shear rate", "Gemessene scheinbare Viskosität in Abhängigkeit von der Scherrate"), template=chart_theme, xaxis_type="log", yaxis_type="log", xaxis_title=tr("Shear rate (s⁻¹)", "Scherrate (s⁻¹)"), yaxis_title=tr("Apparent viscosity (Pa·s)", "Scheinbare Viskosität (Pa·s)"))
    fig_flow.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_flow, width="stretch")

    stress_summary = (
        selected_flow.groupby("ɣ̇ (s⁻¹)", as_index=False)
        .agg(
            **{
                "Mean stress (Pa)": ("σ (Pa)", "mean"),
                "SD stress (Pa)": ("σ (Pa)", "std"),
                "Replicates": ("σ (Pa)", "count"),
            }
        )
        .rename(columns={"ɣ̇ (s⁻¹)": "Shear rate (s⁻¹)"})
    )
    stress_summary["SD stress (Pa)"] = stress_summary["SD stress (Pa)"].fillna(0)
    fig_stress = go.Figure()
    for replicate, replicate_data in selected_flow.groupby("Sample"):
        fig_stress.add_trace(go.Scatter(
            x=replicate_data["ɣ̇ (s⁻¹)"], y=replicate_data["σ (Pa)"], mode="lines+markers", name=str(replicate), showlegend=False,
            line=dict(color="#b8c7d4", width=1), marker=dict(color="#b8c7d4", size=4),
            hovertemplate="Replicate " + str(replicate) + "<br>Shear rate: %{x:.3g} s⁻¹<br>Shear stress: %{y:.3g} Pa<extra></extra>",
        ))
    fig_stress.add_trace(go.Scatter(
        x=stress_summary["Shear rate (s⁻¹)"], y=stress_summary["Mean stress (Pa)"], mode="lines+markers", name="Parent-sample mean ± SD",
        error_y=dict(type="data", array=stress_summary["SD stress (Pa)"], visible=True, thickness=1.3, width=3),
        line=dict(color="#1f4e79", width=4), marker=dict(color="#1f4e79", size=7),
        hovertemplate="Parent mean<br>Shear rate: %{x:.3g} s⁻¹<br>Stress: %{y:.3g} ± %{error_y.array:.3g} Pa<extra></extra>",
    ))
    fig_stress.update_layout(title=tr("Measured shear stress versus shear rate", "Gemessene Schubspannung in Abhängigkeit von der Scherrate"), template=chart_theme, xaxis_type="log", yaxis_type="log", xaxis_title=tr("Shear rate (s⁻¹)", "Scherrate (s⁻¹)"), yaxis_title=tr("Shear stress (Pa)", "Schubspannung (Pa)"), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_stress, width="stretch")

    model_table = pd.DataFrame([{
        "Model": "Power law", "Converged": "Yes", "n": flow_details["n"], "K (Pa·sⁿ)": flow_details["k"], "Yield stress": "Not fitted", "Adjusted R²": flow_details["adj_r2"], "RMSE (Pa)": flow_details["rmse"], "AICc": flow_details["aicc"], "ΔAICc": 0.0, "Observations": flow_details["n_obs"],
    }])
    st.caption("Descriptive constitutive-model diagnostic; it is not used as a material-property result when model quality is inadequate.")
    st.dataframe(model_table, width="stretch", hide_index=True)
    if pd.notna(flow_details["r2"]) and flow_details["r2"] < 0.80:
        st.warning("The fitted power-law model does not adequately represent the complete measured range. The reported K and n values are descriptive and should not be treated as reliable intrinsic material constants.")
    if not flow_fit_points.empty:
        with st.expander("Power-law diagnostic residuals", expanded=False):
            fig_residual = go.Figure(go.Scatter(x=flow_fit_points["Fitted stress (Pa)"], y=flow_fit_points["Stress residual (Pa)"], mode="markers", marker=dict(color="#1f4e79", size=7), name="Measured residual"))
            fig_residual.add_hline(y=0, line_dash="dash", line_color="#555555")
            fig_residual.update_layout(title="Residuals for the descriptive, non-accepted power-law fit", template=chart_theme, xaxis_title="Fitted shear stress (Pa)", yaxis_title="Measured − fitted stress (Pa)")
            st.plotly_chart(fig_residual, width="stretch")

    st.markdown(tr("### Industrial interpretation — selected sample", "### Industrielle Interpretation – ausgewählte Probe"))
    if pd.notna(flow_n):
        behavior = "shear-thinning" if flow_n < 0.95 else "approximately Newtonian over the measured range" if flow_n <= 1.05 else "shear-thickening"
        st.write(f"**{selected_flow_sample}** is {behavior} by the measured power-law index (n = {flow_n:.3f}; R² = {flow_r2:.3f}).")
    st.write(f"Measured apparent viscosity is {eta_low:.3g} Pa·s at the available setpoint nearest {shear_low:.3g} s⁻¹ and {eta_high:.3g} Pa·s near {shear_high:.3g} s⁻¹. The latter is {viscosity_retention:.1f}% of the former.")
    st.caption("K, n, R² and retention are calculations from the displayed measured points. They do not establish a yield stress or extrapolate beyond the workbook range.")

with rheology_tabs[2]:
    st.header(tr("Amplitude sweep", "Amplitudensweep"))
    st.caption(tr("Measured deformation tolerance and structure-retention assessment.", "Bewertung der gemessenen Verformungstoleranz und Strukturerhaltung."))
    amp_samples = sorted(amp["Sample_Family"].dropna().unique())
    selected_amp_sample = st.selectbox(tr("Sample family", "Probenfamilie"), amp_samples, key="amp_sample")
    amp_curve, amp_metrics = amplitude_metrics(amp[amp["Sample_Family"] == selected_amp_sample])
    amp_curve["tan_delta"] = amp_curve['G" (Pa)'] / amp_curve["G' (Pa)"].replace(0, np.nan)

    amp_kpi = st.columns(4)
    amp_kpi[0].metric("Initial G′ reference", f"{amp_metrics['reference_gprime']:.3g} Pa", help="Median G′ of the first up to three measured strain points.")
    amp_kpi[1].metric("LVR limit (±5% G′)", f"{amp_metrics['lvr_limit']:.3g}%", help="Highest measured strain whose G′ remains within ±5% of the initial reference.")
    amp_kpi[2].metric("G′ retention at max strain", f"{amp_metrics['retention']:.1f}%", help="G′ at the highest measured strain divided by the initial G′ reference.")
    amp_kpi[3].metric("Median tanδ (G″/G′)", f"{amp_curve['tan_delta'].median():.3f}", help="Calculated directly from measured G″ and G′ values.")

    amp_plot = amp_curve.melt(id_vars="γ* (%)", value_vars=["G' (Pa)", 'G" (Pa)'], var_name="Modulus", value_name="Pa")
    fig_amp = px.line(
        amp_plot,
        x="γ* (%)",
        y="Pa",
        color="Modulus",
        title=tr(f"Measured viscoelastic moduli vs. strain — {selected_amp_sample}", f"Gemessene viskoelastische Moduli in Abhängigkeit von der Dehnung – {selected_amp_sample}"),
        template=chart_theme,
        log_x=True,
        log_y=True,
    )
    fig_amp.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_amp, width="stretch")

    st.markdown(tr("### Industrial interpretation — selected sample", "### Industrielle Interpretation – ausgewählte Probe"))
    if pd.notna(amp_metrics["lvr_limit"]):
        st.write(f"The measured linear-viscoelastic region extends to {amp_metrics['lvr_limit']:.3g}% strain using a ±5% G′ criterion. At the highest measured strain ({amp_metrics['max_strain']:.3g}%), G′ retains {amp_metrics['retention']:.1f}% of its initial reference.")
    if amp_curve["tan_delta"].median() < 1:
        st.write("Across the measured amplitude points, the median G″/G′ ratio is below 1, so the response is elastically dominated within this test range.")
    else:
        st.write("Across the measured amplitude points, the median G″/G′ ratio is at or above 1, so viscous dissipation is not secondary within this test range.")
    st.caption("The LVR limit is a stated data-reduction criterion, not an unmeasured failure point. No amplitude values are interpolated.")

with rheology_tabs[3]:
    st.header(tr("Frequency sweep", "Frequenzsweep"))
    st.caption(tr("Measured time-scale dependence and elastic-versus-viscous balance.", "Gemessene Zeitskalenabhängigkeit und Verhältnis von elastischem zu viskosem Verhalten."))
    freq_samples = sorted(freq["Sample_Family"].dropna().unique())
    selected_freq_sample = st.selectbox(tr("Sample family", "Probenfamilie"), freq_samples, key="freq_sample")
    freq_curve, freq_metrics = frequency_metrics(freq[freq["Sample_Family"] == selected_freq_sample])

    freq_kpi = st.columns(4)
    freq_kpi[0].metric("Median tanδ (G″/G′)", f"{freq_metrics['tan_delta']:.3f}", help="Calculated from measured G″ and G′; it is distinct from the measured phase angle in degrees.")
    freq_kpi[1].metric("Median G′/G″", f"{freq_metrics['elastic_ratio']:.2f}")
    freq_kpi[2].metric("G′ frequency slope", f"{freq_metrics['gprime_slope']:.3f}", help="Log–log slope of measured G′ versus frequency.")
    freq_kpi[3].metric("G′ fit R²", f"{freq_metrics['gprime_r2']:.3f}")

    freq_plot = freq_curve.melt(id_vars="f (Hz)", value_vars=["G' (Pa)", 'G" (Pa)'], var_name="Modulus", value_name="Pa")
    fig_freq = px.line(
        freq_plot,
        x="f (Hz)",
        y="Pa",
        color="Modulus",
        title=tr(f"Measured viscoelastic moduli across frequency — {selected_freq_sample}", f"Gemessene viskoelastische Moduli über die Frequenz – {selected_freq_sample}"),
        template=chart_theme,
        log_x=True,
        log_y=True,
    )
    fig_freq.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig_freq, width="stretch")

    st.markdown(tr("### Industrial interpretation — selected sample", "### Industrielle Interpretation – ausgewählte Probe"))
    elastic_dominance = tr("elastic-dominant", "elastisch dominiert") if freq_metrics["tan_delta"] < 1 else tr("viscous-dominant", "viskos dominiert")
    st.write(tr(f"The median measured G″/G′ ratio is {freq_metrics['tan_delta']:.3f}; the response is therefore {elastic_dominance} over the measured frequency range.", f"Das gemessene mediane G″/G′-Verhältnis beträgt {freq_metrics['tan_delta']:.3f}; die Antwort ist über den gemessenen Frequenzbereich daher {elastic_dominance}."))
    st.write(tr(f"G′ changes from {freq_metrics['low_gprime']:.3g} Pa at the lowest measured frequency to {freq_metrics['high_gprime']:.3g} Pa at the highest. Its log–log frequency slope is {freq_metrics['gprime_slope']:.3f} (R² = {freq_metrics['gprime_r2']:.3f}).", f"G′ ändert sich von {freq_metrics['low_gprime']:.3g} Pa bei der niedrigsten gemessenen Frequenz auf {freq_metrics['high_gprime']:.3g} Pa bei der höchsten. Die Log-Log-Frequenzsteigung beträgt {freq_metrics['gprime_slope']:.3f} (R² = {freq_metrics['gprime_r2']:.3f})."))
    st.caption(tr("This describes the observed oscillatory response only; it does not assign a gel class or infer behavior outside the measured frequency range.", "Dies beschreibt ausschließlich die beobachtete oszillatorische Antwort; es wird weder eine Gelklasse zugeordnet noch Verhalten außerhalb des Messbereichs abgeleitet."))

with physicochemical_tabs[0]:
    st.header(T["physical"])
    st.caption(tr("Measured-data chapter on physical stability, sedimentation evidence, clarification, and re-dispersibility.", "Messdatenkapitel zu physikalischer Stabilität, Sedimentationsnachweisen, Klärung und Redispergierbarkeit."))

    st.markdown(tr("### 1. Introduction", "### 1. Einleitung"))
    st.markdown(
        tr("This module is limited to measured physicochemical observations and any sedimentation photographs that are actually present in the workspace. It does not infer sedimentation severity from an invented score or unsupported model output.", "Dieses Modul beschränkt sich auf gemessene physikochemische Beobachtungen und tatsächlich im Arbeitsbereich vorhandene Sedimentationsfotografien. Der Schweregrad der Sedimentation wird weder aus einem erfundenen Score noch aus nicht gestützten Modellergebnissen abgeleitet.")
    )

    st.markdown(tr("### 2. Experimental Design", "### 2. Versuchsdesign"))
    if physchem.empty:
        st.warning(tr("The measured physicochemical workbook was not found at data/physicochemical/physicochemical_results.ods.", "Die gemessene physikochemische Arbeitsmappe wurde unter data/physicochemical/physicochemical_results.ods nicht gefunden."))
    else:
        measured_columns = ["Sample_ID", "Storage_Date", "Storage_Duration", "Product_Type", "Brix_Avg", "Sugar_g_L", "Potential_Alcohol_vv", "Density_g_cm3", "Specific_Gravity", "pH"]
        display_df = physchem[measured_columns].copy()
        display_df = display_df.sort_values(["Storage_Date", "Sample_ID"]).reset_index(drop=True)
        st.dataframe(display_df, width="stretch", hide_index=True)

        experimental_summary = st.columns(4)
        with experimental_summary[0]:
            st.metric(tr("Measured samples", "Gemessene Proben"), int(display_df["Sample_ID"].nunique()))
        with experimental_summary[1]:
            st.metric(tr("Storage ages represented", "Erfasste Lagerungsdauern"), display_df["Storage_Duration"].nunique())
        with experimental_summary[2]:
            st.metric(tr("Mean Brix", "Mittlerer Brix-Wert"), f"{safe_mean(display_df['Brix_Avg']):.2f} °Bx")
        with experimental_summary[3]:
            st.metric(tr("Mean pH", "Mittlerer pH-Wert"), f"{safe_mean(display_df['pH']):.2f}")

    # ==========================================================
# REAL SEDIMENTATION ANALYSIS
# ==========================================================

top_tabs[3].markdown(f"### {T['sed_dataset']}")
sed_tabs = top_tabs[3].tabs([
    "📊 " + T["overview"],
    T["sed_images"],
    T["sed_analysis"],
    T["sed_interpretation"],
    T["sed_references"],
])

sed_df = pd.DataFrame({
    "Sample": ["A","B","C","D","E","F","G"],
    "Manufacturing Date": [
        "04.12.2025",
        "04.12.2025",
        "04.12.2025",
        "04.12.2025",
        "24.07.2025",
        "14.03.2025",
        "01.11.2024"
    ],
    "Product Type": [
        "Standard Pasteurized",
        "Standard Pasteurized",
        "Standard Pasteurized",
        "Pasteurized with Spritz",
        "Standard Pasteurized",
        "Standard Pasteurized",
        "Standard Pasteurized"
    ],
    "Mid Sediment (mL)": [8,7,7.5,6,8,5,3.8],
    "Final Sediment (mL)": [5,5,4,5,8,5,3.5]
})
sed_df["Sediment-bed contraction (%)"] = (
    (sed_df["Mid Sediment (mL)"] -
     sed_df["Final Sediment (mL)"])
    / sed_df["Mid Sediment (mL)"] * 100
).round(1)

sed_df["Final-to-mid sediment-bed ratio"] = (
    sed_df["Final Sediment (mL)"]
    / sed_df["Mid Sediment (mL)"]
).round(2)

sed_df["Final-to-mid sediment-bed ratio (%)"] = (
    sed_df["Final-to-mid sediment-bed ratio"] * 100
).round(1)
sed_df["Total sample volume (mL)"] = np.where(sed_df["Sample"] == "G", 10.0, 50.0)
sed_df["Mid sediment-bed fraction (%)"] = (
    100 * sed_df["Mid Sediment (mL)"] / sed_df["Total sample volume (mL)"]
).round(1)
sed_df["Final sediment-bed fraction (%)"] = (
    100 * sed_df["Final Sediment (mL)"] / sed_df["Total sample volume (mL)"]
).round(1)

with sed_tabs[0]:
    st.dataframe(sed_df, width="stretch", hide_index=True)

    col1,col2,col3,col4 = st.columns(4)
    col1.metric(tr("Samples evaluated", "Bewertete Proben"), len(sed_df))
    col2.metric(tr("Observation points", "Beobachtungszeitpunkte"), 2)
    col3.metric(tr("Largest measured sediment-bed contraction", "Größte gemessene Sedimentbettkontraktion"), f"{sed_df['Sediment-bed contraction (%)'].max():.1f}%")
    col4.metric(tr("Highest final sediment volume", "Höchstes finales Sedimentvolumen"), f"{sed_df['Final Sediment (mL)'].max():.1f} mL")
    st.caption(tr("Sediment-bed fractions are calculated using the recorded total sample volumes: 50 mL for Samples A–F and 10 mL for Sample G.", "Die Sedimentbettanteile werden anhand der dokumentierten Gesamtprobenvolumina berechnet: 50 mL für die Proben A–F und 10 mL für Probe G."))

sed_tabs[2].markdown(tr("### Sedimentation results plate", "### Übersicht der Sedimentationsergebnisse"))
sed_plot = sed_df.sort_values("Final sediment-bed fraction (%)").reset_index(drop=True)
sample_order = sed_plot["Sample"].tolist()
sample_y = {sample: index for index, sample in enumerate(sample_order)}
neutral, accent, pale = "#667785", "#173f5f", "#d8e1e8"

# Figure 1 — direct trajectory result.  The common neutral treatment avoids a categorical colour legend.
fig_trajectory = go.Figure()
for _, row in sed_plot.iterrows():
    y = sample_y[row["Sample"]]
    fig_trajectory.add_trace(go.Scatter(
        x=[0, 1], y=[row["Mid sediment-bed fraction (%)"], row["Final sediment-bed fraction (%)"]],
        mode="lines+markers", showlegend=False,
        line=dict(color=neutral, width=1.6), marker=dict(size=8, color=["white", accent], line=dict(color=neutral, width=1.5)),
        customdata=[[row["Sample"], "Mid"], [row["Sample"], "Final"]],
        hovertemplate="Sample %{customdata[0]}<br>%{customdata[1]} sediment-bed fraction: %{y:.1f}%<extra></extra>",
    ))
    fig_trajectory.add_annotation(x=1.03, y=row["Final sediment-bed fraction (%)"], text=f"{row['Sample']}  {row['Final sediment-bed fraction (%)']:.1f}%", showarrow=False, xanchor="left", font=dict(size=11, color="#243447"))
fig_trajectory.update_layout(
    title=tr("A. Sedimentation trajectory map", "A. Verlaufskarte der Sedimentation"), template=chart_theme, height=360, showlegend=False,
    margin=dict(l=55, r=85, t=50, b=45), font=dict(family="Arial, sans-serif", size=13, color="#243447"),
    xaxis=dict(tickmode="array", tickvals=[0, 1], ticktext=[tr("Mid observation", "Zwischenbeobachtung"), tr("Final observation", "Endbeobachtung")], showgrid=False, zeroline=False),
    yaxis=dict(title=tr("Sediment-bed fraction (% of total sample volume)", "Sedimentbettanteil (% des Gesamtprobenvolumens)"), gridcolor="#edf0f2", zeroline=False),
)
fig_trajectory.add_annotation(x=0, y=1.08, xref="x", yref="paper", text="○ Mid", showarrow=False, font=dict(color=neutral, size=11))
fig_trajectory.add_annotation(x=1, y=1.08, xref="x", yref="paper", text="● Final", showarrow=False, font=dict(color=accent, size=11))
sed_tabs[2].plotly_chart(fig_trajectory, width="stretch", config={"displayModeBar": False})

# Figure 2 — numerical fingerprint uses direct values only and makes the result hierarchy immediately visible.
fingerprint_columns = ["Mid sediment-bed fraction (%)", "Final sediment-bed fraction (%)", "Sediment-bed contraction (%)", "Final-to-mid sediment-bed ratio (%)"]
fingerprint_labels = [tr("Mid fraction", "Zwischenanteil"), tr("Final fraction", "Finaler Anteil"), tr("Contraction", "Kontraktion"), tr("Final / mid ratio", "Final-/Zwischenverhältnis")]
fingerprint_values = sed_plot[fingerprint_columns].to_numpy()
fig_fingerprint = go.Figure(go.Heatmap(
    z=fingerprint_values, x=fingerprint_labels, y=[f"Sample {sample}" for sample in sample_order],
    text=np.array([[f"{value:.1f}%" for value in row] for row in fingerprint_values]), texttemplate="%{text}", textfont=dict(size=12),
    colorscale=[[0, "#f3f6f8"], [0.5, "#aebfcd"], [1, accent]], showscale=False, xgap=2, ygap=2,
    hovertemplate="%{y}<br>%{x}: %{z:.1f}%<extra></extra>",
))
fig_fingerprint.update_layout(title=tr("B. Sedimentation fingerprint heatmap", "B. Heatmap des Sedimentationsprofils"), template=chart_theme, height=330, margin=dict(l=55, r=25, t=50, b=35), xaxis=dict(side="top", showgrid=False), yaxis=dict(showgrid=False, autorange="reversed"))
sed_tabs[2].plotly_chart(fig_fingerprint, width="stretch", config={"displayModeBar": False})

# Figure 3 — observation-state diagram, with the identity line as a physical reference rather than a stability class.
axis_limit = float(max(sed_plot["Mid sediment-bed fraction (%)"].max(), sed_plot["Final sediment-bed fraction (%)"].max()) * 1.12)
fig_state = go.Figure()
fig_state.add_trace(go.Scatter(x=[0, axis_limit], y=[0, axis_limit], mode="lines", line=dict(color="#9ba8b3", width=1, dash="dash"), hoverinfo="skip", showlegend=False))
fig_state.add_trace(go.Scatter(
    x=sed_plot["Mid sediment-bed fraction (%)"], y=sed_plot["Final sediment-bed fraction (%)"], mode="markers+text",
    marker=dict(size=11, color=accent, line=dict(color="white", width=1)), text=[f"{sample}" for sample in sample_order], textposition="top center", showlegend=False,
    hovertemplate="Sample %{text}<br>Mid: %{x:.1f}%<br>Final: %{y:.1f}%<extra></extra>",
))
fig_state.add_annotation(x=axis_limit * 0.72, y=axis_limit * 0.84, text=tr("Identity line: no measured bed-volume change", "Identitätslinie: keine gemessene Änderung des Bettvolumens"), showarrow=False, font=dict(size=11, color="#52616d"))
fig_state.add_annotation(x=axis_limit * 0.70, y=axis_limit * 0.34, text=tr("Below line: reduced sediment-bed fraction", "Unterhalb der Linie: verringerter Sedimentbettanteil"), showarrow=False, font=dict(size=11, color="#52616d"))
fig_state.update_layout(title=tr("C. Sedimentation state diagram", "C. Zustandsdiagramm der Sedimentation"), template=chart_theme, height=360, margin=dict(l=60, r=25, t=50, b=50), xaxis=dict(title=tr("Mid sediment-bed fraction (%)", "Sedimentbettanteil Zwischenbeobachtung (%)"), range=[0, axis_limit], zeroline=False), yaxis=dict(title=tr("Final sediment-bed fraction (%)", "Finaler Sedimentbettanteil (%)"), range=[0, axis_limit], zeroline=False, scaleanchor="x", scaleratio=1))
sed_tabs[2].plotly_chart(fig_state, width="stretch", config={"displayModeBar": False})

sed_tabs[2].caption("Samples A–F were evaluated at 50 mL total volume, whereas Sample G was evaluated at 10 mL. All marks are direct graduated-cylinder measurements; no interpolation, kinetic model, stability class, or cross-module comparison is applied.")
sed_tabs[2].info(
    "**Measured observation.** The trajectory map and state diagram show the direct change between the mid and final observations. Sample C has the largest measured sediment-bed contraction (46.7%), while Samples E and F show no measurable change.\n\n"
    "**Derived parameter.** The heatmap reports normalized sediment-bed fractions, contraction, and final-to-mid ratio for the independently evaluated A–G dataset.\n\n"
    "**Literature-supported interpretation.** A decrease in sediment-bed volume is consistent with bed consolidation or particle rearrangement; it does not independently establish redispersibility or suspension stability.\n\n"
    "**Limitation.** Only two observation times and no sedimentation replicates were available. Settling velocity, kinetic modelling, statistical significance, and long-term stability ranking are not supported."
)

sed_tabs[3].markdown("### 6. Scientific Interpretation")

sed_tabs[3].markdown(
    "**Measured observation.** Final sediment-layer heights range from 3.5 to 8.0 mL in the recorded dataset. "
    "The paired trajectories show the within-sample change between the two storage observations.\n\n"
    "**Derived calculation.** Sediment-bed contraction and final-to-mid sediment-bed ratio express the recorded geometric change between the two observations. They do not independently measure redispersibility.\n\n"
    "**Literature-supported interpretation.** Changes in sediment-bed geometry can be consistent with particle-network restructuring during storage; physical stability should also be evaluated with direct redispersion testing, particle-size data, density contrast, and continuous-phase rheology.\n\n"
    "**Hypothesis requiring validation.** Differences among formulations may reflect variation in aggregation or network structure, but the present sedimentation dataset alone does not identify the mechanism."
)
sed_tabs[3].warning("Only two observation times were available and sedimentation measurements were not replicated. Therefore, statistical hypothesis testing, settling-rate estimation, and kinetic modelling are not justified.")

sed_tabs[1].markdown("### 8. Visual Evidence")

with sed_tabs[1]:
  st.subheader("Visual Sedimentation Evolution")

col1, col2 = sed_tabs[1].columns(2)

with col1:
    st.image(
        "images/sediment_mid.png",
        caption="Mid-storage sedimentation observation (11 February)",
        width="stretch"
    )

with col2:
    st.image(
        "images/sediment_final.png",
        caption="Final sedimentation observation (11 March)",
        width="stretch"
    )

sed_tabs[4].markdown("### 9. References")
sed_tabs[4].markdown(
        "- Stokes, G. G. (1851). On the effect of internal friction of fluids on the motion of pendulums.\n"
        "- Mewis, J. and Wagner, N. J. (2012). Colloidal Suspension Rheology.\n"
        "- Food Hydrocolloids — network formation, viscoelastic response, and suspension structure.\n"
        "- Steffe, J. F. (1996). Rheological Methods in Food Process Engineering."
    )

with rheology_tabs[4]:
    st.header(T["summary_header"])
    st.info(
        tr("This section reports only measured observables from the three rheology workbooks and converts them into a research-style stability interpretation.", "Dieser Abschnitt berichtet ausschließlich gemessene Größen aus den drei Rheologie-Arbeitsmappen und überführt sie in eine wissenschaftliche Stabilitätsinterpretation.")
    )

    summary_metrics = pd.DataFrame(
        {
            "Dataset": ["Flow", "Amplitude sweep", "Frequency sweep"],
            "Mean viscosity η": [safe_mean(flow["η (Pa s)"]), np.nan, np.nan],
            "Mean G′": [np.nan, safe_mean(amp["G' (Pa)"]), safe_mean(freq["G' (Pa)"])],
            "Mean G″": [np.nan, safe_mean(amp['G" (Pa)']), safe_mean(freq['G" (Pa)'])],
            "Mean tanδ": [np.nan, np.nan, safe_mean(freq['δ (°)'])],
        }
    )
    st.dataframe(summary_metrics, width="stretch", hide_index=True)

    sample_compare = st.multiselect(
        tr("Sample comparison mode", "Probenvergleich"),
        options=sample_profiles["Sample_ID"].tolist(),
        default=sample_profiles["Sample_ID"].tolist()[:3],
    )

    parameter_features = [
        "Mean_Viscosity",
        "Mean_Gprime",
        "Mean_Gdouble",
        "Mean_tan_delta",
        "Flow_behavior_index_n",
        "Consistency_coefficient_K",
    ]

    if sample_compare:
        parameter_df = sample_profiles[sample_profiles["Sample_ID"].isin(sample_compare)].copy()
        st.markdown(tr("### Sample-level derived rheology parameters", "### Abgeleitete rheologische Parameter auf Probenebene"))
        radar_features = [
            ("Mean_Viscosity", "Low-shear viscosity"),
            ("Flow_behavior_index_n", "Shear-thinning strength"),
            ("Mean_Gprime", "Elastic modulus G′"),
            ("Mean_tan_delta", "Elastic dominance"),
            ("Consistency_coefficient_K", "Frequency independence"),
        ]
        radar_source = parameter_df[["Sample_ID", *[feature for feature, _ in radar_features]]].copy()
        usable_features = [feature for feature, _ in radar_features if radar_source[feature].notna().any()]
        radar_labels = [label for feature, label in radar_features if feature in usable_features]
        radar_normalized = radar_source[usable_features].copy()
        for feature in usable_features:
            values = radar_normalized[feature]
            span = values.max() - values.min()
            radar_normalized[feature] = (values - values.min()) / span if pd.notna(span) and span > 0 else np.nan
        if "Flow_behavior_index_n" in usable_features:
            radar_normalized["Flow_behavior_index_n"] = 1 - radar_normalized["Flow_behavior_index_n"]
        radar_fig = go.Figure()
        palette = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00"]
        for index, (_, row) in enumerate(radar_normalized.iterrows()):
            if row.notna().all():
                radar_fig.add_trace(go.Scatterpolar(
                    r=row.tolist() + [row.iloc[0]], theta=radar_labels + [radar_labels[0]],
                    fill="toself", opacity=0.18, line=dict(color=palette[index % len(palette)], width=2),
                    name=radar_source.iloc[index]["Sample_ID"],
                ))
        radar_fig.update_layout(template=chart_theme, title=tr("Relative rheological fingerprint", "Relatives rheologisches Profil"), height=600,
                                polar=dict(radialaxis=dict(visible=True, range=[0, 1], tickvals=[0, 0.5, 1])),
                                legend=dict(orientation="h", yanchor="bottom", y=1.08))
        st.plotly_chart(radar_fig, width="stretch")
        st.caption(tr("Radar dimensions are min–max normalized across the selected parent samples and therefore represent relative rheological fingerprints rather than values in physical units.", "Die Radardimensionen sind über die ausgewählten Ausgangsproben Min-Max-normalisiert und stellen daher relative rheologische Profile statt Werte in physikalischen Einheiten dar."))
        st.info(tr("The radar area is not a validated stability score. Each rheological dimension must be interpreted separately and together with replicate variability and model quality.", "Die Radarfläche ist kein validierter Stabilitätsscore. Jede rheologische Dimension muss einzeln sowie zusammen mit Replikatvariabilität und Modellqualität interpretiert werden."))
        st.dataframe(
            parameter_df[["Sample_ID", "Product_Type", *parameter_features]],
            width="stretch",
            hide_index=True,
        )
        st.caption(tr("Values are sample-level derived summaries. A parameter forest plot is not shown because replicate-level parameter confidence intervals have not yet been calculated independently.", "Die Werte sind abgeleitete Zusammenfassungen auf Probenebene. Ein Forest-Plot wird nicht gezeigt, da Konfidenzintervalle der Parameter auf Replikatebene noch nicht unabhängig berechnet wurden."))
    else:
        st.warning(tr("Select at least one sample to display the sample-level derived parameter table.", "Wählen Sie mindestens eine Probe aus, um die Tabelle der abgeleiteten Parameter anzuzeigen."))

    st.markdown(tr("### Thesis conclusion", "### Schlussfolgerung der Masterarbeit"))
    st.markdown(
        tr("The synthesis section summarizes the measured rheological evidence in a thesis-style context. The resulting interpretation is based on elastic dominance, structural retention, and suspension behaviour rather than on raw spreadsheet presentation alone.", "Der Syntheseabschnitt fasst die gemessenen rheologischen Erkenntnisse im Kontext der Masterarbeit zusammen. Die Interpretation basiert auf elastischer Dominanz, Strukturerhaltung und Suspensionsverhalten und nicht allein auf der Darstellung von Rohdaten.")
    )

with rheology_tabs[5]:
    st.header(tr("Rheology Metadata and Raw Data", "Rheologie-Metadaten und Rohdaten"))
    sample_overview_table = sample_overview[["Sample_ID", "Product_Type", "Manufacturing_Date", "Number_of_Replicates"]].copy()
    st.dataframe(sample_overview_table, width="stretch", hide_index=True)
    st.subheader(tr("Replicate Details", "Details der Wiederholungen"))
    replicate_details = (
        meta[["Measurement_ID", "Parent_Sample", "Replicate_Number"]]
        .sort_values(["Parent_Sample", "Replicate_Number"])
        .reset_index(drop=True)
    )
    st.dataframe(replicate_details, width="stretch", hide_index=True)
    st.subheader(tr("Raw Rheology Data", "Rheologische Rohdaten"))
    with st.expander(tr("Flow curve workbook data", "Arbeitsmappendaten der Fließkurve")):
        st.dataframe(flow, width="stretch", hide_index=True)
    with st.expander(tr("Amplitude sweep workbook data", "Arbeitsmappendaten des Amplitudensweeps")):
        st.dataframe(amp, width="stretch", hide_index=True)
    with st.expander(tr("Frequency sweep workbook data", "Arbeitsmappendaten des Frequenzsweeps")):
        st.dataframe(freq, width="stretch", hide_index=True)

with rheology_tabs[6]:
    st.header(tr("Rheology References", "Rheologische Literatur"))
    st.caption(tr("Rheology-specific scientific sources supporting interpretation of the measured response.", "Rheologiespezifische wissenschaftliche Quellen zur Unterstützung der Interpretation der gemessenen Antwort."))
    for ref in REFERENCE_LIBRARY:
        with st.expander(ref["title"]):
            st.write(tr("Link to publication:", "Link zur Publikation:"), ref["publication_link"])
            st.write(tr("DOI / journal reference:", "DOI / Zeitschriftenreferenz:"), ref["doi"])
            st.write(tr("Relevance:", "Relevanz:"), ref["relevance"])

with top_tabs[5]:
    st.header(T["literature_header"])
    st.markdown(T["lit_text"])
    st.markdown(
        "- Food Hydrocolloids — network formation, viscoelastic response, and suspension structure.\n"
        "- Journal of Food Engineering — flow behaviour, rheological characterization, and industrial process interpretation.\n"
        "- Journal of Rheology — oscillatory and linear viscoelastic methodology constraints.\n"
        "- Journal of Texture Studies — particulate stability and textural implications."
    )
    st.markdown("### Scientific support principle")
    st.markdown(
        "The measured values from the workbooks remain the analytical foundation of the chapter. The literature is used to support interpretation, strengthen scientific context, and help place the observed response within established rheological theory."
    )
