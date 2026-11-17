import unittest
from app import build_schema

class SchemaTests(unittest.TestCase):
    def test_generates_sql(self):
        result = build_schema(
            "Entities are Student, Course and Enrollment. "
            "A Student has name and email. A Course has title. "
            "A Student enrolls in many Courses through Enrollment."
        )
        self.assertTrue(result["entities"])
        self.assertIn("CREATE TABLE", result["sql"])
        self.assertIn("PRIMARY KEY", result["sql"])

if __name__ == "__main__":
    unittest.main()
