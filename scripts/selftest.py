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


if __name__ == "__main__":
    unittest.main(verbosity=2)
