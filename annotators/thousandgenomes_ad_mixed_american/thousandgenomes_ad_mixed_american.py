import sys
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3
import os

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        out = {}
        chrom = input_data['chrom']
        pos = input_data['pos']
        ref = input_data['ref_base']
        alt = input_data['alt_base']
        
        q = 'select CLM, MXL, PEL, PUR from '\
            +'%s where pos=%s and ref="%s" and alt="%s";' \
            %(chrom, pos, ref, alt)
        self.cursor.execute(q)
        result = self.cursor.fetchone()
        if result:
            out['clm_af'] = result[0] 
            out['mxl_af'] = result[1] 
            out['pel_af'] = result[2] 
            out['pur_af'] = result[3] 
        return out
    def cleanup(self):
        pass

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()