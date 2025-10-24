"""
    AUTHOR: Marco Rondelli
    LICENSE: CC-BY-SA-4.0 license

    DESCRIPTION:
    Generate a new .drawio diagram using the selected JSON file.
    The newly created .drawio file will reside in the Diagrams folder and 
    will look like this:

    Timeline-ABC.drawio
    
    Call this script from the project's root folder like so:

    python ./Scripts/update.py

    See the list of ISO 639-2 codes here (https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes).
"""
import xml.etree.ElementTree as ET
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(project_root, "Diagrams", "Timeline.drawio")

translations_dir = os.path.join(project_root, "Translations")
diagrams_dir = os.path.join(project_root, "Diagrams")

lang_code = input("Input the 3-letter lang code: ").upper()

base_name = os.path.splitext(os.path.basename(input_file))[0]
translation_name = f"{base_name}-{lang_code}.json"
translations_file = os.path.join(translations_dir, translation_name)

if not os.path.exists(translations_file):
    print(f"Error: {translations_file} does not exist.")
    exit(1)

tree = ET.parse(input_file)
root = tree.getroot()

with open(translations_file, "r", encoding="utf-8") as f:
    translations = json.load(f)

for cell in root.iter("mxCell"):
    cell_id = cell.get("id")
    if cell_id and cell_id in translations:
        cell.set("value", translations[cell_id])

output_file = os.path.join(diagrams_dir, f"{base_name}-{lang_code}.drawio")

tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"Created translated diagram: {output_file}")