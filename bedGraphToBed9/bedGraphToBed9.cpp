/*
 * main.cpp
 *
 *  Created on: 25 Out, 2013
 *      Author: marcos
 */
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <sstream>
#include <algorithm>
#include <math.h>

using namespace std;

struct heatMapSettings
{
	std::vector <std::string> vHeatMapColors;
	float fMinThresshold;
	float fMaxThresshold;
};

static std::vector<std::string> split(std::string s, char delim, std::vector<std::string> elems)
{
	std::stringstream ss(s);
	std::string item;
	while(std::getline(ss, item, delim)) {
		elems.push_back(item);
	}
	return elems;
}

static std::vector<std::string> split(const std::string &s, char delim)
{
	std::vector<std::string> elems;
	return split(s, delim, elems);
}


/**
 * \brief Test if a file exitst
 */
bool fexists(const char *filename)
{
  ifstream ifile(filename);
  return ifile;
}

/**
 * \brief Test File Names
 */
bool testFile(string file)
{
	if(!fexists(file.c_str()))
	{
		cout << "Sorry!! Bed file was not defined or the file: " << file.c_str() <<" does not exists !!" << endl;
		return false;
	}
	return true;
}

/**
 * \brief Print Help File
 */
void printHelp()
{
	cout << "bedGraphToBed9 Translates from BedGraph to BED9 heatMap format" << endl;
	cout << "USAGE: bedGraphToBed9 bedGraphFile bedOutputFile listColorsFile minThershhold maxThershhold" << endl;
	cout << "Example: bedGraphToBed9 example.graph.bed example.heatmap.bed example.colors 1 10 "<< endl;
}

/**
 * \brief Initialization heatMap structure
 * \param heatMapConf heatMapSettings reference structure
 * \param string name reference for list colors file,
 * \param float min threshhold value
 * \param float max threshhold value
 * \return false if some values was not correct
 */
bool setHeatMapConf(heatMapSettings & heatMapConf,string & listColorsFile,float min, float max)
{
	//1.CLEAR vector string values
	heatMapConf.vHeatMapColors.clear();
	//2.SET THRESHHOLDS
	heatMapConf.fMaxThresshold = max;
	heatMapConf.fMinThresshold = min;
	//3.ADD STRING r,g,b coordinates
	int nRGBCoordinates = 0;

	ifstream inColorsFile;
	inColorsFile.open(listColorsFile.c_str());
	string lineRead = "";

	if (inColorsFile.is_open())
	{
		if (inColorsFile.good())
		{
			getline (inColorsFile,lineRead);
		}

		while ( ! lineRead.empty())
		{
			heatMapConf.vHeatMapColors.push_back(lineRead);
			nRGBCoordinates ++;
			getline (inColorsFile,lineRead);
		}
	}

	inColorsFile.close();

	//4.TEST NUMBER OF rgb coordinates
	if(nRGBCoordinates == 10)
	{
		return true;
	}

	return false;
}

/**
 * \brief Returns a Heat Map RGB Color coordinate from a score value and a range of value
 * \param $score Given score values
 * \param $maxValue Maximum possible value
 * \param $minValue Minimum possible value
 * \return string rgb color coordinate
 */
string getHeatMapColor(float fScore, heatMapSettings & heatMapConf)
{
	//1.Boundaries correction
	if(fScore > heatMapConf.fMaxThresshold)
	{
		fScore = heatMapConf.fMaxThresshold;
	}
	else if(fScore < heatMapConf.fMinThresshold)
	{
		fScore = heatMapConf.fMinThresshold;
	}

	//2.Index Color
	float fTotal = heatMapConf.fMaxThresshold - heatMapConf.fMinThresshold;
	float fNumericPoint = fScore - heatMapConf.fMinThresshold;
	unsigned int nColorNumber = (unsigned int) round((fNumericPoint/fTotal)*10);

	//3 Extreme limits correction
	if(nColorNumber > 9)
	{
		nColorNumber = 9;
	}
	else if(nColorNumber < 0)
	{
		nColorNumber = 0;
	}

	return heatMapConf.vHeatMapColors[nColorNumber];
}


/**
 * \brief From bedGraph line and it assignedl color builds a Bed9 file
 * \param fields bedGraphLine read bed graph input line
 * \param color rgb color coordinate for the given bed graph line
 * \return BED9 line
 */
string buildNewBed9Line(vector<string> & fields, string & color)
{
	return fields[0]+string("\t")+fields[1]+string("\t")+fields[2]+string("\theatMap\t0\t.\t")+fields[1]+string("\t")+fields[2]+string("\t")+color;
}

/**
 * \brief main function
 */
int main(int argc, char *argv[])
{
	//1.TEST ARGUMENTS
	if(argc != 6)
	{
		printHelp();
		return 0;
	}

	//2.ARGUMENTS
	string sBedGraphFile = argv[1];
	string sBedOutputFile = argv[2];
	string sListColorsFile = argv[3];
	float fMinThershhold = atof(argv[4]);
	float fMaxThershhold = atof(argv[5]);


	//3.TEST BEDGRAPH INPUT FILE
	if(!testFile(sBedGraphFile))
	{
		return 0;
	}

	//3.REMOVE PREVIOUSLY CRETED GOAL FILES
	if(fexists(sBedOutputFile.c_str()))
	{
			remove(sBedOutputFile.c_str());
	}

	//5.HEAT MAP CONFIGURATION SET UP
	heatMapSettings setHeatMap;

	if(!setHeatMapConf(setHeatMap,sListColorsFile,fMinThershhold, fMaxThershhold))
	{
		cout << "Sorry!! List of Colors files must have 10 rgb coordinates!!" << endl;
		return 0;
	}

	//6. READ BED GRAPH INPUT FILE
	ifstream inBedGraph;
	inBedGraph.open(sBedGraphFile.c_str());
	string lineRead = "";

	std::ofstream outFile(sBedOutputFile.c_str(), std::ios_base::app | std::ios_base::out);

	if (inBedGraph.is_open())
	{
		if (inBedGraph.good())
		{
			getline (inBedGraph,lineRead);
		}

		while ( ! lineRead.empty())
		{
			vector<string> fields = split(lineRead, '\t');
			string sColor = getHeatMapColor(atof(fields[3].c_str()),setHeatMap);
			outFile << buildNewBed9Line(fields, sColor) << endl;

			getline (inBedGraph,lineRead);
		}
	}

	//7. CLOSE INPUT AND OUTPUT FILES
	inBedGraph.close();
	outFile.close();

	return 1;
}
