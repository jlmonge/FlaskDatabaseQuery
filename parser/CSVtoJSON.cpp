#include <fstream>
#include <iostream>
#include <vector>
#include <string>

bool prepareFiles(std::ifstream& in, std::ofstream& out);
std::vector<std::string> prepareCats(std::ifstream& in);
unsigned long parse(bool vis, std::ifstream& in, std::ofstream& out, std::vector<std::string>& cats);
std::string indent(unsigned int amt);
void readCurrentLine(bool vis, std::string& ref, std::vector<std::string>& bin);

int main() {
    std::ifstream reader;
    std::ofstream writer;

    std::cout << "Please ensure your .CSV file is in the correct location before starting.\n"
              << "         File path: .\\Files\\input\\" << std::endl;

    while (!prepareFiles(reader, writer)) {
        std::cout << "There was an error opening your files.\nPlease try again, or use CTRL + C to abort." << std::endl;
        reader.close();
        writer.close();
        reader.clear();
        writer.clear();
    }

    std::vector<std::string> catergories = prepareCats(reader);

    char choice;
    bool visuals = false;
    std::cout << "\nThe program is ready to translate your file.\n"
        << "Would you like to see the data while it is being parsed? (Y/N): ";
    std::cin >> choice; choice = toupper(choice);
    while (choice != 'Y' && choice != 'N') {
        std::cout << "Invalid response. Please enter Y for Yes or N for No.\n";
        std::cin >> choice;
    }
    if (choice == 'Y') { visuals = true; }
    
    std::cout << "\nNow translating...\n";
    unsigned long total = parse(visuals, reader, writer, catergories);

    reader.close();
    writer.close();

    std::cout << "The file was translated successfully.\n"
              << total << " lines of data were analyzed.\n"
              << "         File path: .\\Files\\output\\" << std::endl;

    return 0;
}

bool prepareFiles(std::ifstream& in, std::ofstream& out) {
    std::string inFile = ".\\Files\\input\\";
    std::string outFile = ".\\Files\\output\\";
    std::string fileName;

    std::cout << "\nEnter the file to translate to JSON (Do not include the file type): ";
    std::cin >> fileName;
    unsigned int nameSize = fileName.size();

    fileName.append(".csv");
    inFile += fileName;

    fileName.resize(nameSize);
    fileName.append(".json");
    outFile += fileName;

    in.open(inFile);
    out.open(outFile);

    if (in.fail() || out.fail()) { return false; }
    else { return true; }
}

std::vector<std::string> prepareCats(std::ifstream& in) {
    std::vector<std::string> retVec;
    retVec.reserve(15);
    std::string firstLine;
    std::getline(in, firstLine);

    std::cout << "\nCatergories:\n";

    if (in.good()) {
        std::string catBuilder = "";
        for (unsigned i = 0; i < firstLine.size(); ++i) {
            if (firstLine.at(i) != ',') { catBuilder.push_back(firstLine.at(i)); }
            else {
                retVec.push_back(catBuilder);
                std::cout << "   " << retVec.size() << ".   " << retVec.back() << "\n";
                catBuilder.clear();
            }
        }
        std::cout << std::endl;
    }
    else {
        std::cout << "An error occurred while reading the file!\n";
        exit(1);
    }

    return retVec;
}

unsigned long parse(bool vis, std::ifstream& in, std::ofstream& out, std::vector<std::string>& cats) {
    unsigned long retVal = 0;
    unsigned int tab = 1;
    std::string readingLine;
    std::vector<std::string> lineVals;
    lineVals.reserve(cats.size());

    out << "[\n";
    while (std::getline(in, readingLine)) {
        if (!in.fail()) {
            ++retVal;
            if (vis) { std::cout << "Reading entry number " << retVal << "...\n"; }
            readCurrentLine(vis, readingLine, lineVals);
            out << indent(tab) << "{\n"; ++tab;
            for (unsigned i = 0; i < cats.size(); ++i) {
                if ((i + 1) == cats.size()) { out << indent(tab) << "\"" << cats.at(i) << "\": \"" << lineVals.at(i) << "\"\n"; }
                else { out << indent(tab) << "\"" << cats.at(i) << "\": \"" << lineVals.at(i) << "\",\n"; }
            }
            if (in.peek() != -1) { --tab; out << indent(tab) << "},\n"; }
            else { --tab; out << indent(tab) << "}\n"; }
            lineVals.clear();
        }
    }
    out << "]\n";

    return retVal;
}

std::string indent(unsigned int amt) {
    std::string retVal = "";
    for (unsigned i = 0; i < amt; ++i) {
        retVal += "\t";
    }
    return retVal;
}

void readCurrentLine(bool vis, std::string& ref, std::vector<std::string>& bin) {
    std::string val = "";
    for (unsigned i = 0; i < ref.size(); ++i) {
        if (ref.at(i) != ',') { val.push_back(ref.at(i)); }
        else {
            bin.push_back(val);
            if (vis) { std::cout << "   " << bin.size() << ".   " << bin.back() << "\n"; }
            val.clear();
        }
    }
    if (vis) { std::cout << std::endl; }
}