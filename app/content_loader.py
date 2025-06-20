import os
from markdown import markdown


def load_markdown_entries(directory):
    """Load markdown files from a directory into structured entries."""
    entries = []
    if not os.path.isdir(directory):
        return entries

    for filename in sorted(os.listdir(directory)):
        if not filename.endswith(".md"):
            continue
        path = os.path.join(directory, filename)
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        meta = {}
        body = []
        in_meta = True
        for line in lines:
            if in_meta and line.strip() == "":
                in_meta = False
                continue
            if in_meta and ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip().lower()] = value.strip()
            else:
                body.append(line)
        html = markdown("\n".join(body))
        entries.append(
            {
                "slug": os.path.splitext(filename)[0],
                "title": meta.get(
                    "title", os.path.splitext(filename)[0].replace("-", " ").title()
                ),
                "date": meta.get("date", ""),
                "image": meta.get("image", ""),
                "content": html,
            }
        )

    entries.sort(key=lambda e: e.get("date", ""), reverse=True)
    return entries
