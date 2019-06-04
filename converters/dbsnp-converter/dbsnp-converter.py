from cravat import BaseConverter
from cravat import BadFormatError
import re
import os
import sqlite3

class CravatConverter(BaseConverter):
    
    def __init__(self):
        self.format_name = 'dbsnp'
        self.rsid_re = re.compile('rs\d+')
        curdir = os.path.dirname(__file__)
        dbpath = os.path.join(curdir,'data','dbsnp.sqlite')
        try:
            self.dbconn = sqlite3.connect(dbpath)
            self.cursor = self.dbconn.cursor()
        except sqlite3.OperationalError:
            self.dbconn = None
            self.cursor = None
        self.query_template = 'select chrom, pos, ref_len, alt from dbsnp where rsid=?;'
    
    def check_format(self, f):
        return f.readline().startswith('#rsid')
        if self.cursor is None:
            return False
        for l in f:
            if l.startswith('#'):
                continue
            else:
                break
        return self.rsid_re.match(l) is not None
    
    def setup(self, f):
        pass
    
    def convert_line(self, l):
        if l.startswith('#'):
            return []
        toks = l.rstrip('\r\n').split()
        rsid = toks[0]
        sample_id = toks[1] if len(toks) > 1 else None
        tags = toks[2] if len(toks) > 2 else None
        rsnum = int(rsid.replace('rs',''))
        self.cursor.execute(self.query_template, [rsnum])
        out = []
        for r in self.cursor:
            wdict = {}
            chrom, pos, reflen, alt = r
            wdict = {
                'chrom':chrom,
                'pos':pos,
                'ref_base':'N'*reflen,
                'alt_base':alt,
                'tags': tags,
                'sample_id': sample_id
            }
        out.append(wdict)
        return out
