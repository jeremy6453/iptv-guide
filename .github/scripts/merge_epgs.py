import os
import requests
from lxml import etree

iptv_url = os.environ['IPTV_EPG']
nz_url = os.environ['NZ_EPG']

iptv = etree.fromstring(requests.get(iptv_url).content)
nz = etree.fromstring(requests.get(nz_url).content)

merged = etree.Element("tv", attrib=iptv.attrib)
iptv_channels = set()

for ch in iptv.findall("channel"):
    iptv_channels.add(ch.get("id"))
    merged.append(ch)

for ch in nz.findall("channel"):
    if ch.get("id") not in iptv_channels:
        merged.append(ch)

programmes = {}
for p in iptv.findall("programme"):
    key = (p.get("start"), p.get("channel"))
    programmes[key] = p

for p in nz.findall("programme"):
    key = (p.get("start"), p.get("channel"))
    programmes[key] = p

for p in sorted(programmes.values(), key=lambda x: x.get("start")):
    merged.append(p)

with open("epg.xml", "wb") as f:
    f.write(etree.tostring(merged, pretty_print=True, xml_declaration=True, encoding="UTF-8"))

print("epg.xml generated successfully!")
