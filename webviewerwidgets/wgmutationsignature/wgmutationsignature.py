import aiosqlite
import os
import cravat
import cravat.admin_util as au

info = au.get_local_module_info('go')
path = info.directory
wgr = cravat.get_wgs_reader()

async def get_data (queries):
    response = {}
    dbpath = queries['dbpath']

    conn = await aiosqlite.connect(dbpath)
    cursor = await conn.cursor()

    table = 'variant'
    query = 'select name from sqlite_master where type="table" and name="' + table + '"'
    await cursor.execute(query)
    r = await cursor.fetchone()

    from_str = ' from variant '
        
    query = 'select base__chrom, base__pos, base__ref_base, base__alt_base '
    query += from_str
    await cursor.execute(query)

    # get all triplets with 'A' in the middle
    tripletDataA = [a + 'A' + c for a in ['A', 'T', 'G', 'C'] for c in ['A', 'T', 'G', 'C']]

    # get all triplets with 'G' in the middle
    tripletDataG = [a + 'G' + c for a in ['A', 'T', 'G', 'C'] for c in ['A', 'T', 'G', 'C']]

    # initialize triplet dictionaries using dictionary comprehension
    tripletDictAC = {triplet : 0 for triplet in tripletDataA}
    tripletDictAG = {triplet : 0 for triplet in tripletDataA}
    tripletDictAT = {triplet : 0 for triplet in tripletDataA}
    tripletDictGC = {triplet : 0 for triplet in tripletDataG}
    tripletDictGA = {triplet : 0 for triplet in tripletDataG}
    tripletDictGT = {triplet : 0 for triplet in tripletDataG}

    # master triplet dictionary
    masterTripletDict = {'AC': tripletDictAC,
                         'AG': tripletDictAG,
                         'AT': tripletDictAT,
                         'GC': tripletDictGC,
                         'GA': tripletDictGA,
                         'GT': tripletDictGT}

    numSubstitutions = 0

    for row in await cursor.fetchall():
        (chrom, pos, ref_base, alt_base) = row
        
        bases = ['A', 'T', 'G', 'C']

        # only consider substitutions (single base changes only - disregard insertions and deletions)
        if ref_base in bases and alt_base in bases:
            # get the base before and after this position
            base_1 = (wgr[chrom][pos - 1]).upper()
            base_3 = (wgr[chrom][pos + 1]).upper()

            baseChange = ''

            # make key string out of ref and alt bases
            if (ref_base == 'A' and alt_base == 'C') or (ref_base == 'T' and alt_base == 'G'):
                baseChange = 'AC'
            elif (ref_base == 'A' and alt_base == 'G') or (ref_base == 'T' and alt_base == 'C'):
                baseChange = 'AG'
            elif (ref_base == 'A' and alt_base == 'T') or (ref_base == 'T' and alt_base == 'A'):
                baseChange = 'AT'
            elif (ref_base == 'G' and alt_base == 'C') or (ref_base == 'C' and alt_base == 'G'):
                baseChange = 'GC'
            elif (ref_base == 'G' and alt_base == 'A') or (ref_base == 'C' and alt_base == 'T'):
                baseChange = 'GA'
            elif (ref_base == 'G' and alt_base == 'T') or (ref_base == 'C' and alt_base == 'A'):
                baseChange = 'GT'

            # make triplet string
            triplet = base_1 + baseChange[0] + base_3

            # increment frequency of this base change in this triplet by 1
            masterTripletDict[baseChange][triplet] += 1

            numSubstitutions = numSubstitutions + 1

    await cursor.close()
    await conn.close()

    conn = await aiosqlite.connect(os.path.join(path, 
                                        'data', 
                                        'go.sqlite'))

    cursor = await conn.cursor()

    data = [masterTripletDict, numSubstitutions]

    response['data'] = data
    await cursor.close()
    await conn.close()
    return response