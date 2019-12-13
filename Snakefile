# Originally from https://raw.githubusercontent.com/dib-lab/2018-ncbi-lineages/63e8dc784af092293362f2e8e671ae03d1a84d1d/Snakefile

rule all:
    input:
        "example_output.profile"

rule download_wgs_acc2taxid:
    output:
        "nucl_wgs.accession2taxid.gz"
    shell:
        "curl -O -L https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz"

rule download_gb_acc2taxid:
    output:
        "nucl_gb.accession2taxid.gz"
    shell:
        "curl -O -L https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz"

rule download_taxdump:
    output:
        "taxdump/nodes.dmp",
        "taxdump/names.dmp"
    shell:
        "curl -L https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz | (mkdir -p taxdump && cd taxdump && tar xzvf -)"

rule make_taxid:
    input:
        "{name}.csv",
        "nucl_gb.accession2taxid.gz",
        "nucl_wgs.accession2taxid.gz",
        "taxdump/nodes.dmp",
        "taxdump/names.dmp"
    output:
        "{name}.profile"
    shell:
        "./opal_report.py {wildcards.name} {input[0]} {input[1]} {input[2]}"

#        "./make-lineage-csv.py taxdump/{{nodes.dmp,names.dmp}} {input[0]} -o {output}"
