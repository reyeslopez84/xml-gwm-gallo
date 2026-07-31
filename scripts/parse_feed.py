import requests
from xml.etree import ElementTree as ET

URL = "https://maxipublica-inventory-feeds.s3.amazonaws.com/campaigns/xml/group/vehicle_feed_group_e1490ae1e92f.xml"
DEALERS = {
    "3852-Seminuevos_Plasencia_Lopez_Mateos",
    "4054-Seminuevos_Plasencia_Bugambilias"
}

resp = requests.get(URL, timeout=30)
root = ET.fromstring(resp.content)

# Crear nuevo XML con misma estructura raíz
new_root = ET.Element("listings")
title = ET.SubElement(new_root, "title")
title.text = "Feed Seminuevos Plasencia - Lopez Mateos y Bugambilias"

count = 0
for listing in root.findall("listing"):
    dealer_id = listing.findtext("dealer_id", "")
    if dealer_id in DEALERS:
        new_root.append(listing)
        count += 1

# Escribir XML con declaración y encoding utf-8
tree = ET.ElementTree(new_root)
ET.indent(tree, space="  ")
with open("inventario_plasencia.xml", "wb") as f:
    f.write(b'<?xml version="1.0" encoding="utf-8"?>\n')
    tree.write(f, encoding="utf-8", xml_declaration=False)

print(f"{count} vehículos encontrados y guardados en inventario_plasencia.xml")
