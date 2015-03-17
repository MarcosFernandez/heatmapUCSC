General Description
___________________
This directory contains the source code for the heatMapUcsc.py.

heatMapUcsc.py is free software.  See the file COPYING for copying conditions.
heatMapUcsc.py is copyright by the Centro Nacional de Analisis Genomico.(CNAG).

heatMapUcsc.py is a Python script that generates a folder structure to visualize 
Heatmap tracks in UCSC genome browser instances. A Heatmap track is a stack of 
tracks each one coming form a BedGraph file. Per each bed region a colour 
will be assigned according to the signal value.

HeatMap Tracks
______________
A heat map is a graphical representation of data where the individual values contained in a
matrix are represented as colours. HeatMap tracks are a good alternative for representing
BedGraph data where each genomic region has a score value assigned. You can build a
HeatMap from a set of BedGraph files and a range of 10 colours representing 10 cluster divisions 
of your score data.

Public Server Hostage
______________________
HeatMap tracks are managed through track hubs. Track hubs are web-accessible directories of 
genomic data that can be viewed on each instance of UCSC Genome Browser. Hubs are a useful tool 
for visualizing a large number of genome-wide data sets like heat maps. 

The track hub utility allows efficient access to data sets from around the world through the familiar 
Genome Browser interface. The data underlying the tracks and optional sequence in a hub reside 
on the remote server of the data provider rather than at UCSC. Genomic annotations are stored in
compressed binary indexed files in bigBed, bigWig, BAM or VCF format that contain the
data at several resolutions.

When a hub track is displayed in the Genome Browser, only the relevant data needed to support the view 
of the current genomic region are transmitted rather than the entire file. The transmitted data are 
cached on the UCSC server to expedite future access. This on-demand transfer mechanism eliminates 
the need to transmit large data sets across the Internet, thereby minimizing upload time into the browser.
The track hub utility offers a convenient way to view and share very large sets of data.

HeatMap tracks are hubs containing bigBed files and located in a public server. They
can be showed by any UCSC genome browser.

BedGraph Signal Tracks
______________________
To create a HeatMap track you must build a set of BedGraph files to represent each row of your
HeatMap. Recall that the BedGraph must be well formatted which means: 
	A sorted bed file, no headers, four fields (chromosomeName, chromosomeStart, chromosomeEnd,signal) 
	Each field must be separated by tabulator.

Create HeatMap Track
____________________
To start the process of building a HeatMap track you must have access to an URL address for your public server data 
where the HeatMap hub is going to be stored. 

You must specify a Minimum and a Maximum Score values to represent your data in 10 color stages.

You must define a file of RGB colour coordinates per each colour scale. Score values lower
than the Minimum will be painted with first colour and score values over the Maximum will
be painted with 10 th colour.

A CSV list file with one row per BedGraph must be created. Each row must follows next
standard:
	pathBedFileRelativeScratchTmp,”ShortNameIdentification”,”Description Track”

heatMapUcsc.py will automatically create a hub folder structure. Firstly transforming each
BedGraph file to a Bed9 (File containing RGB color information). 
Secondly each Bed9. file will be transformed to a big binary file and finally a set of 
files to manage the hub will be created. ( genomes.txt, hub.txt and trackDb.txt).

A hub structure will be built with bigBinary files (.bb) and hub manager files (genomes.txt, hub.txt and trackDb.txt). 
Copy the complete folder to your public server. Now the HeatMap data will be available to any UCSC Genome Browser.

Other output files
__________________
Once the heatmap is created two files will be generated. The first one is a PNG image with the heatmap legend. The second one
contains the links to be viewed the heatmap in europe and santa cruz instances of the UCSC genome browser.

Depedencies
___________

heatMapUcsc.py uses three external tools to perform the Heatmap creation process.

	1. bedGraphToBed9	C++ app which transform a BedGrapgh file to a bed9 file for code HeatMap
				color regions.	

	2. bedToBigBed		kent C application which transforms a bed file to a bigbed binary file.

	3. fetchChromSizes      kent C application which calculates contig length for a given assembly.

bedGraphToBed9 is distrubuted with heatMapUcsc.py package. You must compile it following the README instructions 
located in bedGraphToBed9 folder.

bedToBigBed must be downloaded from:  

	Linux 64 bit architecture: wget -c http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/bedToBigBed
	For other platforms check http://hgdownload.cse.ucsc.edu/admin/exe/

fetchChromSizes must be downloaded from:

	Linux 64 bit architecture: wget -c http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/fetchChromSizes
  	For other platforms check http://hgdownload.cse.ucsc.edu/admin/exe/

Modify external binary variables
________________________________

You must modify the variables that are storing the path to the external binaries. Those variables are located in the
__init__ method of HeatMapTracks class. You must modify self.bedGraphToBed9, self.bed2BigBed and self.fetchChrSize 
with the path where you have the binaries.

class HeatMapTracks:

    def __init__(self):
        """Class constructor"""
        self.pathList = [] # List of bed paths
        self.shortNameList = [] # List of short names for tracks
        self.descriptionList = [] # List of description per track
        self.bedGraphToBed9 = "/path/to/bedGraphToBed9" #MODIFY ME 
        self.bed2BigBed = "/path/to/bedToBigBed" #MODIFY ME
        self.fetchChrSize = "/path/to/fetchChromSizes" #MODIFY ME
        self.listOfColorsFile = ""
        self.minimum_score = -1
        self.maximum_score = -1
        self.output_dir = ""
        self.assembly_name = ""


External Dependencies Lincenses
_______________________________

bedGraphToBed9 is distrubuted under GPLv3 lincense.

UCSC applications (bedToBigBed and fetchChromSizes) are free for academic, nonprofit, and personal use. A 
license is required for commercial download and installation of these binaries. 
For information about commercial licensing of the Genome Browser software, see http://genome.ucsc.edu/license/


-------------------------------------------------------------------------------
Copyright (C) 2009-2015 Centro Nacional Análisis Genómico (CNAG).

heatMapUcsc.py is free software; you can redistribute it and/or modify it under the
terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or (at your option) any later
version.

heatMapUcsc.py is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
