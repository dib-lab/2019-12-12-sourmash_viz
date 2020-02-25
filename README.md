# gather to opal

Take a gather CSV and one or more NCBI 'accession2taxid' files
and create
1) csv containing accessions, taxid
2) csv with lineage

run:
```bash
python gather-to-opal.py example_output.csv \
    --acc2taxid_files nucl_gb.accession2taxid.gz \
    --acc2taxid_filesnucl_wgs.accession2taxid.gz
```
