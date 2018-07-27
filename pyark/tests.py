import logging
import os
from unittest import TestCase

from mock import patch
from protocols.cva_1_0_0 import ReportEventType, Assembly, Variant, PedigreeInjectRD, ParticipantInjectCancer
from protocols.reports_5_0_0 import Program
from protocols.util import dependency_manager
from protocols.util.factories.avro_factory import GenericFactoryAvro
from requests import ConnectionError

from pyark.cva_client import CvaClient
from pyark.errors import CvaClientError, CvaServerError


class TestPyArk (TestCase):
    # credentials
    CVA_URL_BASE = os.getenv("CVA_URL")
    GEL_USER = os.getenv("GEL_USER")
    GEL_PASSWORD = os.getenv("GEL_PASSWORD")

    def setUp(self):
        logging.basicConfig(level=logging.INFO)
        if self.GEL_PASSWORD is None:
            self.GEL_PASSWORD = ""
        if not self.CVA_URL_BASE or not self.GEL_USER:
            logging.error("Please set the configuration environment variables: CVA_URL, GEL_USER, GEL_PASSWORD")
            raise ValueError("Missing config")
        self.cva = CvaClient(self.CVA_URL_BASE, user=self.GEL_USER, password=self.GEL_PASSWORD)
        self.report_events = self.cva.report_events()
        self.panels = self.cva.panels()
        self.cases = self.cva.cases()
        self.variants = self.cva.variants()
        self.data_intake = self.cva.data_intake()

    def test_get_report_events(self):

        # all_report_events = self.report_events.get_report_events()
        # page_count = 0
        # for batch_report_events in all_report_events:
        #     self.assertTrue(batch_report_events is not None)
        #     # self.assertEqual(len(batch_report_events), 200)
        #     # logging.info("Returned {} report events".format(len(batch_report_events)))
        #     page_count += 1
        #     if page_count == 5:
        #         break
        # self.assertEqual(page_count, 5)

        all_report_events = self.report_events.get_report_events({'limit': 10})
        page_count = 0
        for batch_report_events in all_report_events:
            self.assertTrue(batch_report_events is not None)
            # self.assertEqual(len(batch_report_events), 10)
            # logging.info("Returned {} report events".format(len(batch_report_events)))
            page_count += 1
            if page_count == 5:
                break
        self.assertEqual(page_count, 5)

    def test_get_by_gene_id(self):

        gene_id = "ENSG00000130826"

        # gets variants
        results = self.report_events.get_variants_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_gene_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_transcript_id(self):

        tx_id = "ENST00000426673"

        # gets variants
        results = self.report_events.get_variants_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_transcript_id(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_gene_symbol(self):

        gene_symbol = "BRCA1"

        # gets variants
        results = self.report_events.get_variants_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_gene_symbol(
            Program.rare_disease, ReportEventType.tiered, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variants_by_genomic_region(self):

        assembly = Assembly.GRCh38
        chromosome = 7
        start = 1000000
        end = 2000000

        # gets variants
        results = self.report_events.get_variants_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_variants_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.report_events.get_phenotypes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_phenotypes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets genes
        results = self.report_events.get_genes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.report_events.get_genes_by_genomic_region(
            Program.rare_disease, ReportEventType.tiered,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_all_panels(self):

        panels = self.panels.get_all_panels()
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, list))

    def test_get_panel_summary(self):

        panels = self.panels.get_panels_summary(Program.rare_disease)
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, list))

        panels = self.panels.get_panels_summary(Program.cancer)
        self.assertTrue(panels is not None)
        self.assertTrue(isinstance(panels, list))

    def test_cases_get_by_gene_id(self):

        gene_id = "ENSG00000130826"

        # gets variants
        results = self.cases.get_variants_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_gene_id(
            Program.rare_disease, Assembly.GRCh38,
            gene_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_transcript_id(self):

        tx_id = "ENST00000426673"

        # gets variants
        results = self.cases.get_variants_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_transcript_id(
            Program.rare_disease, Assembly.GRCh38,
            tx_id, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_gene_symbol(self):

        gene_symbol = "BRCA1"

        # gets variants
        results = self.cases.get_variants_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_gene_symbol(
            Program.rare_disease, Assembly.GRCh38,
            gene_symbol, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_cases_variants_by_panel(self):

        panel_name = "cakut"

        # gets variants
        results = self.cases.get_variants_by_panel(Program.rare_disease, panel_name, None, params={'has_reported': True}, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_panel(Program.rare_disease, panel_name, None, params={'has_reported': True}, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results[0], dict))

    def test_get_cases_variants_by_genomic_region(self):

        assembly = Assembly.GRCh38
        chromosome = 7
        start = 1000000
        end = 2000000

        # gets variants
        results = self.cases.get_variants_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_variants_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets phenotypes
        results = self.cases.get_phenotypes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_phenotypes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

        # gets genes
        results = self.cases.get_genes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=False)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, list))

        results = self.cases.get_genes_by_genomic_region(
            Program.rare_disease,
            assembly, chromosome, start, end, include_aggregations=True)
        self.assertTrue(results is not None)
        self.assertTrue(isinstance(results, dict))

    def test_get_variant_by_id(self):

        identifier = "GRCh38: 9: 110303682:C:G"

        # gets variant
        variant = self.variants.get_variant_by_id(identifier=identifier)
        self.assertTrue(variant is not None)
        self.assertTrue(isinstance(variant, Variant))

        # non existing variant
        variant = self.variants.get_variant_by_id(identifier='whatever')
        self.assertFalse(variant)

    def test_get_variants_by_id(self):

        identifiers = ["GRCh38: 9: 110303682:C:G", "GRCh38: 4:  56810156:G:A", "GRCh38:12:  51346624:A:C"]
        variants = self.variants.get_variants_by_id(identifiers=identifiers)
        self.assertTrue(variants is not None)
        self.assertTrue(isinstance(variants, dict))
        self.assertTrue(len(variants) == len(identifiers))
        [self.assertTrue(variants[v] is not None) for v in identifiers]

        non_existing_identifiers = ['whatever', 'this', 'that']
        variants = self.variants.get_variants_by_id(identifiers=non_existing_identifiers)
        self.assertTrue(variants is not None)
        self.assertTrue(isinstance(variants, dict))
        self.assertTrue(len(variants) == len(non_existing_identifiers))
        [self.assertTrue(variants[v] is None) for v in non_existing_identifiers]

        mixed_identifiers = ['whatever', "GRCh38: 9: 110303682:C:G"]
        variants = self.variants.get_variants_by_id(identifiers=mixed_identifiers)
        self.assertTrue(variants is not None)
        self.assertTrue(isinstance(variants, dict))
        self.assertTrue(len(variants) == len(mixed_identifiers))
        self.assertTrue(variants[mixed_identifiers[0]] is None)
        self.assertTrue(variants[mixed_identifiers[1]] is not None)

    def test_post_pedigree(self):
        self._test_post(PedigreeInjectRD, self.data_intake.post_pedigree)

    def test_post_participant(self):
        self._test_post(ParticipantInjectCancer, self.data_intake.post_participant)

    def test_get_transactions(self):
        client = self.cva.transactions()
        id_of_a_transaction = client.get_transactions(params={'limit': 1})[0][0]['id']
        self.assertTrue(client.get_transaction(id_of_a_transaction))
        try:
            self.assertTrue(client.retry_transaction(id_of_a_transaction))
        except CvaServerError as e:
            # this should be a Done transaction so you can't retry it
            self.assertTrue("cannot be retried" in e.message)

    def test_get_transaction_status_only(self):
        client = self.cva.transactions()
        id_of_a_transaction = client.get_transactions(params={'limit': 1})[0][0]['id']
        self.assertEqual(client.get_transaction(id_of_a_transaction, just_return_status=True), 'DONE')

    def test_get_transaction_status_only_fails_if_no_results(self):
        client = self.cva.transactions()
        self.assertRaises(
            CvaClientError,
            lambda: client.get_transaction("notreal", just_return_status=True)
        )

    def test_errors_if_cva_down(self):
        self.assertRaises(
            ConnectionError,
            lambda: CvaClient("https://nowhere.invalid", user='u', password='p').panels().get_all_panels()
        )

    @patch('requests.sessions.Session.get')
    @patch('requests.sessions.Session.post')
    def test_errors_if_4xx(self, post, get):
        self._mock_panels_to_return(get, post, 400)
        self.assertRaises(
            CvaClientError,
            lambda: CvaClient("https://nowhere.invalid", user='u', password='p').panels().get_all_panels()
        )

    @patch('requests.sessions.Session.get')
    @patch('requests.sessions.Session.post')
    def test_errors_if_5xx(self, post, get):
        self._mock_panels_to_return(get, post, 500)
        self.assertRaises(
            CvaServerError,
            lambda: CvaClient("https://nowhere.invalid", user='u', password='p').panels().get_all_panels()
        )

    @patch('requests.sessions.Session.get')
    @patch('requests.sessions.Session.post')
    def test_returns_empty_if_no_results(self, post, get):
        self._mock_panels_to_return(get, post, 200)
        self.assertEqual([],
                         CvaClient("https://nowhere.invalid", user='u', password='p').panels().get_all_panels())

    @staticmethod
    def _mock_panels_to_return(get, post, status_code):
        auth_response = MockResponse(status_code, {'response': [{'result': [{'token': 'xyz'}]}]})
        post.return_value = auth_response
        response = MockResponse(status_code, {})
        get.return_value = response

    def _test_post(self, clazz, post_function):
        model = GenericFactoryAvro.get_factory_avro(
            clazz=clazz,
            version=dependency_manager.VERSION_70,
            fill_nullables=False,
        ).create()

        response = post_function(model)
        # this is stronger than it looks because post checks for errors
        self.assertTrue(response is not None)


class MockResponse:
    def __init__(self, status_code, json_dict):
        self.status_code = status_code
        self.json_dict = json_dict
        self.content = str(json_dict)
        self.text = str(json_dict)
        self.headers = {}

    @staticmethod
    def get(key, default):
        return None

    def json(self):
        return self.json_dict
