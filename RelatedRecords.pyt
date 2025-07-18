import arcpy
from src.relationships import orphaned_records_to_table

class Toolbox(object):
    def __init__(self):
        self.label =  "RelatedRecords"
        self.alias  = "Related Records"
        self.tools = [FindOrphanedRelatedRecords]


class FindOrphanedRelatedRecords(object):
    def __init__(self):
        self.label       = "Find Orphaned Related Records"
        self.description = "Find Orphaned Related Records and return a list of Object IDs that are not related to any parent records."

    def getParameterInfo(self):
        """
        Define the parameters for the tool.
        :return: the list of variables used as parameters for the tool.
        """
        in_related_table = arcpy.Parameter(
            displayName="Related Table",
            name="in_related_table",
            datatype="GPTableView",
            parameterType="Required",
            direction="Input"
        )

        out_orphaned_table = arcpy.Parameter(
            displayName="Orphaned Records Table",
            name="out_orphaned_table",
            datatype="GPTableView",
            parameterType="Required",
            direction="Output"
        )
        parameters = [in_related_table, out_orphaned_table]

        return parameters

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        # Get the input table parameter
        related_table = parameters[0].valueAsText
        out_orphaned_table = parameters[1].valueAsText
        orphaned_records_to_table(related_table, out_orphaned_table)
