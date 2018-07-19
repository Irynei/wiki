import pandas as pd
import numpy as np

def read_csv(file_name):
    return pd.read_csv("data/{0}".format(file_name))

def get_pages(not_translated, translated, all_articles):
    translated_filtered = pd.merge(translated, all_articles, how='inner', on=['title'])
    not_translated_filtered = pd.merge(not_translated, all_articles, how='inner', on=['title'])

    return translated_filtered, not_translated_filtered

def filter_views(data):
    data = data.drop(columns=["Unnamed: 0", "6"])
    data[data == 0] = np.nan
    average = data.drop(columns=["page_id", "title"]).apply(lambda x: np.nanmean(x), axis=1)
    data["average_views"] = average
    return data[["page_id", "average_views"]]

def merge_pages():
    not_translated = read_csv("uk_not_translated.csv")
    translated = read_csv("uk_translated.csv")
    all_articles = read_csv("all_uk_pages.csv")

    translated_filtered, not_translated_filtered = get_pages(not_translated, translated, all_articles)

    test = pd.merge(translated_filtered, not_translated_filtered, how='inner', on=['title'])
    if test.shape[0] != 0:
        print("Collision appeared {0} times".format(test.shape[0]))

    revisions_count = read_csv("revisions_count.csv")

    print(translated_filtered.shape)
    print(not_translated_filtered.shape)

    translated_filtered = pd.merge(translated_filtered, revisions_count, how='inner', left_on=['id'],
                                   right_on=['page_id'])
    not_translated_filtered = pd.merge(not_translated_filtered, revisions_count, how='inner', left_on=['id'],
                                       right_on=['page_id'])

    image_count = read_csv("number_of_imagelinks.csv")

    translated_filtered = pd.merge(translated_filtered, image_count, how='left', left_on=['id'], right_on=['page_id'])
    not_translated_filtered = pd.merge(not_translated_filtered, image_count, how='left', left_on=['id'],
                                       right_on=['page_id'])

    translations_count = read_csv("number_of_translations.csv")

    translated_filtered = pd.merge(translated_filtered, translations_count, how='left', left_on=['id'],
                                   right_on=['page_id'])
    not_translated_filtered = pd.merge(not_translated_filtered, translations_count, how='left', left_on=['id'],
                                       right_on=['page_id'])

    translated_filtered = translated_filtered.drop(['page_id_x', 'page_id_y', 'page_id'], axis=1)
    not_translated_filtered = not_translated_filtered.drop(['page_id_x', 'page_id_y', 'page_id'], axis=1)
    translated_filtered = translated_filtered.rename(columns={'id': 'page_id'})
    not_translated_filtered = not_translated_filtered.rename(columns={'id': 'page_id'})

    first_edit = read_csv("first_edit_all_uk_pages.csv")
    first_edit = first_edit.drop(columns= ["first_edit", "end_date"], axis=1)

    not_translated_filtered = pd.merge(not_translated_filtered, first_edit, how='inner', on=['page_id'])
    translated_filtered = pd.merge(translated_filtered, first_edit, how='inner', on=['page_id'])

    contributors = read_csv("contributions_by_username_or_ip_all_uk_pages.csv")

    not_translated_filtered = pd.merge(not_translated_filtered, contributors, how='inner', on=['page_id'])
    translated_filtered = pd.merge(translated_filtered, contributors, how='inner', on=['page_id'])

    not_translated_views = read_csv("not_translated_views_from_2018.csv")
    translated_views = read_csv("translated_views_from_2018.csv")

    not_translated_views = filter_views(not_translated_views)
    translated_views = filter_views(translated_views)

    not_translated_filtered = pd.merge(not_translated_filtered, not_translated_views, how='inner', on=['page_id'])
    translated_filtered = pd.merge(translated_filtered, translated_views, how='inner', on=['page_id'])


    print(translated_filtered.shape)
    print(not_translated_filtered.shape)

    return translated_filtered, not_translated_filtered

# translated_filtered, not_translated_filtered = merge_pages()
# translated_filtered.to_csv('data/translated_filtered.csv', index=False)
# not_translated_filtered.to_csv('data/not_translated_filtered.csv', index=False)