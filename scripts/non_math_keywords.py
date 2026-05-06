"""SSOT for non-math topic keyword detection.

Both `lint-data.py` (warns/blocks adding such papers) and
`eject-non-math-publications.py` (cleans existing yaml) MUST import from
here. Otherwise the two diverge and a paper passes one check but not the
other.

Rule of thumb for adding a new keyword:
  - It must be a phrase that NO mathematician would have in a paper title.
  - Use \b word boundaries so 'rna' doesn't match 'Inte-rna-tional'.
  - When uncertain, write the bigram (e.g. 'gas sensor', 'bone drill') —
    single common words are a footgun.

Two layers of detection:
  1. HARD_NON_MATH (title regexes) — block papers with obvious non-math
     phrases anywhere in the title.
  2. NON_MATH_VENUES (journal substring) — block papers published in
     journals that don't publish pure / theoretical math content. Uses
     case-insensitive substring on the journal name.
"""
import re

HARD_NON_MATH = [
    # Materials & nano
    r'\bgraphene\b', r'\bnanocomposite\b', r'\bperovskite\b',
    r'\blithium battery\b', r'\bsolar cell\b', r'\bfuel cell\b',
    r'\belectromagnetic shielding\b',
    r'\belectromagnetic interference shielding\b',
    r'\bantibacterial\b', r'\bcatalyst\b', r'\bmetal[- ]organic framework\b',
    r'\bwater splitting\b', r'\bphotovoltaic\b',
    r'\bnanocrystal\b', r'\bquantum dot device\b',
    r'\bdielectric (response|loss|spectroscopy)\b',
    r'\bferroelectric (film|device)\b',
    r'\bnano[- ](structured|particle|material)\b',
    r'\bgas sensor\b', r'\bhydrogen (absorption|storage)\b',
    r'\b(NO2|H2S|NH3|CO2|VOC) (detection|sensing)\b',
    r'\belectrochemical (feature|stability|cycling|propert)\b',
    r'\b(MXene|Ti3C2|SnO2|TiO2|MOF[- ]derived)\b',
    r'\bphase structure\b', r'\bcycl(ing|e) stability\b',
    r'\b(blue|red|green)[- ]emitting\b',
    r'\bdoped\s+(Cs\d|Rb\d|Pb\d)\b',
    # Bio / med
    r'\bbiomaterials?\b', r'\bdrug delivery\b', r'\btissue engineering\b',
    r'\bwearable device\b', r'\bbiomedical (imaging|application)\b',
    r'\bbone (drill|fracture|tumor|defect)\b',
    r'\bspine (surgery|fusion)\b',
    r'\b(tumor|cancer) (treatment|therapy|biopsy|resection)\b',
    r'\bclinical (trial|outcome|practice)\b',
    r'\bpatient (outcome|recovery|cohort)\b',
    r'\bantibody\b', r'\bantimicrobial\b', r'\bvaccine\b',
    r'\bcrystal structure of full length\b',
    r'\b(LC3B|protein) mutant\b',
    # CS / NLP / IR (recommender systems, NOT math optimization)
    r'\brecommender system\b', r'\brecommendation algorithm\b',
    r'\bsentiment analysis\b', r'\bcollaborative filtering\b',
    r'\bnatural language processing\b', r'\bword embedding\b',
    r'\buser response modeling\b', r'\buser profiling\b',
    r'\b(suggestion|review|comment) mining\b',
    r'\bart critic\b', r'\bblending of predictions\b',
    # ML applied to non-math
    r'\bdeep learning (model|approach|method)\b',
    r'\bneural network (training|architecture)\b',
    r'\btransformer (model|architecture) for (text|nlp|recommendation)\b',
    r'\b(graph neural network|gnn)\b',
    r'\bmachine learning (framework|pipeline) for\b',
    r'\bmaterials? (science|characterization|discovery)\b',
    r'\bcrack (propagation|coalescence)\b',
    # Network science / complex systems engineering
    r'\b(structure|structural) controllability of (complex )?network\b',
    r'\bpreferential matching\b',
    r'\bcomplex network\b',
    r'\bsmall[- ]world network\b',
    # Applied / experimental physics & engineering instrumentation
    r'\bneutron[- ](focusing|scattering|imaging|optic)\b',
    r'\bsmall[- ]angle neutron scattering\b',
    r'\bsupermirror (assembly|system)\b',
    r'\bx[- ]ray (tomography|crystallograph|scattering experiment)\b',
    r'\bsynchrotron (radiation|beamline|experiment)\b',
    r'\bcyclotron (beam|experiment)\b',
    r'\b(detector|spectrometer) (assembly|design|calibration)\b',
    r'\b(silicon|GaN|InGaAs) (device|wafer|MOSFET|transistor)\b',
    r'\bplasma (etching|deposition|treatment)\b',
    r'\bMEMS (sensor|device)\b',
    r'\bvibration (control|isolation|damping)\b',
    r'\b(boiler|reactor|turbine) (efficiency|operation|design)\b',
    r'\bfinite element (analysis|simulation) of\b',
    r'\bfluid (flow|dynamics) (simulation|analysis)\b',
    # Experimental nuclear / astroparticle physics (NOT mathematical physics)
    r'\b(transfer|fusion) reaction\b',
    r'\bTrojan Horse (method|approach)\b',
    r'\bnuclear astrophysics\b',
    r'\bnuclear (reaction|structure) studies?\b',
    r'\bradioactive (nuclear )?beam\b',
    r'\b(short-lived|exotic) (neutron-rich )?(isotope|nucle[ius])\b',
    r'\bneutron-rich \d+[A-Z][a-z]?\b',  # e.g. neutron-rich 129Cd
    r'\bdipole radiation in fusion\b',
    r'\bstored (exotic )?(nuclei|ions)\b',
    r'\bmass measurements? of (stored )?(exotic|neutron-rich)\b',
    r'\bnuclear physics (mid term )?plan\b',
    r'\b(cross section|resonance) measurement\b',
    r'\bp\.?\s*\d+(\s*\(γ,\s*[αpn])\b',  # nuclear reaction notation
    r'\bLNGS\b', r'\bLNL\b', r'\bGSI\b', r'\bRIKEN\b',  # nuclear physics labs
    # Nuclear reactions in (n,α) / (α,p) / (p,α) notation — definitively
    # experimental nuclear physics, never mathematical physics
    r'\b\d{1,3}[A-Z][a-z]?\s*\(\s*[αpndt]\s*,\s*[αpndt]\s*\)\b',
    r'\bBig Bang nucleosynthesis\b', r'\bAGB nucleosynthesis\b',
    r'\bstellar nucleosynthesis\b',
    r'\b[Cc]osmological Li[- ]problem\b',
    r'\b(level scheme|shell model description)\b',
    r'\b\d{1,3}[A-Z][a-z]?\s*\+\s*\d{1,3}[A-Z][a-z]?\b',  # 12C+16O nucl notation
    r'\bAGB\s+star',
    # Chemistry experimental
    r'\b(synthesis|preparation) of \w+ (nanoparticles?|nanorods?|nanowires?|nanofibers?|hydrogel)\b',
    r'\bphotoluminescence\b', r'\belectroluminescence\b',
    r'\b(SERS|surface-enhanced Raman)\b',
    # Earth / environmental
    r'\bgroundwater (quality|contamination)\b',
    r'\bremote sensing (image|application|of)\b',
    r'\bclimate (model|simulation) of\b',
    # Agriculture / food
    r'\b(crop|grain) yield\b',
    r'\bpest (control|management)\b',
]

# Journals / venues whose papers should never be in a pure-math researcher's
# yaml. Substring match (case-insensitive) on the `journal` field.
NON_MATH_VENUES = [
    # Engineering / instrumentation
    'nuclear instruments and methods',
    'review of scientific instruments',
    'ieee transactions on',
    'measurement science and technology',
    # Nuclear / particle physics (definitively NOT mathematical physics)
    'physical review c',
    'physical review. c',
    'european physical journal a',
    'european physical journal, a',
    'epj web of conferences',
    'jpscp',  # JPS Conference Proceedings
    'astrophysical journal',  # 99% astronomy/astro-physics, not math-phys
    'nuclear physics a',
    'progress in particle and nuclear physics',
    'few-body systems',
    # Applied physics / materials
    'applied physics letters',
    'physical review applied',
    'physical review materials',
    'advanced materials',
    'acs nano',
    'nano letters',
    'small ',  # journal "Small"
    'angewandte chemie',
    'journal of materials chemistry',
    'chemistry of materials',
    'journal of the american chemical society',
    'jacs au',
    'rsc advances',
    'soft matter',
    'macromolecules',
    'biomacromolecules',
    'nano energy',
    'energy & environmental science',
    'sensors and actuators',
    'journal of the electrochemical society',
    'journal of alloys and compounds',
    'ceramics international',
    'journal of colloid and interface',
    'journal of power sources',
    'international journal of hydrogen energy',
    'journal of physical chemistry',
    # Biomedical
    'nature medicine', 'nature communications biology',
    'plos one', 'plos biology',
    'cell reports', 'cell metabolism',
    'lancet', 'jama',
    'biomaterials', 'biomaterial science',
    'tissue engineering', 'orthopaedics',
    # CS / IR / NLP
    'communications in computer and information science',
    'lecture notes in computer science',  # too broad, but mostly applied
    'ieee access',
    'expert systems with applications',
    # General-interest journals where math papers go to specific issues only
    # — these are NOT auto-rejected; we trust title check instead.
]
# Note: "Nature Communications" appears in BOTH math-physics and materials/bio
# papers. We do NOT blacklist it; rely on title keyword match instead.

_COMPILED = [re.compile(p, re.IGNORECASE) for p in HARD_NON_MATH]


def is_non_math_title(title):
    """Return the pattern that matched, or None."""
    if not title:
        return None
    for pat in _COMPILED:
        if pat.search(title):
            return pat.pattern
    return None


def is_non_math_venue(journal):
    """Return the matched venue substring, or None."""
    if not journal:
        return None
    j = journal.lower()
    for v in NON_MATH_VENUES:
        if v in j:
            return v
    return None


def is_non_math(title=None, journal=None):
    """Combined check. Returns (kind, evidence) or None."""
    t = is_non_math_title(title)
    if t:
        return ('title', t)
    v = is_non_math_venue(journal)
    if v:
        return ('venue', v)
    return None
