# =============================================================================
# A/B Test Design and Statistical Analysis
# =============================================================================
# What this project does:
#   - Demonstrates the full lifecycle of a real A/B experiment:
#       1. Define hypothesis and success metric
#       2. Calculate required sample size (power analysis)
#       3. Simulate running the experiment
#       4. Analyze results with statistical significance testing
#       5. Produce a clean, shareable results readout
#
# Experiment scenario:
#   We are testing a new onboarding flow (Variant B) vs. the current flow
#   (Control A) to see if it improves the 7-day activation rate.
#   Hypothesis: Variant B will increase activation rate from 38% to 44%.
#
# Why this matters for product analytics roles:
#   A/B testing is listed explicitly in the job description. Being able to
#   design tests correctly (not just analyze results) is what separates
#   mid-level analysts from senior ones.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy import stats
from scipy.stats import norm
import os

np.random.seed(99)
os.makedirs("outputs", exist_ok=True)

print("=" * 60)
print("PROJECT 2: A/B Test Design and Statistical Analysis")
print("=" * 60)


# -----------------------------------------------------------------------------
# STEP 1: Define the experiment parameters
# -----------------------------------------------------------------------------

EXPERIMENT_NAME      = "Onboarding Flow Redesign"
SUCCESS_METRIC       = "7-Day Activation Rate"
BASELINE_RATE        = 0.38   # Current activation rate (Control)
EXPECTED_LIFT        = 0.06   # We expect +6 percentage points
TARGET_RATE          = BASELINE_RATE + EXPECTED_LIFT
SIGNIFICANCE_LEVEL   = 0.05   # Alpha: 5% false positive rate
STATISTICAL_POWER    = 0.80   # 80% chance of detecting a real effect

print(f"\nExperiment:       {EXPERIMENT_NAME}")
print(f"Metric:           {SUCCESS_METRIC}")
print(f"Control rate:     {BASELINE_RATE:.0%}")
print(f"Target rate:      {TARGET_RATE:.0%}  (expected lift: +{EXPECTED_LIFT:.0%})")
print(f"Alpha (sig lvl):  {SIGNIFICANCE_LEVEL}")
print(f"Power:            {STATISTICAL_POWER:.0%}")


# -----------------------------------------------------------------------------
# STEP 2: Power analysis - how many users do we need?
# -----------------------------------------------------------------------------
# This is critical: running a test without enough users is one of the most
# common mistakes in experimentation. The formula below calculates the minimum
# sample size needed per variant.

def calculate_sample_size(p_control, p_treatment, alpha=0.05, power=0.80):
    """
    Calculate required sample size per variant for a two-proportion z-test.

    Parameters:
        p_control   : baseline conversion rate
        p_treatment : expected conversion rate in treatment
        alpha       : significance level (probability of false positive)
        power       : statistical power (probability of detecting real effect)

    Returns:
        Minimum sample size needed per variant (integer)
    """
    # z-scores for alpha/2 (two-tailed) and power
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)

    # Pooled proportion under null hypothesis
    p_pooled = (p_control + p_treatment) / 2

    # Standard error under null (for significance threshold)
    se_null      = np.sqrt(2 * p_pooled * (1 - p_pooled))
    # Standard error under alternative (for power)
    se_alt       = np.sqrt(p_control * (1 - p_control) + p_treatment * (1 - p_treatment))

    effect_size  = abs(p_treatment - p_control)
    n            = ((z_alpha * se_null + z_power * se_alt) / effect_size) ** 2

    return int(np.ceil(n))

required_n = calculate_sample_size(BASELINE_RATE, TARGET_RATE, SIGNIFICANCE_LEVEL, STATISTICAL_POWER)
total_users = required_n * 2

print(f"\n--- POWER ANALYSIS RESULTS ---")
print(f"Required users per variant:  {required_n:,}")
print(f"Total users needed:          {total_users:,}")
print(f"\nAt 500 new signups/day, runtime = {total_users/500:.1f} days "
      f"({total_users/500/7:.1f} weeks)")


# -----------------------------------------------------------------------------
# STEP 3: Simulate the experiment results
# -----------------------------------------------------------------------------
# We simulate slightly better than expected results for Variant B to make
# the analysis interesting.

ACTUAL_CONTROL_RATE   = 0.381  # Very close to baseline (stable)
ACTUAL_TREATMENT_RATE = 0.447  # Slightly above target

control_users   = required_n + 120   # Slight imbalance is realistic
treatment_users = required_n + 95

# Simulate individual user outcomes (1 = activated, 0 = did not)
control_outcomes   = np.random.binomial(1, ACTUAL_CONTROL_RATE,   control_users)
treatment_outcomes = np.random.binomial(1, ACTUAL_TREATMENT_RATE, treatment_users)

control_conversions   = control_outcomes.sum()
treatment_conversions = treatment_outcomes.sum()
control_rate_obs      = control_conversions   / control_users
treatment_rate_obs    = treatment_conversions / treatment_users
observed_lift         = treatment_rate_obs - control_rate_obs
relative_lift         = observed_lift / control_rate_obs * 100

print(f"\n--- EXPERIMENT RESULTS ---")
print(f"\n{'Metric':<35} {'Control (A)':>14} {'Treatment (B)':>14}")
print("-" * 65)
print(f"{'Users in variant':<35} {control_users:>14,} {treatment_users:>14,}")
print(f"{'Activated users':<35} {control_conversions:>14,} {treatment_conversions:>14,}")
print(f"{'Observed activation rate':<35} {control_rate_obs:>14.2%} {treatment_rate_obs:>14.2%}")
print(f"{'Absolute lift':<35} {'':>14} {observed_lift:>+14.2%}")
print(f"{'Relative lift':<35} {'':>14} {relative_lift:>+13.1f}%")


# -----------------------------------------------------------------------------
# STEP 4: Statistical significance test (two-proportion z-test)
# -----------------------------------------------------------------------------

p_pooled_obs = (treatment_conversions + control_conversions) / (treatment_users + control_users)
se_pooled    = np.sqrt(p_pooled_obs * (1 - p_pooled_obs) * (1/treatment_users + 1/control_users))
z_stat       = (treatment_rate_obs - control_rate_obs) / se_pooled
p_value      = 1 - norm.cdf(z_stat)   # one-tailed (testing B > A)

significant = p_value < SIGNIFICANCE_LEVEL

print(f"\n--- STATISTICAL TEST ---")
print(f"Test type:        Two-proportion z-test (one-tailed)")
print(f"Z-statistic:      {z_stat:.4f}")
print(f"P-value:          {p_value:.4f}")
print(f"Significant:      {'YES' if significant else 'NO'} (alpha = {SIGNIFICANCE_LEVEL})")

# Confidence interval for the lift
se = np.sqrt(control_rate_obs * (1 - control_rate_obs) / control_users +
             treatment_rate_obs * (1 - treatment_rate_obs) / treatment_users)
z_ci = stats.norm.ppf(0.975)
ci_lower = observed_lift - z_ci * se
ci_upper = observed_lift + z_ci * se

print(f"95% CI for lift:  [{ci_lower:+.2%},  {ci_upper:+.2%}]")


# -----------------------------------------------------------------------------
# STEP 5: Visualizations
# -----------------------------------------------------------------------------

# Chart A: Conversion rates comparison
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

# Bar chart: control vs treatment
colors    = ["#A8C8F0", "#2563A8"]
variants  = ["Control A\n(Current Onboarding)", "Variant B\n(New Onboarding)"]
rates     = [control_rate_obs * 100, treatment_rate_obs * 100]
bars      = axes[0].bar(variants, rates, color=colors, width=0.45, edgecolor="white", linewidth=1.5)

for bar, rate in zip(bars, rates):
    axes[0].text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                 f"{rate:.2f}%", ha="center", va="bottom", fontsize=13, fontweight="bold")

axes[0].set_ylim(0, max(rates) * 1.2)
axes[0].set_ylabel("7-Day Activation Rate (%)", fontsize=11)
axes[0].set_title("A/B Test: Activation Rate by Variant", fontsize=13, fontweight="bold")
axes[0].spines["top"].set_visible(False)
axes[0].spines["right"].set_visible(False)

sig_text = f"p = {p_value:.4f}  {'(Statistically Significant)' if significant else '(Not Significant)'}"
axes[0].text(0.5, 0.92, sig_text, ha="center", transform=axes[0].transAxes,
             fontsize=9, color="#2563A8" if significant else "#CC4444",
             bbox=dict(boxstyle="round,pad=0.3", facecolor="#EEF2F8", edgecolor="#2563A8", alpha=0.8))

# Chart B: Lift with confidence interval
axes[1].axhline(0, color="#999999", linewidth=1.2, linestyle="--")
axes[1].errorbar(["Observed Lift"], [observed_lift * 100],
                 yerr=[[( observed_lift - ci_lower) * 100],
                        [(ci_upper  - observed_lift) * 100]],
                 fmt="o", color="#2563A8", markersize=10, capsize=8,
                 capthick=2, linewidth=2.5)
axes[1].axhline(EXPECTED_LIFT * 100, color="#E05C2A", linewidth=1.5,
                linestyle=":", label=f"Expected lift: +{EXPECTED_LIFT:.0%}")
axes[1].set_ylabel("Lift in Activation Rate (percentage points)", fontsize=11)
axes[1].set_title("Observed Lift with 95% Confidence Interval", fontsize=13, fontweight="bold")
axes[1].legend(fontsize=10)
axes[1].spines["top"].set_visible(False)
axes[1].spines["right"].set_visible(False)

plt.suptitle(f"Experiment: {EXPERIMENT_NAME}", fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("outputs/04_ab_test_results.png", dpi=150, bbox_inches="tight")
plt.close()
print("\nChart saved: outputs/04_ab_test_results.png")


# -----------------------------------------------------------------------------
# STEP 6: Final decision readout (executive summary)
# -----------------------------------------------------------------------------

print("\n" + "=" * 60)
print("EXPERIMENT READOUT SUMMARY")
print("=" * 60)
print(f"Experiment:    {EXPERIMENT_NAME}")
print(f"Metric:        {SUCCESS_METRIC}")
print(f"Duration:      Completed at {total_users:,} total users")
print(f"Result:        {'SHIP IT - Variant B wins' if significant else 'DO NOT SHIP - No significant effect'}")
print(f"Observed lift: {observed_lift:+.2%} (relative: +{relative_lift:.1f}%)")
print(f"Confidence:    95% CI [{ci_lower:+.2%}, {ci_upper:+.2%}]")
print(f"P-value:       {p_value:.4f}")

if significant:
    print(f"\nRecommendation: Roll out Variant B to 100% of users.")
    print(f"Estimated impact: If {total_users:,} users/month see this flow,")
    print(f"  expect approximately {int(observed_lift * total_users):,} additional")
    print(f"  activations per month.")
else:
    print(f"\nRecommendation: Do not ship. Investigate further.")

print("=" * 60)
