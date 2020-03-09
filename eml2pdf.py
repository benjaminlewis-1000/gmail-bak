#! /usr/bin/env python

# Eml to pdf

import os
import email
import eml_parser


def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial


path = './life_updates'
listing = os.listdir(path)

for fle in listing:
    if str.lower(fle[-3:])=="eml":
        fullfile = os.path.join(path, fle)
        msg = email.message_from_file(open(fullfile))
        with open(fullfile, 'rb') as fhdl:
            raw_email = fhdl.read()
        parsed = eml_parser.eml_parser.decode_email_b(raw_email)

        print(parsed)
        print(dir(msg))
        attachments=msg.get_payload()
        print(attachments)

        print(fle)
        for attachment in attachments:
            try:
                fnam=attachment.get_filename()
                f=open(fnam, 'wb').write(attachment.get_payload(decode=True,))
                # print(dir(f), fnam)
                f.close()
            except Exception as detail:
                #print detail
                pass

    exit()