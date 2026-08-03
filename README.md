# 🛡️ Employee Engagement, Satisfaction & Burnout Diagnostic
### Preventive HR Analytics for Palo Alto Networks

A data-driven HR diagnostic tool that flags burnout risk and disengagement **before** employees resign — shifting HR from reactive attrition analysis to preventive employee experience management.

---

## 📌 Problem Statement

Palo Alto Networks currently lacks:
- A unified engagement health index
- Clear visibility into burnout-prone employee groups
- Understanding of how overtime, work-life balance, and satisfaction interact
- Preventive insights into employee experience deterioration

As a result, HR interventions are often late-stage and reactive. This project fixes that.

---

## 🔑 Key Finding

Burnout risk — calculated purely from data HR already collects — predicts attrition **before** it happens:

| Burnout Risk Level | Attrition Rate |
|---|---|
| Low | 6.6% |
| Medium | 19.7% |
| High | 36.9% |

Statistically significant (chi-square test, p < 0.0001). High-risk employees leave at more than 5x the rate of low-risk employees.

---

## 📊 Dashboard Modules

| Module | What it shows |
|---|---|
| Engagement Health Overview | Org-wide engagement score, satisfaction distribution |
| Burnout Risk Dashboard | High-risk employee segments, overtime & work-life imbalance |
| Role & Career Stage Analysis | Engagement by job role/level, tenure trends, promotion stagnation |
| Manager Action Panel | Low-engagement alerts, priority intervention areas |

Interactive filters: Department, Job Role, Overtime toggle, Engagement threshold slider, Tenure range selector.

---

## 🧮 KPIs Computed

- **Engagement Index** — composite of JobInvolvement, JobSatisfaction, EnvironmentSatisfaction, RelationshipSatisfaction
- **Burnout Risk Score** — overtime + low work-life balance + low engagement
- **Work-Life Balance Index** — average balance rating
- **Satisfaction Stability Score** — consistency across satisfaction dimensions
- **Workload Stress Indicator** — travel frequency + overtime intensity

---

## 📈 Methodology

1. **Data Validation & Normalization** — validated ordinal scales, handled missing values
2. **Engagement Index Construction** — combined 4 satisfaction dimensions into a standardized score
3. **Burnout Risk Identification** — flagged overtime + low work-life balance + low engagement
4. **Workload & Stress Analysis** — compared engagement across overtime, travel, and commute groups
5. **Career-Stage Engagement Analysis** — identified stagnation-linked disengagement patterns
6. **Engagement vs Attrition** — contextual comparison (not predictive modeling) between employees who stayed vs. left

---

## 📄 Deliverables

- Research Paper — EDA, insights, recommendations
- Executive Summary — stakeholder-facing summary
- Live Streamlit Dashboard

---

## 🙋 About

Built as part of the Unified Mentor HR Analytics track, using real HR data from Palo Alto Networks (1,470 employee records).
