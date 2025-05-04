from extract_deseases_json import extract_level3_features
from fix_markdown import fix_markdown_headers
from format_markdown import parse_markdown_nested
import json
import os

# file_name = 'Chẩn-đoán-và-điều-trị-bệnh-Nội-tiết-chuyển-hóa' 
# file_name = 'HDĐT-Cơ-Xương-Khớp'  
# file_name = "Huong-dan-Chan-doan-va-dieu-tri-mot-so-benh-ly-huyet-hoc" # fail
# file_name = "QD_ban_hanh_HD_chan_doan__dieu_tri_benh_than_man_va_mot_so_benh_ly_than__2024_08_12_f0584"
# file_name = "Truyen-nhiem-1"
file_name= "benhhoc_1"

# fixed_lines = fix_markdown_headers(f"markdown/{file_name}.md")

# with open(f"data/data_markdown/{file_name}.md", 'w', encoding='utf-8') as f:
#     f.writelines(fixed_lines)

# print(f"✅ Đã sửa xong file markdown, lưu tại: data/data_markdown/{file_name}.md")

tree_result = parse_markdown_nested(f"data/data_markdown/{file_name}.md")

with open(f"data/tree_json/{file_name}.json", "w", encoding="utf-8") as f:
    json.dump(tree_result, f, ensure_ascii=False, indent=4)

print(f"✅ Đã lưu phân cấp chi tiết vào 'data/tree_json/{file_name}.json'")


level3_features = extract_level3_features(f"data/tree_json/{file_name}.json", lv=3)
result = []
for item in level3_features:
    if len(item) > 1:
        result.append(item)

with open(f"data/json/{file_name}.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print(f"✅ Đã lưu dạng feature các mục bệnh vào 'data/json/{file_name}.json'")
