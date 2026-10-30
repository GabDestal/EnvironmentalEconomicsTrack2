from config import OUT_DIR, ROOT

SECTION_3 = ROOT / "paper" / "03_summary_statistics.md"


def test_section_3_tables_are_the_generated_ones():
    paper = SECTION_3.read_text(encoding="utf-8")
    for name in ("table_summary.md", "txx_baseline.md"):
        table = (OUT_DIR / name).read_text(encoding="utf-8").strip()
        assert table in paper, f"outputs/{name} differs from the table in {SECTION_3.name}: paste it again"
