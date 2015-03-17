#!/usr/bin/env python
import os
import os.path
import argparse
import sys
import subprocess
import re
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


class RGBColors(object):
    
    def __init__(self):
        """Class constructor"""
        self.redList = [] # List or red coordinates
        self.greenList = [] # List of green coordinates
        self.blueList = [] # List of blue coordinates

    def readColorFile(self, fileColors):
        """Parser a color file
           fileColors - File path to RGB colors file
           returns True if the file was correctly parsed otherwise returns false
        """
       
        with open(fileColors, "r") as inColors:
            for line in inColors:
                rgbCoodinates = line.rstrip().split(',')
	        if len(rgbCoodinates) == 3:
                    if(int(rgbCoodinates[0]) >= 0 and int(rgbCoodinates[0]) <= 255):
                        self.redList.append(float(float(rgbCoodinates[0])/255.0))
                    if(int(rgbCoodinates[1]) >= 0 and int(rgbCoodinates[1]) <= 255):
                        self.greenList.append(float(float(rgbCoodinates[1])/255.0))
                    if(int(rgbCoodinates[2]) >= 0 and int(rgbCoodinates[2]) <= 255):
                        self.blueList.append(float(float(rgbCoodinates[2])/255.0))
        
        if  len(self.redList) != 10 or len(self.greenList) != 10 or len(self.blueList) != 10:
            return False

        return True


class HeatMapTracks:

    def __init__(self):
        """Class constructor"""
        self.pathList = [] # List of bed paths
        self.shortNameList = [] # List of short names for tracks
        self.descriptionList = [] # List of description per track
        self.bedGraphToBed9 = "/home/devel/mfernand/src/bedGraphToBed9/Release/bedGraphToBed9"
        self.bed2BigBed = "/home/devel/mfernand/src/heatMapUcsc/UCSC/bedToBigBed"
        self.fetchChrSize = "/home/devel/mfernand/src/heatMapUcsc/UCSC/fetchChromSizes"
        self.listOfColorsFile = ""
        self.minimum_score = -1
        self.maximum_score = -1
        self.output_dir = ""
        self.assembly_name = ""

    def setScores(self,minimum,maximum):
        """Updates minimum and maximum scores
           minimum - minimu score value 
           maximum - maximum score value 
        """
        self.maximum_score = int(maximum)
        self.minimum_score = int(minimum)
        

    def setListColors(self,listColors):
        """Updates list of colors """
        self.listOfColorsFile = listColors

    def setOutputDir(self,outDir):
        """Updates output directory """
        self.output_dir = outDir

    def setAssemblyName(self,assembly):
        """Updates output directory """
        self.assembly_name = assembly

    def parseHeatMap(self, fileHeatMap):
        """Parser a color file
           fileHeatMap - File path to stack of tracks that forms a HeatMap
           returns True if the file was correctly parsed otherwise returns false
        """
       
        with open(fileHeatMap, "r") as inTracks:
            for line in inTracks:
                bedInfo = line.rstrip().split(',')
	        if len(bedInfo) == 3:
                    if os.path.exists(bedInfo[0]):
		        self.pathList.append(bedInfo[0])
                    else:
                        print "Sorry!! File " + bedInfo[0] + " does not exists!!"
                        return False
                    
                    self.shortNameList.append(bedInfo[1])
                    self.descriptionList.append(bedInfo[2])
        
        if  len(self.pathList) != len(self.shortNameList) or len(self.shortNameList) != len(self.descriptionList):
            return False

        return True

    def fromBedGraphToBigBed(self,shortName):
	"""Calls bedGraphToBed9 per each bed graph file """
        dirTracks = self.output_dir + "/" + shortName  + "/tracks/"
        if not os.path.exists(dirTracks):
            os.makedirs(dirTracks)
        
        os.system(self.fetchChrSize + " " + self.assembly_name + " > " + self.output_dir + "/" + self.assembly_name+ ".chrom.sizes")

        for i in range(0,len(self.pathList)):
           
            os.system(self.bedGraphToBed9 + " " + self.pathList[i] + " " + self.output_dir + "/" \
                      + self.shortNameList[i]+ ".bed9" + " " + self.listOfColorsFile + " " + str(self.minimum_score) + " " + str(self.maximum_score))
            os.system(self.bed2BigBed + " " + "-type=bed9" + " " + self.output_dir + "/" + self.shortNameList[i]+ ".bed9" \
                      + " " + self.output_dir + "/" + self.assembly_name + ".chrom.sizes" + " " + dirTracks + "/" + self.shortNameList[i]+ ".bb")

    def buildHeatMapHub(self,shortName,description):
        """ Generates a HeatMap Hub File
        shortName - HeatMap Shortname
        description - Heatmap description name
        """
        dirHub = self.output_dir + "/" + shortName  + "/tracks/"
	pathHub = dirHub + "hub.txt"
	genomesFile = "genomes.txt";
	
        if not os.path.exists(dirHub):
            os.makedirs(dirHub)

	with open(pathHub, 'w') as hubFile:
            hubFile.write("hub "+ description + "\n")
            hubFile.write("shortLabel "+ shortName + "\n")
            hubFile.write("longLabel "+ description + "\n")
            hubFile.write("genomesFile "+ genomesFile + "\n")
            hubFile.write("email marcos.fernandez@upf.edu \n")

    def buildGenomesFile(self,shortName):
        """ Generates a HeatMap genomes file
        shortName - HeatMap Shortname
        """
        dirHub = self.output_dir + "/" + shortName  + "/tracks/"
        genomesFile = dirHub + "genomes.txt"
        trackDb = self.assembly_name + "/trackDb.txt"
	
	if not os.path.exists(dirHub):
            os.makedirs(dirHub)

        with open(genomesFile, 'w') as genFile:
            genFile.write("genome " + self.assembly_name + "\n")
            genFile.write("trackDb " + trackDb + "\n")

    def buildTrackDbFile(self,shortName,description,heatMapUrl):
        """ Generates trackDb files for the heat map
        shortName - HeatMap Shortname
        description - Heatmap description name
        heatMapUrl - Public URL where the heatmap will be accesible
        """
        dirTrackDB = self.output_dir + "/" + shortName  + "/tracks/" + self.assembly_name + "/"
        trackDb = dirTrackDB + "/trackDb.txt"
	
        if not os.path.exists(dirTrackDB):
            os.makedirs(dirTrackDB)

        with open(trackDb, 'w') as trackFile:
            #Header Section
            trackFile.write("track " + shortName + "\n")
            trackFile.write("compositeTrack on\n")
            trackFile.write("shortLabel " + shortName + "\n")
            trackFile.write("longLabel " + description + "\n")
            trackFile.write("type bigBed 9 .\n") 
            trackFile.write("visibility dense\n")
            trackFile.write("itemRgb on\n")
            trackFile.write("\n")

            #Tracks Section
            for i in range(0,len(self.shortNameList)):
                trackFile.write("track " + self.shortNameList[i] + "\n")
                trackFile.write("parent " + shortName +" on\n")
                trackFile.write("bigDataUrl " + heatMapUrl + "/" + shortName + "/tracks/" + self.shortNameList[i]+ ".bb\n")
                trackFile.write("shortLabel " + self.shortNameList[i] + "\n")
                trackFile.write("longLabel " + self.descriptionList[i] + "\n")
                trackFile.write("type bigBed 9 .\n")
                trackFile.write("visibility dense\n")
                trackFile.write("itemRgb on\n")
                trackFile.write("denseCoverage 0\n")
                trackFile.write("maxWindowToDraw 3000000\n")
                trackFile.write("\n")

def drawLegend(minimum,maximum,colors,dirOutput):
    """Draws a legend of color and ranges
    minimum - minimum score value
    maximum - maximum score value
    colors - RGBColors instance object
    dirOutput - Directory output """
    listRanges = []
    listLabels = []
    rangeHeatmap = maximum - minimum

    step = 0;
    for i in range(10):
        level = rangeHeatmap * (i/10.0)
        listRanges.append(level)
        if len(listRanges) == 2:
            step = level - listRanges[0]

    listRanges.append(listRanges[-1] + step)
   
    last = 0.0
    for i in range(len(listRanges)):
        if i == 0:
            last = float(i)
        else: 
            listLabels.append(str(last) + "-" + str(listRanges[i]))
            last = float(i)

    fig, axes = plt.subplots(nrows=10)
    fig.subplots_adjust(top=0.95, bottom=0.01, left=0.2, right=0.99)
    axes[0].set_title('Heatmap legend', fontsize=14)

    index = 0
    for ax, name in zip(axes, listLabels):
        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.1
        y_text = pos[1] + pos[3]/2.
        
        fig.text(x_text, y_text, name,  fontsize=10)
        ax.add_patch(Rectangle((x_text + 0.75, 0.7), -0.8, -0.2, edgecolor='none',facecolor=[colors.redList[index],colors.greenList[index],colors.blueList[index]]))
        index = index + 1

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()
   
    #Save legend 
    if not os.path.exists(dirOutput):
        os.makedirs(dirOutput)

    fig.savefig(dirOutput + '/heatmap.legend.png')


def check_parameters(args):
    """ Checks user parameters 
    args - parsed arguments
    """
    errorList = []
    
    if not args.assembly:
	errorList.append("Sorry!! Assembly name is empty!!")

    if not args.short_name:
        errorList.append("Sorry!! HeatMap short name is empty!!")

    if not args.description:
        errorList.append("Sorry!! HeatMap description is empty!!")

    if not args.url:
        errorList.append("Sorry!! Url description is empty!!")
   
    if not args.min_score:
        errorList.append("Sorry!! Minimum score value is empty!!")

    if not args.max_score:
        errorList.append("Sorry!! Maximum score value is empty!!")

    if args.min_score >= args.max_score:
        errorList.append("Sorry!! Maximum score con not be lower than Minimum score value!!")    
        
    if not args.rgb_list_file:
        errorList.append("Sorry!! No rgb list file selected!!")

    if not args.track_cfg_file:
        errorList.append("Sorry!! No track HeatMap file selected!!")

    if not args.out_dir:
        errorList.append("Sorry!! No Output directory selected!!")    

    if len(errorList) > 0:
        for error in errorList:
            print error
        return False
    
    return True





#1.Create object for argument parsinng
parser = argparse.ArgumentParser(prog="heatMapUcsc",description="Creates a remote server HeatMap track to be viewed in some UCSC genome browser.")     

#2.1 Definition of input parameters
input_group = parser.add_argument_group('Inputs')
input_group.add_argument('--assembly', dest="assembly", metavar="assembly", help='Assembly name. For exmple: hg19')
input_group.add_argument('--hm-short-name', dest="short_name", metavar="sort_name", help='HeatMap Short Name')
input_group.add_argument('--hm-description', dest="description", metavar="description", help='HeatMap Description')
input_group.add_argument('--hm-url', dest="url", metavar="url", help='Remote server URL from which the heatmap will be dowloaded.')
input_group.add_argument('--hm-min-score', dest="min_score", metavar="min_score", help='Minimum score value to represent the data in 10 color stages.')
input_group.add_argument('--hm-max-score', dest="max_score", metavar="max_score", help='Maximum score value to represent the data in 10 color stages.')
input_group.add_argument('--rgb-list-file', dest="rgb_list_file", metavar="rgb_list_file", help='File list of rgb color coordinates, it must have 10 lines and for each line a RGB coordinate.')

#2.2 Definition of configuration parameters
config_group = parser.add_argument_group('Configuration')
config_group.add_argument('--track-config-file', dest="track_cfg_file", metavar="track_cfg_file", help='File track configuration file. Format:\
                          One line per heatmap track (Heatmap is a stack of tracks). bedGraphFilePath,ShortName,Description')

#2.3 Ouput
config_group = parser.add_argument_group('Output')
config_group.add_argument('--output-directory', dest="out_dir", metavar="out_dir", help='Ouput directory')

#3. Argument parsing
args = parser.parse_args()

#3.1 Check Parameters
if not check_parameters(args):
    sys.exit()

#4. Check and file parsing
#4.1. Create object class RGBColors
rgbManager = RGBColors()
#4.2 RGB Color List Parsing
if not rgbManager.readColorFile(args.rgb_list_file):
    print "Sorry!! Sorry RGB list file is not well formatted!!"
    sys.exit()

#5. Check Track file list
#5.1. HeatMap tracks
heatmapTracks = HeatMapTracks()
#5.2. HeatMap tracks parsing
if not heatmapTracks.parseHeatMap(args.track_cfg_file):
    print "Sorry!! Sorry Heat Map list file is not well formatted!!"
    sys.exit()

#5.3. HeatMap legend for the color meanings
drawLegend(float(args.min_score),float(args.max_score),rgbManager,args.out_dir)
sys.exit()

#6. Transform BEDGRAPH TO BIGBED
heatmapTracks.setScores(args.min_score,args.max_score)
heatmapTracks.setListColors(args.rgb_list_file)
heatmapTracks.setOutputDir(args.out_dir)
heatmapTracks.setAssemblyName(args.assembly)

heatmapTracks.fromBedGraphToBigBed(args.short_name)

#7. HEAT MAP CONFIGURATION
heatmapTracks.buildHeatMapHub(args.short_name,args.description);
heatmapTracks.buildGenomesFile(args.short_name);
heatmapTracks.buildTrackDbFile(args.short_name,args.description,args.url)
	
#8. DO LEGEND FILE

#9. UCSC LINKS
print "Done!! Move The Heatmap directory structure to the url server:" + args.url
print "Please consider the option to remove bed9. These files may be removed."

euroLink = "http://genome-euro.ucsc.edu/cgi-bin/hgTracks?db=" + args.assembly
euroLink = euroLink + "&hubUrl=" + args.url + "/" + args.short_name + "/tracks/hub.txt";

print "Euro UCSC: " + euroLink
		
ucscLink = "http://genome.ucsc.edu/cgi-bin/hgTracks?db=" + args.assembly
ucscLink = ucscLink + "&hubUrl=" + args.url + "/" + args.short_name + "/tracks/hub.txt";

print "Californa UCSC: " + ucscLink

with open(args.out_dir + "/" + args.short_name + ".links" , 'w') as links:
    links.write("Euro UCSC: " + euroLink + "\n")
    links.write("Californa UCSC: " + ucscLink + "\n")
 




