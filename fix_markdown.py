import re

def fix_markdown_headers(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    fixed_lines = []
    for line in lines:
        raw = line.rstrip('\n')
        m = re.match(r'^(#{1,6})\s+(.*)$', raw)
        if not m:
            fixed_lines.append(line)
            continue

        hashes, title = m.groups()
        title = title.strip()

        # Unwrap bold or italic markers to inspect content
        bold_match = re.match(r'^\*\*(.+?)\*\*$', title)
        italic_match = re.match(r'^\*(.+?)\*$', title)
        if bold_match:
            inner = bold_match.group(1).strip()
        elif italic_match:
            inner = italic_match.group(1).strip()
        else:
            inner = title

        # Check for numbered headers (even if wrapped in ** or *)
        is_numbered = (
            re.match(r'^[IVXLCDM]+\.', inner) or
            re.match(r'^\d+\.\d+\.\d+\.\d+', inner) or
            re.match(r'^\d+\.\d+\.\d+', inner) or
            re.match(r'^\d+\.\d+', inner) or
            re.match(r'^\d+\.', inner)
        )

        # Handle bold formatting
        if bold_match:
            if inner.isupper() or is_numbered:
                # keep bold for uppercase or numbered headers
                content = f"**{inner}**"
            else:
                # bold but neither uppercase nor numbered → normal text
                fixed_lines.append(f"{inner}\n")
                continue
        # Handle italic formatting
        elif italic_match:
            if is_numbered:
                # treat numbered italic as header, drop italic markers
                content = inner
            else:
                # italic non-numbered → normal text
                fixed_lines.append(f"{inner}\n")
                continue
        else:
            # Remove stray * or _ that are not part of ** or __
            content = re.sub(r'(?<!\*)\*(?!\*)|(?<!_)_(?!_)', '', title).strip()

        # Determine header level based on plain content
        plain = re.sub(r'^\*\*(.+?)\*\*$', r'\1', content)
        level = 2  # default ##
        if re.match(r'^[IVXLCDM]+\.', plain):
            level = 3
        elif re.match(r'^\d+\.\d+\.\d+\.\d+', plain):
            level = 7  # beyond ###... treat specially or adjust as needed
        elif re.match(r'^\d+\.\d+\.\d+', plain):
            level = 6
        elif re.match(r'^\d+\.\d+', plain):
            level = 5
        elif re.match(r'^\d+\.', plain):
            level = 4

        fixed_lines.append(f"{'#' * level} {content}\n")

    return fixed_lines
