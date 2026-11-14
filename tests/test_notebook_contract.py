import json
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_PATH = PROJECT_ROOT / "hospital-data-converter.ipynb"


class TestNotebookContract(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with NOTEBOOK_PATH.open(encoding="utf-8") as notebook_file:
            notebook = json.load(notebook_file)

        source_parts = []

        for cell in notebook["cells"]:
            source = cell.get("source", "")

            if isinstance(source, list):
                source = "".join(source)

            source_parts.append(source)

        cls.source = "\n".join(source_parts)

    def test_notebook_exists(self):
        self.assertTrue(NOTEBOOK_PATH.exists())

    def test_expected_tables_are_referenced(self):
        expected_tables = [
            "patients",
            "encounters",
            "conditions",
            "observations",
            "medications",
            "practitioners",
            "organizations",
        ]

        for table_name in expected_tables:
            self.assertIn(table_name, self.source)

    def test_sql_audit_sections_are_present(self):
        expected_sections = [
            "quality_leaderboard_query",
            "patient_readiness_query",
            "readiness_distribution_query",
            "primary_remediation_query",
        ]

        for section_name in expected_sections:
            self.assertIn(section_name, self.source)


if __name__ == "__main__":
    unittest.main()
    