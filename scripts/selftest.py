"""Self-tests for the pack scripts. Stdlib unittest only."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _mdtable
import _packmodel as pm

GOOD = "# T\n\n| id | status |\n|---|---|\n| a | done |\n"


class TestMdtable(unittest.TestCase):
    def test_parses_a_well_formed_table(self):
        t = _mdtable.find_tables(GOOD)[0]
        self.assertEqual(t.header, ["id", "status"])
        self.assertEqual(t.rows, [{"id": "a", "status": "done"}])

    def test_column_names_are_case_insensitive(self):
        text = "# T\n\n| Fact | Value | Verified by | Last verified |\n|---|---|---|---|\n| OS | Windows | AHMAD | 2026-01-01 |\n"
        t = _mdtable.find_tables(text)[0]
        self.assertEqual(t.header, ["Fact", "Value", "Verified by", "Last verified"])
        self.assertEqual(t.rows[0]["last verified"], "2026-01-01")
        self.assertEqual(t.col("Verified by"), ["AHMAD"])

    def test_ragged_row_is_an_error_not_a_silent_skip(self):
        bad = GOOD.replace("| a | done |", "| a | done | extra |")
        with self.assertRaises(_mdtable.TableError):
            _mdtable.find_tables(bad)

    def test_replace_table_round_trips(self):
        t = _mdtable.find_tables(GOOD)[0]
        out = _mdtable.replace_table(GOOD, t, [{"id": "b", "status": "pending"}])
        self.assertIn("| b | pending |", out)
        self.assertNotIn("| a | done |", out)
        self.assertTrue(out.startswith("# T"))

    def test_h2_blocks_split_in_file_order(self):
        blocks = _mdtable.h2_blocks("# H\n## One\na\n## Two\nb\n")
        self.assertEqual([t for t, _ in blocks], ["One", "Two"])
        self.assertEqual(blocks[0][1], "## One\na")

    def test_fenced_blocks_are_found(self):
        self.assertEqual(_mdtable.fenced_blocks("x\n" + chr(96) * 3 + "\nhi\n" + chr(96) * 3 + "\n"), [(2, "hi")])

    def test_an_escaped_pipe_is_not_a_delimiter(self):
        text = "# T\n\n| id | note |\n|---|---|\n| a | " + chr(96) + "x \\| y" + chr(96) + " |\n"
        t = _mdtable.find_tables(text)[0]
        self.assertEqual(t.rows[0]["note"], chr(96) + "x | y" + chr(96))

    def test_render_escapes_a_pipe_inside_a_cell(self):
        out = _mdtable.render(["id", "note"], [{"id": "a", "note": "x|y"}])
        self.assertEqual(out[2], "| a | x\\|y |")
        back = _mdtable.find_tables("# T\n\n" + "\n".join(out) + "\n")[0]
        self.assertEqual(back.rows[0]["note"], "x|y")

    def test_has_answers_for_column_names_ignoring_case(self):
        t = _mdtable.find_tables("# T\n\n| ID | Status |\n|---|---|\n| a | done |\n")[0]
        self.assertTrue(t.has("id"))
        self.assertTrue(t.has("id", "STATUS"))
        self.assertFalse(t.has("owner"))


class TestPackModel(unittest.TestCase):
    def test_a_timestamp_needs_an_offset(self):
        self.assertIsNone(pm.parse_ts("2026-10-13"))
        self.assertIsNone(pm.parse_ts("2026-10-13 10:00"))
        ts = pm.parse_ts("2026-10-13T10:00:00+03:00")
        self.assertIsNotNone(ts)
        self.assertEqual(int(ts.utcoffset().total_seconds()), 10800)

    def test_entries_split_on_h2_and_carry_a_stable_key(self):
        pack = pm.Pack(Path("."))
        text = (pm.BEGIN + "\n## 2026-10-13T10:00:00+03:00 First\nbody a\n"
                "## 2026-10-12T10:00:00+03:00 Second\nbody b\n" + pm.END + "\n")
        pack.read = lambda rel: text
        entries = pack.entries("docs/03-handoff.md")
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].key, "2026-10-13T10:00:00+03:00|2026-10-13T10:00:00+03:00 First")

    def test_no_markers_means_no_entries(self):
        pack = pm.Pack(Path("."))
        pack.read = lambda rel: "## 2026-10-13T10:00:00+03:00 Orphan\n"
        self.assertEqual(pack.entries("docs/03-handoff.md"), [])

    def test_size_counts_the_bytes_git_stores(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "a.md"
            f.write_bytes(b"one\r\ntwo\r\n")
            self.assertEqual(f.stat().st_size, 10)
            self.assertEqual(pm.Pack(Path(d)).size("a.md"), 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
