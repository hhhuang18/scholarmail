#!/usr/bin/env python

import imaplib
import email
import socket
import socks
from lxml import etree
import pandas as pd
import time
import os
import json
from tqdm import tqdm


def is_in_filter_list(string, filter_list=['Kerr']):
    filter_list = [f.lower() for f in filter_list]
    filter_string = string.lower().replace(',', ' ').replace(
        '-', ' ').replace(':', ' ').split(' ')
    set1 = set(filter_list)
    set2 = set(filter_string)
    return bool(set1.intersection(set2))


def get_email(path_conf):
    with open(path_conf, 'r') as load_f:
        conf = json.load(load_f)

    if conf['proxy']:
        print('setting proxy...')
        socks.set_default_proxy(
            socks.HTTP, conf['proxy_ip'], conf['proxy_port'])
        socket.socket = socks.socksocket

    conn = imaplib.IMAP4_SSL(conf['server'], conf['port'])
    print('server connected.')

    conn.login(conf['email'], conf['passkey'])
    print('login successful.')

    # auto select scholar based on address
    # do not need to label the emails as "scholar"
    conn.select('Inbox')
    _, d = conn.search(None, 'FROM', '"scholaralerts-noreply@google.com"')

    mail_list = d[0].split()
    print('get mails : ', len(mail_list))

    df = pd.DataFrame(columns=('title', 'link', 'info',
                      'abstract', 'source', 'filtered'))
    file_name = time.strftime("%Y%m%d%H%M%S", time.localtime())

    if len(mail_list) > 0:
        for l in tqdm(mail_list):
            _, data = conn.fetch(l, '(RFC822)')
            msg = email.message_from_string(data[0][1].decode('utf-8'))
            sub = msg.get('subject')
            mail_source = email.header.decode_header(sub)[0][0]
            if not mail_source.isascii():
                mail_source = mail_source.decode('utf-8')
            mail_content = msg.get_payload(decode=True).decode(
                'utf-8').replace('<br>', '#br#').replace('<b>', '').replace('</b>', '')

            selector = etree.HTML(mail_content)
            title = selector.xpath('/html/body/div/h3/a/text()')
            link = selector.xpath('/html/body/div/h3/a/@href')
            info = selector.xpath('/html/body/div/div/text()')
            info = [str(k).replace('\xa0', '') for k in info][:-1]
            tqdm.write('>>> solving mail: %s from %s get %d paper' % (l.decode('utf-8'),
                                                                    mail_source, len(title)))
            for n in range(len(title)):
                lk = link[n]

                try:
                    dic = {'title': title[n],
                        'link': lk,
                        'info': info[2*n],
                        'abstract': info[2*n+1],
                        'source': mail_source,
                        'filtered': is_in_filter_list(title[n], filter_list=conf['filter_list'])}
                    df = df.append(dic, ignore_index=True)
                except:
                    tqdm.write('>>> error: '+title[n])

            # mark this email as deleted
            if conf['remove_mail']:
                conn.store(l, '+X-GM-LABELS', '\\Trash')

        temp = []
        for row in df['abstract']:
            temp.append(row.replace('#br#', '<br>'))
        df['abstract'] = temp

        df.sort_values('title', inplace=True, ignore_index=True)
        # df.to_csv(os.path.join(file_name + '.csv'), index=None)

        # move the deleted emails to trash
        if conf['remove_mail']:
            conn.expunge() 
        
        return file_name, df
    else:
        return file_name, False

    


if __name__ == '__main__':
    get_email()
