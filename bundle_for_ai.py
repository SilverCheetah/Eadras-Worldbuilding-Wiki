#!/usr/bin/env python3
"""Bundle the Eadras wiki into 20 topical documents for AI ingestion.

Outputs: generated/01-foundations.md ... generated/20-artifacts-antagonists-rpg.md

Exclusions:
- wiki/_sealed/*   (OOC plot-spine secrets; sealed-folder rule)
- wiki/log.md      (634KB operational change log; not canon)
- wiki/templates/* (Templater syntax templates; not canon)

Includes wiki/index.md in bucket 01 (useful as a master TOC for ingesting AIs).

Each bundle has:
- A header (bundle number, title, mini-TOC, file count)
- Each source page concatenated with a clear filename separator
- Frontmatter preserved
- Original wikilinks intact
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
WIKI = ROOT / "wiki"
OUT = ROOT / "generated"

# Files to exclude entirely from any bundle.
EXCLUDE_RELATIVE = {
    "log.md",  # 634KB append-only operational log
}
EXCLUDE_DIRS = {
    "_sealed",   # OOC plot-spine secrets
    "templates", # Templater syntax stubs
}

# Bucket plan. Each bucket: (slug, human-readable title, [list of wiki-relative paths]).
# Files appear here exactly once across all buckets; the script validates this.
BUCKETS = [
    (
        "foundations-and-meta",
        "Foundations & Meta",
        [
            "index.md",
            "system-governance.md",
            "tags.md",
            "naming-conventions.md",
            "calendar.md",
            "principles-of-eadras.md",
            "modernity.md",
            "open-questions.md",
            "worldbuilding-needs.md",
            "inspirations.md",
        ],
    ),
    (
        "omniverse-cosmology",
        "Omniverse Cosmology",
        [
            "omniverse.md",
            "mythos.md",
            "eadras-cosmology.md",
            "concordance.md",
            "nexus.md",
            "bastion-of-light.md",
            "omniversal-creator.md",
            "omniversal-laws.md",
            "axes-of-creation.md",
            "chaos.md",
            "aberrations.md",
            "neverborn.md",
            "observer-and-naming.md",
            "night-sky-cosmology.md",
            "planewalkers.md",
            "voroik.md",
            "archons.md",
            "dao.md",
        ],
    ),
    (
        "planes-moons-exile-realms",
        "Planes of Eadras, Moons, Exile Realms",
        [
            "spirits.md",
            "back-rooms.md",
            "celestia.md",
            "seraphim.md",
            "nyxar.md",
            "devils.md",
            "feywild.md",
            "shadowdark.md",
            "limina.md",
            "solarion.md",
            "dreadharrow.md",
            "four-moons-of-eadras.md",
            "gaia.md",
            "veyr-keth.md",
            "firethorn-hold.md",
        ],
    ),
    (
        "creator-deities-elder-gods",
        "Creator Deities, Elder Gods, The Three",
        [
            "primordial-duo.md",
            "creation-myth.md",
            "gods-of-eadras.md",
            "ioa.md",
            "nara.md",
            "raja.md",
            "vos.md",
            "qoxli.md",
            "daj.md",
            "sylph.md",
            "nox.md",
            "lirra.md",
            "shali.md",
            "shani.md",
            "the-three.md",
        ],
    ),
    (
        "ascended-mortal-gods-divine-constructs",
        "Ascended Mortal Gods & Divine Constructs",
        [
            "aramet.md",
            "ixthal.md",
            "three-last-lights.md",
            "nine-embers-of-renewal.md",
            "inki.md",
            "din-shadar.md",
            "baldaran.md",
            "imma.md",
            "velveth.md",
            "apotheosis.md",
            "icons.md",
            "the-long-quiet.md",
            "hall-of-the-long-quiet.md",
            "divine-concordat.md",
            "divine-containment-protocols.md",
        ],
    ),
    (
        "doctrine-bureaucracy-religion",
        "Doctrine, Divine Bureaucracies, Religion",
        [
            "doctrine-of-unheld-hand.md",
            "doctrine-of-open-palm.md",
            "three-bells-of-intervention.md",
            "hearth-witness-mandate.md",
            "petition-of-abandoned-circumstance.md",
            "decree-of-shali-shani-ioa.md",
            "divine-bureaucracy.md",
            "infernal-bureaucracy.md",
            "religion-in-eadras.md",
            "baldaranic-council-cycle.md",
        ],
    ),
    (
        "timeline-cataclysm-era",
        "Timeline, Cataclysm Era, Pre-Cataclysm World",
        [
            "eadras-timeline.md",
            "eadras-tectonic-history.md",
            "pre-cataclysm-relics.md",
            "arathi-cataclysm.md",
            "worldbreaker-mechanism.md",
            "worldbreaker-scar.md",
            "post-cataclysm-fauna.md",
            "chaos-crusades.md",
            "altea.md",
            "altean-highlands.md",
        ],
    ),
    (
        "arathi-civilization-vaults",
        "Arathi Civilization, Vaults, Lost Primer",
        [
            "arathi.md",
            "arathi-servitors.md",
            "arathi-geo-substrate.md",
            "arathi-golden-age-map.md",
            "kudur-etir.md",
            "lost-primer.md",
            "deep-vaults.md",
            "vault-concordat.md",
            "unsealing-oath.md",
            "obsidian-sanctum.md",
            "fallback-doctrine.md",
            "absence-traditions.md",
        ],
    ),
    (
        "dragons-unicorns-demons",
        "Dragons, Unicorns, Demons",
        [
            "dragons.md",
            "ratharil.md",
            "great-exchange.md",
            "unicorns.md",
            "unicorn-plains.md",
            "herd-listeners.md",
            "unicorn-wound-keeping.md",
            "circling-of-the-returned.md",
            "demons.md",
            "demon-prince-of-the-open-wound.md",
        ],
    ),
    (
        "firethorn-demon-war-banishment",
        "Firethorn Era, Demon War, Banishment, Unreceived",
        [
            "firethorn-empire.md",
            "demon-war.md",
            "battle-of-the-broken-conclaves.md",
            "three-who-stood.md",
            "three-thirds-of-the-rathar.md",
            "great-betrayal.md",
            "great-banishment.md",
            "tomb-of-the-last-guardians.md",
            "demonfall-marches.md",
            "woundwatch.md",
            "unreceived.md",
            "ledger-wall.md",
        ],
    ),
    (
        "crusade-era-modern-foundations",
        "Anti-Magic Crusade Era & Modern Foundations",
        [
            "anti-magic-crusade.md",
            "century-of-sorrows.md",
            "knights-of-lirra.md",
            "thousand-year-dimming.md",
            "lost-zenith.md",
            "grand-conjunction.md",
            "eras.md",
            "first-rebrightening.md",
            "mythic-recitations.md",
        ],
    ),
    (
        "progenitor-and-engineered-races",
        "Progenitor & Engineered Races",
        [
            "peoples-of-eadras.md",
            "elfen.md",
            "velrathi.md",
            "tarans.md",
            "rathari.md",
            "orugi.md",
            "grugi.md",
            "el-mer.md",
            "sea-tua.md",
            "aetherins.md",
            "mitans.md",
            "titans.md",
            "trolls.md",
        ],
    ),
    (
        "modern-humanoid-races-beastfolk-katharim",
        "Modern Humanoid Races, Beast-folk, Katharim",
        [
            "humans.md",
            "elves.md",
            "dwarves.md",
            "gnomes.md",
            "goblins.md",
            "halflings.md",
            "orcs.md",
            "beast-folk.md",
            "katharim.md",
            "kharathen.md",
        ],
    ),
    (
        "modern-fae-oceanic-dragonfolk-other-races",
        "Modern Fae, Oceanic, Dragonfolk, Other Races",
        [
            "fae.md",
            "centaurs.md",
            "goliath.md",
            "merfolk.md",
            "merrow.md",
            "sirens.md",
            "shimmercloaks.md",
            "ink-lords.md",
            "tideclad.md",
            "kuo-toa.md",
            "sahuagin.md",
            "golems.md",
            "dragonfolk.md",
            "dragonborn.md",
            "kobolds.md",
            "lizardfolk.md",
            "snakefolk.md",
            "turkorcs.md",
        ],
    ),
    (
        "culture-food-drink-bathing",
        "Cultural Layer: Food, Drink, Bathing, Ethics",
        [
            "food-and-drink.md",
            "pre-empire-foodways.md",
            "aqua-vitae.md",
            "elfen-blossom-wines.md",
            "velrathi-tea-culture.md",
            "velrathi-cognitive-frogs.md",
            "goblin-ancestor-liquor.md",
            "orcish-drinks.md",
            "taran-venom-aged-liquor.md",
            "orden-whale-honey-mead.md",
            "tchoukou.md",
            "goblin-tunnel-cheese.md",
            "bathing-customs.md",
            "philosophy-of-contribution.md",
            "flyting.md",
            "three-cultures-ethical-triangle.md",
        ],
    ),
    (
        "architecture-and-modern-polities-i",
        "Architecture & Modern Polities I (Amunorians, Bold, Orden, Azure)",
        [
            "velrathi-architecture.md",
            "taran-architecture.md",
            "elfen-architecture.md",
            "amunorians.md",
            "bold.md",
            "orden.md",
            "azure-basin.md",
            "conduit-cities.md",
            "oldest-continuous-settlements.md",
            "house-sitharis.md",
            "clan-nightshade.md",
            "harvey-wash.md",
            "verdant-scar.md",
        ],
    ),
    (
        "modern-polities-ii-frontier",
        "Modern Polities II & Frontier (Dragon Empire, Tariq, Gray Matriarchy, Fae-da'Nar)",
        [
            "dragon-empire.md",
            "tariq-al-honor.md",
            "gray-matriarchy.md",
            "she-who-shall-not-be-named.md",
            "thorn-sanctum.md",
            "fae-da-nar.md",
            "four-laws-of-fae-da-nar.md",
            "the-shunned.md",
            "frontier-hospitality.md",
            "threshold-cities.md",
            "kingdom-of-xanar.md",
            "flesh-eaters.md",
        ],
    ),
    (
        "continents-and-major-places",
        "Continents & Major Places",
        [
            "arathalassic-sea.md",
            "arathyn.md",
            "eldravath.md",
            "avalon.md",
            "damedes.md",
            "culethor.md",
            "therion.md",
            "aurettos.md",
            "varkhul.md",
            "continental-ward.md",
        ],
    ),
    (
        "magic-system-orders-languages",
        "Magic System, Magical Orders, Languages",
        [
            "magic-in-eadras.md",
            "eldritch.md",
            "eldritch-cycle.md",
            "seven-conduits.md",
            "source-surges.md",
            "true-language.md",
            "draconic-language.md",
            "pillar-magic.md",
            "wizards.md",
            "priests.md",
            "lexanari.md",
            "netharim.md",
            "druids.md",
            "windspeakers.md",
            "order-sharanel.md",
            "order-sworn-netharim.md",
            "dashar.md",
            "heart-of-the-goddess.md",
            "weavespinners.md",
            "crystalmancy.md",
            "magitek.md",
            "mana-metals.md",
            "necromancy-and-undeath.md",
        ],
    ),
    (
        "artifacts-antagonists-rpg-protocols",
        "Artifacts, Antagonists, Characters, RPG, Protocols",
        [
            "runeswords.md",
            "spear-of-crystallized-entropy.md",
            "worldender.md",
            "worldender-crystal.md",
            "firethorn-throne.md",
            "hall-of-kings.md",
            "tome-of-baldaran.md",
            "alien-objects.md",
            "goldenwood.md",
            "xarvion.md",
            "velena.md",
            "black-hand.md",
            "white-palm.md",
            "rpg/README.md",
            "rpg/closed-time-bubble.md",
            "rpg/wizard-mechanics.md",
            "rpg/priest-mechanics.md",
            "rpg/pillar-magic-mechanics.md",
            "protocols/README.md",
            "protocols/race-deepening-protocol.md",
            "protocols/core-canon-and-thematic-principles.md",
        ],
    ),
]

# ============================================================================
# Validation: every wiki page must appear in exactly one bucket (or be excluded)
# ============================================================================

def discover_wiki_files() -> set[str]:
    """All wiki .md files, relative to wiki/, with forward slashes."""
    files: set[str] = set()
    for path in WIKI.rglob("*.md"):
        rel = path.relative_to(WIKI).as_posix()
        if rel in EXCLUDE_RELATIVE:
            continue
        if any(part in EXCLUDE_DIRS for part in path.relative_to(WIKI).parts):
            continue
        files.add(rel)
    return files


def validate_buckets() -> tuple[set[str], set[str], set[str]]:
    """Return (all_bucketed, missing_from_buckets, duplicated_in_buckets)."""
    discovered = discover_wiki_files()
    seen: dict[str, int] = {}
    for _slug, _title, files in BUCKETS:
        for f in files:
            seen[f] = seen.get(f, 0) + 1
    bucketed = set(seen.keys())
    missing = discovered - bucketed
    extra = bucketed - discovered
    duplicates = {f for f, n in seen.items() if n > 1}
    return discovered, missing | extra, duplicates


def write_bundle(idx: int, slug: str, title: str, files: list[str]) -> Path:
    """Write one bundle file. Returns its path."""
    out_path = OUT / f"{idx:02d}-{slug}.md"
    lines: list[str] = []

    # Header
    lines.append(f"# Eadras Wiki Bundle {idx:02d} of 20 — {title}")
    lines.append("")
    lines.append(
        f"**Scope**: {len(files)} wiki page(s) on the topic of *{title}*. "
        f"Concatenated for AI ingestion; original frontmatter and wikilinks preserved. "
        f"Source-of-truth remains the individual pages under `wiki/`."
    )
    lines.append("")
    lines.append("**Contents**:")
    lines.append("")
    for f in files:
        lines.append(f"- `wiki/{f}`")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Body: each page with a clear separator
    for f in files:
        src = WIKI / f
        if not src.exists():
            raise FileNotFoundError(f"Listed in bucket {idx:02d} but not found on disk: wiki/{f}")
        body = src.read_text(encoding="utf-8")
        lines.append("")
        lines.append(f"<!-- ============================================================ -->")
        lines.append(f"<!-- SOURCE: wiki/{f}                                              -->")
        lines.append(f"<!-- ============================================================ -->")
        lines.append("")
        lines.append(body.rstrip())
        lines.append("")
        lines.append("")

    OUT.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path


def main() -> int:
    if not WIKI.exists():
        print(f"FATAL: wiki/ not found at {WIKI}", file=sys.stderr)
        return 2
    if len(BUCKETS) != 20:
        print(f"FATAL: bucket plan has {len(BUCKETS)} entries; needs exactly 20", file=sys.stderr)
        return 2

    discovered, mismatched, duplicates = validate_buckets()
    if mismatched or duplicates:
        # Report and abort — do not write partial output.
        if mismatched:
            print("FATAL: bucket plan does not equal discovered wiki file set.", file=sys.stderr)
            seen = {f for _s, _t, fs in BUCKETS for f in fs}
            missing = sorted(discovered - seen)
            extra = sorted(seen - discovered)
            if missing:
                print(f"  Missing from buckets ({len(missing)}):", file=sys.stderr)
                for f in missing:
                    print(f"    - {f}", file=sys.stderr)
            if extra:
                print(f"  Listed in buckets but not on disk ({len(extra)}):", file=sys.stderr)
                for f in extra:
                    print(f"    - {f}", file=sys.stderr)
        if duplicates:
            print(f"FATAL: pages duplicated across buckets ({len(duplicates)}):", file=sys.stderr)
            for f in sorted(duplicates):
                print(f"    - {f}", file=sys.stderr)
        return 1

    print(f"Validation OK: {len(discovered)} wiki pages mapped into 20 buckets.")
    print(f"Excluded: wiki/log.md, wiki/_sealed/*, wiki/templates/*")
    print()

    total_bytes = 0
    for i, (slug, title, files) in enumerate(BUCKETS, start=1):
        path = write_bundle(i, slug, title, files)
        size = path.stat().st_size
        total_bytes += size
        print(f"  {path.name}  ({len(files):>2} pages, {size:>10,} bytes)")

    print()
    print(f"Wrote 20 bundles to {OUT}/, total {total_bytes:,} bytes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
