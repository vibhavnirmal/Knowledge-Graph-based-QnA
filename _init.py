import getopt
import sys

from kwQnA._exportPairs import exportToJSON
from kwQnA._getentitypair import GetEntity
from kwQnA._graph import GraphEnt
from kwQnA._qna import QuestionAnswer


class Main:
    """docstring for Main."""

    def __init__(self):
        super(Main, self).__init__()
        self.qna = QuestionAnswer()
        self.getEntity = GetEntity()
        self.export = exportToJSON()
        self.graph = GraphEnt()

    def main(self, argv):
        inputfile = ''
        inputQue = ''
        try:
            opts, args = getopt.getopt(argv, "hi:q:g:s:", ["ifile=", "question=","showGraph=","showEntities="])
            if opts == [] and args == []:
                print("ERROR")
                print("Help:")
                print("python init.py -i <TextFileName> -q <Question> -s <show Ent>")
        except getopt.GetoptError as err:
            sys.exit(2)

        for opt, arg in opts:
            showGraph , showEntities= "f", "f"
            if opt == '-h':
                print ('test.py -i <inputfile> -q <question> -g <y or n> -s <Show Entities>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-q", "--question"):
                inputQue = arg
            elif opt in ("-g", "--showGraph"):
                showGraph = arg
            elif opt in ("-s", "--showEntities"):
                showEntities = arg
            else:
                assert False, "unhandled option"

        return inputfile, inputQue, showGraph, showEntities


if __name__ == "__main__":
    initialize = Main()
    inputfile, inputQue, showGraph, showEntities = initialize.main(sys.argv[1:])

    input_file = open(inputfile,"r+")

    if inputfile:
        refined_text = initialize.getEntity.preprocess_text(input_file)

        dataEntities, numberOfPairs = initialize.getEntity.get_entity(refined_text)
        """ getentity return dataentity[0] """
        if dataEntities:
            initialize.export.dumpdata(dataEntities[0])

            if showEntities in ('y', 'yes', 'true'):
                print(dataEntities[0])

            if showGraph in ('y', 'yes', 'true'):
                initialize.graph.createGraph(dataEntities[0])

            if inputQue:
                outputAnswer = initialize.qna.findanswer(inputQue, numberOfPairs)

                print("------------------------------------------------------------------------------------------------------------")
                print("Question: ",inputQue)
                print("Answer:   ",outputAnswer)
                print("------------------------------------------------------------------------------------------------------------")

    else:
        print("No Input file detected")
