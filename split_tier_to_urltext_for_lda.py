import csv
import pandas as pd
import re #regular expression
import argparse
import os

"""
This module/script takes the tagged url output from train_LDA with n topics, splits it into n groups and merges each group with original data to produce separate url, text.csvs ready to run further LDA on


Example usage:
python split_tier_to_urltext_for_lda.py --out_path ../DATA/output --preLDA_fpath input/test_urltext.csv --tagged_fpath input/test_tags.csv
"""  
__author__ = "Ellie King"
__copyright__ = "Government Digital Service, 10/07/2017"

parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument(
    '--num_topics', dest='num_topics', metavar='N', type = int, default=None,
    help='number of topics used in LDA'
)

parser.add_argument(
    '--out_path', dest='out_path', metavar='OUTPUT FOLDER', default=None,
    help='export split dfs to csv'
)

parser.add_argument(
    '--preLDA_fpath', dest='prelda_filename', metavar='FILENAME', default=None,
    help='import original url text data in csv'
)

parser.add_argument(
    '--tagged_fpath', dest='taggedurls_filename', metavar='FILENAME', default=None,
    help='import tagged urls in csv output from top level of hierarchy, first LDA'
)


def read_data(preLDA_fpath, tagged_fpath):
    """Function to read in original data and tagged documents after LDA with 5 topics"""
    df_tag = pd.read_csv(tagged_fpath, header=None, names=list('abcdefgh'))
    df_preLDA = pd.read_csv(preLDA_fpath)
    return(df_tag, df_preLDA)

def clean_tagged_urls(df_tag):
    """function to clean the dataframe to result in url 
    topic_id cols"""
    #drop the leading parentheses
    df_tag['b'] = df_tag['b'].str.replace(r'\[\(', '') 
    # drop the columns containing topics of lower (or equal probability)
    df2_tag =  df_tag.drop(df_tag.columns[[2, 3, 4, 5, 6, 7]], axis=1)
    # name the remaining two columns
    df2_tag.columns = ['url', 'topic_id']
    return(df2_tag)


def split_urls_by_topic(df_tag_clean, num_topics):
    """Function to split datframe into n separate dfs filtered on topic_id"""
    urls_by_topic_filtered = [] #create empty list
    for num in range(1, num_topics+1):
        urls_by_topic_filtered.append(df_tag_clean[df_tag_clean.topic_id == str(num)])
    return urls_by_topic_filtered

    
def get_text_by_merging(urls_by_topic_filtered):
    #merge on the index column to get text back from original url, text data
    urltext_by_topic = []
    for df in urls_by_topic_filtered:
        urltext_by_topic.append(pd.merge(df, df_preLDA, left_index = True, right_index = True , indicator = True))
    return urltext_by_topic


def tidy_to_urltext(urltext_by_topic):
    """Function to keep only the url and text columns of the documents tagged with each topic"""
    tidy_urltext_by_topic = []
    for df in urltext_by_topic:
        tidy_urltext_by_topic.append(df.drop(df.columns[[1, 2, 4]], axis=1))
    return(tidy_urltext_by_topic)

def namecols_urltext(tidy_urltext_by_topic):
    """Function to keep only the url and text columns of the documents tagged with each topic"""
    for df in tidy_urltext_by_topic:
            df.columns = ['url', 'text'] #rename columns as they will be expected in train_LDA.py
    return(tidy_urltext_by_topic)

def write_to_csvs(named_urltext_by_topic, out_path):
    for index, df in enumerate(named_urltext_by_topic):
        fname = "{}{}{}".format("topic", str(index), ".csv")
        df.to_csv(
        os.path.join(out_path, fname), index = False
        )


if __name__ == '__main__':
    args = parser.parse_args()
    print(" out path{}".format(args.out_path))
    print("Loading input file {}".format(args.prelda_filename))
    print("Loading input file {}".format(args.taggedurls_filename))
    df_tag, df_preLDA = read_data(
        preLDA_fpath = args.prelda_filename, 
        tagged_fpath = args.taggedurls_filename,
        )

    print(df_preLDA.head(10))

    print("Cleaning tags")
    df_tag_clean = clean_tagged_urls(df_tag)

    print("Splitting by topic")
    urls_by_topic_filtered = split_urls_by_topic(df_tag_clean, num_topics = args.num_topics)

    print("Merging to text file")
    urltext_by_topic = get_text_by_merging(urls_by_topic_filtered)

    print("Tidying up")
    tidy_urltext_by_topic = tidy_to_urltext(urltext_by_topic)

    print("Naming columns")
    named_urltext_by_topic = namecols_urltext(tidy_urltext_by_topic)

    print("Write to file")
    write_to_csvs(named_urltext_by_topic, out_path = args.out_path)

