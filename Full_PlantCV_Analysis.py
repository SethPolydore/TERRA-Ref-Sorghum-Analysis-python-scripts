import sys
import argparse
import csv
from datetime import datetime

def options():
    parser = argparse.ArgumentParser(description="Convert timestamp dates into 'days after planting'.")
    parser.add_argument("-i", "--input", help="Input file.", required=True)
    parser.add_argument("-prog", "--progs", help="Programs to run", required=False, nargs='+', default=["All"])
    parser.add_argument("-o", "--output", help="Prefix for CSV file output by this script", required=False, default=None)
    parser.add_argument("-d", "--planting_date", help="Plantiing date of experiment.  Otherwise, lowest timepoint will be used.", required=False, default=None)
    args = parser.parse_args()
    return args



def Adjust_Measurments_by_Zoom(input, output, planting_date=""):
    with open ("zoom_calibration_factors.csv",'r') as Locus_File:
        zoom_calibrations={}
        reader=csv.reader(Locus_File, delimiter=',')
        for row_num, line in enumerate(reader):
            if not line[0] in zoom_calibrations and not row_num==0:
                zoom_calibrations[line[0]]={"cm":line[2], "cm2":line[3]}

    with open (input,'r') as Locus_File:
        reader=csv.reader(Locus_File, delimiter=',')
        ignore_columns=set()
        cm_columns=set()
        area_columns=set()
        zoom_columns=0

        with open(output, "w") as filetowrite:
            for row_num, line in enumerate(reader):
                if row_num==0:
                    for i, x in enumerate(line):
                        if x in ("camera",	"solidity", "imgtype",	"zoom",	"exposure",	"horizontal_reference_position", "gain",
                                 "percent_area_above_reference", "percent_area_below_reference","frame", "lifter", "timestamp", "vStamp",	"plantbarcode",
                                 "treatment", "cartag", "measurementlabel", "other", "id", "image", "sample", "in_bounds",
                                 "object_in_frame", "Width_Designation", "hue_circular_mean", "hue_circular_std", "hue_median",
                                 "nir_mean", "nir_median", "nir_stdev", "mean_index_gdvi", "med_index_gdvi", "std_index_gdvi",
                                 "mean_index_psri",	"med_index_psri", "std_index_psri", "mean_index_ndvi", "med_index_ndvi",
                                 "std_index_ndvi", "convex_hull_vertices", "ellipse_major_axis", "ellipse_minor_axis", "ellipse_angle", "ellipse_eccentricity",
                                 "percent_area_below_reference", "vertical_reference_position", "percent_area_left_reference", "percent_area_right_reference"):
                            ignore_columns.add(i)
                            filetowrite.write(x)
                            if x=="zoom":
                                zoom_columns=i

                        else:
                            if x in ("area", "convex_hull_area", "area_above_reference", "area_below_reference", "area_left_reference", "area_right_reference"):
                                area_columns.add(i)
                            elif x in ("perimeter", "width", "height", "longest_path", "height_above_reference", "height_below_reference", "width_left_reference",
                                       "width_right_reference", ):
                                cm_columns.add(i)

                            filetowrite.write(x+"_adj")

                        if not i==len(line)-1:
                            filetowrite.write(",")
                else:
                    for i, x in enumerate(line):
                        calibration = ''.join(c for c in line[zoom_columns] if c.isdigit())
                        if i in ignore_columns:
                            filetowrite.write(x)
                        else:
                            try:
                                if i in area_columns:
                                    filetowrite.write(str(float(x)/float(zoom_calibrations[calibration]["cm2"])))
                                elif i in cm_columns:
                                    filetowrite.write(str(float(x)/float(zoom_calibrations[calibration]["cm"])))
                            except ValueError:
                               filetowrite.write(x)

                        if not i==len(line)-1:
                            filetowrite.write(",")

                filetowrite.write("\n")

    output = output + "_Zoom_Adjusted_Measurements.csv"
    return output

def Concatenate_Lines(input, output, planting_date=""):
    with open(output,'w') as filetowrite:
        with open (input,'r') as Locus_File:
            reader=csv.reader(Locus_File, delimiter=',')
            NDVI_Columns=[]
            PSRI_Columns=[]
            last_line = ""
            line_length=0
            z=0
            for c, line in enumerate(reader):
                newline=False
                if c==0:
                    for i, x in enumerate(line):
                       filetowrite.write(x)
                       if "ndvi" in x.lower():
                         NDVI_Columns.append(i)
                         try:
                            line[i+1]
                         except IndexError:
                            last_line="ndvi"
                       elif "psri" in x.lower():
                         PSRI_Columns.append(i)
                         try:
                            line[i+1]
                         except IndexError:
                            last_line="psri"
                       if i==len(line)-1:
                        filetowrite.write("\n")
                        line_length=i
                       else:
                        filetowrite.write(",")
                else:
                   for i, x in enumerate(line):
                       if line[16]=="PSRI array data" and i in PSRI_Columns:
                        filetowrite.write(x)
                        if z < line_length:
                           filetowrite.write(",")
                        z+=1

                       elif line[16]=="NDVI array data" and i in NDVI_Columns:
                        filetowrite.write(x)
                        if z < line_length:
                           filetowrite.write(",")
                        z+=1

                       elif line[16] == "default" and not i in (NDVI_Columns + PSRI_Columns):
                        filetowrite.write(x)
                        if z < line_length:
                           filetowrite.write(",")
                        z+=1

                       if z>=line_length+1:
                        filetowrite.write("\n")
                        z=0

    output = output + "_SingleLine.csv"
    return output

def Timepoints_to_Date(input, output, planting_date=""):
    with open (input,'r') as Locus_File:
        reader=csv.reader(Locus_File, delimiter=',')
        timestamp_column=0
        barcode_column=0
        assign_dict={}
        headers=[]
        if planting_date is None:
            for row_num, line in enumerate(reader):
                if row_num == 0:
                    for i, x in enumerate(line):
                        if "timestamp" in x:
                            timestamp_column= i
                        if "plantbarcode" in x:
                            barcode_column= i
                        if x == "frame":
                            frame_column = i
                        headers.append(x)
                else:
                    if not str(line[barcode_column]+"_"+line[frame_column]) in assign_dict:
                        assign_dict[str(line[barcode_column]+"_"+line[frame_column])] = {}
                    if not str(line[timestamp_column].split()[0]) in assign_dict[str(line[barcode_column]+"_"+line[frame_column])]:
                        assign_dict[str(line[barcode_column]+"_"+line[frame_column])][str(line[timestamp_column].split()[0])]=[]
                    for i, x in enumerate(line):
                        assign_dict[str(line[barcode_column]+"_"+line[frame_column])][str(line[timestamp_column].split()[0])].append(x)


            min_timepoints={}
            with open(output, 'w') as filetowrite:
                for i, x in enumerate(headers):
                    filetowrite.write(x)
                    if not i==len(headers)-1:
                        filetowrite.write(",")
                filetowrite.write("\n")

                for barcodes in assign_dict:
                    for timestamps in assign_dict[barcodes]:
                        if not barcodes in min_timepoints:  #"%m/%d/%Y"
                            min_timepoints[barcodes]=datetime.strptime(timestamps, "%Y-%m-%d")
                        elif datetime.strptime(timestamps, "%Y-%m-%d") < min_timepoints[barcodes]:
                            min_timepoints[barcodes]=datetime.strptime(timestamps, "%Y-%m-%d")

                for barcodes in assign_dict:
                    for timestamps in assign_dict[barcodes]:
                        for i, x in enumerate(assign_dict[barcodes][timestamps]):
                            if i == timestamp_column:
                                filetowrite.write(str((datetime.strptime(x.split()[0], "%Y-%m-%d") - min_timepoints[barcodes]).days))
                            else:
                                filetowrite.write(x)
                            if not i==len(assign_dict[barcodes][timestamps])-1:
                                filetowrite.write(",")
                        filetowrite.write("\n")

        else:
            with open(output, 'w') as filetowrite:
                for row_num, line in enumerate(reader):
                    if row_num == 0:
                        for i, x in enumerate(line):
                            if "timestamp" in x:
                                timestamp_column= i
                            filetowrite.write(x)
                            if not i==len(line)-1:
                                filetowrite.write(",")
                        filetowrite.write("\n")
                    else:
                        for i, x in enumerate(line):
                            if i==timestamp_column:
                               filetowrite.write(str((datetime.strptime(x.split()[0], "%Y-%m-%d") - datetime.strptime(planting_date, "%Y-%m-%d")).days))
                            else:
                                filetowrite.write(x)
                            if not i==len(line)-1:
                                filetowrite.write(",")
                        filetowrite.write("\n")

    output = output + "_timepoints_converted_to_DAP.csv"
    return output


def Assign_Thins(input, output, planting_date=""):
    with open (input,'r') as Locus_File:
        reader=csv.reader(Locus_File, delimiter=',')
        frame_column=0
        width_column=0
        timestamp_column=0
        barcode_column=0
        assign_dict={}
        thin_rows=[]
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
               try:
                assign_dict[str(line[barcode_column])][str(line[timestamp_column])].append({line[frame_column]:float(line[width_column])})
               except ValueError:
                assign_dict[str(line[barcode_column])][str(line[timestamp_column])].append({line[frame_column]:0})

    max_timepoints={}
    for barcodes in assign_dict:
        for timestamps in assign_dict[barcodes]:
            if not barcodes in max_timepoints:
                max_timepoints[barcodes]=int(timestamps)
            elif int(timestamps) > max_timepoints[barcodes]:
                max_timepoints[barcodes]=int(timestamps)

    #print(max_timepoints)
    for barcodes in assign_dict:
        for timestamps in assign_dict[barcodes]:
            if int(timestamps) == max_timepoints[barcodes]:
                for z, list in enumerate(assign_dict[barcodes][timestamps]):
                    globals()["list"+str(z+1)] = list

                try:
                    for width in  assign_dict[barcodes][timestamps][0].keys():
                        key1=width
                    for width in  assign_dict[barcodes][timestamps][1].keys():
                        key2=width

                    if list1[key1] < list2[key2]:
                        thin_rows.append(barcodes+"_"+key1)
                    else:
                        thin_rows.append(barcodes+"_"+key2)

                except IndexError:
                    for width in  assign_dict[barcodes][timestamps][0].keys():
                        key1=width
                    thin_rows.append(barcodes+"_"+key1)

    with open(output, 'w') as filetowrite:
        with open (input,'r') as Locus_File:
            reader=csv.reader(Locus_File, delimiter=',')
            for row_num, line in enumerate(reader):
                for i, x in enumerate(line):
                    filetowrite.write(x+",")
                    #if not i==len(line)-1:
                    #    filetowrite.write(",")
                if row_num==0:
                    filetowrite.write("Width_Designation\n")
                elif line[barcode_column]+"_"+line[frame_column] in thin_rows:
                    filetowrite.write("thin\n")
                else:
                    filetowrite.write("Wide\n")

    output = output + "_WideDesignationsAdded.csv"
    return output


# Run the main program
###########################################
def main():
    """Main program.
    """
    args=options()
    input = args.input
    output = args.output
    mode=""

    additions={"Concatenate_Lines":{"input": "", "output":"_SingleLine.csv"},
               "Timepoints_to_Date":{"input":"_SingleLine.csv", "output":"_timepoints_converted_to_DAP.csv"},
               "Adjust_Measurments_by_Zoom":{"input":"_timepoints_converted_to_DAP.csv", "output":"_Zoom_Adjusted_Measurements.csv"},
               "Assign_Thins":{"input":"_Zoom_Adjusted_Measurements.csv", "output":"_WideDesignationsAdded.csv"}}

    if "All" in args.progs:
        mode="all"
        args.progs = ["Concatenate_Lines", "Timepoints_to_Date", "Adjust_Measurments_by_Zoom", "Assign_Thins"]

    for i, prog in enumerate(args.progs):
        i_addition=""
        o_addition=""
        if mode=="all":
            i_addition = additions[prog]["input"]
            o_addition = additions[prog]["output"]
        if i>0:
            input=output
        globals()[prog](input=input+i_addition, output=output+o_addition, planting_date=args.planting_date)

###########################################


if __name__ == '__main__':
    main()