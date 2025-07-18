import arcpy
import os

def get_parent_relation(related_table):
    """
    Get the parent table of a related table.
    :param related_table: The name of the related table.
    :return: The name of the parent table.
    """
    desc = arcpy.Describe(related_table)
    if desc.relationshipClassNames:
        return desc.relationshipClassNames[0]
    return None

def get_unique_field_value(table, field):
    """
    Get the unique value of a field in a table.
    :param table: The name of the table.
    :param field: The name of the field.
    :return: The unique value of the field.
    """
    output  = []
    with arcpy.da.SearchCursor(table, [field]) as cursor:
        for row in cursor:
            output.append(row[0])
    return set(output)

def find_relationship_by_name(workspace, relation_name):
    """
    Find a relationship class by its name in a given workspace.
    :param workspace: The workspace where the relationship class is located.
    :param relation_name: The name of the relationship class.
    :return: The relationship class if found, otherwise None.
    """
    workspace_description = arcpy.da.Describe(workspace)
    for child in workspace_description['children']:
        if child['name'] == relation_name and child['dataElementType'] == 'DERelationshipClass':
            return child
    return None


def find_orphaned_related_records(related_table):
    """
    Find orphaned related records in a related table.
    :param related_table: The name of the related table.
    :return: A list of Object IDs that are not related to any parent records.
    """
    relation_name = get_parent_relation(related_table)
    if not relation_name:
        raise Exception(f"Relationship class not found for {related_table}")

    # Get the workspace of the related table and the list of its relationship
    related_table_desc = arcpy.da.Describe(related_table)
    workspace = related_table_desc['path']
    relation_des = find_relationship_by_name(workspace, relation_name)
    parent_feature_class = os.path.join(workspace, relation_des['originClassNames'][0])
    parent_key = relation_des['originClassKeys'][0][0]
    child_key = relation_des['originClassKeys'][1][0]

    parent_ids = get_unique_field_value(parent_feature_class, parent_key)
    child_ids = get_unique_field_value(related_table, child_key)
    orphaned_ids = child_ids - parent_ids
    return orphaned_ids


