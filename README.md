🧪 A/B Test Design & Statistical Analysis (Python)
🎯Project Overview
---
A Python project demonstrating the complete lifecycle of a product A/B experiment — from writing the hypothesis and calculating required sample size through running the test, analyzing results with statistical significance testing, and producing a go/no-go business readout. The experiment tests a redesigned onboarding flow (Variant B) against the current flow (Control A) to determine whether the change meaningfully improves the 7-day activation rate.

📊 Key Analytical Insights 
---
1. The New Onboarding Flow Produced a Statistically Significant Lift
Variant B increased the 7-day activation rate by +4.97 percentage points — a relative improvement of 12.2% — with a p-value of 0.0077, well below the 0.05 significance threshold.
The Evidence: With 1,149 users in Variant B and 1,174 in Control A, the test reached full statistical power before being called. The 95% confidence interval for the lift was [+0.95%, +9.00%], meaning the true effect is very unlikely to be zero.
Takeaway: Ship Variant B. Estimated impact at current traffic volume is approximately 104 additional activations per month.
2. Running a Power Analysis Before the Test Prevented a False Conclusion
A pre-test power analysis determined that 1,054 users per variant were required to reliably detect the expected +6 percentage point lift with 80% statistical power.
The Evidence: Without this calculation, a team might have called the test after only a few hundred users — at which point the results would have been noisy and unreliable, risking either a false positive (shipping something that does not work) or a false negative (abandoning something that does).
Takeaway: Experiment design is as important as the analysis itself. Calculating sample size before launching a test is non-negotiable for trustworthy results.
---
🔍 Methodology
---
Experiment Design & Technical Implementation
Hypothesis Definition: Established a clear null hypothesis (no difference between variants) and alternative hypothesis (Variant B activation rate > Control A), with a predefined significance level of 0.05 and statistical power of 0.80.
Power Analysis: Calculated minimum sample size per variant using a two-proportion z-test formula, accounting for baseline conversion rate, expected lift, alpha, and power.
Experiment Simulation: Generated individual user-level outcome data for both variants using `numpy.random.binomial`, simulating realistic conversion rates with natural statistical noise.
Statistical Significance Test: Applied a two-proportion z-test (one-tailed) to test whether Variant B's conversion rate was significantly higher than Control A's, producing a z-statistic, p-value, and 95% confidence interval for the lift.
Results Visualization: Built a two-panel chart showing the conversion rate comparison by variant and the observed lift with its confidence interval plotted against the expected lift target.

📁 Files
---
File	Description
`ab_test_analysis.py`	Full experiment lifecycle script with inline comments
`outputs/04_ab_test_results.png`	Results chart: conversion rates and confidence interval

🛠️ Tools & Libraries
---
Tool	Purpose
Python	Core programming language
numpy	Experiment simulation and statistical calculations
scipy	Normal distribution functions for z-test and power analysis
matplotlib	Results visualization

📖 Glossary of Metrics
---
A/B Test: A controlled experiment where users are randomly split between two versions of an experience to measure which performs better on a defined metric.
Power Analysis: A calculation performed before running a test to determine the minimum number of users needed to reliably detect a real effect if one exists.
Statistical Significance: A result is statistically significant when the probability of observing it by random chance alone falls below the predefined threshold (alpha), typically 5%.
P-Value: The probability that the observed difference between variants occurred by random chance. A p-value below 0.05 means the result is statistically significant.
Confidence Interval: A range of values that is likely to contain the true lift with a specified level of certainty (here, 95%). If the interval does not include zero, the result is significant.
Statistical Power: The probability that the test will correctly detect a real effect when one exists. 80% power is the standard minimum threshold.

Data Source
---
All data is synthetically generated using Python's `numpy` library to simulate realistic A/B experiment outcomes with controllable conversion rates and statistical noise.
