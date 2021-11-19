import sys
import os
from cravat import BaseAnnotator
from cravat import InvalidData
import sqlite3

class CravatAnnotator(BaseAnnotator):

    def annotate(self, input_data):
        chrom = input_data['chrom']
        self.cursor.execute(
            f'select sig, disease_refs, disease_names, rev_stat, id from {chrom} where pos=? and ref=? and alt=?;',
            (input_data['pos'], input_data['ref_base'], input_data['alt_base'])
        )
        qr = self.cursor.fetchone()
        if qr is not None:
            return {
                'sig':qr[0],
                'disease_refs':qr[1],
                'disease_names':qr[2],
                'rev_stat':qr[3],
                'id': qr[4],
            }

    def postprocess(self):
        for lnum, line, input_data, secondary_data in self._get_input():
            try:
                self.log_progress(lnum)
                # * allele and undefined non-canonical chroms are skipped.
                if self.is_star_allele(input_data) or self.should_skip_chrom(input_data):
                    continue
                chrom = input_data['chrom']
                self.cursor.execute(
                    f'select sig, disease_refs, disease_names, rev_stat, id from {chrom} where pos=? and ref=? and alt=?;',
                    (input_data['pos'], input_data['ref_base'], input_data['alt_base'])
                )
                qr = self.cursor.fetchone()
                if qr is None:
                    continue
                output_dict = {
                    'sig':qr[0],
                    'disease_refs':qr[1],
                    'disease_names':qr[2],
                    'rev_stat':qr[3],
                    'id': qr[4],
                }
                output_dict = self.handle_jsondata(output_dict)
                output_dict[self._id_col_name] = input_data[self._id_col_name]
                output_dict = self.fill_empty_output(output_dict)
                self.output_writer.write_data(output_dict)
            except Exception as e:
                self._log_runtime_exception(lnum, line, input_data, e)

if __name__ == '__main__':
    annotator = CravatAnnotator(sys.argv)
    annotator.run()
