'''
LCRGenie (c) University of Liverpool 2020

LCRGenie is licensed under the MIT License.

To view a copy of this license, visit <http://opensource.org/licenses/MIT/>.

@author:  Zulko
@author:  neilswainston
'''
from collections import OrderedDict

import sbol


def parse(sbol_doc=None, path=None):
    '''Parse SBOL and extract an assembly plan.

    Parameters
    ----------

    sbol_doc
      A PySBOL Document() containing the designs and parts seqs.
      A path to a SBOL .xml file can be provided instead.

    path
      A path to a SBOL .xml file

    Returns
    -------

    (parts_seqs, parts_per_construct, constructs_seqs)
      Assembly plan data:
      - parts_seqs is of the form ``{part_id: 'ATTTGTGTGC...'}``,
      - parts_per_constructs is of the form ``{construct_id: [part_id_1,...]}``
      - constructs_seqs is of the form ``{construct_id: 'ATGCCC...'}``.
    '''
    if path is not None:
        sbol_doc = sbol.Document()
        sbol_doc.read(path)

    parts_seqs = {
        seq.displayId.replace('_sequence', ''): seq.elements.upper()
        for seq in sbol_doc.sequences
    }

    parts_per_construct = [
        (component.displayId, [c.displayId[:-2] for c in component.components])
        for component in sbol_doc.componentDefinitions
        if len(component.components)
    ]

    constructs_seqs = [
        (construct_name, ''.join([parts_seqs[part] for part in parts]))
        for construct_name, parts in parts_per_construct
    ]

    return parts_seqs, \
        OrderedDict(parts_per_construct), \
        OrderedDict(constructs_seqs)
