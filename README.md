<div align="center">

# 🏭 Predictive Maintenance for Industrial Equipment
### *From Reactive Repairs to Smart Decisions — Aligned with Industry 5.0*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)](https://jupyter.org)
[![XGBoost](https://img.shields.io/badge/XGBoost-Enabled-brightgreen?style=for-the-badge)](https://xgboost.readthedocs.io)
[![LightGBM](https://img.shields.io/badge/LightGBM-Enabled-blue?style=for-the-badge)](https://lightgbm.readthedocs.io)
[![SHAP](https://img.shields.io/badge/SHAP-Explainability-orange?style=for-the-badge)](https://shap.readthedocs.io)
[![Dataset](https://img.shields.io/badge/Dataset-UCI_AI4I_2020-9C27B0?style=for-the-badge)](https://archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset)

<br/>

> *"During my time at **Rockwell Automation**, I saw firsthand how equipment downtime at plants like **IFFCO** doesn't just impact revenue — it disrupts entire supply chains. That's when predictive maintenance stopped being a data science problem for me, and became a responsibility."*

</div>

---

## 🎯 The Problem This Solves

In a 24×7 continuous manufacturing environment, a **3.4% failure rate** isn't "low" — it's a recurring operational leak. Each unplanned breakdown can cost **₹10–25 Lakhs** in lost production and emergency repairs.

This project builds an industrial-grade AI system that converts catastrophic ₹25 Lakh breakdowns into ₹2 Lakh planned maintenance windows — by catching failures **hours before they happen**.

---

## 🗺️ Project Architecture at a Glance

```
Raw Sensor Data ──► Physics-Driven Features ──► Multi-Model ML ──► SHAP Explainability
                                                        │
                                                        ▼
              Deployment-Ready Model ◄── Risk Tier Score ◄── Threshold Tuning
                        │
                        ▼
        [Human-Centric Output] + [Drift Monitoring] + [Sustainability Analysis]
```

| Step | What Happens | Why It Matters |
|------|-------------|----------------|
| 0–1 | Setup & Data Loading | UCI AI4I 2020 dataset — 10,000 real machine records |
| 2 | Exploratory Data Analysis | 8 visualization deep-dives with dual technical + business insights |
| 3 | Physics-Driven Feature Engineering | Power curves, thermal gradients, overstrain index — not just statistics |
| 4 | Multi-Model ML Training | LR · Random Forest · Gradient Boost · XGBoost · **LightGBM** (winner) |
| 5 | SHAP Explainability | Black box → trusted tool for the shop floor |
| 6 | Threshold Tuning | Recall-first strategy; tuned to minimize missed failures |
| 7 | Failure Mode-Specific Models | Predict *which* failure (TWF / HDF / PWF / OSF), not just *if* |
| 8 | Business Impact Analysis | ROI quantified in ₹ Crores, not just AUC scores |
| 9 | Maintenance Priority Score | Color-coded risk tiers a plant engineer can act on immediately |
| 10 | Industry 5.0 — Human-Centric AI | Plain-language operator explainer + uncertainty flagging |
| 11 | Sustainability & Energy Efficiency | CO₂ footprint estimation from inefficient operation |
| 12 | Model Drift Monitoring (PSI) | Resilience-first — knows when it needs retraining |
| 13 | Model Persistence & Deployment | Production-ready, `joblib`-serialized, inference-ready |
| 14 | Final Summary | Lessons from the shop floor |

---

## ⚡ Key Technical Highlights

### 🔬 Physics-First Feature Engineering
Rather than blindly feeding raw sensor data into a model, every engineered feature has a **physical justification**:

| Feature | Formula | Physical Meaning |
|---------|---------|-----------------|
| `Temp_Delta` | Process_Temp − Air_Temp | Thermal gap; drops below 8.6K → HDF imminent |
| `Power_W` | Torque × (RPM × 2π/60) | Real mechanical output; outside 3500–9000W = danger |
| `Strain_Index` | Tool_Wear × Torque | Cumulative mechanical fatigue — catches OSF early |
| `Power_Out_of_Range` | Binary flag | Immediate high-signal guardrail for the classifier |
| `Low_Temp_Delta` | ΔT < 8.6K flag | Deterministic HDF trigger (captures 95%+ of HDF events) |

### 🤖 Model Performance
- **Recall: 0.85** — Catches 85% of all failures before they happen
- **F1-Score: 0.78** — Robust despite 3.4% class imbalance (handled via SMOTE)
- **LightGBM** chosen for production: fastest inference, lowest memory, native categorical support — ideal for edge deployment on PLCs

### 🧠 SHAP Explainability
Discovered that **engineered features** (`Power_Out_of_Range`, `Strain_Index`) outrank raw sensors in the model's decision hierarchy — validating that *leading indicators* (strain/power) matter more than *lagging indicators* (temperature) for early warning.

### 🎛️ Threshold Strategy
Threshold shifted from `0.5 → 0.3` — because mathematically, you can afford **200–400 false alarms** and still break even on a single prevented failure.

---

## 🏭 Industry 5.0 Alignment

This notebook goes beyond standard ML. It's designed around all three pillars of **Industry 5.0**:

| Pillar | What's Built |
|--------|-------------|
| 🧑‍🔧 **Human-Centric** | Plain-language operator explainer · SHAP decision support · Human review queue for uncertain predictions |
| 🛡️ **Resilience** | Ensemble uncertainty quantification · PSI drift monitoring · Recall-first threshold tuning |
| 🌱 **Sustainability** | Energy efficiency analysis · CO₂ footprint estimation · Maintenance-as-emissions-reduction |

---

## 🚀 Getting Started

**Run in Google Colab (Recommended) — No setup needed:**

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

**Or run locally:**

```bash
# Clone the repo
git clone https://github.com/CodeWithSrish/predictive-maintenance.git
cd predictive-maintenance

# Install dependencies
pip install ucimlrepo shap imbalanced-learn xgboost lightgbm joblib scikit-learn pandas matplotlib seaborn

# Launch notebook
jupyter notebook Predictive_Maintenance.ipynb
```

> ⏱️ **Runtime:** ~3–5 minutes on Google Colab (CPU). Dataset auto-downloads via `ucimlrepo`.

---

## 📊 Dataset

**AI4I 2020 Predictive Maintenance Dataset** — UCI Machine Learning Repository  
10,000 records · 14 features · 5 failure modes · 3.4% failure rate

```
Features: Air Temp (K) · Process Temp (K) · RPM · Torque (Nm) · Tool Wear (min) · Product Type
Targets:  Machine Failure · TWF · HDF · PWF · OSF · RNF
```

---

## 🗂️ Repository Structure

```
📦 predictive-maintenance
 ┣ 📓 Predictive_Maintenance.ipynb   # Main notebook — all 14 steps
 ┣ 📄 README.md                      # You are here
 ┗ 📁 models/                        # Saved LightGBM model (generated on run)
     ┗ lgbm_maintenance_model.pkl
```

---

## 🧰 Tech Stack

`Python 3.8+` · `scikit-learn` · `XGBoost` · `LightGBM` · `SHAP` · `imbalanced-learn (SMOTE)` · `pandas` · `numpy` · `matplotlib` · `seaborn` · `joblib` · `ucimlrepo`

---

## 👩‍💻 Author

**Srishti Rajput**  
*Data Scientist*  
Inspired by real-world experience at **Rockwell Automation** and exposure to large-scale process operations at **IFFCO**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/srishti-rajput-629201263/)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat-square&logo=github)](https://github.com/CodeWithSrish)

---

## 💡 Five Lessons from the Shop Floor

1. **Physics first, then ML** — Engineer features from process knowledge, not just statistics
2. **Recall over accuracy** — In maintenance, a missed failure is never acceptable
3. **Explainability = adoption** — A model the engineer doesn't trust never gets deployed
4. **Quantify in ₹, not AUC** — ROI converts stakeholders faster than metrics
5. **Build for the edge** — Production models must be fast, light, and interpretable

---

<div align="center">

*This project is not just about predicting failures.*  
*It's about building systems that manufacturing engineers can trust, operators can understand, and plant managers can justify to the board.*

⭐ **Star this repo if you found it useful!**

</div>
