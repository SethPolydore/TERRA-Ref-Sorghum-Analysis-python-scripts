import csv
import argparse

## Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Convert timestamp dates into 'days after planting'.")
    parser.add_argument("-i", "--input", help="Input file.", required=True, nargs='+')
    parser.add_argument("-o", "--output", help="File to write with 'days after planting data'", required=True)
    args = parser.parse_args()
    return args

args = options()
headers=[]
barcodes={}
append_list=[]
character_row={}

with open (args.output,'w') as filetowrite:
    for file in args.input:
        frame_column=0
        zoom_column=0
        barcode_column=0
        timestamp_column=0
        width_designation_column=0
        with open (file,'r') as Locus_File:
            reader=csv.reader(Locus_File, delimiter=",")
            for row_num, line in enumerate(reader):
                for i, x in enumerate(line):
                    if row_num==0:
                        headers.append(x)
                        if "zoom" in x:
                            zoom_column=i
                        if "frame" in x:
                            frame_column=i
                        if "plantbarcode" in x:
                            barcode_column=i
                        if "timestamp" in x:
                            timestamp_column=i
                        if "width_designation" in x.lower():
                            width_designation_column=i

                    if not row_num==0:
                        if not line[width_designation_column] in append_list:
                            append_list.append(line[width_designation_column])
                        if not line[barcode_column] in barcodes:
                            barcodes[line[barcode_column]]={}
                        if not line[zoom_column] in barcodes[line[barcode_column]]:
                            barcodes[line[barcode_column]][line[zoom_column]] = {}
                        if not line[timestamp_column] in barcodes[line[barcode_column]][line[zoom_column]]:
                            barcodes[line[barcode_column]][line[zoom_column]][line[timestamp_column]]={}
                        if not line[width_designation_column] in barcodes[line[barcode_column]][line[zoom_column]][line[timestamp_column]]:
                               barcodes[line[barcode_column]][line[zoom_column]][line[timestamp_column]][line[width_designation_column]]=[]
                               character_row[line[barcode_column]+"_"+line[zoom_column]+"_"+line[timestamp_column]+"_"+line[width_designation_column]]=row_num
                        if row_num==character_row[line[barcode_column]+"_"+line[zoom_column]+"_"+line[timestamp_column]+"_"+line[width_designation_column]]:
                            barcodes[line[barcode_column]][line[zoom_column]][line[timestamp_column]][line[width_designation_column]].append(x)


    for width_designation in ("thin", "Wide"):
        for i,x in enumerate(headers):
            filetowrite.write(x+"_"+width_designation)
            if i<(len(headers)-1)*len(append_list):
                filetowrite.write(",")
    filetowrite.write("\n")

    for plantbarcode in barcodes:
        for zoom in barcodes[plantbarcode]:
            for timestamp in barcodes[plantbarcode][zoom]:
                for width_designation in ("thin", "Wide"):
                    try:
                        for i,x in enumerate(barcodes[plantbarcode][zoom][timestamp][width_designation]):
                            filetowrite.write(x)
                            if i<(len(headers)-1)*len(barcodes[plantbarcode][zoom][timestamp][width_designation]):
                                filetowrite.write(",")
                    except KeyError:
                        for _ in range(len(headers)-1):
                            filetowrite.write("NA,")
                        filetowrite.write(width_designation)
                        if  width_designation == "thin":
                            filetowrite.write(",")
                        else:
                            filetowrite.write("Wide")
##                        if width_designation == "thin":
##                            if i<(len(headers)-1)*len(barcodes[plantbarcode][zoom][timestamp]["Wide"]):
##                                filetowrite.write(",")
##                        else:
##                            if i<(len(headers)-1)*len(barcodes[plantbarcode][zoom][timestamp]["thin"]):
##                                filetowrite.write(",")

                filetowrite.write("\n")