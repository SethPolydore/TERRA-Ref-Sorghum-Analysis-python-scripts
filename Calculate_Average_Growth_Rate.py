import argparse
import csv

def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--input", help="Input image file.", required=True)
    parser.add_argument("-o", "--output", help="Output directory for image files.", required=True)
    parser.add_argument("-ig", "--ignore", help="Columns to ignore.", nargs='+', required=False)
    args = parser.parse_args()
    return args

dictionary_list={}

def main():
    args=options()
    with open (args.input,'r') as Locus_File:
        with open(args.output, 'w+') as filetowrite:
            reader=csv.reader(Locus_File, delimiter='\t')
            filetowrite.write("Barcode,Width_Designation,Frame,Camera,Beginning_Timepoint,")
            for row_num, line in enumerate(reader):
                dict_to_write=line[9]+"_"+line[66]+"_"+line[5]+"_"+line[0]
                if not row_num == 0:
                    line[7]=int(line[7])
                    if not dict_to_write in dictionary_list:
                        dictionary_list[dict_to_write]={}
                    if not line[7] in dictionary_list[dict_to_write]:
                        dictionary_list[dict_to_write][line[7]]=[]
                for i, x in enumerate(line):
                    if row_num==0:
                        if not str(i+1) in args.ignore:
                            filetowrite.write(x+"_dif,")
##                            if not i == (len(line)-len(args.ignore)-1):  #fix later
##                               filetowrite.write(',')
                    else:
                        if not str(i+1) in args.ignore:
                            dictionary_list[dict_to_write][line[7]].append(x)
                if row_num==0:
                    filetowrite.write('\n')

            for barcodes in dictionary_list:
##                print(barcodes, dictionary_list[barcodes])
                barcode_timepoints=[]
                for timepoints in dictionary_list[barcodes]:
                    barcode_timepoints.append(timepoints)
                barcode_timepoints.sort()
                for time in range(len(barcode_timepoints)):
                    if not time == len(barcode_timepoints)-1:
                        for x in barcodes.split("_"):
                            filetowrite.write(x+",")
                        #print(dictionary_list[barcodes][barcode_timepoints[time]])
                        filetowrite.write(str(barcode_timepoints[time])+",")
                        for stats_range in range(len(dictionary_list[barcodes][barcode_timepoints[time]])):
                            #print(stats_range)
                            dif = float(dictionary_list[barcodes][barcode_timepoints[time+1]][stats_range]) - float(dictionary_list[barcodes][barcode_timepoints[0]][stats_range])
                            filetowrite.write(str(dif)+",")
                        filetowrite.write("\n")
if __name__ == '__main__':
    main()
