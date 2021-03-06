from pyark import cva_client
from protocols.protocol_7_3.cva import EvidenceEntryAndVariants


class EvidencesClient(cva_client.CvaClient):

    _BASE_ENDPOINT = "evidences"

    def __init__(self, **params):
        cva_client.CvaClient.__init__(self, **params)

    def get_evidences(self, source, max=None, **params):
        url = "{endpoint}/sources/{source}".format(endpoint=self._BASE_ENDPOINT, source=source)
        results = self._paginate(endpoint=url, max=max, **params)
        for r in results:
            yield EvidenceEntryAndVariants.fromJsonDict(r)

    def post_evidences(self, evidence, **params):
        """
        :type evidence: EvidenceEntryAndVariants
        :type params: dict
        :rtype: dict
        """
        return self._post(self._BASE_ENDPOINT, evidence.toJsonDict(), params)
