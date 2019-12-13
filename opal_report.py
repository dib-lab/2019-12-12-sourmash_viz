#! /usr/bin/env python


def gen_report(sample_id, ranks, taxonomy_id, program, taxons):
    output = f"""# Taxonomic Profiling Output
@SampleID:{sample_id}
@Version:0.9.3
@Ranks:{ranks}
@TaxonomyID:{taxonomy_id}
@__program__:{program}
@@TAXID\tRANK\tTAXPATH\tTAXPATHSN\tPERCENTAGE
"""
    all_taxons = []
    for tax in taxons:
        tax_line = "\t".join(tax)
        all_taxons.append(tax_line)

    return output + "\n".join(all_taxons)


def test_gen_report():
    output = gen_report("sample", "phylum|genus", "ncbi_2018", "sourmash", taxons=[])

    assert "Version:0.9.3" in output
    assert "@@TAXID\tRANK\tTAXPATH\tTAXPATHSN\tPERCENTAGE" in output

    past_first_line = False
    for line in output.splitlines():
        if not past_first_line:
            assert line.startswith("#")
            past_first_line = True
            continue

        if line.startswith("@@"):
            break

        assert line.startswith("@"), (i, line)


def test_gen_report_2():
    output = gen_report("sample", "phylum|genus", "ncbi_2018", program="sourmash lca", taxons=[])

    assert "sourmash gather" not in output
    assert "sourmash lca" in output


def test_gen_report_3():
    taxons = [
      "2157,superkingdom,2157,Archaea,0.074565".split(","),
      "2,superkingdom,2,Bacteria,99.925435".split(",")
    ]

    output = gen_report("sample", "phylum|genus", "ncbi_2018",
                        program="sourmash lca", taxons=taxons)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--program", type=str, default="sourmash gather")
    parser.add_argument("sample", type=str)
    parser.add_argument("taxonomy", type=str)
    parser.add_argument("-r", "--ranks", type=str,
                        default="superkingdom|phylum|class|order|family|genus|species|strain")
    parser.add_argument("-o", "--output", type=argparse.FileType("wt"), default=None)
    args = parser.parse_args()

    report = gen_report(sample_id=args.sample,
                        taxonomy_id=args.taxonomy,
                        ranks=args.ranks,
                        program=args.program)
    if args.output:
        args.output.write(report)
    else:
        print(report)
