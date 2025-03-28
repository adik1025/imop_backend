# An Overview of SD IMOP
Last Updated: 3/27/25

---

# SD IMOP: San Diego Infrastructure Management Optimization Platform

SD IMOP is a data-driven platform designed to optimize infrastructure maintenance across San Diego. By harnessing historical repair records, citizen-reported issues, and facility condition assessments, SD IMOP leverages machine learning to predict when and where maintenance is needed. The goal is to enable proactive repair scheduling, reduce overall costs, and enhance public safety.

---

## Pilot City Checkpoint

### Project Introduction
SD IMOP addresses the challenge of aging urban infrastructure by forecasting maintenance needs before critical failures occur. The platform analyzes historical data—such as street repair projects, pothole reports, and Facility Condition Index (FCI) ratings—to generate predictive insights. These predictions support city planners in prioritizing repairs and allocating resources more effectively.

**Key Objectives:**
- Transition from reactive repairs to proactive maintenance.
- Improve asset lifespan and public safety.
- Optimize resource allocation and reduce emergency repair costs.
- Provide actionable, data-driven insights to decision makers.

---

### Scope / Ideate

#### Data Sources
- **Streets Repair Projects:** Historical records detailing repair start dates, project status, and geographic locations.
- **Pothole Repair Requests:** Citizen reports on potholes and road damages, including timestamps and locations.
- **Facility Condition Index (FCI):** Condition ratings and repair cost estimates for city-owned assets.
- **Supplementary Data:** Traffic volumes, weather data, and urban zoning information to contextualize maintenance demands.

#### Project Focus
- **Prediction:** Forecast the urgency of maintenance needs for various infrastructure elements.
- **Prioritization:** Generate a ranked list of assets based on predicted risk and repair urgency.
- **Visualization:** Create interactive, map-based dashboards that display current asset conditions and forecasted maintenance schedules.

#### Key Features
- **Predictive Modeling:** Utilize time-series forecasting and regression models to predict maintenance needs.
- **Spatial Analysis:** Integrate geospatial data to identify clusters of high-risk infrastructure.
- **Resource Allocation Recommendations:** Provide insights on how to best allocate maintenance crews and budgeting for repairs.
- **User Interaction:** Allow city planners and maintenance teams to interact with the data, drill down into specific regions, and update records based on on-ground feedback.

---

### [Research (ML Data Set)](https://github.com/adik1025/aibe_frontend/issues/10)
#### Data Collection & Preprocessing
- **Aggregation:** Combine datasets from the City of San Diego Open Data Portal covering repair projects, pothole requests, and FCI ratings.
- **Cleaning:** Standardize timestamps, handle missing values, and ensure consistency across datasets.
- **Geocoding:** Convert addresses and location descriptions to latitude and longitude coordinates for spatial analysis.

#### Feature Engineering
- **Temporal Features:**  
  - Time since last repair  
  - Day of week, month, and seasonality indicators  
  - Repair frequency over defined time windows
- **Spatial Features:**  
  - Proximity to high-traffic areas or environmental stressors  
  - Clustering of repair records to identify hotspot regions
- **Asset Characteristics:**  
  - Age and material of infrastructure assets  
  - Historical condition ratings from FCI datasets
- **External Factors:**  
  - Weather conditions (rainfall, temperature fluctuations)  
  - Traffic volume data that may influence wear and tear

#### Modeling Approach
- **Initial Models:**  
  - Regression models (e.g., Linear Regression, Random Forest Regressor) to predict a continuous “maintenance urgency” score.
  - Classification models to flag assets as “High Risk” or “Low Risk.”
- **Evaluation Metrics:**  
  - Mean Absolute Error (MAE) for regression forecasts  
  - Accuracy and F1 score for classification tasks
- **Iteration:**  
  - Continuous refinement using cross-validation and incorporation of user feedback to improve prediction accuracy.

---

### Tinker (GitHub Repo, Demo)

#### GitHub Repository Structure
- **SDIMOP_frontend:**  
  - Contains the web-based user interface built using modern frameworks (e.g., React or Vue.js).  
  - Features interactive maps (Leaflet.js or Google Maps API) that display maintenance predictions and asset statuses.
  - Includes APIs for the models and analytics
- **SDIMOP_ml:**  
  - Houses all scripts and notebooks for data preprocessing, feature engineering, and machine learning model development.  
  - Includes pipelines for training, validation, and deployment of models.

#### Demo Overview
- **Interactive Dashboard:**  
  - A map view highlighting infrastructure assets with color-coded markers indicating repair urgency.
  - A sidebar table with detailed predictions, sortable by risk level, last repair date, and geographic proximity.
- **User Input & Feedback:**  
  - Allow users (e.g., city maintenance planners) to select specific neighborhoods or assets.
  - Incorporate a feedback loop where on-ground updates can adjust model predictions over time.
- **API Endpoints:**  
  - Endpoints for retrieving current asset conditions, forecasting future repairs, and submitting user feedback.
- **Deployment:**  
  - The demo is containerized using Docker for easy deployment and scalability, with CI/CD pipelines set up via GitHub Actions.

---

## Team Organization

|Team Member | Role|
|---------|-----------------------------------|
| Adi     | Scrum Master                      |
| Ansh    | Assistant Scrum Master            |
| Derek   | Scrum - Frontend Engineer         |
| Gyutae  | Scrum - Frontend Engineer         |
| Rayhaan | Scrum - Machine Learning Engineer |
| Aadi    | Scrum - Machine Learning Engineer |

---

## Timeline

- **Week 1 – Ideation & Setup:**  
  - Define project scope, collect datasets, and set up repositories.
- **Week 2 – Data Preprocessing & Model Prototyping:**  
  - Clean data, perform feature engineering, and build initial models.
- **Week 3 – Backend Development:**  
  - Develop API endpoints and integrate ML model predictions.
- **Week 4 – Frontend Integration:**  
  - Create interactive dashboards and integrate mapping features.
- **Week 5 – Testing & Refinements:**  
  - Deploy demo, collect user feedback, and iterate on model performance and UI enhancements.
- **Final Presentation:**  
  - Showcase a fully integrated, working platform with live predictions and interactive visualizations.

---

## Conclusion

SD IMOP is engineered to revolutionize how San Diego approaches infrastructure maintenance. By predicting repair needs and optimizing resource allocation, the platform aims to enhance public safety, reduce repair costs, and extend the lifespan of critical urban assets. The comprehensive integration of historical data, machine learning, and interactive visualization ensures that SD IMOP not only addresses immediate operational challenges but also sets a scalable model for future smart city initiatives.

This project represents a collaborative effort among a skilled team of engineers and data scientists, dedicated to transforming public asset management through innovative technology. With continuous feedback loops and iterative improvements, SD IMOP is poised to deliver long-term value to the City of San Diego and serve as a blueprint for similar initiatives elsewhere.
