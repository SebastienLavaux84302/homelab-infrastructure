import importlib.util
import unittest
from pathlib import Path


path = Path(__file__).resolve().parents[1] / "roles/lab_sonarqube/filter_plugins/java_properties.py"
spec = importlib.util.spec_from_file_location("java_properties", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class JavaPropertyTests(unittest.TestCase):
    def test_backslash_spaces_and_separators(self):
        self.assertEqual(module.java_property(" a\\b:c=d#!"), r"\ a\\b\:c\=d\#\!")

    def test_control_characters_and_unicode(self):
        self.assertEqual(module.java_property("é\t\n😀"), r"\u00e9\t\n\ud83d\ude00")

    def test_rejects_nul_and_non_string(self):
        with self.assertRaises(module.AnsibleFilterError):
            module.java_property("bad\x00value")
        with self.assertRaises(module.AnsibleFilterError):
            module.java_property(None)


if __name__ == "__main__":
    unittest.main()
