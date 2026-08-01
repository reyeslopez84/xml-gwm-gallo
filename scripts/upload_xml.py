import requests
import base64
import os

TOKEN = os.environ["GH_TOKEN"]
REPO = "reyeslopez84/xml-gwm-gallo"
FILE_PATH = "inventario_plasencia.xml"
API_URL = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json"
}

# Leer el XML generado
with open(FILE_PATH, "rb") as f:
    content = base64.b64encode(f.read()).decode()

# Obtener SHA actual del archivo (necesario para actualizar)
resp = requests.get(API_URL, headers=headers)
sha = resp.json().get("sha") if resp.status_code == 200 else None

# Subir via API (crea o actualiza)
payload = {
    "message": "Update inventario_plasencia.xml",
    "content": content,
}
if sha:
    payload["sha"] = sha

resp = requests.put(API_URL, headers=headers, json=payload)

if resp.status_code in (200, 201):
    print(f"Archivo subido exitosamente ({resp.status_code})")
else:
    print(f"Error: {resp.status_code} - {resp.text}")
    exit(1)
