"""
    AUTHOR: Marco Rondelli
    LICENSE: CC-BY-SA-4.0 license

    DESCRIPTION:
    Extract text from the original .drawio file and create a dedicated JSON file 
    with ISO 639-2:1998 3-letter language codes for translation. The generated 
    JSON will reside in the Translations folder and will look like this:

    Timeline-ABC.JSON
    
    Call this script from the project's root folder like so:

    python ./Scripts/extract.py

    See the list of ISO 639-2 codes here (https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes).
"""
import xml.etree.ElementTree as ET
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(project_root, "Diagrams", "Timeline.drawio")
translations_dir = os.path.join(project_root, "Translations")

lang_code = input("Input the 3-letter lang code: ").upper()

base_name = os.path.splitext(os.path.basename(input_file))[0]
output_file = os.path.join(translations_dir, f"{base_name}-{lang_code}.json")

tree = ET.parse(input_file)
root = tree.getroot()

labels = {}

# Skip numbers on the timeline
for cell in root.iter("mxCell"):
    cell_id = cell.get("id")
    value = cell.get("value")
    if cell_id and value and not ("<h3>" in value and "<span>" in value):
        labels[cell_id] = value

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(labels, f, ensure_ascii=False, indent=2)

print(f"Extracted {len(labels)} labels to {output_file}")