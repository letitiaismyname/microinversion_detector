#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import sys
import itertools

def parseArguments():
    """
    Parse Arguments, sets default values, type of arguments, and help documentation
    :return:
    Parse arguments used for file in and file out
    """
    # making the parser
    parser = argparse.ArgumentParser()
    # adding different parse arguments
    parser.add_argument("-d","--data",
                        help = "file to read",
                        type = argparse.FileType('r'),
                        default = sys.stdin)
    parser.add_argument("-o","--data_out",
                        help = "file to write",
                        type = argparse.FileType('w'),
                        default = sys.stdout)

    args = parser.parse_args()
    return args

def readTSV(file):
    """
    Takes TSV file as input, generates dictionary for each line (each variant) with name, chr, start, end, len as keys
    :return:
    """

    for tupleLine in enumerate(file):
        if tupleLine[0] == 0:
            continue
        else:
            dict={}
            line = tupleLine[1]
            line = line.rstrip()
            values = line.split('\t')# outputs a list called values, filled with strings that correspond to the tab separated text
            dict['Name'] = values[0]
            dict['Chr'] = values[1]
            dict['Start'] = values[2]
            dict['End'] = values[3]
            dict['Len'] = values[4]
            yield dict


def convert(dict):
    """
    Input dictionary with TSV headers as keys
    Output values from dictionary keys into list
    :param dict:
    :return:
    """
    variantList = []
    variantList.append(dict['Chr'])
    variantList.append(dict['Start'])
    variantList.append(dict['Name'][2:len(dict['Name'])-1]) # remove quotes and @ sign
    variantList.append('N')
    variantList.append('<INV>')
    variantList.append('.')
    variantList.append('.')
    variantList.append("END={};SVTYPE=INV".format(dict['End']))

    return variantList



def vcfWriter(variantGenerator, file):
    """Inputting a generator that produces lists, with strings corresponding to each VCF column as items in the list, and file to write
    Outputting file with 1. Header 2. Each list becomes a VCF record with tab separators"""
    # vcfFile = open(file, "w")
    file.write("""##fileformat=VCFv4.2
##INFO=<ID=END,Number=1,Type=Integer,Description=“End position of the variant described in this record”>
##INFO=<ID=SVTYPE,Number=1,Type=String,Description=“Type of structural variant”>
##ALT=<ID=IV,Description=“Inversion”>
#CHROM	POS	ID	REF ALT QUAL	FILTER	INFO""")
    # for element in variantList:
    file.write(str('\n'))
    for item in variantGenerator:
        # file.write(item)
        # file.write(''.join(str(item)))
        file.write(item[0]+'\t'+item[1]+'\t'+item[2]+'\t'+item[3]+'\t'+item[4]+'\t'+item[5]+'\t'+item[6]+'\t'+item[7])
        file.write(str('\n'))


            # now I would like to catch all of those dictionaries in a list....


def main():
    args = parseArguments()

    variantSpecs = itertools.imap(convert, readTSV(args.data)) # generators can act like lists
    vcfWriter(variantSpecs, args.data_out)


    # variantList = convert(dict)
    # print(variantList)


if __name__ == '__main__':
    main()









