import os
import joblib
import pandas as pd
import numpy as np
import warnings
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
import traceback

warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# 1. Inisialisasi FastAPI
app = FastAPI(
    title="Agro-Environmental Predictor API",
    description="API untuk memprediksi keberhasilan pertumbuhan tanaman",
    version="2.0.0"
)

# 2. Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Manajemen Path Asset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../../model")

MODEL_PATH = os.path.join(MODEL_DIR, "model_final.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
FEAT_PATH = os.path.join(MODEL_DIR, "feature_names.pkl")

# 4. Global Variables
model = None
scaler = None
feature_names = None

# 5. Load Asset saat Startup
@app.on_event("startup")
def startup_event():
    global model, scaler, feature_names
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"❌ ERROR: Model tidak ditemukan di {MODEL_PATH}")
            return
        
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        feature_names = joblib.load(FEAT_PATH)
        
        print("=" * 50)
        print("✅ BACKEND ASSETS LOADED")
        print(f"📦 Model: {type(model).__name__}")
        print(f"🔢 Total Features: {len(feature_names)}")
        
        # Cek class labels model
        if hasattr(model, "classes_"):
            print(f"🏷️ Model Classes: {model.classes_}")
            print(f"   (0={model.classes_[0]}, 1={model.classes_[1]})")
            
            # Auto-detect: Jika class 1 adalah label positif (Tumbuh)
            if model.classes_[1] == 1:
                print("✅ Interpretasi: 1 = Tumbuh, 0 = Gagal")
            else:
                print("⚠️ Interpretasi: 1 = Gagal, 0 = Tumbuh")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ GAGAL MEMUAT ASSET: {str(e)}")
        traceback.print_exc()

# 6. Skema Input Request
class PredictRequest(BaseModel):
    bulk_density: float = Field(..., description="Bulk Density (g/cm³)")
    organic_matter_pct: float = Field(..., description="Organic Matter (%)")
    cation_exchange_capacity: float = Field(..., description="CEC (meq/100g)")
    salinity_ec: float = Field(..., description="Salinity (dS/m)")
    buffering_capacity: float = Field(..., description="Buffering Capacity")
    soil_moisture_pct: float = Field(..., description="Soil Moisture (%)")
    soil_temp_c: float = Field(..., description="Soil Temperature (°C)")
    air_temp_c: float = Field(..., description="Air Temperature (°C)")
    light_intensity_par: float = Field(..., description="Light Intensity (PAR)")
    soil_ph: float = Field(..., description="Soil pH")
    moisture_regime: int = Field(..., ge=0, le=2, description="Moisture Regime")
    thermal_regime: int = Field(..., ge=0, le=2, description="Thermal Regime")
    nutrient_balance: int = Field(..., ge=0, le=2, description="Nutrient Balance")

# 7. Endpoint Health Check
@app.get("/health")
def health_check():
    return {
        "status": "healthy" if model is not None else "model_not_loaded",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

# 8. Endpoint Root
@app.get("/")
def home():
    return {
        "status": "Online",
        "timestamp": datetime.now().isoformat(),
        "model_info": {
            "loaded": model is not None,
            "features": len(feature_names) if feature_names is not None else 0
        }
    }

# 9. Endpoint Prediksi Utama
@app.post("/predict")
def predict(request: PredictRequest):
    if model is None or scaler is None:
        raise HTTPException(status_code=503, detail="Model atau Scaler belum dimuat")
    
    try:
        # a. Konversi input ke DataFrame
        input_data = {
            'bulk_density': request.bulk_density,
            'organic_matter_pct': request.organic_matter_pct,
            'cation_exchange_capacity': request.cation_exchange_capacity,
            'salinity_ec': request.salinity_ec,
            'buffering_capacity': request.buffering_capacity,
            'soil_moisture_pct': request.soil_moisture_pct,
            'soil_temp_c': request.soil_temp_c,
            'air_temp_c': request.air_temp_c,
            'light_intensity_par': request.light_intensity_par,
            'soil_ph': request.soil_ph,
            'moisture_regime': request.moisture_regime,
            'thermal_regime': request.thermal_regime,
            'nutrient_balance': request.nutrient_balance
        }
        
        df_input = pd.DataFrame([input_data])
        
        # b. Feature alignment
        for col in feature_names:
            if col not in df_input.columns:
                df_input[col] = 0
        
        df_input = df_input[feature_names]
        
        # c. Scaling
        scaled_data = scaler.transform(df_input)
        
        # d. Prediksi
        prediction_raw = model.predict(scaled_data)[0]
        prediction = int(prediction_raw)
        
        # e. Probabilitas
        confidence = None
        if hasattr(model, "predict_proba"):
            probs = model.predict_proba(scaled_data)[0]
            confidence = float(np.max(probs))
        
        # f. INTERPRETASI HASIL - AUTO DETECT
        # Deteksi apakah model menggunakan 1=Tumbuh atau 1=Gagal
        if hasattr(model, "classes_"):
            # Jika class 1 adalah 1, maka prediction=1 berarti Tumbuh
            if model.classes_[1] == 1:
                is_success = (prediction == 1)
            else:
                is_success = (prediction == 0)
        else:
            # Default: asumsikan 1 = Tumbuh
            is_success = (prediction == 1)
        
        # Set hasil berdasarkan auto-detection
        if is_success:
            result_text = "Tumbuh"
            result_en = "Suitable"
            color_code = "#28A745"
        else:
            result_text = "Gagal"
            result_en = "Not Suitable"
            color_code = "#FF4B4B"
        
        print(f"🎯 Prediction: {prediction} -> {result_text} (conf: {confidence:.2%})")
        
        return {
            "prediction": prediction,
            "result": result_text,
            "result_en": result_en,
            "confidence": round(confidence, 4) if confidence else None,
            "color": color_code,
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"❌ Prediction Error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=str(e))

# 10. Jalankan Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)