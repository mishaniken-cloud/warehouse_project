import sqlite3
import json
import csv
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import yaml

DB_NAME = 'warehouse.db'
OUT_DIR = 'out'

def get_connection():
    return sqlite3.connect(DB_NAME)

def fetch_data():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id, p.name, p.category_id, c.name as category_name 
        FROM Product p 
        JOIN Category c ON p.category_id = c.id
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def prepare_nested_data(rows):
    data = []
    for row in rows:
        data.append({
            "id": row['id'],
            "name": row['name'],
            "category": {
                "id": row['category_id'],
                "name": row['category_name']
            }
        })
    return data

def export_json(data):
    with open(os.path.join(OUT_DIR, 'data.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def export_csv(rows):
    with open(os.path.join(OUT_DIR, 'data.csv'), 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'name', 'category_id', 'category_name'])
        for row in rows:
            writer.writerow([row['id'], row['name'], row['category_id'], row['category_name']])

def export_xml(data):
    root = ET.Element('products')
    for item in data:
        prod = ET.SubElement(root, 'product')
        ET.SubElement(prod, 'id').text = str(item['id'])
        ET.SubElement(prod, 'name').text = item['name']
        cat = ET.SubElement(prod, 'category')
        ET.SubElement(cat, 'id').text = str(item['category']['id'])
        ET.SubElement(cat, 'name').text = item['category']['name']
    
    xml_str = ET.tostring(root, encoding='unicode')
    dom = xml.dom.minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent='  ')
    lines = pretty_xml.split('\n')
    if lines and lines[0].strip() == '':
        lines = lines[1:]
    pretty_xml = '\n'.join(lines)
    
    with open(os.path.join(OUT_DIR, 'data.xml'), 'w', encoding='utf-8') as f:
        f.write(pretty_xml)

def export_yaml(data):
    with open(os.path.join(OUT_DIR, 'data.yaml'), 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    rows = fetch_data()
    nested_data = prepare_nested_data(rows)
    export_json(nested_data)
    export_csv(rows)
    export_xml(nested_data)
    export_yaml(nested_data)

if __name__ == "__main__":
    main()