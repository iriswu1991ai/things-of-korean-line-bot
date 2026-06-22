import json
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORK_DIR = os.path.join(PROJECT_ROOT, "work", "krdict")
PACKAGE_DIR = os.path.join(PROJECT_ROOT, "work", "python-packages")
sys.path.insert(0, PACKAGE_DIR)

from opencc import OpenCC
from wordfreq import zipf_frequency


def read_json(name, fallback):
    path = os.path.join(WORK_DIR, name)
    if not os.path.exists(path):
        return fallback
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def write_json(name, value):
    path = os.path.join(WORK_DIR, name)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write("\n")


index = read_json("index.json", [])
frequencies = {}

for item in index:
    word = item["word"]
    if word not in frequencies:
        frequencies[word] = zipf_frequency(word, "ko")

write_json("frequencies.json", frequencies)
print(f"Frequency scores: {len(frequencies)}")

entries = read_json("entries.json", [])
if entries:
    converter = OpenCC("s2twp")
    for entry in entries:
        entry["translation"] = converter.convert(entry.get("translation", ""))
        entry["definitionZh"] = converter.convert(entry.get("definitionZh", ""))
    write_json("entries.json", entries)
    print(f"Traditional Chinese converted: {len(entries)}")
