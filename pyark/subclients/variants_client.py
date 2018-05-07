import pyark.cva_client as cva_client
from protocols.cva_1_0_0 import Variant


class VariantsClient(cva_client.CvaClient):

    def __init__(self, url_base, token):
        cva_client.CvaClient.__init__(self, url_base, token=token)

    def get_variant_by_id(self, identifier):
        """

        :param identifier:
        :type identifier: str
        :return:
        :rtype: Variant
        """
        results, _ = self.get("variants/{identifier}".format(identifier=identifier))
        assert len(results) == 1, "Unexpected number of variants returned when searching by identifier"
        variant = Variant.fromJsonDict(results[0])
        return variant
