# -*- coding: utf-8 -*-
import imaplib
import os
import getpass
import re
from datetime import datetime
from dateutil.parser import parse
import eml_parser


UID_RE = re.compile(r".*\d+\s+\(UID (\d+)\)")
FILE_RE = re.compile(r"(\d+).eml$")
# GMAIL_FOLDER_NAME = "[Gmail]/All Mail"
GMAIL_FOLDER_NAME = '"Life Updates"'

app_pwd = 'ihcguvwcrqvwahhn'

OUT_FOLDER = '/home/benjamin/git_repos/gmail-backup/life_updates'


# def getUIDForMessage(svr, n):
#     resp, lst = svr.fetch(n, 'UID')
#     print(resp, lst)
#     m = UID_RE.match(str(lst[0]))
#     if not m:
#         raise Exception(
#             "Internal error parsing UID response: %s %s.  Please try again" % (resp, lst))
#     return m.group(1)


def downloadMessage(svr, n, fname):
    resp, lst = svr.fetch(n, '(RFC822)')
    if resp != 'OK':
        raise Exception("Bad response: %s %s" % (resp, lst))
    f = open(os.path.join(OUT_FOLDER, fname), 'w')
    f.write(lst[0][1].decode('utf-8'))
    f.close()



def get_credentials():
    user = 'speedyswimmer1000@gmail.com' # raw_input("Gmail address: ")
    pwd = app_pwd # getpass.getpass("Gmail password: ")
    return user, pwd



if __name__ == "__main__":
    # do_backup()
    # main()


    svr = imaplib.IMAP4_SSL('imap.gmail.com')
    user, pwd = get_credentials()
    svr.login(user, pwd)

    resp, [countstr] = svr.select(GMAIL_FOLDER_NAME, True)
    count = int(countstr)
    typ, data = svr.search(None, 'ALL')

    existing_files = os.listdir(OUT_FOLDER)

    for num in data[0].split():
        # uid = getUIDForMessage(svr, num)
        # getUIDForMessage(svr, num)
        typ, data = svr.fetch(num, '(BODY.PEEK[HEADER] FLAGS)')
        # print()
        multipleTos = False
        toline = re.match('.*To(.*):', str(data[0][1]), re.IGNORECASE)
        if toline:
            # print("TOLINE: ", toline.group(1))
            tl = toline.group(1)
            if re.match('.*Nicholas.*', tl) or re.match('.*Daniel.*', tl) or re.match('.*Joshua.*', tl) or re.match('.*Williams.*', tl):
                multipleTos = True

        bccd = False
        not_fwd_or_re = True
        for l in str(data[0][1]).split('\\r\\n'):
            # print(l)
            d = re.match('Date:(.*)', l)
            if d:
                date = d.group(1)
                date = parse(date)
                # print(date)
                date = date.strftime('%Y_%B_%d-%H_%m_%S')

            subj = re.match('.*Subject:(.*)', l)
            if subj:
                sub_line = subj.group(1).lower()
                # print(sub_line)
                if 're:' in sub_line or 'fwd:' in sub_line:
                    not_fwd_or_re = False

                    # print(data[0][1])
            send = re.match('.*From:(.*)', l)
            if send:
                sender = send.group(1)
                if 'benjamin.lewis.1000' in sender or 'speedyswimmer1000' in sender:
                    i_sent = True
                else:
                    i_sent = False

            if re.match('.*CC:', l, re.IGNORECASE) :
                bccd = True


        print(date, sender, i_sent)

        if date == '2018_September_01' and i_sent:
            print(bccd, multipleTos, not_fwd_or_re, i_sent and (bccd or multipleTos) and not_fwd_or_re, tl)
            for l in data[0][1].decode('utf-8').split('\r\n'):
                print(l)

            # exit()

        nodown = '/home/benjamin/git_repos/gmail-backup/nodown'

        outfile = date + '.eml'
        if i_sent and (bccd or multipleTos) and not_fwd_or_re:
            if not outfile in existing_files:
                downloadMessage(svr, num, os.path.join(OUT_FOLDER, outfile))
                # typ, fulldata = svr.fetch(num, 'RFC822')
        else:
            if not outfile in os.listdir(nodown):
                downloadMessage(svr, num, os.path.join(nodown, outfile))

    svr.close()
    svr.logout()

    print("TO Manage (remote download?): 2019-08-05")
    # print('Shouldn''t: 2018-12-04, 2018-11-04, 2019-03-09')
    print('Should: 2019-01-21, 2019-09-01')