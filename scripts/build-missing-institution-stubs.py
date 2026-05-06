"""Create stub institution yamls for slugs referenced in people yaml but
without corresponding files under data/institutions/.

Stubs are minimal — just slug + name + tags so the lint passes. Maintainers
can fill in details (city, country, url) later.
"""
import os
import re
import sys
import yaml
from pathlib import Path

ROOT = Path(__file__).parent.parent
PEOPLE_DIR = ROOT / 'data/people'
INST_DIR = ROOT / 'data/institutions'

# Hand-written name dictionary so the stub is non-trivial.
# Entries: slug → (zh_name, en_name, country, city)
KNOWN = {
    'amss-cas': ('中国科学院数学与系统科学研究院', 'Academy of Mathematics and Systems Science, CAS', 'China', 'Beijing'),
    'bit': ('北京理工大学', 'Beijing Institute of Technology', 'China', 'Beijing'),
    'boston-u': ('波士顿大学', 'Boston University', 'USA', 'Boston'),
    'cmls-polytechnique': ('巴黎综合理工学院数学中心', 'Centre de Mathématiques Laurent Schwartz, École polytechnique', 'France', 'Palaiseau'),
    'college-de-france': ('法兰西公学院', 'Collège de France', 'France', 'Paris'),
    'ens-paris': ('巴黎高等师范学院', 'École Normale Supérieure (Paris)', 'France', 'Paris'),
    'eth-zurich': ('苏黎世联邦理工学院', 'ETH Zürich', 'Switzerland', 'Zurich'),
    'euler-institute': ('欧拉国际数学研究所', 'Euler International Mathematical Institute', 'Russia', 'Saint Petersburg'),
    'genova': ('热那亚大学', 'University of Genoa', 'Italy', 'Genoa'),
    'gottingen': ('哥廷根大学', 'University of Göttingen', 'Germany', 'Göttingen'),
    'henan': ('河南大学', 'Henan University', 'China', 'Kaifeng'),
    'ias': ('普林斯顿高等研究院', 'Institute for Advanced Study (Princeton)', 'USA', 'Princeton'),
    'ibs-cgp': ('IBS 几何与物理中心', 'Center for Geometry and Physics, Institute for Basic Science', 'Korea', 'Pohang'),
    'ictp': ('国际理论物理中心', 'International Centre for Theoretical Physics', 'Italy', 'Trieste'),
    'imj-prg': ('巴黎左岸数学研究所', 'Institut de Mathématiques de Jussieu – Paris Rive Gauche', 'France', 'Paris'),
    'ipmu': ('Kavli IPMU', 'Kavli Institute for the Physics and Mathematics of the Universe', 'Japan', 'Kashiwa'),
    'ist-lisboa': ('里斯本高等理工学院', 'Instituto Superior Técnico (Lisbon)', 'Portugal', 'Lisbon'),
    'jilin-u': ('吉林大学', 'Jilin University', 'China', 'Changchun'),
    'kavli-ipmu': ('Kavli IPMU (东京大学)', 'Kavli IPMU, University of Tokyo', 'Japan', 'Kashiwa'),
    'kias': ('韩国高等研究院', 'Korea Institute for Advanced Study', 'Korea', 'Seoul'),
    'lanzhou-university': ('兰州大学', 'Lanzhou University', 'China', 'Lanzhou'),
    'leningrad-state': ('列宁格勒国立大学（今圣彼得堡国立大学）', 'Leningrad State University (now Saint Petersburg State University)', 'Russia', 'Saint Petersburg'),
    'lgu': ('列宁格勒国立大学', 'Leningrad State University', 'Russia', 'Saint Petersburg'),
    'loughborough': ('拉夫堡大学', 'Loughborough University', 'UK', 'Loughborough'),
    'manchester': ('曼彻斯特大学', 'University of Manchester', 'UK', 'Manchester'),
    'mannheim': ('曼海姆大学', 'University of Mannheim', 'Germany', 'Mannheim'),
    'maryland': ('马里兰大学', 'University of Maryland', 'USA', 'College Park'),
    'michigan-state': ('密歇根州立大学', 'Michigan State University', 'USA', 'East Lansing'),
    'milan': ('米兰大学', 'University of Milan', 'Italy', 'Milan'),
    'minnesota': ('明尼苏达大学', 'University of Minnesota', 'USA', 'Minneapolis'),
    'missouri': ('密苏里大学', 'University of Missouri', 'USA', 'Columbia'),
    'mpi-bonn': ('波恩马普数学所', 'Max Planck Institute for Mathematics, Bonn', 'Germany', 'Bonn'),
    'msri': ('数学科学研究所 (现 SLMath)', 'Mathematical Sciences Research Institute (now SLMath)', 'USA', 'Berkeley'),
    'nanjing': ('南京大学', 'Nanjing University', 'China', 'Nanjing'),
    'nanjing-u': ('南京大学', 'Nanjing University', 'China', 'Nanjing'),
    'northwestern': ('西北大学（美国）', 'Northwestern University', 'USA', 'Evanston'),
    'notre-dame': ('圣母大学', 'University of Notre Dame', 'USA', 'Notre Dame'),
    'ntu': ('国立台湾大学', 'National Taiwan University', 'Taiwan', 'Taipei'),
    'nus': ('新加坡国立大学', 'National University of Singapore', 'Singapore', 'Singapore'),
    'oregon': ('俄勒冈大学', 'University of Oregon', 'USA', 'Eugene'),
    'padova': ('帕多瓦大学', 'University of Padua', 'Italy', 'Padua'),
    'paris-vii': ('巴黎第七大学（今巴黎大学）', 'Paris Diderot University (now Université Paris Cité)', 'France', 'Paris'),
    'princeton': ('普林斯顿大学', 'Princeton University', 'USA', 'Princeton'),
    'qufu-normal': ('曲阜师范大学', 'Qufu Normal University', 'China', 'Qufu'),
    'stanford': ('斯坦福大学', 'Stanford University', 'USA', 'Stanford'),
    'stony-brook': ('石溪大学', 'Stony Brook University', 'USA', 'Stony Brook'),
    'texas-am': ('德州农工大学', 'Texas A&M University', 'USA', 'College Station'),
    'ucberkeley': ('加州大学伯克利分校', 'University of California, Berkeley', 'USA', 'Berkeley'),
    'ucsb': ('加州大学圣塔芭芭拉分校', 'University of California, Santa Barbara', 'USA', 'Santa Barbara'),
    'ucsd': ('加州大学圣地亚哥分校', 'University of California, San Diego', 'USA', 'San Diego'),
    'uiuc': ('伊利诺伊大学香槟分校', 'University of Illinois Urbana-Champaign', 'USA', 'Urbana'),
    'upc-barcelona': ('加泰罗尼亚理工大学', 'Universitat Politècnica de Catalunya', 'Spain', 'Barcelona'),
    'upenn': ('宾夕法尼亚大学', 'University of Pennsylvania', 'USA', 'Philadelphia'),
    'uppsala': ('乌普萨拉大学', 'Uppsala University', 'Sweden', 'Uppsala'),
    'utah': ('犹他大学', 'University of Utah', 'USA', 'Salt Lake City'),
    'utrecht': ('乌得勒支大学', 'Utrecht University', 'Netherlands', 'Utrecht'),
    'wisconsin-madison': ('威斯康星大学麦迪逊分校', 'University of Wisconsin–Madison', 'USA', 'Madison'),
}


def main():
    existing = set()
    for f in INST_DIR.glob('*.yaml'):
        if f.name.startswith('_'):
            continue
        existing.add(f.stem)

    needed = set()
    for f in PEOPLE_DIR.glob('*.yaml'):
        if f.name.startswith('_'):
            continue
        d = yaml.safe_load(f.read_text()) or {}
        for e in (d.get('career_timeline') or []):
            v = e.get('institution')
            if v and isinstance(v, str) and re.match(r'^[a-z][a-z0-9-]*$', v):
                needed.add(v)
    missing = needed - existing

    created = 0
    for slug in sorted(missing):
        meta = KNOWN.get(slug)
        if meta:
            zh, en, country, city = meta
        else:
            # Fallback: title-case slug as English
            en = ' '.join(t.title() for t in slug.split('-'))
            zh = '[待补充]'
            country = '[待补充]'
            city = '[待补充]'
        path = INST_DIR / f'{slug}.yaml'
        path.write_text(
            f"slug: {slug}\n"
            f"name:\n"
            f"  zh: {zh!r}\n"
            f"  en: {en!r}\n"
            f"city: {city}\n"
            f"country: {country}\n"
            f"relevance: low\n"
            f"tags:\n"
            f"  - stub\n"
        )
        created += 1
        print(f'  created {slug}: {zh} / {en}')
    print(f'\nCreated {created} stub institution yamls.')


if __name__ == '__main__':
    main()
