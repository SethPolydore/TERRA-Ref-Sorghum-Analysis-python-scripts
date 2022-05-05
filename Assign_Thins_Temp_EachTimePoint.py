import argparse
import csv

def options():
    parser = argparse.ArgumentParser(description="For Sorghum plants, it finds which frame is wider than the other.")
    parser.add_argument("-i", "--input", help="Input file.", required=True)
    parser.add_argument("-o", "--output", help="File to write with 'days after planting data'", required=True)
    args = parser.parse_args()
    return args

def main():
    args = options()
    with open (args.input,'r') as Locus_File:
        reader=csv.reader(Locus_File, delimiter=',')
        frame_column=0
        width_column=0
        timestamp_column=0
        barcode_column=0
        assign_dict={}
        thin_list=[]
        for row_num, line in enumerate(reader):
            if row_num == 0:
                for i, x in enumerate(line):
                    if x == "frame":
                        frame_column = i
                    if "width" in x.lower():
                        width_column = i
                    if "timestamp" in x:
                        timestamp_column= i
                    if "cartag" in x:
                        barcode_column= i
            else:
               if not str(line[barcode_column]) in assign_dict:
                    assign_dict[str(line[barcode_column])] = {}
               if not str(line[timestamp_column]) in assign_dict[str(line[barcode_column])]:
                    assign_dict[str(line[barcode_column])][str(line[timestamp_column])]=[]

               assign_dict[str(line[barcode_column])][str(line[timestamp_column])].append({row_num: line[width_column]})

    thin_rows = []
    for barcodes in assign_dict:
        for timestamps in assign_dict[barcodes]:
            for z, list in enumerate(assign_dict[barcodes][timestamps]):
                globals()["list"+str(z+1)] = list

            try:
                for width in  assign_dict[barcodes][timestamps][0].keys():
                    key1=width
                for width in  assign_dict[barcodes][timestamps][1].keys():
                    key2=width

            except IndexError:
                for width in  assign_dict[barcodes][timestamps][0].keys():
                    key1=width
                thin_rows.append(key1)

            if list1[key1] < list2[key2]:
                thin_rows.append(key1)
            else:
                thin_rows.append(key2)


    with open(args.output, 'w') as filetowrite:
        with open (args.input,'r') as Locus_File:
            reader=csv.reader(Locus_File, delimiter=',')
            for row_num, line in enumerate(reader):
                for x in line:
                    filetowrite.write(x)
                    if not x==len(line)-1:
                        filetowrite.write(",")
                if row_num==0:
                    filetowrite.write("Width_Designation\n")
                elif row_num in thin_rows:
                    filetowrite.write("thin\n")
                else:
                    filetowrite.write("Wide\n")

if __name__=='__main__':
    main()