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
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in HARD_NON_MATH]


def is_non_math_title(title):
    """Return the pattern that matched, or None."""
    if not title:
        return None
    for pat in _COMPILED:
        if pat.search(title):
            return pat.pattern
    return None
