#!/usr/bin/env python3
"""
Inventory papers/raw and propose organized folder structure.

Goals:
- Find duplicate files by content hash.
- Extract metadata (title, author) from PDFs/PPTs without reading full content.
- Suggest topic categories based on filenames and metadata.
- Produce a machine-readable report for review before moving files.

Usage:
    python scripts/organize_papers.py
"""

import csv
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

RAW_DIR = Path("papers/raw")
REPORT_JSON = Path("papers/_organization_report.json")
REPORT_CSV = Path("papers/_organization_report.csv")

# Topics inferred from filename keywords. Lowercase keys.
TOPIC_KEYWORDS = {
    "acquisition": ["acquisition", "geometry", "survey", "land", "marine", "obc", "nodal", "seismic acquisition", "geometry normalisation", "footprint", " nazemnaya sejsmorazvedka", "сейсморазведка", "геометрия", "геометрии"],
    "signal_processing": ["signal processing", "digital signal", "fourier", "filter", "filtering", "spectral", "wavelet", "linear algebra", "impulses operators", "operators", "k-filter"],
    "deconvolution": ["decon", "deconvolution", "wavelet decon", "spiking", "predictive decon", "signature decon", "mbwp", "zero phasing", "dekonvolyutsii", "деконволюция"],
    "noise_attenuation": ["noise", "denoise", "denoising", "swell", "linear noise", "ground roll", "coherent noise", "random noise", "swami", "median", "cadzow", "svd", "nucns", "rscd", "surface wave", "guided waves", "помех", "подавление помех"],
    "multiples": ["multiple", "multiples", "demultiple", "srme", "epsi", "swd", "mwd", "wema", "water bottom", "mpfi", "prediction and subtraction", "adaptive subtraction", "adsub"],
    "velocity": ["velocity", "nmo", "velocity analysis", "velocity model", "velocity building", "tomography", "model building", "vel analysis", "vel mod build", "velocity model building", "vmb", "fwi", "full waveform inversion"],
    "migration": ["migration", "pstm", "prestm", "kirchhoff", "rtm", "beam", "imaging", "mig fundamentals", "wavefield extrapolation", "ray tracing", "migration basics", "migration overview", "pstm walkthrough", "pstm overview", "dip aperture", "anisotropy"],
    "statics": ["static", "statics", "near surface", "refraction", "datum", "weathering", "вчр", "высокочастотная", "модель вчр", "переломленным"],
    "q_and_absorption": ["q", "q-compensation", "inverse q", "absorption", "attenuation", "kjartansson", "futterman", "kramers-kronig", "kramers kronig"],
    "radon_taup": ["radon", "tau-p", "taup", "hyperbolic radon", "parabolic radon", "tau p"],
    "regularization": ["regularization", "interpolation", "5d", "x-spread", "xspread", "ovt", "offset vector tile", "cross-spread", "orthogonal geom", "cov vs offset"],
    "qc": ["qc", "quality control", "data qc", "well-driven", "well tie", "data analysis"],
    "formats": ["segy", "segd", "sps", "ukooa", "format", "seg-d", "seg-y", "field tape"],
    "general": ["introduction", "overview", "basics", "fundamentals", "processing", "training manual", "course notes", "seismic data analysis"],
}


def md5_file(path: Path, block_size: int = 65536) -> str:
    """Compute MD5 hash of a file efficiently."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def run_cmd(args: list, timeout: int = 30) -> str:
    """Run a command and return stdout as string."""
    try:
        result = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=timeout
        )
        return result.stdout or ""
    except Exception:
        return ""


def parse_pdfinfo(path: Path) -> dict:
    """Extract Title and Author from pdfinfo output."""
    out = run_cmd(["pdfinfo", str(path)])
    info = {"title": "", "author": "", "pages": ""}
    for line in out.splitlines():
        if line.startswith("Title:"):
            info["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Author:"):
            info["author"] = line.split(":", 1)[1].strip()
        elif line.startswith("Pages:"):
            info["pages"] = line.split(":", 1)[1].strip()
    return info


def parse_exiftool(path: Path) -> dict:
    """Extract Title and Author from Office/PDF files using exiftool."""
    out = run_cmd(["exiftool", "-Title", "-Author", "-Creator", "-Pages", str(path)])
    info = {"title": "", "author": "", "pages": ""}
    for line in out.splitlines():
        if line.startswith("Title"):
            info["title"] = line.split(":", 1)[1].strip()
        elif line.startswith("Author"):
            info["author"] = line.split(":", 1)[1].strip()
        elif line.startswith("Creator") and not info["author"]:
            # Fallback for Office docs where Author may be empty.
            info["author"] = line.split(":", 1)[1].strip()
        elif line.startswith("Pages"):
            info["pages"] = line.split(":", 1)[1].strip()
    return info


def first_page_text(path: Path) -> str:
    """Extract text from the first page of a PDF."""
    out = run_cmd(["pdftotext", "-f", "1", "-l", "1", str(path), "-"], timeout=20)
    return out.strip()


def guess_title_author_from_text(text: str) -> tuple:
    """Very lightweight heuristic: title is the longest early line, author follows keywords."""
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    # Filter out short fragments and obvious headers.
    candidates = [line for line in lines[:20] if len(line) > 12 and not line.lower().startswith(("abstract", "introduction", "figure"))]
    title = candidates[0] if candidates else ""
    author = ""
    for line in lines[:30]:
        lower = line.lower()
        if any(word in lower for word in ["by ", "author", "authors", "presented by"]):
            # Simple cleanup.
            author = line.replace("by", "").replace("By", "").strip(" :")
            break
    return title, author


def is_likely_textbook(path: Path, size: int, pages: str) -> bool:
    """Identify broad reference books / textbooks. Avoid classifying large PPT courses as textbooks."""
    name = path.name.lower()
    suffix = path.suffix.lower()

    # PPT/PPTX course decks are almost never textbooks.
    if suffix in {".ppt", ".pptx"}:
        return False

    known_textbook_markers = [
        "seismicdataanalysis",
        "seismic data analysis",
        "methods of seismic",
        "practical seismic",
        "advanced digital signal processing",
        "сейсморазведка",
        "sejsmorazvedka",
        "kolichestvennaya seysmologiya",
        "illustrated seismic processing",
        "training manual",
        "introduction to linear algebra",
        "tsvankin",
        "bleistein",
        "cherepovskij",
        "bondarev",
        "бондарев",
    ]
    normalized_name = name.replace("-", " ").replace("_", " ")
    if any(marker in normalized_name for marker in known_textbook_markers):
        return True

    # Heuristic: very large PDF with > 200 pages and a generic/broad title.
    try:
        if size > 50_000_000 and int(pages) > 200:
            return True
    except ValueError:
        pass
    return False


def second_pass_topic(path: Path, topic: str, text: str) -> str:
    """For uncategorized items, try to classify from first-page text content."""
    if topic != "uncategorized":
        return topic
    if not text:
        return topic

    text_lower = text.lower()
    text_lower = text_lower.replace("-", " ").replace("_", " ")

    # Re-use topic keywords but add content-specific clues.
    content_keywords = {
        "migration": ["migration", "kirchhoff", "pstm", "prestack", "wavefield extrapolation", "rtm", "imaging"],
        "velocity": ["velocity model", "velocity analysis", "tomography", "nmo", "model building"],
        "multiples": ["multiple", "multiples", "srme", "demultiple", "surface-related", "internal multiple"],
        "deconvolution": ["deconvolution", "decon", "wavelet", "inverse filter", "spiking"],
        "noise_attenuation": ["noise", "denoise", "ground roll", "surface wave", "coherent noise", "random noise", "swami", "cadzow"],
        "statics": ["static", "statics", "near surface", "refraction", "weathering", "first break"],
        "q_and_absorption": ["q", "attenuation", "absorption", "quality factor", "anelastic"],
        "radon_taup": ["radon", "tau-p", "tau p", "parabolic", "hyperbolic"],
        "regularization": ["regularization", "interpolation", "5d", "aliasing", "reconstruction"],
        "signal_processing": ["fourier", "filter", "spectral", "wavelet transform", "curvelet"],
        "formats": ["seg-y", "seg-d", "format", "standard"],
        "acquisition": ["acquisition", "geometry", "survey", "receiver", "source"],
        "textbooks": ["chapter", "exercises", "textbook"],
    }

    scores = {}
    for t, keywords in content_keywords.items():
        score = 0
        for kw in keywords:
            if kw in text_lower:
                score += len(kw.split()) + 1
        if score:
            scores[t] = score

    if not scores:
        return topic
    return max(scores, key=scores.get)


def extract_metadata(path: Path) -> dict:
    """Route to the best available metadata extractor."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        info = parse_pdfinfo(path)
        # Fallback to exiftool if pdfinfo yields nothing useful.
        if not info["title"] and not info["author"]:
            info = parse_exiftool(path)
        # Fallback to first-page text for PDFs with no useful metadata.
        if not info["title"] and not info["author"]:
            text = first_page_text(path)
            title, author = guess_title_author_from_text(text)
            info["title"] = title
            info["author"] = author
            info["first_page_text"] = text
        else:
            info["first_page_text"] = ""
        return info
    else:
        info = parse_exiftool(path)
        info["first_page_text"] = ""
        return info


def sanitize_filename(name: str) -> str:
    """Make a name safe for filesystem use."""
    name = name.replace(":", " -").replace("/", "_").replace("\\", "_")
    name = re.sub(r"[\s]+", " ", name).strip()
    return name


def suggest_topic(path: Path, meta: dict, size: int) -> str:
    """Suggest a topic folder based on filename, parent directory names, and metadata."""
    # First, manual filename overrides.
    if path.name in FILENAME_TOPIC_OVERRIDES:
        return FILENAME_TOPIC_OVERRIDES[path.name]

    # Then, check for textbooks / large reference works.
    if is_likely_textbook(path, size, meta.get("pages", "")):
        return "textbooks"

    text = " ".join([path.name, str(path.parent)]).lower()
    text = text.replace("_", " ").replace("-", " ")

    # Strong parent-folder signals: some raw folders are already grouped.
    parent_signals = {
        "migration": ["migr", "piet gerritsma"],
        "multiples": ["eage_course_multiples", "demultiple"],
        "deconvolution": ["mbwp_instructions", "deconvolution"],
        "regularization": ["regularisation"],
        "noise_attenuation": ["de-noise", "denoise"],
        "velocity": ["velocity"],
        "formats": ["segd", "segy", "sps"],
        "general": ["data analysis", "odt1"],
    }
    for topic, signals in parent_signals.items():
        if any(signal in text for signal in signals):
            return topic

    scores = {}
    for topic, keywords in TOPIC_KEYWORDS.items():
        score = 0
        for kw in keywords:
            if kw in text:
                # Longer keyword matches are more specific.
                score += len(kw.split()) + 1
        if score:
            scores[topic] = score

    if not scores:
        return "uncategorized"
    # Return topic with highest score.
    return max(scores, key=scores.get)


def clean_title(title: str) -> str:
    """Remove unhelpful prefixes from extracted titles."""
    title = title.strip()
    prefixes = [
        "Microsoft PowerPoint - ",
        "Microsoft Word - ",
        "PowerPoint Presentation",
        "Presentation Title Goes Here",
        "Untitled",
        "Slide 1",
        "AL InTouch Content Word Template",
        "This is the title of an example SEG abstract",
    ]
    for prefix in prefixes:
        if title.startswith(prefix):
            title = title[len(prefix):].strip()
    return title


# Manual topic overrides for filenames that are otherwise hard to classify.
FILENAME_TOPIC_OVERRIDES = {
    "FlatironsTrainingManual.pdf": "general",
    "CurveletTransform.pdf": "signal_processing",
    "2012_FB_IJones_NearSurface.pdf": "statics",
    "IvanovEtAlsegam2017-17793766.1.pdf": "statics",
    "IvanovEtAlsegam2017-17793766.1 (2).pdf": "statics",
    "IvanovEtAlsegam2017-17793766.1 (3).pdf": "statics",
    "foti2011.pdf": "statics",
    "foti2011 (2).pdf": "statics",
    "1999_Xia_Li_OU_Thesis.pdf": "general",
    "SEG-1991-1428.pdf": "formats",
    "002_AAA_4039688_01.ppt": "noise_attenuation",
    "lecture.pdf": "general",
    "lecture-1.pdf": "general",
    "lecture-2.pdf": "general",
    "lecture5 (2).pdf": "general",
    "drthesis_2020_Sarajaervi.pdf": "general",
    "369_1.9781560803041.all.pdf": "general",
    "geokniga-15355379782982.pdf": "textbooks",
    "RobustDec2019_ZhangYuan.pdf": "deconvolution",
    "adsub_test.pptx": "multiples",
    "miao2009.pdf": "noise_attenuation",
    "CRR201211.pdf": "general",
    "CRR201314.pdf": "general",
    "CRR201749.pdf": "general",
    "sedi_surface.pdf": "statics",
    "2008-43.pdf": "general",
    "2003-33.pdf": "general",
    "ji0623002.pdf": "general",

    "Datta_abm_mac_v3.pdf": "migration",
    "Datta_abm_mac_v3-1.pdf": "migration",
    "wit2002-hertweck.pdf": "q_and_absorption",
    "03_Strategies_Parameters_Omega2_3737355 _01.ppt": "deconvolution",
    "03_Strategies_Parameters_Omega2_3737355 _01 (2).ppt": "deconvolution",
    "03_Strategies_Parameters_Omega2_3737355 _01 (3).ppt": "deconvolution",
    "2011_Стандартные_оценки_качества_полевого_сейсмического_материала (3).pdf": "qc",
    "Avtoref_Amani_Mangua.pdf": "general",
    "dissertation1.pdf": "general",
    "dissertation1-1.pdf": "general",
}

# Manual overrides for filenames that are otherwise meaningless.
FILENAME_OVERRIDES = {
    # Major textbooks / reference works
    "geokniga-15355379782982.pdf": "Yilmaz - Seismic Data Analysis.pdf",
    "geokniga-seismicdataanalysis.pdf": "Yilmaz - Seismic Data Analysis.pdf",
    "geokniga-practical-seismic-data-analysis.pdf": "Yilmaz - Seismic Data Analysis.pdf",
    "geokniga-advanced-digital-signal-processing-seismic-data.pdf": "Yilmaz - Advanced Digital Signal Processing of Seismic Data.pdf",
    "geokniga-kolichestvennaya-seysmologiya-tom-2.pdf": "Aki and Richards - Quantitative Seismology, Vol 2.pdf",
    "geokniga-tsvankiniseismicwavefieldsinlayeredisotropicmediasamizdatpress1995tk105sgsp.pdf": "Tsvankin - Seismic Wavefields in Layered Isotropic Media.pdf",
    "2007-Бондарев Сейсморазведка.pdf": "Bondarev - Seismorazvedka.pdf",
    "Methods_of_Seismic_Data_Processing.pdf": "Methods of Seismic Data Processing.pdf",
    "Methods_of_Seismic_Data_Processing-1.pdf": "Methods of Seismic Data Processing.pdf",
    "HATTON_Processing.pdf": "Hatton - Seismic Data Processing.pdf",
    "Introduction to Linear Algebra Fifth Edition by Gilbert Strang.pdf": "Strang - Introduction to Linear Algebra 5th Ed.pdf",
    "FlatironsTrainingManual.pdf": "Flatirons - Seismic Processing Training Manual.pdf",
    "CurveletTransform.pdf": "Curvelet Transform.pdf",
    "SEG-1991-1428.pdf": "SEG 1991-1428.pdf",
    "2012_FB_IJones_NearSurface.pdf": "Jones - Near Surface.pdf",
    "1999_Xia_Li_OU_Thesis.pdf": "Li - PhD Thesis 1999.pdf",
    # Bad-metadata fixes
    "002_AAA_4039688_01.ppt": "Anomalous Amplitude Attenuation (AAA).ppt",
    "step_1_initial_MBWP_OPER_CREATE.ppt": "MBWP Step 1 - Initial Operator.ppt",
    "step_2_estimating_MBWP_paramters.ppt": "MBWP Step 2 - Estimating Parameters.ppt",
    "step_3_final_MBWP_oper.ppt": "MBWP Step 3 - Final Operator.ppt",
    "MBWP_model_equations.ppt": "MBWP Model Equations.ppt",
    "DGS_MBWP_update_2008.ppt": "MBWP Update 2008.ppt",
    "MBWP_w_constraining_filter_procedure3.ppt": "MBWP Constraining Filter Procedure.ppt",
    "03_Strategies_Parameters_Omega2_3737355 _01.ppt": "Deconvolution Strategies and Parameters Omega2.ppt",
    "03_Strategies_Parameters_Omega2_3737355 _01 (2).ppt": "Deconvolution Strategies and Parameters Omega2.ppt",
    "03_Strategies_Parameters_Omega2_3737355 _01 (3).ppt": "Deconvolution Strategies and Parameters Omega2.ppt",
    "04_DECON_Issues_Omega2_3737355 _01.ppt": "Deconvolution Issues Omega2.ppt",
    "04_DECON_Issues_Omega2_3737355 _01 (2).ppt": "Deconvolution Issues Omega2.ppt",
    "04_DECON_Issues_Omega2_3737355 _01 (3).ppt": "Deconvolution Issues Omega2.ppt",
    "SEG-SPS-Format-rev-2_1.pdf": "SEG SPS Format rev 2.1.pdf",
    "MPFI - Best Practice v3_7274381_06 (2).pdf": "MPFI Best Practice v3.pdf",
    "MPFI - Best Practice v3_7274381_06.pdf": "MPFI Best Practice v3.pdf",
    "Best_Practice_CADZOW_v2_7017202_03.pdf": "Cadzow Best Practice v2.pdf",
    "Best_Practice_NUCNS_v4_7206366_03.pdf": "NUCNS Best Practice v4.pdf",
    "RSCD Best Practice v3_7284556_01.pdf": "RSCD Best Practice v3.pdf",
    "SRME_Lecture_Part2_2005_09.ppt": "SRME Lecture Part 2 2005.ppt",
    "waveequations-4speedsound.pdf": "Wave Equations for Sound Speed.pdf",
    "qapp.pdf": "Q Application Reference.pdf",
    "qest.pdf": "Q Estimation Reference.pdf",
    "02_Why_TauP_Transform_jan07_3737355 _01.ppt": "Why Tau-P Transform.ppt",
    "02_Why_TauP_Transform_jan07_3737355 _01 (2).ppt": "Why Tau-P Transform.ppt",
    "02_Why_TauP_Transform_jan07_3737355 _01 (3).ppt": "Why Tau-P Transform.ppt",
    "57951-whats-the-datum-01.pdf": "What's the Datum.pdf",
    "57951-whats-the-datum-01 (2).pdf": "What's the Datum.pdf",
    "57951-whats-the-datum-01 (5).pdf": "What's the Datum.pdf",
    "57951-whats-the-datum-01 (6).pdf": "What's the Datum.pdf",
    "57951-whats-the-datum-01 (7).pdf": "What's the Datum.pdf",
    "sedi_surface.pdf": "SEDI Surface Waves.pdf",
    "Этап_1_04_Тр_Обработка_Построение_модели_ВЧР_по_преломленным_волнам_ext.pdf": "Russian Report - Refraction Statics Model Building.pdf",
    "Этап_2_04_Тр_Обработка_Подавление_помех_до_деконволюции_оценка_результатов_v2.pdf": "Russian Report - Noise Attenuation Before Deconvolution.pdf",
    "foti2011.pdf": "Foti - Surface Wave Methods.pdf",
    "foti2011 (2).pdf": "Foti - Surface Wave Methods.pdf",
    "2017_d-2017-476-6-693.pdf": "2017_d-2017-476-6-693.pdf",
    "25856559.pdf": "25856559.pdf",
    "02_FOOTPRINT_Omega2_may06_4039690_01.ppt": "Footprint Omega2.ppt",
    "02_FOOTPRINT_Omega2_may06_4039690_01 (2).ppt": "Footprint Omega2.ppt",
    "GEOMETRY_LAND.pdf": "Geometry Land.pdf",
    "MBWP_report_blurb_for zero phasing.doc": "MBWP Report Blurb - Zero Phasing.doc",
    "RobustDec2019_ZhangYuan.pdf": "Robust Deconvolution 2019 Zhang Yuan.pdf",
    "2010_osobennosti-algoritma-f_x-dekonvolyutsii.pdf": "Features of FX Deconvolution Algorithm.pdf",
    "2010_osobennosti-algoritma-f_x-dekonvolyutsii (2).pdf": "Features of FX Deconvolution Algorithm.pdf",
    "2010_osobennosti-algoritma-f_x-dekonvolyutsii (3).pdf": "Features of FX Deconvolution Algorithm.pdf",
    "the-application-of-wavelet-deconvolution-for-noise-reduction-in-seismic-data-preprint.pdf": "Wavelet Deconvolution for Noise Reduction.pdf",
    "O-zadachakh-dekonvolyutsii-seysmicheskikh-zapisey_2022.pdf": "On Deconvolution of Seismic Records.pdf",
    "O-zadachakh-dekonvolyutsii-seysmicheskikh-zapisey_2022 (2).pdf": "On Deconvolution of Seismic Records.pdf",
    # EAGE multiples course - keep descriptive original filenames
    "00_titleslide_EET.pdf": "EAGE EET - Title Slide.pdf",
    "01_whats_the_problem.pdf": "EAGE EET 01 - Whats the Problem.pdf",
    "02_move-out_discrimination.pdf": "EAGE EET 02 - Move-out Discrimination.pdf",
    "03_predictive_deconvolution.pdf": "EAGE EET 03 - Predictive Deconvolution.pdf",
    "04_wave_field_extrapolation.pdf": "EAGE EET 04 - Wave Field Extrapolation.pdf",
    "05_principles_SRME.pdf": "EAGE EET 05 - Principles of SRME.pdf",
    "06_practical_aspects_SRME.pdf": "EAGE EET 06 - Practical Aspects of SRME.pdf",
    "07_adaptive_substraction.pdf": "EAGE EET 07 - Adaptive Subtraction.pdf",
    "08_towards_3d_multiple_removal.pdf": "EAGE EET 08 - Towards 3D Multiple Removal.pdf",
    "09_internal_multiple_removal.pdf": "EAGE EET 09 - Internal Multiple Removal.pdf",
    "10a_EPSI.pdf": "EAGE EET 10a - EPSI.pdf",
    "10b_imaging_multiples.pdf": "EAGE EET 10b - Imaging Multiples.pdf",
    "10c_towards_FWI.pdf": "EAGE EET 10c - Towards FWI.pdf",
    # Other specific overrides
    "Bashir Y. Seismic Imaging Methods and Applications...Oil...2022.pdf": "Bashir - Seismic Imaging Methods and Applications 2022.pdf",
    "bleistein2001.pdf": "Bleistein - Mathematical Methods for Wave Phenomena 2001.pdf",
    "486_cherepovskij_a_v_nazemnaya_sejsmorazvedka_novogo_tehnologicheskogo.pdf": "Cherepovsky - Land Seismic Surveying.pdf",
    "Datta_abm_mac_v3.pdf": "Datta - Anisotropic Beam Migration.pdf",
    "Datta_abm_mac_v3-1.pdf": "Datta - Anisotropic Beam Migration.pdf",
    "01_Rawlinson_Seismic_Ray_Tracing_and_2007.pdf": "Rawlinson - Seismic Ray Tracing and Wavefront Tracking 2007.pdf",
    "lecture-1.pdf": "Lecture 1.pdf",
    "lecture-2.pdf": "Lecture 2.pdf",
    "lecture5 (2).pdf": "Lecture 5 - Surface Waves and Dispersion.pdf",
    "2003-33.pdf": "2003-33.pdf",
    "ji0623002.pdf": "ji0623002.pdf",
}


def apply_filename_override(path: Path, proposed: str) -> str:
    """Use known readable filenames when the original filename is cryptic."""
    return FILENAME_OVERRIDES.get(path.name, proposed)


USELESS_NAMES = {
    "user", "users", "unknown", "untitled", "administrator", "admin",
    "adobe", "indesign", "arbortext", "microsoft", "word", "powerpoint",
    "goofy", "salevin", "mwnorr1", "roma", "gary", "pc bureau", "paradigm",
    "latex with hyperref", "prof. dr. heiner igel",
}


def is_useful_name(name: str) -> bool:
    """Return False if the extracted author/title is a software placeholder or generic term."""
    if not name:
        return False
    normalized = name.lower().strip(" .,:-_")
    # If any useless token is the whole or dominant part, reject.
    for bad in USELESS_NAMES:
        if bad in normalized:
            return False
    return True


def propose_filename(path: Path, meta: dict) -> str:
    """Propose a clean filename with author and title if available."""
    suffix = path.suffix.lower()

    author = meta.get("author", "")
    title = clean_title(meta.get("title", ""))

    # Clean up author.
    if author:
        author = sanitize_filename(author)
        # Take only first author or last name if too long.
        if len(author) > 60:
            author = author.split(",")[0].strip()
        if len(author) > 60:
            author = author.split()[0].strip()

    # Clean up title.
    if title:
        title = sanitize_filename(title)
        # Truncate very long titles.
        if len(title) > 100:
            title = title[:100].rsplit(" ", 1)[0] + "..."

    useful_author = is_useful_name(author)
    useful_title = is_useful_name(title)

    if useful_author and useful_title:
        proposed = f"{author} - {title}{suffix}"
    elif useful_title:
        proposed = f"{title}{suffix}"
    elif useful_author:
        proposed = f"{author}{suffix}"
    else:
        # Fallback: use existing filename without duplicate counter suffix.
        base = path.stem
        base = re.sub(r"\s*\(\d+\)\s*$", "", base)
        base = sanitize_filename(base)
        proposed = f"{base}{suffix}"

    proposed = apply_filename_override(path, proposed)
    return proposed


def unique_path(topic: str, name: str, used: dict) -> str:
    """Ensure proposed filename is unique within its topic folder."""
    key = (topic, name.lower())
    if key not in used:
        used[key] = 0
        return f"{topic}/{name}"
    used[key] += 1
    stem, suffix = Path(name).stem, Path(name).suffix
    new_name = f"{stem}_{used[key]}{suffix}"
    return f"{topic}/{new_name}"


def is_metadata_file(path: Path) -> bool:
    """True for Windows/macOS metadata and temp files."""
    name = path.name
    return (
        name == "Thumbs.db"
        or ".Zone.Identifier" in name
        or ":$DATA" in name
        or name.startswith("~$")
        or name.startswith(".")
    )


def main():
    entries = []
    hashes = {}
    duplicates = []
    used_names = {}

    print(f"Scanning {RAW_DIR} ...")
    files = sorted(p for p in RAW_DIR.rglob("*") if p.is_file())
    total = len(files)
    print(f"Found {total} files.")

    for i, path in enumerate(files, 1):
        if i % 50 == 0:
            print(f"  processed {i}/{total}")

        if is_metadata_file(path):
            continue

        size = path.stat().st_size
        rel = path.relative_to(RAW_DIR)
        fhash = md5_file(path)

        is_duplicate_of = ""
        if fhash in hashes:
            is_duplicate_of = hashes[fhash]
            duplicates.append((str(rel), is_duplicate_of))
        else:
            hashes[fhash] = str(rel)

        meta = extract_metadata(path)
        topic = suggest_topic(path, meta, size)
        # Second-pass classification from first-page content for uncategorized PDFs.
        topic = second_pass_topic(path, topic, meta.get("first_page_text", ""))
        proposed_name = propose_filename(path, meta)
        proposed_path = unique_path(topic, proposed_name, used_names)

        entries.append(
            {
                "current_path": str(rel),
                "size_bytes": size,
                "md5": fhash,
                "is_duplicate_of": is_duplicate_of,
                "suggested_topic": topic,
                "proposed_path": proposed_path,
                "title": meta.get("title", ""),
                "author": meta.get("author", ""),
                "pages": meta.get("pages", ""),
            }
        )

    # Sort entries by topic and then proposed path.
    entries.sort(key=lambda x: (x["suggested_topic"], x["proposed_path"]))

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(
            {
                "source_dir": str(RAW_DIR),
                "total_files": len(entries),
                "duplicates_count": len(duplicates),
                "entries": entries,
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    with open(REPORT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "current_path",
                "suggested_topic",
                "proposed_path",
                "is_duplicate_of",
                "size_bytes",
                "pages",
                "title",
                "author",
            ],
        )
        writer.writeheader()
        for e in entries:
            writer.writerow(
                {
                    "current_path": e["current_path"],
                    "suggested_topic": e["suggested_topic"],
                    "proposed_path": e["proposed_path"],
                    "is_duplicate_of": e["is_duplicate_of"],
                    "size_bytes": e["size_bytes"],
                    "pages": e["pages"],
                    "title": e["title"],
                    "author": e["author"],
                }
            )

    print(f"\nReport written to:")
    print(f"  {REPORT_JSON}")
    print(f"  {REPORT_CSV}")
    print(f"\nFound {len(duplicates)} duplicate files.")
    print("Review the CSV, adjust TOPIC_KEYWORDS if needed, then run a move script.")


if __name__ == "__main__":
    main()
