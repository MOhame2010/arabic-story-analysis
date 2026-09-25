import os
import json
import yaml

IGNORED_LEVELS = ["01-text-identity"]

def load_structure():
    if not os.path.exists("structure.yaml"):
        return {}
    with open("structure.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def generate_yaml(fields):
    data = {}
    if fields:
        for key, field in fields.items():
            data[key] = field.get("value", "") if isinstance(field, dict) else ""
    return data

def generate_schema(title, fields):
    properties = {}
    required = []
    
    if fields:
        for key, field in fields.items():
            field_type = field.get("type", "string") if isinstance(field, dict) else "string"
            properties[key] = {
                "type": field_type,
                "description": f"حقل {key}"
            }
            required.append(key)
        
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": title,
        "type": "object",
        "properties": properties,
        "required": required
    }

def main():
    structure = load_structure()
    levels = structure.get("levels", {})
    
    for level_dir, level_info in levels.items():
        if level_dir in IGNORED_LEVELS:
            print(f"تخطي المستوى: {level_dir} (مستثنى)")
            continue
            
        if not os.path.exists(level_dir):
            os.makedirs(level_dir)
            
        level_info = level_info or {}
        title = level_info.get("title", level_dir)
        fields = level_info.get("fields", {})
        
        # 1. generate data.yaml
        yaml_data = generate_yaml(fields)
        yaml_path = os.path.join(level_dir, "data.yaml")
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
            
        # 2. generate data.json
        json_path = os.path.join(level_dir, "data.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(yaml_data, f, ensure_ascii=False, indent=2)
            
        # 3. generate schema.json
        schema_data = generate_schema(title, fields)
        schema_path = os.path.join(level_dir, "schema.json")
        with open(schema_path, "w", encoding="utf-8") as f:
            json.dump(schema_data, f, ensure_ascii=False, indent=2)
            
        print(f"تم إنشاء الملفات في: {level_dir}")

if __name__ == "__main__":
    main()
