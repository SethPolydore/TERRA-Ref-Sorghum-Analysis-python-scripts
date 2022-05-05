import csv
import argparse

def options():
    parser = argparse.ArgumentParser(description="Convert timestamp dates into 'days after planting'.")
    parser.add_argument("-i", "--input", help="Input file.", required=True)
    parser.add_argument("-o", "--output", help="Prefix for CSV file output by this script", required=False, default=None)
    args = parser.parse_args()
    return args

args=options()
with open(args.output,'w+') as filetowrite:
    with open (args.input,'r') as Locus_File:
        reader=csv.reader(Locus_File, delimiter=',')
        plants_id={}
        headers={}
        unique_treatments=[]
        timestamp_column=0
        headers_unique=[]
        zoom_column=0
        genotype_column=0
        filetowrite.write("Genotype,timestamp,zoom,")
        for row_num, line in enumerate(reader):
            if row_num==0:
                for i, x in enumerate(line):
                    if not i==0:
                        if "timestamp" in x:
                            timestamp_column=i
                        if "Genotype" in x:
                            genotype_column=i
                        if "zoom" in x:
                            zoom_column=i
                        if "treatment" in x:
                            treatment_column=i

                        filetowrite.write(x)
                        headers[i]=x
                        if not x in headers_unique:
                            headers_unique.append(x)
                        if i<len(line)-1:
                            filetowrite.write(",")
            else:
                if not line[treatment_column] in unique_treatments:
                    unique_treatments.append(line[treatment_column])
                barcodes=line[genotype_column]+"_"+line[timestamp_column]+"_"+line[zoom_column]
                if not barcodes in plants_id:
                    plants_id[barcodes] = {}
                if not line[treatment_column] in plants_id[barcodes]:
                    plants_id[barcodes][line[treatment_column]] = {}
                for i, x in enumerate(line):
                    if not i==0:
                        if not headers[i] in plants_id[barcodes][line[treatment_column]]:
                           plants_id[barcodes][line[treatment_column]][headers[i]] = {}
                        plants_id[barcodes][line[treatment_column]][headers[i]] = x

    filetowrite.write("\n")
    unique_treatments.sort(reverse=True)
    for barcodes in plants_id:
        for splits in barcodes.split("_"):
            filetowrite.write(splits+",")
        for counts, header in enumerate(headers_unique):
            min=""
            max=""
            for treatment in (100, 30):
                try:
##                    for header in plants_id[barcodes][str(treatment)]:
                    if max =="":
                        max=plants_id[barcodes][str(treatment)][header]
                    else:
                        min=plants_id[barcodes][str(treatment)][header]
                except KeyError:
                    pass

##                print(barcodes, header, max, min)
            try:
                filetowrite.write(str(float(max) - float(min)))
            except ValueError:
                filetowrite.write("NA")
            if counts < len(headers_unique)-1:
                filetowrite.write(",")

        filetowrite.write("\n")