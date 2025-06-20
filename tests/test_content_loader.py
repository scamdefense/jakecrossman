from app.content_loader import load_markdown_entries


def test_load_markdown_entries(tmp_path):
    directory = tmp_path / "entries"
    directory.mkdir()
    md = directory / "example.md"
    md.write_text("Title: Example\nDate: 2025-01-01\nImage: test\n\nBody text")

    entries = load_markdown_entries(directory)
    assert len(entries) == 1
    entry = entries[0]
    assert entry["title"] == "Example"
    assert "<p>Body text</p>" in entry["content"]
