#!/usr/bin/env python

import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os
import json


def concat_func(x):
    result = pd.Series({
        'link': x['link'][x['link'].index[0]],
        'info': ','.join(x['info'].unique()),
        'abstract': ','.join(x['abstract'].unique()),
        'source': '<br>'.join(x['source'].unique()),
        'source_count': len(x['source'])
    })
    return result


def gen_html(file_name, path_conf, path_html, df):
    # df = pd.read_csv(os.path.join('./csv', file_name + '.csv'))

    with open(path_conf, 'r') as load_f:
        conf = json.load(load_f)
    if conf['apply_filter']:
        df = df.drop(df[df['filtered'] == True].index)

    result = df.groupby(df['title']).apply(concat_func).reset_index()
    result.sort_values('source_count', inplace=True,
                       ignore_index=True, ascending=False)
    item_count = len(result)
    title_count = df['title'].value_counts().to_dict()
    source_count = df['source'].value_counts().to_dict()
    data = [k for k in result.T.to_dict().values()]

    loader = FileSystemLoader(os.path.dirname(os.path.abspath(__file__)))
    env = Environment(loader=loader)
    template = env.get_template('temperate.html')
    text = template.render(item_count=str(item_count),
                           source_count=source_count, data=data)

    f = open(os.path.join(path_html, file_name + '.html'), 'w')
    f.write(text)
    f.close()
    print('done')


if __name__ == '__main__':
    gen_html(input('input file name without extension:'))
