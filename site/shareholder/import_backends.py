#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests

from django.conf import settings

from shareholder.models import Bank


class SwissBankImportBackend(object):

    def _call_url(self):
        return requests.get(settings.SWISS_BANKS_DOWNLOAD_URL)

    def _get_or_create_bank(self, data):
        defaults = dict(
            short_name=data['short_name'],
            name=data['name'],
            postal_code=data['postal_code'],
            address=data.get('domizil') or data['address'],
            city=data['city'],
            swift=data['swift'],
        )
        bank, created = Bank.objects.get_or_create(
            bcnr=data['bcnr'], branchid=data['branchid'],
            defaults=defaults)
        if created:
            print 'created {}'.format(bank)
        else:
            Bank.objects.filter(pk=bank.pk).update(**defaults)
            print 'updated {}'.format(bank)

    def _prepare_data(self, response):
        print "encoding: {}".format(response.encoding)
        # convert to python string
        content = response.content.decode(response.encoding)
        return content

    def _split_line(self, line):
        """
        split line into content strings and remove spaces
        """
        # based on https://goo.gl/i926Wr
        data = dict(
            group=line[0:2].strip(),
            bcnr=line[2:7].strip(),
            branchid=line[7:11].strip(),
            bcnrnew=line[11:16].strip(),
            sicnr=line[16:22].strip(),
            headquarterbcnr=line[22:27].strip(),
            bctype=line[27:28].strip(),
            valid_since=line[28:36].strip(),
            sic=line[36:37].strip(),
            eurosic=line[37:38].strip(),
            language=line[38:39].strip(),
            short_name=line[39:54].strip(),
            name=line[54:114].strip(),
            domizil=line[114:149].strip(),
            address=line[149:184].strip(),
            postal_code=line[184:194].strip(),
            city=line[194:229].strip(),
            phone=line[229:247].strip(),
            fax=line[247:265].strip(),
            country_phone_prefix=line[265:270].strip(),
            country_code=line[270:272].strip(),
            post_account_nr=line[272:284].strip(),
            swift=line[284:298].strip(),
        )

        return data

    def update(self):
        """
        download and import swiss bank list
        """
        response = self._call_url()
        content = self._fetch_data(response)
        lines = content.split('\n')

        # iterate and save/update to Banks model
        for line in lines[:-1]:
            data = self._split_line(line)
            self._get_or_create_bank(data)
