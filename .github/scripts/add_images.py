import os, json, requests
from lxml import etree
from urllib.parse import quote

tree = etree.parse("epg.xml")
root = tree.getroot()
cache_file = "images.json"
cache = json.load(open(cache_file)) if os.path.exists(cache_file) else {}

def get_image(title):
    t = title.strip().lower()
    if t in cache:
        return cache[t]
    resp = requests.get(
        f"https://api.themoviedb.org/3/search/tv?api_key={os.getenv('TMDB_API_KEY')}&query={quote(t)}"
    ).json()
    image = ""
    if resp.get("results"):
        poster = resp["results"][0].get("poster_path")
        if poster:
            image = f"https://image.tmdb.org/t/p/w500{poster}"
    cache[t] = image
    return image

for prog in root.findall("programme"):
    title = prog.findtext("title")
    if not title:
        continue
    img_url = get_image(title)
    if img_url:
        icon = etree.Element("icon", src=img_url)
        prog.append(icon)

tree.write("epg.xml", pretty_print=True, xml_declaration=True, encoding="UTF-8")
with open("images.json", "w") as f:
    json.dump(cache, f, indent=2)

print("Images added.")
