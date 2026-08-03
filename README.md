---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/palo-alto-networks-engagement.git
cd palo-alto-networks-engagement
```

### 2. Set up a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the dashboard
```bash
cd app
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`.

---

## 🛠️ Tech Stack

- **Python** — pandas, numpy, scikit-learn, scipy
- **Visualization** — Plotly, Matplotlib, Seaborn
- **Dashboard** — Streamlit
- **Analysis** — Jupyter Notebook

---

## 📈 Methodology

1. **Data Validation & Normalization** — validated ordinal scales, handled missing values
2. **Engagement Index Construction** — combined 4 satisfaction dimensions into a standardized score
3. **Burnout Risk Identification** — flagged overtime + low work-life balance + low engagement
4. **Workload & Stress Analysis** — compared engagement across overtime, travel, and commute groups
5. **Career-Stage Engagement Analysis** — identified stagnation-linked disengagement patterns
6. **Engagement vs Attrition** — contextual comparison (not predictive modeling) between employees who stayed vs. left

Full methodology and findings: [`outputs/research_paper.md`](outputs/research_paper.md)

---

## 📄 Deliverables

- ✅ [Research Paper](outputs/research_paper.md) — EDA, insights, recommendations
- ✅ [Executive Summary](outputs/executive_summary.md) — stakeholder-facing summary
- ✅ Live Streamlit Dashboard

---

## 📜 License

This project is for educational purposes as part of the Unified Mentor program.

---

## 🙋 Author

Built by s.pushpalatha as part of the Unified Mentor HR Analytics track.
