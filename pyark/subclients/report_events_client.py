import pyark.cva_client as cva_client
from enum import Enum
from protocols.cva_1_0_0 import ReportEventEntry, Program, ReportEventType, Assembly


class ReportEventsClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_report_events(self, params={}):
        """

        :return:
        """
        more_results = True
        while more_results:
            results, next_page_params = self.get("report-events", params=params)
            report_events = list(map(lambda x: ReportEventEntry.fromJsonDict(x), results))
            if next_page_params:
                params[cva_client.CvaClient.LIMIT_PARAM] = next_page_params[cva_client.CvaClient.LIMIT_PARAM]
                params[cva_client.CvaClient.MARKER_PARAM] = next_page_params[cva_client.CvaClient.MARKER_PARAM]
            else:
                more_results = False
            for report_event in report_events:
                yield report_event

    class OutputEntities(Enum):
        variants = 'variants'
        phenotypes = 'phenotypes'
        genes = 'genes'

    @staticmethod
    def _by_program_and_type(program, report_event_type):
        return "report-events/programs/{program}/types/{type}".format(program=program, type=report_event_type)

    @staticmethod
    def _by_type(report_event_type):
        return "report-events/types/{type}".format(type=report_event_type)

    @staticmethod
    def _by_gene_id(assembly, gene_id):
        return "gene-ids/{assembly}/{gene_id}".format(assembly=assembly, gene_id=gene_id)

    @staticmethod
    def _by_transcript_id(assembly, transcript_id):
        return "transcript-ids/{assembly}/{transcript_id}".format(assembly=assembly, transcript_id=transcript_id)

    @staticmethod
    def _by_gene_symbol(assembly, gene_symbol):
        return "gene-symbols/{assembly}/{gene_symbol}".format(assembly=assembly, gene_symbol=gene_symbol)

    @staticmethod
    def _by_panel(panel_name):
        return "panels/{panel_name}".format(panel_name=panel_name)

    @staticmethod
    def _by_genomic_coordinates(assembly, chromosome, start, end):
        return "genomic-regions/{assembly}/{chromosome}/{start}/{end}".format(
            assembly=assembly, chromosome=chromosome, start=start, end=end)

    def get_variants_by_gene_id(self, program, report_event_type, assembly, gene_id,
                                include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_gene_id(assembly, gene_id),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_transcript_id(self, program, report_event_type, assembly, transcript_id,
                                      include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type transcript_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_transcript_id(assembly, transcript_id),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_gene_symbol(self, program, report_event_type, assembly, gene_symbol,
                                    include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_symbol: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_gene_symbol(assembly, gene_symbol),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_panel(self, report_event_type, panel_name, panel_version,
                              include_aggregations=False, params={}):
        """

        :type report_event_type: ReportEventType
        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_type(report_event_type),
                ReportEventsClient._by_panel(panel_name),
                self.OutputEntities.variants.value]
        if params is None:
            params = {}
        if panel_version:
            params['panel_version'] = panel_version
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_variants_by_genomic_region(self, program, report_event_type, assembly, chromosome, start, end,
                                       include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self.OutputEntities.variants.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_phenotypes_by_gene_id(self, program, report_event_type, assembly, gene_id,
                                  include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_gene_id(assembly, gene_id),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_phenotypes_by_transcript_id(self, program, report_event_type, assembly, transcript_id,
                                        include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type transcript_id: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_transcript_id(assembly, transcript_id),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_phenotypes_by_gene_symbol(self, program, report_event_type, assembly, gene_symbol,
                                      include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type gene_symbol: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_gene_symbol(assembly, gene_symbol),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_phenotypes_by_panel(self, report_event_type, panel_name, panel_version,
                                include_aggregations=False, params={}):
        """

        :type report_event_type: ReportEventType
        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_type(report_event_type),
                ReportEventsClient._by_panel(panel_name),
                self.OutputEntities.phenotypes.value]
        if params is None:
            params = {}
        if panel_version:
            params['panel_version'] = panel_version
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_phenotypes_by_genomic_region(self, program, report_event_type, assembly, chromosome, start, end,
                                         include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self.OutputEntities.phenotypes.value]
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_genes_by_panel(self, report_event_type, panel_name, panel_version,
                           include_aggregations=False, params={}):
        """

        :type report_event_type: ReportEventType
        :type panel_name: str
        :type panel_version: str
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_type(report_event_type),
                ReportEventsClient._by_panel(panel_name),
                self.OutputEntities.genes.value]
        if params is None:
            params = {}
        if panel_version:
            params['panel_version'] = panel_version
        return self.get_aggregation_query(path, include_aggregations, params)

    def get_genes_by_genomic_region(self, program, report_event_type, assembly, chromosome, start, end,
                                    include_aggregations=False, params={}):
        """

        :type program: Program
        :type report_event_type: ReportEventType
        :type assembly: Assembly
        :type chromosome: str
        :type start: int
        :type end: int
        :type include_aggregations: bool
        :type params: dict
        :return:
        """
        path = [ReportEventsClient._by_program_and_type(program, report_event_type),
                ReportEventsClient._by_genomic_coordinates(assembly, chromosome, start, end),
                self.OutputEntities.genes.value]
        return self.get_aggregation_query(path, include_aggregations, params)
