#! /usr/bin/env python
"""
Take a GATHER OUTPUT file [full of accessions] and one or more NCBI 'accession2taxid' files
and create a CSV named 'gather_csv.taxid' that contains the accessions
and their associated taxids.
"""

from __future__ import print_function
import argparse
import gzip
import re
import pandas as pd

import sys
import csv

import ncbi_taxdump_utils

def get_taxid(gather_csv, acc2taxid_files):

    gather_info = pd.read_csv(gather_csv)
    # grab the acc from gather column `name`
    gather_info["accession"] = gather_info["name"].str.replace("\s.*", "")
    m = 0
    # init opal_info df
    opal_info = gather_info[["accession", "f_unique_weighted"]]
    opal_info.set_index("accession")
    acc_set = set(opal_info["accession"])

    for filename in args.acc2taxid_files:
        if not acc_set: break

        xopen = open
        if filename.endswith('.gz'):
            xopen = gzip.open

        with xopen(filename, 'rt') as fp: # ruun through acc2taxid files
            next(fp)                #  skip headers
            for n, line in enumerate(fp):
                if not acc_set: break

                if n and n % 1000000 == 0:
                    print(u'\r\033[K', end=u'')
                    print('... read {} lines of {}; found {} of {}'.format(n, filename, m, m + len(acc_set)), end='\r')

                try:
                    acc, _, taxid, _ = line.split()
                except ValueError:
                    print('ignoring line', (line,))
                    continue

                if acc in acc_set:
                    # not currently working
                    import pdb;pdb.set_trace()

                    m += 1
                    opal_info[acc]["taxid"]= taxid
                    acc_set.remove(acc)

                    if not acc_set:
                        break
    if acc_set:
        print('failed to find {} acc'.format(len(acc_set)))
    else:
        print('found all {} accessions!'.format(m))

    #hacky for now
    opal_info.to_csv("opal_info.csv")
    return opal_info

def get_row_lineage(row, taxfoo, want_taxonomy):
    # maybe use expand to add the columns
    lin_dict = taxfoo.get_lineage_as_dict(row['taxid'], want_taxonomy)
    for rank in want_taxonomy:
        name = lin_dict.get(rank, '')
        row[rank] = name
    return row


def get_lineage(opal_info, nodes_dmp, names_dmp):
    want_taxonomy = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species', 'strain']
    taxfoo = ncbi_taxdump_utils.NCBI_TaxonomyFoo()
    taxfoo.load_nodes_dmp(nodes_dmp)
    taxfoo.load_names_dmp(names_dmp)
    opal_info.apply(lambda row: get_row_lineage(row, taxfoo, want_taxonomy), axis=1)
    return opal_info


def main(gather_csv, acc2taxid_files, nodes_dmp, names_dmp, acc_info=None):
    if acc_info:
        opal_info = pd.read_csv(acc_info)
    else:
        opal_info = get_taxid(gather_csv, acc2taxid_files)

    opal_info = get_lineage(opal_info, nodes_dmp, names_dmp)

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('gather_csv')
    p.add_argument('--acc2taxid_files', nargs='+')
    p.add_argument('--nodes_dmp', default="taxdump/nodes_dmp")
    p.add_argument('--names_dmp', default="taxdump/names_dmp")
    p.add_argument('--acc_info') #, default="opal_info.csv")
    p.add_argument('-o', '--output', type=argparse.FileType('wt'))
    args = p.parse_args()

    main(args.gather_csv, args.acc2taxid_files, args.nodes_dmp, args.names_dmp, args.acc_info)
