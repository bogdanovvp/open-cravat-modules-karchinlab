from cravat.cravat_report import CravatReport
import sys
import datetime
import re
import csv
import zipfile
import os
import aiosqlite3

class Reporter(CravatReport):

    def setup (self):
        self.wf = None
        self.filenames = []
        self.filename = None
        self.filename_prefix = None
        if self.savepath == None:
            self.filename_prefix = 'cravat_result'
        else:
            self.filename_prefix = self.savepath
        if not 'type' in self.confs:
            self.info_type = 'combined'
        else:
            info_type = self.confs['type']
            if info_type in ['separate', 'combined']:
                self.info_type = self.confs['type']
            else:
                self.info_type = 'separate'
        self.info_fieldname_prefix = 'CRV'
        self.col_names_to_skip = ['base__uid', 'base__chrom', 'base__pos', 'base__ref_base', 'base__alt_base', 'tagsampler__numsample', 'tagsampler__samples', 'tagsampler__tags', 'vcfinfo__phred', 'vcfinfo__filter', 'vcfinfo__zygosity', 'vcfinfo__alt_reads', 'vcfinfo__tot_reads', 'vcfinfo__af', 'vcfinfo__hap_block', 'vcfinfo__hap_strand']
        if len(self.args.inputfiles) > 1:
            self.logger.error(Exception('Only 1 input file can be taken. Exiting without creating a report.'))
            return False

    def end (self):
        if self.wf is not None:
            self.wf.close()
        zf = zipfile.ZipFile(self.filename_prefix + '.vcf.zip', mode='w', compression=zipfile.ZIP_DEFLATED)
        for filename in self.filenames:
            zf.write(filename, os.path.relpath(filename, start=os.path.dirname(filename)))
        zf.close()

    async def connect_db (self, dbpath=None):
        if dbpath != None:
            self.dbpath = dbpath
        if self.dbpath == None:
            sys.stderr.write('Provide a path to aggregator output')
            exit()
        if os.path.exists(self.dbpath) == False:
            sys.stderr.write(self.dbpath + ' does not exist.')
            exit()
        self.conn = await aiosqlite3.connect(self.dbpath)
        self.cursor = await self.conn.cursor()
        self.cursor2 = await self.conn.cursor()
        '''
        await self.cursor.execute('select distinct(base__sample_id) from sample')
        self.samples = []
        rows = await self.cursor.fetchall()
        if rows is None or len(rows) == 0:
            self.samples.append('NOSAMPLEID')
        else:
            for row in rows:
                self.samples.append(row[0])
        '''

    def write_preface (self, level): 
        self.level = level
        if self.wf is not None:
            self.wf.close()
        if level != 'variant':
            return
        self.filename = self.filename_prefix + '.' + level + '.vcf'
        self.filenames.append(self.filename)
        self.wf = open(self.filename, 'w', encoding='utf-8', newline='')
        lines = ['#fileformat=VCFv4.2',
            '#OpenCRAVATFileDate=' + datetime.datetime.now().strftime('%Y%m%d'),
        ]
        self.write_preface_lines(lines)
        self.vcflines = {}
        self.input_path_dict = {}
        if self.args.inputfiles is not None:
            if type(self.args.inputfiles) is str:
                self.args.inputfiles = [self.args.inputfiles]
            for i in range(len(self.args.inputfiles)):
                self.input_path_dict[self.args.inputfiles[i]] = i
            written_headers = []
            self.samples = []
            num_inputfiles = len(self.args.inputfiles)
            for inputfile in self.args.inputfiles:
                inputfile_prefix = os.path.basename(inputfile).split('.')[0]
                input_path_no = self.input_path_dict[inputfile]
                self.vcflines[input_path_no] = {}
                f = open(inputfile)
                lineno = 0
                for line in f:
                    lineno += 1
                    if line.startswith('##fileformat='):
                        continue
                    if line.startswith('##'):
                        if not line in written_headers:
                            self.wf.write(line)
                            written_headers.append(line)
                    elif line.startswith('#CHROM'):
                        toks = line[:-1].split('\t')
                        if len(toks) >= 10:
                            if num_inputfiles == 1:
                                self.samples.extend([v for v in toks[9:]])
                            else:
                                self.samples.extend([inputfile_prefix + '_' + v for v in toks[9:]])
                    elif line.startswith('#') == False:
                        self.vcflines[input_path_no][lineno] = line[:-1]
                f.close()

    def write_header (self, level):
        self.level = level
        if self.level != 'variant':
            return
        self.output_candidate = {}
        self.col_names = []
        if self.info_type == 'separate':
            for column in self.colinfo[self.level]['columns']:
                col_name = column['col_name']
                col_type = column['col_type'].capitalize()
                col_desc = column['col_desc']
                if col_name in self.col_names_to_skip:
                    continue
                if col_desc is None:
                    col_desc = ''
                line = '#INFO=<ID={},Number=A,Type={},Description="{}">'.format(col_name, col_type, col_desc)
                self.write_preface_line(line)
                self.col_names.append(col_name)
            line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'
            line += '\t'.join(self.samples)
            self.write_preface_line(line)
        elif self.info_type == 'combined':
            line = '#INFO=<ID={},Number=A,Type=String,Description="OpenCRAVAT annotation. Format: '.format(self.info_fieldname_prefix)
            columns_to_add = []
            desc = []
            for column in self.colinfo[self.level]['columns']:
                col_name = column['col_name']
                col_desc = column['col_desc']
                if col_name in ['base__uid', 'base__chrom', 'base__pos', 'base__ref_base', 'base__alt_base']:
                    continue
                columns_to_add.append(col_name)
                if col_desc is not None:
                    desc.append(col_name + '=' + col_desc)
                self.col_names.append(col_name)
            line += '|'.join(columns_to_add)
            line += ' Explanation: {}'.format('|'.join(desc))
            line += '">'
            self.write_preface_line(line)
            line = 'CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t'
            line += '\t'.join(self.samples)
            self.write_preface_line(line)
            
    async def write_table_row (self, row):
        if self.level != 'variant':
            return
        columns = self.colinfo[self.level]['columns']
        row = list(row)
        writerow = []
        info = []
        chrom = None
        pos = None
        uid = None
        ref = None
        alt = None
        qual = None
        filt = None
        fmt = None
        pathno = None
        lineno = None
        for i in range(len(columns)):
            column = columns[i]
            col_name = column['col_name']
            cell = row[i]
            if col_name == 'base__uid':
                uid = cell
                q = 'select base__fileno, base__original_line from mapping where base__uid={}'.format(uid)
                await self.cursor2.execute(q)
                rows2 = await self.cursor2.fetchall()
                for row2 in rows2:
                    (pathno, lineno) = row2
                    if pathno not in self.output_candidate:
                        self.output_candidate[pathno] = {}
                    vcfline = self.vcflines[pathno][lineno]
                    if lineno not in self.output_candidate[pathno]:
                        alts = vcfline.split('\t')[4].split(',')
                        noalts = len(alts)
                        self.output_candidate[pathno][lineno] = {'noalts': noalts, 'line': vcfline, 'annots': []}
            elif col_name == 'base__all_mappings':
                cell = cell.replace('; ', '&')
                cell = cell.replace(' ', '-')
                info.append(cell)
            elif col_name in self.col_names_to_skip:
                continue
            else:
                if cell is None:
                    infocell = ''
                elif type(cell) is str:
                    cell = cell.replace('; ', '&')
                    cell = cell.replace(';', '&')
                    cell = cell.replace(' ', '-')
                    infocell = '"' + cell + '"'
                else:
                    infocell = str(cell)
                info.append(infocell)
            '''
            elif col_name == 'base__chrom':
                chrom = cell.lstrip('chr')
            elif col_name == 'base__pos':
                pos = cell
            elif col_name == 'base__ref_base':
                ref = cell
            elif col_name == 'base__alt_base':
                alt = cell
            '''
            '''
            elif col_name == 'tagsampler__numsample':
                continue
            elif col_name == 'tagsampler__samples':
                samples_with_variant = cell.split(',')
                sample_cols = []
                for s in self.samples:
                    if s in samples_with_variant:
                        sample_cols.append('1|1')
                    else:
                        sample_cols.append('')
            elif col_name == 'vcfinfo__phred':
                qual = cell.split(';')[0]
            elif col_name == 'vcfinfo__filter':
                filt = cell.split(';')[0]
            '''
        out = self.output_candidate[pathno][lineno]
        noalts = out['noalts']
        annots = out['annots']
        annots.append(info)
        if len(annots) == noalts:
            numfields = len(annots[0])
            combined_annots = [['.' for j in range(noalts)] for i in range(numfields)]
            for fieldno in range(len(annots[0])):
                for altno in range(noalts):
                    combined_annots[fieldno][altno] = annots[altno][fieldno]
            if self.info_type == 'separate':
                info_add_list = []
                for colno in range(len(self.col_names)):
                    info_add_list.append(self.col_names[colno] + '=' + ','.join(combined_annots[colno]))
                info_add_str = ';'.join(info_add_list)
            elif self.info_type == 'combined':
                info_add_str = self.info_fieldname_prefix + '=' + '|'.join([','.join(altlist) for altlist in combined_annots])
            toks = out['line'].split('\t')
            toks[7] = toks[7] + ';' + info_add_str
            writerow = toks
            self.write_body_line(writerow)
            del self.output_candidate[pathno][lineno]

    def write_body_lines (self, lines):
        if self.level != 'variant':
            return
        for line in lines:
            self.write_body_line(line)
    
    def write_body_line (self, row):
        if self.level != 'variant':
            return
        self.wf.write('\t'.join(row) + '\n')
    
    def write_preface_lines (self, lines):
        if self.level != 'variant':
            return
        for line in lines:
            self.write_preface_line(line)
    
    def write_preface_line (self, line):
        if self.level != 'variant':
            return
        self.wf.write('#' + line + '\n')

    def substitute_val (self, level, row):
        if level in self.column_subs:
            for i in self.column_subs[level]:
                if row[i] is not None:
                    sub = self.column_subs[level][i]
                    for target in sub:
                        row[i] = re.sub('\\b' + target + '\\b', sub[target], row[i])
        return row

def main ():
    reporter = Reporter(sys.argv)
    reporter.run()

if __name__ == '__main__':
    main()
