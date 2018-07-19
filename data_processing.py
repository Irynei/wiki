import numpy as np
import pandas as pd


def read_csv(file_name):
    return pd.read_csv("data/{0}".format(file_name))


def filter_views(data):
    data = data.drop(columns=["Unnamed: 0", "6"])
    data[data == 0] = np.nan
    average = data.drop(columns=["page_id", "title"]).apply(lambda x: np.nanmean(x), axis=1)
    data["average_views"] = average
    return data[["page_id", "average_views"]]


def merge(translated, not_translated, other, how, left_on, right_on):
    translated = pd.merge(left=translated,
                          right=other,
                          how=how,
                          left_on=[left_on],
                          right_on=[right_on])

    not_translated = pd.merge(left=not_translated,
                              right=other,
                              how=how,
                              left_on=[left_on],
                              right_on=[right_on])
    return translated, not_translated


def merge_pages():
    not_translated = read_csv("uk_not_translated.csv")
    translated = read_csv("uk_translated.csv")
    all_articles = read_csv("all_uk_pages.csv")
    revisions_count = read_csv("revisions_count.csv")
    image_count = read_csv("number_of_imagelinks.csv")
    translations_count = read_csv("number_of_translations.csv")
    first_edit = read_csv("first_edit_all_uk_pages.csv")
    contributors = read_csv("contributions_by_username_or_ip_all_uk_pages.csv")
    not_translated_views = read_csv("not_translated_views_from_2018.csv")
    translated_views = read_csv("translated_views_from_2018.csv")

    not_translated_views = filter_views(not_translated_views)
    translated_views = filter_views(translated_views)

    first_edit = first_edit.drop(columns=["first_edit", "end_date"], axis=1)

    translated, not_translated = merge(translated, not_translated, all_articles, 'inner', 'title',
                                       'title')

    assert pd.merge(translated, not_translated, how='inner', on=['title']).shape[0] == 0, \
        "Translated and not translated articles are overlapping"

    translated, not_translated = merge(translated, not_translated, revisions_count, 'inner', 'id',
                                       'page_id')

    translated, not_translated = merge(translated, not_translated, image_count, 'left', 'id',
                                       'page_id')

    translated, not_translated = merge(translated, not_translated, translations_count, 'left', 'id',
                                       'page_id')

    translated = translated.drop(['page_id_x', 'page_id_y', 'page_id'], axis=1)
    not_translated = not_translated.drop(['page_id_x', 'page_id_y', 'page_id'], axis=1)

    translated = translated.rename(columns={'id': 'page_id'})
    not_translated = not_translated.rename(columns={'id': 'page_id'})

    translated, not_translated = merge(translated, not_translated, first_edit, 'inner', 'page_id',
                                       'page_id')

    translated, not_translated = merge(translated, not_translated, contributors, 'inner', 'page_id',
                                       'page_id')

    not_translated = pd.merge(not_translated, not_translated_views, how='inner', on=['page_id'])
    translated = pd.merge(translated, translated_views, how='inner', on=['page_id'])

    print(translated.shape)
    print(not_translated.shape)

    return translated, not_translated


translated_filtered, not_translated_filtered = merge_pages()
translated_filtered.to_csv('data/translated_filtered.csv', index=False)
not_translated_filtered.to_csv('data/not_translated_filtered.csv', index=False)
