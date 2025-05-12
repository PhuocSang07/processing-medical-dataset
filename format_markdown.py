import re
import json

def parse_markdown_nested(file_path, lv=3):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Tìm các headers từ cấp 2 đến cấp 6
    # header_pattern = re.compile(r'^(#{2,8})\s+\*+\s*(.*?)\*+\s*$', re.MULTILINE)
    header_pattern = re.compile(r'^(#{1,8})\s+\*?(.*?)\*?\s*$', re.MULTILINE)
    headers = list(header_pattern.finditer(content))

    def build_tree(headers, content):
        stack = []
        root = []

        for i, header in enumerate(headers):
            level = len(header.group(1))  # số lượng dấu #
            title = header.group(2).strip()
            start = header.end()
            end = headers[i + 1].start() if i + 1 < len(headers) else len(content)
            body = content[start:end].strip()

            node = {}
            if level == lv:
                node["header"] = title.strip()
            else:
                node["title"] = title.strip()

            node["level"] = level
            node["content"] = body.strip()
            node["children"] = []

            # Gỡ node cũ ra khỏi stack nếu cùng hoặc cao hơn level
            while stack and stack[-1]["level"] >= level:
                stack.pop()

            if not stack:
                root.append(node)
            else:
                stack[-1]["children"].append(node)

            stack.append(node)

        return root

    return build_tree(headers, content)
