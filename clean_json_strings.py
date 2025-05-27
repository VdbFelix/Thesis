def clean_text(file):
    file = file.replace(".", " ")
    return re.sub(r"[^\w\s]", "", file)
#note that this function serves specifically to clean the JOSN strings by replacing periods by spaces

def clean_json_strings(obj):
    if isinstance(obj, dict):
        return {k: clean_json_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_strings(item) for item in obj]
    elif isinstance(obj, str):
        return clean_text(obj)
    else:
        return obj
