# app/utils/audio_features.py
# Aquí pondrás funciones concretas para extraer MFCC, ZCR, energy, etc.
# En pruebas vamos a usar stubs (simulación).
import numpy as np

def extract_mfcc_from_bytes(file_bytes: bytes, n_mfcc: int = 13):
    # En producción: usar librosa, scipy o un microservicio Python especializado.
    # Aquí devolvemos una lista simulada con n_mfcc valores.
    return list(np.random.rand(n_mfcc))

def extract_features(file_bytes: bytes):
    mfcc = extract_mfcc_from_bytes(file_bytes)
    energy = float(np.random.rand(1)[0])
    return {"mfcc": mfcc, "energy": energy}
