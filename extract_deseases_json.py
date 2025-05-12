import json

def extract_features(json_path, lv_parent=2,lv=3):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = []

    def process_children_from_lv(node):
        """
        Đệ quy từ level 3 trở đi: gom title + content + children thành đoạn văn.
        """
        sections = []
        title = node.get("title", "")
        content = node.get("content", "").strip()
        if title or content:
            sections.append(f"{title}: {content}" if title else content)

        for child in node.get("children", []):
            sections.append(process_children_from_lv(child))

        return "\n\n".join(sections)

    def recurse_nodes(nodes):
        for node in nodes:
            if node["level"] == lv_parent:
                entry = {"Bệnh": node.get("header", "")}
                for child in node.get("children", []):
                    child_sections = []
                    
                    if child["level"] == lv:
                        child_sections.append(process_children_from_lv(child))
                    # if child["level"] == 3:
                    #     child_sections.append(process_children_from_lv(child))
                    entry[child["title"]] = "\n\n".join(child_sections).replace(child["title"] + ": ", "").strip()
                result.append(entry)

            elif node["level"] > 2:
                recurse_nodes(node.get("children", []))

    recurse_nodes(data)
    return result
