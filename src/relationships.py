import arcpy


def get_parent_table(related_table):
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