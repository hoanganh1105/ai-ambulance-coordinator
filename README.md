# 🚑 AI Ambulance Coordinator

AI Ambulance Coordinator is an intelligent emergency response system developed for the **Introduction to Artificial Intelligence (CO2017)** course at **Ho Chi Minh City University of Technology (HCMUT)**.

The system integrates multiple AI techniques to support **medical diagnosis** and **emergency routing optimization** for ambulances.

---

# 📚 Course Information

| Field           | Information                                       |
| --------------- | ------------------------------------------------- |
| **Course Name** | Introduction to Artificial Intelligence           |
| **Course ID**   | CO2017                                            |
| **Semester**    | Semester II – Academic Year 2025–2026             |
| **Instructor**  | Dr. Truong Vinh Lan                               |
| **University**  | Ho Chi Minh City University of Technology (HCMUT) |

---

# 👥 Team Members

| Name           | Student ID  | Email      |
| -------------- | ----------- | ---------- |
| Your Full Name | Your ID     | Your Email |
| Member 2 Name  | Member 2 ID |            |
| Member 3 Name  | Member 3 ID |            |
| Member 4 Name  | Member 4 ID |            |

---

# 🎯 Project Objective

The **AI Ambulance Coordinator** is designed to improve emergency medical response by automating two critical phases:

## Phase 1 — Medical Diagnosis

A **Machine Learning model (Decision Tree)** analyzes patient symptoms to predict potential diseases.
A **rule-based system (IF–THEN rules)** then prioritizes emergency cases based on diagnosis severity.

## Phase 2 — Emergency Routing

The system determines the fastest route for ambulances by combining:

* **Bayesian Networks** to estimate traffic congestion probabilities
* **A* Search Algorithm** to compute optimal navigation paths
* **Heuristic functions** to guide efficient pathfinding

This integration allows the system to **simulate intelligent decision-making in emergency medical services**.

---

# 🧠 AI Techniques Used

The project integrates **4+ major AI components** required by the course:

| AI Component             | Implementation                                      |
| ------------------------ | --------------------------------------------------- |
| Representation & Search  | State-space modeling with **A*** search             |
| Heuristic Function       | **Euclidean Distance** for path optimization        |
| Knowledge Representation | **IF–THEN rule system** for patient priority        |
| Probabilistic Reasoning  | **Bayesian Networks** for traffic prediction        |
| Machine Learning         | **Decision Tree classifier** for disease prediction |

---

# 📂 Project Structure

```
ai-ambulance-coordinator/
│
├── features/
│   ├── disease_classes.npy
│   ├── symptom_features.npy
│   └── trained_model.joblib
│
├── modules/
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── ml_model.py
│   ├── search.py
│   ├── bayesian_network.py
│   └── rules_engine.py
│
├── notebooks/
│   └── Main_Pipeline.ipynb
│
├── reports/
│   ├── final_report.pdf
│   └── eda_visualizations.ipynb
│
├── requirements.txt
└── README.md
```

### Folder Description

| Folder               | Description                                               |
| -------------------- | --------------------------------------------------------- |
| **features/**        | Extracted features, disease labels, and trained ML models |
| **modules/**         | Core system modules for AI algorithms                     |
| **notebooks/**       | Google Colab notebooks for testing and integration        |
| **reports/**         | Final report and analysis visualizations                  |
| **requirements.txt** | Python dependencies                                       |

---

# ⚙️ Getting Started

The project is designed to run **entirely on Google Colab** without mounting personal cloud storage.

## Prerequisites

You need a **Kaggle API Token** to automatically download the dataset.

1. Go to Kaggle → Account → Create API Token
2. Download `kaggle.json`

---

# ▶️ Running the System

## Step 1 — Open Google Colab

Open:

```
notebooks/Main_Pipeline.ipynb
```

---

## Step 2 — Set Kaggle Credentials

```python
import os

os.environ['KAGGLE_USERNAME'] = "your_username"
os.environ['KAGGLE_KEY'] = "your_key"
```

---

## Step 3 — Clone Repository

```bash
!git clone https://github.com/your-username/ai-ambulance-coordinator.git
%cd ai-ambulance-coordinator
```

---

## Step 4 — Run the Pipeline

From the Colab menu:

```
Runtime → Run All
```

This will automatically:

1. Download dataset
2. Preprocess symptom data
3. Train the Decision Tree model
4. Perform disease prediction
5. Compute optimal ambulance routes

---

# 🏗 System Architecture

The overall system workflow is shown below:

```
Patient Symptoms
       │
       ▼
Machine Learning Model
(Decision Tree)
       │
       ▼
Disease Prediction
       │
       ▼
Rule-Based System
(IF–THEN)
       │
       ▼
Priority Assignment
       │
       ▼
Traffic Bayesian Network
       │
       ▼
A* Search Algorithm
       │
       ▼
Optimal Ambulance Route
```

---

# 📊 Machine Learning Model

**Algorithm:** Decision Tree Classifier

Dataset characteristics:

| Feature            | Value   |
| ------------------ | ------- |
| Number of symptoms | 377     |
| Number of diseases | 773     |
| Total samples      | 246,945 |
| Test split         | 20%     |
| Model accuracy     | ~81.44% |

Input symptoms are represented as **binary vectors**:

```
0 → symptom absent  
1 → symptom present
```

---

# 📄 Project Deliverables

| Deliverable           | Link                          |
| --------------------- | ----------------------------- |
| Final Report (PDF)    | reports/final_report.pdf      |
| Google Colab Notebook | notebooks/Main_Pipeline.ipynb |
| Source Code           | modules/                      |

---

# 🧪 Future Improvements

Potential improvements include:

* Implement **Naive Bayes (BernoulliNB)** for binary symptom data
* Perform **Hyperparameter Tuning with GridSearchCV**
* Address **Class Imbalance** using:

  * `class_weight="balanced"`
  * SMOTE resampling
* Improve symptom representation to include **severity levels**

---

# 📜 License

This project is developed **for academic purposes** as part of the
**CO2017 – Introduction to Artificial Intelligence course at HCMUT**.

---

# ⭐ Acknowledgement

Special thanks to **Dr. Truong Vinh Lan** for guidance throughout the course.
