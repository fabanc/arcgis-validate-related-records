import arcpy


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

        parameters = [in_related_table]

