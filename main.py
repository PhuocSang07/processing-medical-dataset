from extract_deseases_json import extract_features
from fix_markdown import fix_markdown_headers
from format_markdown import parse_markdown_nested
import json
import os

file_name= "benhhoc_3"
lv_parent=3 # lv maximun
lv_child=4 # lv child of lv_parent

### PHASE 1:  Format markdown file
# fixed_lines = fix_markdown_headers(f"markdown/{file_name}.md")
# with open(f"data/data_markdown/{file_name}.md", 'w', encoding='utf-8') as f:
#     f.writelines(fixed_lines)
# print(f"✅ Đã sửa xong file markdown, lưu tại: data/data_markdown/{file_name}.md")

### PHASE 2:  Parse markdown file to JSON Tree
tree_result = parse_markdown_nested(f"data/data_markdown/{file_name}.md", lv_parent)

with open(f"data/tree_json/{file_name}.json", "w", encoding="utf-8") as f:
    json.dump(tree_result, f, ensure_ascii=False, indent=4)

print(f"✅ Đã lưu phân cấp chi tiết vào 'data/tree_json/{file_name}.json'")

### PHASE 3:  Extract disease features from JSON Tree
level3_features = extract_features(f"data/tree_json/{file_name}.json", lv=lv_child)
result = []
for item in level3_features:
    if len(item) > 1:
        result.append(item)

with open(f"data/json/{file_name}.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"✅ Đã lưu dạng feature các mục bệnh vào 'data/json/{file_name}.json'")
