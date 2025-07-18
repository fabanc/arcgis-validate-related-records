import arcpy
import os
import unittest
from unittest import TestCase

import src.relationships as relationships

if __name__ == '__main__':
    unittest.main()


class TestRelationships(TestCase):
    test_dir = os.path.dirname(os.path.realpath(__file__))
    test_data_input = os.path.join(test_dir, "data", "input")
    test_data_output = os.path.join(test_dir, "data", "output")
    database_name = "RelationTestCasesSimple.gdb"
    database_path = os.path.join(test_data_output, database_name)

    def setUp(self):
        """
        Set up the file geodatabase and any necessary data for the tests from
        our XML template.
        :return:
        """

        # Delete the database if it exists (has been created in a previous test run)
        if arcpy.Exists(self.database_path):
            arcpy.management.Delete(self.database_path)

        xml_template = os.path.join(self.test_data_input, "RelationTestCasesSimple.xml")
        if not os.path.exists(xml_template):
            raise FileNotFoundError(f"XML template not found: {xml_template}")

        arcpy.management.CreateFileGDB(self.test_data_output, self.database_name)
        arcpy.management.ImportXMLWorkspaceDocument(
            self.database_path,
            xml_template,
            import_type="DATA"
        )

    def test_get_parent_relation(self):
        """
        Test the get_parent_table function returns a result when a table is related to a parent table, and
        that is returns None when the table is not related to a parent table.
        :return:
        """

        related_table = os.path.join(self.database_path, "accomodation_type")
        unrelated_feature_class = os.path.join(self.database_path, "pois")
        unrelated_table = os.path.join(self.database_path, "version")

        parent = relationships.get_parent_relation(related_table)
        self.assertIsNotNone(parent)

        parent = relationships.get_parent_relation(unrelated_table)
        self.assertIsNone(parent)

        parent = relationships.get_parent_relation(unrelated_feature_class)
        self.assertIsNone(parent)

    def test_get_unique_field_value(self):
        """
        Test the get_unique_field_value function returns a set of unique values from a field in a table.
        :return:
        """

        table = os.path.join(self.database_path, "accomodation_type")
        field = 'PARENT_ID'
        unique_values = relationships.get_unique_field_value(table, field)
        self.assertEqual(3, len(unique_values))

        table = os.path.join(self.database_path, "version")
        field = 'OBJECTID'
        unique_values = relationships.get_unique_field_value(table, field)
        self.assertEqual(0, len(unique_values))

        table = os.path.join(self.database_path, "pois")
        field = 'OBJECTID'
        unique_values = relationships.get_unique_field_value(table, field)
        self.assertEqual(0, len(unique_values))

    def test_find_orphaned_related_records(self):
        table = os.path.join(self.database_path, "accomodation_type")
        orphans = relationships.find_orphaned_related_records(table)
        self.assertEqual(2, len(orphans))

        # Check the function returns an error if the table is not related to a parent table
        table = os.path.join(self.database_path, "version")
        with self.assertRaises(Exception) as context:
            relationships.find_orphaned_related_records(table)
        ex = context.exception
        self.assertEqual(str(ex), f"Relationship class not found for {table}")

        # Check the function returns an error if the feature class is not related to a parent table
        table = os.path.join(self.database_path, "pois")
        with self.assertRaises(Exception) as context:
            relationships.find_orphaned_related_records(table)
        ex = context.exception
        self.assertEqual(str(ex), f"Relationship class not found for {table}")