library(ggplot2)
library(cowplot)
library(stringr)
library(rlang)

dfs <- na.omit(TM21_allpoints)

column_names=list(area_adj_thin = 'Plant Area',
                  convex_hull_area_adj_thin = 'Convex Hull Area',
                  solidity_thin = 'Solidity',
                  perimeter_adj_thin = 'Perimeter',
                  width_adj_thin = 'Width',
                  height_adj_thin = 'Height',
                  longest_path_adj_thin = 'Longest Path',
                  convex_hull_vertices_thin = 'Number Of CH Vertices',
                  ellipse_major_axis_thin = 'Ellipse Major Axis',
                  ellipse_minor_axis_thin = 'Ellipse Minor Axis',
                  ellipse_angle_thin = 'Ellipse Angle',
                  ellipse_eccentricity_thin = 'Ellipse Eccentricity',
                  height_above_reference_adj_thin = 'Height Above Reference',
                  height_below_reference_adj_thin = 'Height Below Reference',
                  area_above_reference_adj_thin = 'Area Above Reference',
                  percent_area_above_reference_thin = 'Percent Area Above Reference',
                  area_below_reference_adj_thin = 'Area Below Reference',
                  percent_area_below_reference_thin = 'Percent Area Below Reference',
                  hue_circular_mean_thin = 'Hue Circular Mean',
                  hue_circular_std_thin = 'Hue Circular STD',
                  hue_median_thin = 'Hue Circular Median',
                  nir_mean_thin = 'NIR Mean',
                  nir_median_thin = 'NIR Median',
                  nir_stdev_thin = 'NIR STD',
                  mean_index_gdvi_thin = 'GDVI Mean',
                  med_index_gdvi_thin = 'GDVI Median',
                  std_index_gdvi_thin = 'GDVI STD',
                  mean_index_psri_thin = 'PSRI Mean',
                  med_index_psri_thin = 'PSRI Median',
                  std_index_psri_thin = 'PSRI STD',
                  mean_index_ndvi_thin = 'NDVI Mean',
                  med_index_ndvi_thin = 'NDVI Median',
                  std_index_ndvi_thin = 'NDVI STD',
                  area_adj_Wide = 'Plant Area',
                  convex_hull_area_adj_Wide = 'Convex Hull Area',
                  solidity_Wide = 'Solidity',
                  perimeter_adj_Wide = 'Perimeter',
                  width_adj_Wide = 'Width',
                  height_adj_Wide = 'Height',
                  longest_path_adj_Wide = 'Longest Path',
                  convex_hull_vertices_Wide = 'Number Of CH Vertices',
                  ellipse_major_axis_Wide = 'Ellipse Major Axis',
                  ellipse_minor_axis_Wide = 'Ellipse Minor Axis',
                  ellipse_angle_Wide = 'Ellipse Angle',
                  ellipse_eccentricity_Wide = 'Ellipse Eccentricity',
                  height_above_reference_adj_Wide = 'Height Above Reference',
                  height_below_reference_adj_Wide = 'Height Below Reference',
                  area_above_reference_adj_Wide = 'Area Above Reference',
                  percent_area_above_reference_Wide = 'Percent Area Above Reference',
                  area_below_reference_adj_Wide = 'Area Below Reference',
                  percent_area_below_reference_Wide = 'Percent Area Below Reference',
                  hue_circular_mean_Wide = 'Hue Circular Mean',
                  hue_circular_std_Wide = 'Hue Circular STD',
                  hue_median_Wide = 'Hue Circular Median',
                  nir_mean_Wide = 'NIR Mean',
                  nir_median_Wide = 'NIR Median',
                  nir_stdev_Wide = 'NIR STD',
                  mean_index_gdvi_Wide = 'GDVI Mean',
                  med_index_gdvi_Wide = 'GDVI Median',
                  std_index_gdvi_Wide = 'GDVI STD',
                  mean_index_psri_Wide = 'PSRI Mean',
                  med_index_psri_Wide = 'PSRI Median',
                  std_index_psri_Wide = 'PSRI STD',
                  mean_index_ndvi_Wide = 'NDVI Mean',
                  med_index_ndvi_Wide = 'NDVI Median',
                  std_index_ndvi_Wide = 'NDVI STD',
                  area_adj = 'Plant Area',
                  convex_hull_area_adj = 'Convex Hull Area',
                  solidity = 'Solidity',
                  perimeter_adj = 'Perimeter',
                  width_adj = 'Width',
                  height_adj = 'Height',
                  longest_path_adj = 'Longest Path',
                  convex_hull_vertices = 'Number Of CH Vertices',
                  ellipse_major_axis = 'Ellipse Major Axis',
                  ellipse_minor_axis = 'Ellipse Minor Axis',
                  ellipse_angle = 'Ellipse Angle',
                  ellipse_eccentricity = 'Ellipse Eccentricity',
                  height_above_reference_adj = 'Height Above Reference',
                  height_below_reference_adj = 'Height Below Reference',
                  area_above_reference_adj = 'Area Above Reference',
                  percent_area_above_reference = 'Percent Area Above Reference',
                  area_below_reference_adj = 'Area Below Reference',
                  percent_area_below_reference = 'Percent Area Below Reference',
                  width_left_reference_adj = 'Width Left of Reference',
                  width_right_reference_adj = 'Width Right of Reference',
                  area_left_reference_adj = 'Area Left of Reference',
                  percent_area_left_reference = 'Percent Area Left of Reference',
                  area_right_reference_adj = 'Area Right of Reference',
                  percent_area_right_reference = 'Percent Area Right of Reference',
                  hue_circular_mean = 'Hue Circular Mean',
                  hue_circular_std = 'Hue Circular STD',
                  hue_median = 'Hue Circular Median',
                  nir_mean = 'NIR Mean',
                  nir_median = 'NIR Median',
                  nir_stdev = 'NIR STD',
                  mean_index_gdvi = 'GDVI Mean',
                  med_index_gdvi = 'GDVI Median',
                  std_index_gdvi = 'GDVI STD',
                  mean_index_psri = 'PSRI Mean',
                  med_index_psri = 'PSRI Median',
                  std_index_psri = 'PSRI STD',
                  mean_index_ndvi = 'NDVI Mean',
                  med_index_ndvi = 'NDVI Median',
                  std_index_ndvi = 'NDVI STD')


for (i in colnames(dfs)){
  if (class(dfs[,i])=="numeric"){
    #print(class(i))
    names = unlist(column_names[i])
    
    if (grepl("area", i, fixed=FALSE, ignore.case = TRUE) &&
        !grepl("percent", i, fixed=FALSE, ignore.case = TRUE)){
      addition = bquote(.(names) ~" ("*cm^2*")")
    } else if (grepl("perimeter", i, fixed=FALSE, ignore.case = TRUE) ||
               grepl("width", i, fixed=FALSE, ignore.case = TRUE) ||
               grepl("longest_path", i, fixed=FALSE, ignore.case = TRUE) ||
               grepl("height", i, fixed=FALSE, ignore.case = TRUE)) {
      addition = bquote(.(names) ~" ("*cm*")")  
    } else {addition = bquote(.(names))}
    
    
    test <- ggplot(dfs, aes_string(x="timestamp", y=i)) +
    geom_point(shape=21, alpha=0.007, aes(group=timestamp, fill=as.factor(dbscan_Clusters)))+geom_smooth(aes(color=as.factor(dbscan_Clusters), linetype=as.factor(dbscan_Clusters)), size=2) +  
    scale_fill_manual(values=c("0"="orange","1"="red","2"="black","3"="blue","4"="yellow","5"="chartreuse3","6"="cornsilk3","7"="lightsalmon","hotpink","darkseagreen","gold4","green3","cornsilk2","chocolate3","brown1","azure3")) +
    scale_color_manual(values=c("0"="orange","1"="red","2"="black","3"="blue","4"="yellow","5"="chartreuse3","6"="cornsilk3","7"="lightsalmon","darkseagreen","gold4","green3","cornsilk2","chocolate3","brown1")) +
    theme_classic() +
    theme(axis.text.x = element_text(color="black",size=12), axis.text.y = element_text(color="black",size=12), axis.line = element_line(size = 1, linetype = "solid"), axis.title = element_text(size=16), legend.position="none") + 
    xlab("Days After Planting") +
    ylab(addition) +
    scale_linetype_manual(values=c(1,1,1,1,1,1,1,1,6,6,1,1,1,1,1)) +
    scale_y_reverse()
    assign(paste(i,"_ggplot", sep=""), test)
  }
}
