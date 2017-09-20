# coding: utf-8
import csv
import pandas as pd
import re #regular expression
import argparse
import os

"""
This script takes the tagged url output from train_LDA, cleans itand writes it to csv, where it will subsequently be read into R for performance metrics.  


Example usage:
python clean_lda_out.py --out_path ../DATA/education/clean_lda_output/clean_154tops_educ.csv --taxonfile ../DATA/education/educ_link_taxonpath.csv --raw_lda ../DATA/education/raw_lda_tag_output/educ_154tops_tags.csv
"""  
__author__ = "Ellie King"
__copyright__ = "Government Digital Service, 20/09/2017"


parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument(
    '--out_path', dest='out_path', metavar='OUTPUT FOLDER', default=None,
    help='export cleaned url, topics 1-3 and probs 1-3 to csv'
)

parser.add_argument(
    '--taxonfile', dest='taxons_filename', metavar='FILENAME', default=None,
    help='import original url taxonpath data in csv'
)

parser.add_argument(
    '--raw_lda', dest='raw_taggedurls_filename', metavar='FILENAME', default=None,
    help='import tagged urls in csv output from LDA'
)


def read_data(taxonfile, raw_lda):
    """Function to read in original data and tagged documents after LDA"""
    tags = pd.read_csv(raw_lda, header=None, names=['Link', 'topic1', 'p1', 'topic2', 'p2', 'topic3', 'p3'])
    print(tags.head(5))
    original = pd.read_csv(taxonfile)
    print(original.head(5))
    return(tags, original)

def clean_tags(tags):
    """function to clean the dataframe from weird parentheses"""
    #drop the leading parentheses
    nourls = tags.drop('Link', axis=1) # don't mess with urls as these are used in merges
    urls = tags['Link']
    tags2 = nourls.apply(lambda x: x.str.replace(r'\[', ''), axis=1)
    tags3 = tags2.apply(lambda x: x.str.replace(r'\(', ''), axis=1)
    tags4 = tags3.apply(lambda x: x.str.replace(r'\]', ''), axis=1)
    tags5 = tags4.apply(lambda x: x.str.replace(r'\)', ''), axis=1)

    cleaned_tags = pd.merge(urls.to_frame(), tags5, left_index = True, right_index = True)

    return cleaned_tags

def get_taxons_by_merging(cleaned_tags):
    #merge on the Link column to get taxons (user research) in same frame as topics (LDA output)
    both = pd.merge(cleaned_tags, original, how = 'outer', on = 'Link', indicator = True)
    
    print("shape of merged df is {}".format(both.shape))
    print("shape of url, taxonpath data is {}".format(original.shape))
    print("shape of url, topic 1-3, p1-3 data is {}".format(tags.shape))

    print(pd.crosstab(index = both['_merge'], columns = 'count'))
    return both


# THIS MERGE EXPLORATION IS CONTINUED IN R performance_notebook_r.Rmd
# pd.crosstab(index = both['_merge'], columns = 'count')
# both = pd.merge(out_lda, original, how = 'left', on = 'Link', indicator = True)
# both.shape
# pd.crosstab(index = both['_merge'], columns = 'count')
# both = pd.merge(original, out_lda, how = 'left', on = 'Link', indicator = True)
# pd.crosstab(index = both['_merge'], columns = 'count')

# original.Link.nunique()
# out_lda.Link.nunique()
# original.shape
# out_lda.shape
# both.Link.nunique()

def save_tag_top(cleaned_tags, out_path):
    """write to csv"""
    cleaned_tags.to_csv(out_path, index = False)


if __name__ == '__main__':
    args = parser.parse_args()
    
    print("Loading input file {}".format(args.taxons_filename))
    print("Loading input file {}".format(args.raw_taggedurls_filename))
    tags, original = read_data(
        taxonfile = args.taxons_filename, 
        raw_lda = args.raw_taggedurls_filename,
        )

cleaned_tags = clean_tags(tags)
print(cleaned_tags.head(5))

# taxon_tops = get_taxons_by_merging(cleaned_tags)
# print(taxon_tops.head(5))

save_tag_top(cleaned_tags, args.out_path)