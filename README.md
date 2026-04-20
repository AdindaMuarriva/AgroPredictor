# 🌱 Agro-Environmental Suitability Predictor

Aplikasi berbasis Machine Learning untuk memprediksi apakah tanaman dapat tumbuh berdasarkan kondisi tanah dan lingkungan.

---

## 🚀 Tech Stack

* Python
* Scikit-learn
* FastAPI (Backend)
* Streamlit (Frontend)

---

## 📊 Dataset

Menggunakan dataset agro-environmental (Kaggle) dengan fitur seperti:

* Soil properties (bulk density, pH, salinity)
* Environmental conditions (temperature, moisture, light)

Target:

* `failure_flag`

  * 0 → Suitable
  * 1 → Not Suitable

---

## ⚙️ Cara Menjalankan

### 1. Backend

```bash
cd application/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 2. Frontend

```bash
cd application/frontend
pip install -r requirements.txt
streamlit run main.py
```

---

## 🔗 API Endpoint

**POST `/predict`**

Request:

```json
{
  "bulk_density": 1.2,
  "organic_matter_pct": 5.0,
  "cation_exchange_capacity": 10.0,
  "salinity_ec": 1.0,
  "buffering_capacity": 5.0,
  "soil_moisture_pct": 30.0,
  "soil_temp_c": 25.0,
  "air_temp_c": 28.0,
  "light_intensity_par": 800.0,
  "soil_ph": 6.5,
  "moisture_regime": 1,
  "thermal_regime": 1,
  "nutrient_balance": 0.0
}
```

Response:

```json
{
  "prediction": 0,
  "interpretation": "Suitable"
}
```

