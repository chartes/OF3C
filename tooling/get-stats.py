# Create stats for README.md
import glob
import tabulate
from typing import Iterable, Dict

print("\n## Token, Lemma and POS counts\n")


def read_csv(filepath: str) -> Iterable[Dict[str, str]]:
    with open(filepath) as f:
        for idx, line in enumerate(f.readlines()):
            if idx == 0:
                header = line.strip().split("\t")
                continue
            elif not line.strip():
                continue
            line = dict(zip(header, line.strip().split("\t")))
            yield line
    return None


from collections import Counter, defaultdict

stats = defaultdict(Counter)

for file in glob.glob("output-lemma-pos/*.tsv"):
    for line in read_csv(file):
        if not line:
            continue
        for key, value in line.items():
            stats[key][value] += 1

count_table = [
    ["Category", "Different", "Total", "Values with 1 occurrence only"]
]

for key, label in (("token", "Forms"), ("lemma", "Lemma"), ("POS", "POS")):
    count_table.append([label, f"{len(stats[key]):,}", f"{sum(stats[key].values()):,}", f"{list(stats[key].values()).count(1):,}"])

count_table = tabulate.tabulate(count_table, headers="firstrow", tablefmt="github")

print(count_table)

# Morphology

stats2 = defaultdict(Counter)

for file in glob.glob("output-morph/*.tsv"):
    for line in read_csv(file):
        if not line:
            continue
        for key, value in line.items():
            stats2[key][value] += 1

morph_table = [
    ["Category", "Different", "Total", "Non-x values"]
]


for key, label in (
    ('MODE', 'Mode'),
    ('TEMPS', 'Temps'),
    ('PERS', 'Personne'),
    ('NOMB', 'Nombre'),
    ('GENRE', 'Genre'),
    ('CAS', 'Cas'),
    ('DEGRE', 'Degre'),
    #('SPEC', 'Spec?')
):
    morph_table.append([label, f"{len(stats2[key]):,}", f"{sum(stats2[key].values()):,}", f"{sum(stats2[key].values())-(stats2[key][key+'=x']+stats2[key][key+'.=x']):,}"])

morph_table = tabulate.tabulate(morph_table, headers="firstrow", tablefmt="github")

print("\n## Morphology counts\n")
print("*Non-x* values means that the category actually applied to the token: a verb will have a DEGRE annotation of x, because verb can't have DEGRE.\n")

print(morph_table)

for key, label in [
    ("POS", "POS"),
    ('MODE', 'Mode'),
    ('TEMPS', 'Temps'),
    ('PERS', 'Personne'),
    ('NOMB', 'Nombre'),
    ('GENRE', 'Genre'),
    ('CAS', 'Cas'),
    ('DEGRE', 'Degre'),]:
    print(f"\n ## {label}\n")

    s = stats2
    if key == "POS":
        s = stats

    print(tabulate.tabulate([(x, f"{y:,}") for x, y in s[key].most_common()], headers=["Value", "Count"], tablefmt="github"))