from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import numpy as np
import joblib
import os
from datetime import datetime

app = FastAPI(title="Agro Predictor API", version="1.0.0")

# =========================
# CORS Configuration
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Untuk development, batasi di production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Config Path
# =========================
MODEL_PATH = "model/model.pkl"
model = None

# =========================
# Load Model
# =========================
def load_model():
    global model
    try:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
            print(f"✅ Model loaded successfully from {MODEL_PATH}")
        else:
            print(f"⚠️ Model not found at {MODEL_PATH}, using dummy model")
            model = None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        model = None

# Load model saat startup
load_model()

# =========================
# Request Schema
# =========================
class InputData(BaseModel):
    bulk_density: float = Field(..., ge=0, le=3, description="Bulk density (g/cm³)")
    organic_matter_pct: float = Field(..., ge=0, le=100, description="Organic matter (%)")
    cation_exchange_capacity: float = Field(..., ge=0, le=100, description="CEC (meq/100g)")
    salinity_ec: float = Field(..., ge=0, le=50, description="Salinity (dS/m)")
    buffering_capacity: float = Field(..., ge=0, le=50, description="Buffering capacity")
    soil_moisture_pct: float = Field(..., ge=0, le=100, description="Soil moisture (%)")
    soil_temp_c: float = Field(..., ge=0, le=60, description="Soil temperature (°C)")
    air_temp_c: float = Field(..., ge=0, le=60, description="Air temperature (°C)")
    light_intensity_par: float = Field(..., ge=0, le=2000, description="Light intensity (PAR)")
    soil_ph: float = Field(..., ge=0, le=14, description="Soil pH")
    moisture_regime: int = Field(..., ge=0, le=2, description="Moisture regime: 0=Dry, 1=Moderate, 2=Wet")
    thermal_regime: int = Field(..., ge=0, le=2, description="Thermal regime: 0=Cold, 1=Temperate, 2=Hot")
    nutrient_balance: float = Field(..., ge=-100, le=100, description="Nutrient balance")
    
    class Config:
        json_schema_extra = {
            "example": {
                "bulk_density": 1.20,
                "organic_matter_pct": 5.00,
                "cation_exchange_capacity": 10.00,
                "salinity_ec": 1.00,
                "buffering_capacity": 5.00,
                "soil_moisture_pct": 30.00,
                "soil_temp_c": 25.00,
                "air_temp_c": 28.00,
                "light_intensity_par": 800.00,
                "soil_ph": 6.50,
                "moisture_regime": 0,
                "thermal_regime": 1,
                "nutrient_balance": 0.00
            }
        }

# =========================
# Response Schema
# =========================
class PredictionResponse(BaseModel):
    prediction: int
    interpretation: str
    confidence: Optional[float] = None
    timestamp: str
    input_summary: Dict[str, Any]

# =========================
# Root Endpoint
# =========================
@app.get("/")
def root():
    return {
        "message": "🌾 Agro Predictor API is running",
        "status": "active",
        "model_loaded": model is not None,
        "endpoints": {
            "predict": "/predict (POST)",
            "health": "/health (GET)",
            "docs": "/docs (GET)"
        }
    }

# =========================
# Health Check
# =========================
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

# =========================
# Predict Endpoint
# =========================
@app.post("/predict", response_model=PredictionResponse)
def predict(data: InputData):
    """
    Predict whether the soil conditions are suitable for planting.
    Returns 1 for Suitable, 0 for Not Suitable.
    """
    
    try:
        # Log request
        print(f"📊 Prediction request received at {datetime.now()}")
        print(f"   Input: {data.model_dump()}")
        
        # Urutan HARUS sama seperti training model
        input_array = np.array([[
            data.bulk_density,
            data.organic_matter_pct,
            data.cation_exchange_capacity,
            data.salinity_ec,
            data.buffering_capacity,
            data.soil_moisture_pct,
            data.soil_temp_c,
            data.air_temp_c,
            data.light_intensity_par,
            data.soil_ph,
            data.moisture_regime,
            data.thermal_regime,
            data.nutrient_balance
        ]])
        
        confidence = None
        
        # =========================
        # Model Prediction
        # =========================
        if model is not None:
            # Jika model adalah classifier dengan predict_proba
            if hasattr(model, 'predict_proba'):
                pred_proba = model.predict_proba(input_array)[0]
                pred = model.predict(input_array)[0]
                confidence = float(max(pred_proba))
            else:
                pred = model.predict(input_array)[0]
        else:
            # =========================
            # Dummy Model Logic
            # =========================
            # Bobot untuk setiap parameter (contoh sederhana)
            weights = {
                'soil_moisture': 0.15,
                'organic_matter': 0.12,
                'ph': 0.10,
                'temperature': 0.10,
                'cec': 0.08,
                'light': 0.08,
                'nutrient': 0.12,
                'moisture_regime': 0.10,
                'thermal_regime': 0.10,
                'bulk_density': -0.05,
                'salinity': -0.15,
                'buffering': 0.05
            }
            
            # Hitung skor
            score = 0
            score += data.soil_moisture_pct * weights['soil_moisture']
            score += data.organic_matter_pct * weights['organic_matter']
            score += (7.0 - abs(data.soil_ph - 6.5)) * 10 * weights['ph']
            score += data.air_temp_c * weights['temperature']
            score += data.cation_exchange_capacity * weights['cec']
            score += (data.light_intensity_par / 2000) * 100 * weights['light']
            score += data.nutrient_balance * weights['nutrient']
            score += (data.moisture_regime + 1) * 15 * weights['moisture_regime']
            score += (data.thermal_regime + 1) * 10 * weights['thermal_regime']
            score -= data.bulk_density * 20 * abs(weights['bulk_density'])
            score -= data.salinity_ec * 5 * abs(weights['salinity'])
            score += data.buffering_capacity * weights['buffering']
            
            # Normalisasi skor ke range 0-100
            score = max(0, min(100, score))
            
            # Threshold untuk klasifikasi
            pred = 1 if score > 45 else 0
            confidence = score / 100 if pred == 1 else (100 - score) / 100
        
        # =========================
        # Response
        # =========================
        response = PredictionResponse(
            prediction=int(pred),
            interpretation="Suitable" if pred == 1 else "Not Suitable",
            confidence=round(confidence, 3) if confidence else None,
            timestamp=datetime.now().isoformat(),
            input_summary={
                "soil_moisture": f"{data.soil_moisture_pct}%",
                "organic_matter": f"{data.organic_matter_pct}%",
                "soil_ph": data.soil_ph,
                "salinity": f"{data.salinity_ec} dS/m",
                "temperature": f"{data.air_temp_c}°C"
            }
        )
        
        print(f"✅ Prediction result: {response.interpretation} (confidence: {response.confidence})")
        return response
        
    except Exception as e:
        print(f"❌ Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

# =========================
# Batch Prediction (Optional)
# =========================
@app.post("/predict/batch")
def predict_batch(data_list: list[InputData]):
    """Batch prediction for multiple inputs"""
    results = []
    for data in data_list:
        try:
            input_array = np.array([[
                data.bulk_density,
                data.organic_matter_pct,
                data.cation_exchange_capacity,
                data.salinity_ec,
                data.buffering_capacity,
                data.soil_moisture_pct,
                data.soil_temp_c,
                data.air_temp_c,
                data.light_intensity_par,
                data.soil_ph,
                data.moisture_regime,
                data.thermal_regime,
                data.nutrient_balance
            ]])
            
            if model is not None:
                pred = model.predict(input_array)[0]
            else:
                score = data.soil_moisture_pct + data.organic_matter_pct - data.salinity_ec + data.nutrient_balance
                pred = 1 if score > 20 else 0
            
            results.append({"prediction": int(pred), "interpretation": "Suitable" if pred == 1 else "Not Suitable"})
        except Exception as e:
            results.append({"error": str(e)})
    
    return {"results": results, "total": len(results)}

# =========================
# Run Server (Development)
# =========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)