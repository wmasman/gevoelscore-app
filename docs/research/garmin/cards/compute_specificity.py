"""Compute specificity / precision / posterior tables for load-bearing anchors.

Per locked spec at methodology/specificity-tables-spec.md (2026-06-07).
This is a derivative computation over locked result-data.json files; no
new hypothesis test, no new null draws. Reads from result-data.json,
applies Bayes per locked formulas in spec section 3, writes the two
output markdown tables (card-b-train-specificity.md and
card-b2-validate-specificity.md).

Output is deterministic — same inputs always produce same outputs.
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
GARMIN_ROOT = HERE.parent
HYPOTHESES = GARMIN_ROOT / "hypotheses"

OUT_TRAIN = HERE / "card-b-train-specificity.md"
OUT_VALIDATE = HERE / "card-b2-validate-specificity.md"

# Locked era day counts and base rates (spec section 4)
TRAIN_DAYS = 485
VALIDATE_DAYS = 887
TRAIN_CRASHES = 14
VALIDATE_CRASHES = 15
TRAIN_BASE = TRAIN_CRASHES / TRAIN_DAYS
VALIDATE_BASE = VALIDATE_CRASHES / VALIDATE_DAYS

# Card-text implication tiers (spec section 7)
def implication(precision: float, lift: float) -> str:
    if lift >= 5.0 and precision >= 0.30:
        return "Tier A — informative for next-N-day awareness"
    if lift >= 2.0 and 0.05 <= precision < 0.30:
        return "Tier B — slightly elevated; reflective use only, no alerting"
    if lift < 2.0 or precision < 0.05:
        return "Tier C — too broad as forward signal; retrospective annotation only"
    return "Tier B (boundary)"


def bayes(recall: float, null_fire: float, base: float) -> dict:
    precision = (recall * base) / (recall * base + null_fire * (1 - base)) if (recall * base + null_fire * (1 - base)) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    lift = precision / base if base > 0 else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "lift": lift,
    }


# Anchor specifications (locked per spec section 5)
ANCHORS_TRAIN = [
    # (label, result-data path, arm-key, recall-field, null-field, disc-field, magnitude-field, magnitude-label, notes)
    ("H02b train 3d (max contiguous stress >=75 >=5min, delta >=+10 min)",
     "H02b-stress-spikes/result-data.json", "train",
     "crash_pct_at_threshold", "null_pct_at_threshold",
     "discrimination_pp", "median_delta_minutes",
     "median delta (min)",
     "PRIMARY anchor for Card (b) train-era"),

    ("H02d train bridge x 5d (sentinel-corrected spike)",
     "H02d-stress-spikes-uncensored/result-data.json", "bridge__5d/train",
     "crash_pct_at_threshold", "null_pct_at_threshold",
     "discrimination_pp", "median_delta_minutes",
     "median delta (min)",
     "Corroborating: strongest train-era discrimination (+31.8 pp)"),

    ("HA07d train 4d N_std=1.5 bidirectional (sleep stress variability)",
     "HA07d-sleep-stress-variability/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_train",
     "frac_event", "frac_null", "discrimination_pp", "median_magnitude",
     "median |z|",
     "Cross-era anchor: both-eras SUPPORTED + v2 RESCUE"),

    ("HA11 train 4d N_std=1.5 one-sided elevated (U-dip event count)",
     "HA11-stress-udip/result-data.json",
     "4d_primary_Nstd1.5_one_sided_elevated_train",
     "frac_event", "frac_null", "discrimination_pp", "median_magnitude",
     "median signed z",
     "Corroborating: v2 RESCUE Cat 1 canonical decline"),

    ("HA07c train 4d N_std=1.5 one-sided elevated (sleep stress mean delta)",
     "HA07c-sleep-stress-mean-delta/result-data.json",
     "4d_primary_Nstd1.5_one_sided_elevated_train",
     "frac_event", "frac_null", "discrimination_pp", "median_magnitude",
     "median signed z",
     "Corroborating: train SUPPORTED (HRV-proxy)"),

    ("HA08c train 4d N_std=1.5 one-sided elevated (sleep stress slope)",
     "HA08c-sleep-stress-slope/result-data.json",
     "4d_primary_Nstd1.5_one_sided_elevated_train",
     "frac_event", "frac_null", "discrimination_pp", "median_magnitude",
     "median signed z",
     "Corroborating: train SUPPORTED (multi-day creep)"),

    ("HA06b train 4d N_std=1.5 bidirectional (RHR z-score)",
     "HA06b-rhr-zscore/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_train",
     "frac_event", "frac_null", "discrimination_pp", "median_magnitude",
     "median |z|",
     "Reported for completeness; PERMANENTLY DEMOTED by v2 Cat 4 CLOSE (not used for card framing)"),
]

ANCHORS_VALIDATE = [
    ("HA07d validate 4d N_std=1.5 bidirectional (sleep stress variability)",
     "HA07d-sleep-stress-variability/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_validate",
     "frac_event", "frac_null", "discrimination_pp", "median_magnitude",
     "median |z|",
     "PRIMARY anchor for Card (b2) validate-era; project's only overall-SUPPORTED + v2-validated finding"),

    ("HA10 validate 4d N_std=1.5 bidirectional (morning BB peak z)",
     "HA10-bb-overnight-recharge/result-data.json",
     "4d_primary_Nstd1.5_bidirectional_validate",
     "frac_event", "frac_null", "discrimination_pp", "median_abs_z",
     "median |z|",
     "Corroborating: v2 RESCUE Cat 3 rising/late-peak"),
]


def load_arm(rel_path: str, arm_key: str) -> dict:
    p = HYPOTHESES / rel_path
    d = json.loads(p.read_text())
    # Handle nested keys (H02d uses "bridge__5d/train" format with slash)
    if "/" in arm_key:
        parts = arm_key.split("/")
        cur = d
        if "results" in cur:
            cur = cur["results"]
        for part in parts:
            cur = cur[part]
        return cur
    return d[arm_key]


def compute_anchor_row(label: str, rel_path: str, arm_key: str,
                       recall_field: str, null_field: str,
                       disc_field: str, mag_field: str, mag_label: str,
                       notes: str, base_rate: float) -> dict:
    arm = load_arm(rel_path, arm_key)
    recall = arm[recall_field]
    null_fire = arm[null_field]
    disc_pp = arm[disc_field]
    magnitude = arm.get(mag_field)

    b = bayes(recall, null_fire, base_rate)

    # Sensitivity arm: precision at 0.5x and 2x base rate
    half = bayes(recall, null_fire, base_rate * 0.5)
    double = bayes(recall, null_fire, base_rate * 2.0)

    impl = implication(b["precision"], b["lift"])

    return {
        "label": label,
        "notes": notes,
        "recall": recall,
        "null_fire": null_fire,
        "discrimination_pp": disc_pp,
        "magnitude": magnitude,
        "mag_label": mag_label,
        "precision": b["precision"],
        "f1": b["f1"],
        "lift": b["lift"],
        "precision_half_base": half["precision"],
        "precision_double_base": double["precision"],
        "implication": impl,
    }


def render_table(rows: list[dict], base_rate: float, base_label: str,
                 era_label: str, card_label: str, n_days: int,
                 n_crashes: int) -> str:
    lines = []
    lines.append(f"# {card_label} — specificity / precision / posterior tables\n")
    lines.append(f"**Locked 2026-06-07** per [specificity-tables-spec.md](../methodology/specificity-tables-spec.md). "
                 f"Derivative computation over locked result-data.json files. "
                 f"Required output before any card.md is drafted (playbook §2.7 + §6.2).\n")
    lines.append(f"## Era parameters\n")
    lines.append(f"- **Era**: {era_label}")
    lines.append(f"- **Days in window**: {n_days}")
    lines.append(f"- **crash_v1 episodes**: {n_crashes}")
    lines.append(f"- **Base rate** P(crash on any day) = **{base_rate*100:.2f}%**\n")

    lines.append(f"## Main table\n")
    lines.append("| anchor | recall | null_fire | disc (pp) | magnitude | **precision** | **lift** | F1 | implication |")
    lines.append("|---|---:|---:|---:|---|---:|---:|---:|---|")
    for r in rows:
        mag_str = f"{r['magnitude']:.3f} ({r['mag_label']})" if r['magnitude'] is not None else "—"
        lines.append(
            f"| {r['label']} | "
            f"{r['recall']*100:.1f}% | {r['null_fire']*100:.1f}% | "
            f"{r['discrimination_pp']:+.1f} | {mag_str} | "
            f"**{r['precision']*100:.2f}%** | **{r['lift']:.2f}×** | "
            f"{r['f1']:.4f} | {r['implication']} |"
        )

    lines.append("\n## Notes per anchor\n")
    for r in rows:
        lines.append(f"- **{r['label']}**: {r['notes']}")

    lines.append("\n## Base-rate sensitivity\n")
    lines.append("Precision computed at 0.5×, 1×, 2× the locked base rate "
                 "(captures uncertainty about whether the era's crash rate is "
                 "representative).\n")
    lines.append(f"| anchor | precision @ {base_rate*0.5*100:.2f}% | precision @ {base_rate*100:.2f}% (locked) | precision @ {base_rate*2*100:.2f}% |")
    lines.append("|---|---:|---:|---:|")
    for r in rows:
        lines.append(
            f"| {r['label']} | "
            f"{r['precision_half_base']*100:.2f}% | "
            f"**{r['precision']*100:.2f}%** | "
            f"{r['precision_double_base']*100:.2f}% |"
        )

    lines.append("\n## Reading guide\n")
    lines.append("- **recall** = P(card fires | crash on day D) — same as the result.md `frac_event` column")
    lines.append("- **null_fire** = P(card fires | random day D) — same as `frac_null`")
    lines.append("- **precision** = P(crash on day D | card fires on day D) — the Bayes posterior")
    lines.append("- **lift** = precision / base_rate — how much firing multiplies the prior")
    lines.append("- **F1** = 2 · precision · recall / (precision + recall)\n")
    lines.append("Implication tiers per [spec §7](../methodology/specificity-tables-spec.md):")
    lines.append("- **Tier A**: lift ≥ 5× AND precision ≥ 30% — informative for next-N-day awareness")
    lines.append("- **Tier B**: lift 2-5× AND precision 5-30% — reflective use only, no alerting")
    lines.append("- **Tier C**: lift < 2× OR precision < 5% — retrospective annotation only\n")
    lines.append(f"Tier C is the playbook §6.6 no-go boundary: no crash-risk %, traffic lights, "
                 f"push notifications, or automated targets regardless of recall/discrimination magnitude.")
    return "\n".join(lines)


def main():
    print(f"Locked base rates:")
    print(f"  train:    {TRAIN_CRASHES} crashes / {TRAIN_DAYS} days = {TRAIN_BASE*100:.2f}%")
    print(f"  validate: {VALIDATE_CRASHES} crashes / {VALIDATE_DAYS} days = {VALIDATE_BASE*100:.2f}%")
    print()

    train_rows = [compute_anchor_row(*a, TRAIN_BASE) for a in ANCHORS_TRAIN]
    validate_rows = [compute_anchor_row(*a, VALIDATE_BASE) for a in ANCHORS_VALIDATE]

    train_md = render_table(
        train_rows, TRAIN_BASE, "train (2022-09-03 to 2023-12-31)",
        "train (pre-cliff era)", "Card (b) — train-era retrospective per-crash",
        TRAIN_DAYS, TRAIN_CRASHES,
    )
    OUT_TRAIN.write_text(train_md, encoding="utf-8")
    print(f"Wrote {OUT_TRAIN}")

    validate_md = render_table(
        validate_rows, VALIDATE_BASE, "validate (2024-01-01 to 2026-06-05)",
        "validate (post-cliff era)", "Card (b2) — validate-era retrospective per-crash",
        VALIDATE_DAYS, VALIDATE_CRASHES,
    )
    OUT_VALIDATE.write_text(validate_md, encoding="utf-8")
    print(f"Wrote {OUT_VALIDATE}")

    print()
    print("=== TRAIN summary ===")
    for r in train_rows:
        print(f"  {r['label'][:60]:60} precision={r['precision']*100:5.2f}%  lift={r['lift']:4.2f}x  {r['implication']}")
    print()
    print("=== VALIDATE summary ===")
    for r in validate_rows:
        print(f"  {r['label'][:60]:60} precision={r['precision']*100:5.2f}%  lift={r['lift']:4.2f}x  {r['implication']}")


if __name__ == "__main__":
    main()
