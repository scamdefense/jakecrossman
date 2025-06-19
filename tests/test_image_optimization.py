import builtins
from pathlib import Path
from image_optimization import ImageOptimizer


def test_run_optimization_summary(monkeypatch, tmp_path, capsys):
    optimizer = ImageOptimizer(base_dir=tmp_path)
    optimizer.images_dir.mkdir(parents=True)
    optimizer.optimized_dir.mkdir(parents=True)

    monkeypatch.setattr(optimizer, "check_dependencies", lambda: True)
    monkeypatch.setattr(optimizer, "create_usage_examples", lambda: None)
    monkeypatch.setattr(optimizer, "get_image_files", lambda: [Path("dummy.jpg")])
    monkeypatch.setattr(optimizer, "get_file_size_mb", lambda path: 2)
    monkeypatch.setattr(
        optimizer,
        "optimize_image",
        lambda path: {
            "original_size": 2,
            "webp_created": True,
            "original_optimized": True,
            "webp_size": 1,
            "optimized_size": 1.5,
            "errors": [],
        },
    )
    monkeypatch.setattr(builtins, "input", lambda: "y")

    optimizer.run_optimization()
    out = capsys.readouterr().out
    assert "WebP total: 1.00 MB (50.0% savings)" in out
    assert "Optimized total: 1.50 MB (25.0% savings)" in out
