import requests
import json
from xml.etree import ElementTree as ET

URL = "https://maxipublica-inventory-feeds.s3.amazonaws.com/campaigns/xml/group/vehicle_feed_group_e1490ae1e92f.xml"
DEALERS = {
    "3852-Seminuevos_Plasencia_Lopez_Mateos",
    "4054-Seminuevos_Plasencia_Bugambilias"
}

resp = requests.get(URL, timeout=30)
root = ET.fromstring(resp.content)

autos = []
for vehicle in root.iter("vehicle"):
    dealer = vehicle.findtext("dealer_id", "")
    if dealer in DEALERS:
        autos.append({
            "dealer_id": dealer,
            "id": vehicle.findtext("id"),
            "make": vehicle.findtext("make"),
            "model": vehicle.findtext("model"),
            "year": vehicle.findtext("year"),
            "price": vehicle.findtext("price"),
            "mileage": vehicle.findtext("mileage"),
            "vin": vehicle.findtext("vin"),
            "image_url": vehicle.findtext("image_url"),
        })

with open("inventario_plasencia.json", "w", encoding="utf-8") as f:
    json.dump(autos, f, ensure_ascii=False, indent=2)

print(f"{len(autos)} vehículos encontrados")
