import os

import pandas as pd
import taxonomy

from gather_to_opal import get_row_taxpath, summarize_all_levels

taxo = None


def setup_module():
    global taxo
    taxo = taxonomy.Taxonomy.from_ncbi(
        os.path.join("taxdump", "nodes.dmp"), os.path.join("taxdump", "names.dmp")
    )


def test_get_row_taxpath():
    tax_ranks = "superkingdom|phylum|class|order|family|genus|species".split("|")

    test_data = [{
    'accession': 'BAHQ02000907',
    'percentage': 2.928177,
    'taxid': 1232439,
    }]

    test_df = pd.DataFrame(test_data).set_index("accession")

    tax_df = test_df.apply(lambda row: get_row_taxpath(row, taxo, tax_ranks), axis=1)

    assert len(tax_df) == 1
    assert tax_df.loc["BAHQ02000907"]["rank"] == "species"
    assert tax_df.loc["BAHQ02000907"]["taxpath"] == "2|1239|186801|186802|||1232439"


def test_summarize_all_levels():
    pass
