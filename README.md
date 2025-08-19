# 🧬 PlasmidFlow  
**Interactive Visualization of Plasmid-Driven Traits Across Environments**

![License](https://img.shields.io/badge/license-MIT-green.svg)  
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)  
![Flask](https://img.shields.io/badge/framework-Flask-red.svg)  
![Plotly](https://img.shields.io/badge/visualization-Plotly-orange.svg)  
![Bootstrap](https://img.shields.io/badge/UI-Bootstrap-lightblue.svg)

---

## 📌 Overview
PlasmidFlow is a **modular client–server web interface** for **visualizing plasmid–host–trait interactions**.  
It combines **Flask + SQLAlchemy + pandas/NumPy** on the backend with a **Bootstrap + Plotly.js** frontend.

Key features:
- 📂 Upload plasmid datasets (CSV with traits)
- 🔍 Apply filters by **environment** or **trait type**
- 🔗 Generate **Sankey diagrams** of gene transfer
- 🌐 Build **network graphs** of shared plasmids
- 🔥 Render **heatmaps** of trait presence
- 🎨 Customize node colors, edge colors, font sizes, and background
- 💾 Save / load JSON style profiles for reproducibility
- 📤 Export figures as **SVG / PNG / PDF** (via Kaleido)
- 🗄️ Persistence via **SQLite (default)** or **PostgreSQL**

---

## 🏗️ System Architecture
![PlasmidFlow Architecture](docs/architecture.png) <!-- replace with your image path -->

**Client (Browser):**
- Sidebar + header (navigation & branding)
- Data panel (upload datasets, apply filters)
- Visualization panel (render interactive plots & customize styles)

**Server (Flask):**
- Routes (`/api/upload`, `/api/figure`, `/api/export`)
- Data parsing/validation with **pandas/NumPy**
- Graph generation with **Plotly & NetworkX**
- Persistent storage with **SQLite/Postgres**

---

## 🚀 Quickstart

```bash
# Clone the repo
git clone https://github.com/yourusername/PlasmidFlow.git
cd PlasmidFlow

# Create environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
export FLASK_DEBUG=1
export SECRET_KEY=change-this
python app.py
```

Open 👉 [http://localhost:10000](http://localhost:10000)

---

## 📊 CSV Input Format
Your input must include these columns:

| Column       | Description                          |
|--------------|--------------------------------------|
| `Plasmid_ID` | Unique plasmid identifier            |
| `Host_Genome`| Host genome name/ID                  |
| `Environment`| Environment label                    |
| `ARGs`       | Antimicrobial resistance traits      |
| `Virulence`  | Virulence traits                     |
| `T4SS`       | Type IV secretion system presence    |
| `MGEs`       | Mobile genetic elements              |

✅ Example: [`assets/plasmidflow_example_input.csv`](assets/plasmidflow_example_input.csv)

---

## 🎨 Customization
- **Node Color** → `"red"`  
- **Edge Color** → `"skyblue"`  
- **Background** → `"white"`  
- **Font Size** → `14`  
- **Matrix Colorscales** → `Blues, Viridis, Plasma, Cividis, Inferno`  

Save your style as JSON and reload anytime for reproducibility.

---

## 📤 Export Options
Figures can be exported in high-resolution using **Kaleido**:
- **PNG** for presentations
- **SVG** for vector graphics
- **PDF** for publications

---

## 🗄️ Database Support
- **SQLite** (default) → lightweight persistence for local use.  
- **PostgreSQL** → scalable and concurrent querying.  

Switch by setting:
```bash
export DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/plasmidflow
```

---

## 📸 Screenshots
| Upload & Filters | Sankey Diagram | Network Graph | Trait Heatmap |
|------------------|----------------|---------------|---------------|
| ![upload](docs/upload.png) | ![sankey](docs/sankey.png) | ![network](docs/network.png) | ![heatmap](docs/heatmap.png) |

---

## 📚 Citation
If you use PlasmidFlow in your work, please cite:  

> *PlasmidFlow: A Web-based Platform for Interactive Visualization of Plasmid-Driven Traits* (2025)  

---

## 🛠️ Built With
- [Flask](https://flask.palletsprojects.com/)  
- [Bootstrap](https://getbootstrap.com/)  
- [Plotly](https://plotly.com/python/)  
- [NetworkX](https://networkx.org/)  
- [pandas](https://pandas.pydata.org/) / [NumPy](https://numpy.org/)  
- [Kaleido](https://github.com/plotly/Kaleido)  

---

## 📄 License
MIT License © 2025 PlasmidFlow Team

---
⭐ **Star this repo** if you find it useful!  
