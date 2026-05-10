# AI Ambulance Coordinator — Intelligent Ambulance Dispatch System

The AI system developed as part of the course *Introduction to Artificial Intelligence* assignment.

## 📚 Course Information

| Field           | Information                                       |
| --------------- | ------------------------------------------------- |
| **Course Name** | Introduction to Artificial Intelligence           |
| **Course ID**   | CO2017                                            |
| **Semester**    | Semester II – Academic Year 2025–2026             |
| **Instructor**  | Dr. Trương Vĩnh Lân                               |
| **University**  | Ho Chi Minh City University of Technology (HCMUT) |

## 👥 Team Members

| Name           | Student ID  | Email      |
| -------------- | ----------- | ---------- |
| Huỳnh Hoàng Anh | 2410078 | anh.huynh1105@hcmut.edu.vn |
| Nguyễn Đăng Khánh | 2311512 | khanh.nguyennttt040905@hcmut.edu.vn |
| Hồ Đắc Minh Phương | 2312738 | hophuong11052005@gmail.com |
| Nguyễn Anh Quân | 2412899 | quan.nguyen2412899@hcmut.edu.vn |

---

## 📖 Overview
In emergency medicine, the "golden hour" can determine patient outcomes. This system answers the question: **How to assign a single ambulance when multiple calls arrive simultaneously?** Instead of using strict first-come-first-served, the system combines AI techniques to make informed dispatch decisions:

- **Forecasting & Diagnosis:** Machine learning models provide preliminary diagnoses and a simple Bayesian network estimates traffic risk.
- **Triage & Prioritization:** Logic-based inference ranks urgency based on reported symptoms and likely diagnoses.
- **Route Optimization:** An A* search finds shortest routes on a road graph whose edge weights are updated by traffic estimates.

---

## 📊 Datasets and Dependencies
**Datasets**:
- **[Disease–Symptom Dataset](https://www.kaggle.com/datasets/dhivyeshrk/diseases-and-symptoms-dataset)** for training the diagnostic classifier.
- **[Delhi Traffic Patterns Dataset](https://www.kaggle.com/datasets/guriya79/understanding-delhi-traffic-patterns)** for training the traffic forecasting model.

**Main dependencies**:
- [**kagglehub**](https://github.com/Kaggle/kagglehub) for downloading datasets.
- **[OSMnx](https://osmnx.readthedocs.io/en/stable/)** for map data (road network) of the target region (default: Delhi, India).
- [**pyDatalog**](https://sites.google.com/site/pydatalog/home) for implementation of the rule-based `PatientPrioritizer`.
- [**scikit-learn**](https://scikit-learn.org/stable/) for comparing standard machine learning models with our self-imlemented one.
- [**pgmpy**](https://pgmpy.org/index.html) for comparing standanrd Bayesian Network model with our self-implemented one.

   All dependencies in detail are listed in `requirements.txt`.

---

## 🚀 How to run
The project is designed to run **entirely on Google Colab** without mounting personal cloud storage. Installations are also handled automatically in our notebook.

### Quick start
Open the [project's notebook on Google colab](https://colab.research.google.com/github/hoanganh1105/ai-ambulance-coordinator/blob/main/notebooks/Main_Pipeline.ipynb) and jump to section **Hệ thống tích hợp**, then:
1. **Configure environment:** open the main notebook and set parameters (optional):
   - `time_of_day`: "Morning Peak" / "Afternoon" / "Evening Peak" / "Night"
   - `day_of_week`: "Weekday" / "Weekend"
   - `weather_condition`: "Clear" / "Rain" / "Fog" / "Heatwave"
2. **Run the notebook:** execute all cells (Runtime → Run All).
3. **Interact with the UI (final cell):**
   - Step 1: click the ambulance position on the map.
   - Step 2: click patient locations, enter symptoms, and click **"Thêm bệnh nhân"** for each case.
   - Step 3: click **"Kết thúc và trả kết quả"** to run the pipeline and display the selected route.

---

## 🗂 Repository layout
```
├── features/
├── modules/
│   ├── core/
│   │   ├── disease_classifier.py
│   │   ├── map_router.py
│   │   ├── patient_prioritizer.py
│   │   └── traffic_estimator.py
│   ├── models/
│   │   ├── simple_bayesian_network.py
│   │   ├── simple_classifier.py
│   │   ├── simple_search_algorithm.py
│   │   └── simple_street_graph.py
│   └── ui/
│       └── dispatch_ui.py
└── notebooks/
│   └── Main_Pipeline.ipynb
└── reports/
    └── final_report.pdf
```

### Folder Description

| Folder               | Description                                                    |
| -------------------- | ---------------------------------------------------------------|
| **features/**        | Extracted features, disease labels and knowledge base          |
| **modules/core/**     | Core system modules for AI algorithms                          |
| **modules/models/**   | Self-implemented algorithms, data structures, and models       |
| **modules/ui/**       | Support system interaction via a graphic interface on notebook |
| **notebooks/**       | Google Colab notebooks for testing and integration             |
| **reports/**         | Project's report                                               |


### 📄 Project Deliverables

A [PDF project report](reports/final_report.pdf) (in `report/`) and a [Colab notebook](https://colab.research.google.com/github/hoanganh1105/ai-ambulance-coordinator/blob/main/notebooks/Main_Pipeline.ipynb) (in `notebooks/`) is available.

---

## 🏗 System architecture and Pipeline

### Core AI components
| Component | Source file | Purpose |
| :--- | :--- | :--- |
| **Map & Search** | `map_router.py`, `simple_search_algorithm.py` | Manage state-space model (OSMnx-like graph) with **A\*** search. |
| **Prioritization / Reasoning** | `patient_prioritizer.py` | Use Datalog-style rules to rank patients based on symptoms and predicted disease. |
| **Traffic Forecasting** | `traffic_estimator.py` | Bayesian network that estimates traffic and updates edge weights. |
| **Disease Diagnosis** | `disease_classifier.py` | ML model that predicts likely disease from symptoms. |

The listed AI components above function using either internal implementations (in `modules/models`) or external libraries. Additionally, `dispatch_ui.py` is provided to support interaction via graphic interface.

### Pipeline
The runtime pipeline contains three main phases:
1. **Initialization:** load maps, datasets, and populate models/knowledge bases.
2. **Environment update:** `TrafficEstimator` predicts traffic (by time, weather, road type) and updates graph edge weights.
3. **Operational flow:**
   - Receive a list of patients (location + symptoms).
   - Run the disease classifier to obtain each patient's predicted disease.
   - Select the highest-priority patients using the reasoning engine.
   - Compute routes and choose the closest patient among the top-priority group to dispatch the ambulance.

---

## 📜 License

This project is developed **for academic purposes** as part of the
**CO2017 – Introduction to Artificial Intelligence course at HCMUT**.

## ⭐ Acknowledgement

Special thanks to **Dr. Truong Vinh Lan** for guidance throughout the course.
