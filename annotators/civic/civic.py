import sys
from cravat import BaseAnnotator
from cravat import constants, InvalidData
from pyliftover import LiftOver
import sqlite3
import requests
import json
import os
import re

class CravatAnnotator(BaseAnnotator):

    def setup(self):
        self.civicdata = {}
        lifter = LiftOver(constants.liftover_chain_paths['hg19'])
        page_url = 'https://civicdb.org/api/variants?count=500&page=1'
        while page_url is not None:
            try:
                r = requests.get(page_url, timeout=5)
            except requests.exceptions.ConnectionError:
                msg = 'ERROR: Incomplete CIVIC data load'
                print(msg)
                self.logger.error(msg)
                break
            d = json.loads(r.text)
            records = d['records']
            page_url = d['_meta']['links']['next']
            for variant in records:
                chrom_37 = variant['coordinates']['chromosome']
                pos_37 = variant['coordinates']['start']
                if chrom_37 is None or pos_37 is None: continue
                new_coords = lifter.convert_coordinate("chr" + chrom_37, int(pos_37))
                if len(new_coords) > 0:
                    chrom_38 = new_coords[0][0].replace('chr','')
                    pos_38 = new_coords[0][1]
                else:
                    continue
                ref = variant['coordinates']['reference_bases']
                alt = variant['coordinates']['variant_bases']
                toks = [chrom_38, pos_38, ref, alt]
                if None not in toks:
                    vkey = ':'.join(map(str, toks))
                    self.civicdata[vkey] = variant
                else:
                    continue        

    def annotate(self, input_data, secondary_data=None):
        var_key = ":".join([input_data["chrom"][3:],str(input_data["pos"]),input_data["ref_base"],input_data["alt_base"]])
        match = self.civicdata.get(var_key)
        if match is not None:
            out = {}
            out["description"] = re.sub('\s',' ', match.get('description',''))
            out["clinical_a_score"] = match['civic_actionability_score']
            civic_id = match['id']
            out['id'] = civic_id
            evidence_link = 'https://civicdb.org/api/variants/{civic_id}/evidence_items?count=5000&page=1'.format(civic_id=civic_id)
            r = requests.get(evidence_link)
            d = json.loads(r.text)
            diseases = []
            for x in  d['records']:
                if 'disease' not in x or x['disease'] is None or 'display_name' not in x['disease']:
                    continue 
                disease_name = x['disease']['display_name']
                if disease_name is not None and disease_name not in diseases:
                    diseases.append(disease_name)

            if len(diseases) > 0:
                out['diseases'] = ', '.join(sorted(diseases))
            return out
    
    def cleanup(self):
        pass
        
if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
