import os

import pandas as pd
import taxonomy

from gather_to_opal import get_row_taxpath, summarize_all_levels

taxo = None


def setup_module():
    global taxo
    taxo = taxonomy.Taxonomy.from_ncbi(
        os.path.join("taxdump", "nodes.dmp"), os.path.join("taxdump", "names.dmp"),
    )


def test_get_row_taxpath():
    tax_ranks = "superkingdom|phylum|class|order|family|genus|species".split("|")

    test_data = [
        {"accession": "BAHQ02000907", "percentage": 2.928177, "taxid": 1232439}
    ]

    test_df = pd.DataFrame(test_data).set_index("accession")

    tax_df = test_df.astype(object).apply(
        lambda row: get_row_taxpath(row, taxo, tax_ranks), axis=1
    )

    assert len(tax_df) == 1
    assert tax_df.loc["BAHQ02000907"]["rank"] == "species"
    assert tax_df.loc["BAHQ02000907"]["taxpath"] == "2|1239|186801|186802|||1232439"


def test_get_row_taxpath_strain():
    tax_ranks = "superkingdom|phylum|class|order|family|genus|species|strain".split("|")

    test_data = [{"accession": "strain", "percentage": 2.928177, "taxid": 547042}]

    test_df = pd.DataFrame(test_data).set_index("accession")

    tax_df = test_df.astype(object).apply(
        lambda row: get_row_taxpath(row, taxo, tax_ranks), axis=1
    )

    assert len(tax_df) == 1
    assert tax_df.loc["strain"]["rank"] == "strain"
    assert (
        tax_df.loc["strain"]["taxpath"] == "2|976|200643|171549|815|816|387090|547042"
    )


def test_summarize_all_levels():
    tax_ranks = "superkingdom|phylum|class|order|family|genus|species".split("|")

    test_data = [
        {"accession": "BAHQ02000907", "percentage": 2, "taxid": 1232439},
        {"accession": "FCFA01000001", "percentage": 4, "taxid": 33038},
    ]

    test_df = pd.DataFrame(test_data).set_index("accession")

    tax_df = test_df.astype(object).apply(
        lambda row: get_row_taxpath(row, taxo, tax_ranks), axis=1
    )

    summary_df = summarize_all_levels(tax_df, tax_ranks)

    assert len(summary_df) == len(summary_df["taxid"].unique())

    summary_df.set_index("taxid", inplace=True)

    assert len(summary_df) == 8
    assert summary_df.loc["2"]["percentage"] == 6
    assert len(summary_df[summary_df["rank"] == "species"]) == 2


def test_summarize_all_levels_strain():
    tax_ranks = "superkingdom|phylum|class|order|family|genus|species|strain".split("|")

    test_data = [
        {"accession": "strain1", "percentage": 2, "taxid": 999407},
        {"accession": "strain2", "percentage": 4, "taxid": 742735},
    ]

    test_df = pd.DataFrame(test_data).set_index("accession")

    tax_df = test_df.apply(lambda row: get_row_taxpath(row, taxo, tax_ranks), axis=1)

    summary_df = summarize_all_levels(tax_df, tax_ranks)

    assert len(summary_df) == len(summary_df["taxid"].unique())

    summary_df.set_index("taxid", inplace=True)

    # one item for each rank in the lineage, except for strain (which has two)
    assert len(summary_df) == 9

    assert summary_df.loc["2"]["percentage"] == 6
    assert summary_df.loc["1531"]["percentage"] == 6
    assert len(summary_df[summary_df["rank"] == "species"]) == 1


def test_summarize_all_levels_subspecies():
    tax_ranks = "superkingdom|phylum|class|order|family|genus|species|strain".split("|")

    test_data = [
        {"accession": "subspecies", "percentage": 2, "taxid": 644357},
    ]

    test_df = pd.DataFrame(test_data).set_index("accession")

    tax_df = test_df.apply(lambda row: get_row_taxpath(row, taxo, tax_ranks), axis=1)

    summary_df = summarize_all_levels(tax_df, tax_ranks)

    assert len(summary_df) == len(summary_df["taxid"].unique())

    summary_df.set_index("taxid", inplace=True)

    # since subspecies is not in tax_ranks, summary_df will have 7 items,
    # one for each level of the lineage (except strain)
    assert len(summary_df) == 7

    assert summary_df.loc["2"]["percentage"] == 2
    assert summary_df.loc["2371"]["percentage"] == 2
    assert len(summary_df[summary_df["rank"] == "species"]) == 1
