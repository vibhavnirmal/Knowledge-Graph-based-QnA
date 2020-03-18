import sys, getopt
from getentitypair import GetEntity
from qna import QuestionAnswer
from exportPairs import exportToJSON
from graph import GraphEnt

class Main:
    """docstring for Main."""

    def __init__(self):
        super(Main, self).__init__()
        self.qna = QuestionAnswer()
        self.x = GetEntity()
        self.exp = exportToJSON()
        self.graph = GraphEnt()

    def main(self, argv):
        inputfile = ''
        inputQue = ''
        try:
            # print("Here")
            opts, args = getopt.getopt(argv, "hi:q:g:s:", ["ifile=", "question=","showGraph=","showEntities="])
            # print(opts, args)
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
                # print(inputQue)
            elif opt in ("-g", "--showGraph"):
                showGraph = arg
            elif opt in ("-s", "--showEntities"):
                showEntities = arg
            else:
                assert False, "unhandled option"

        # print ('Input file is "', inputfile,'"')
        return inputfile, inputQue, showGraph, showEntities


if __name__ == "__main__":
    p = Main()
    inputfile, questionWeAsked, showGraph, showEntities = p.main(sys.argv[1:])
    dataEntities, numberOfPairs = p.x.get_entity(str(inputfile))
    if inputfile:
        p.exp.dumpdata(dataEntities[0])

        if showEntities in ('y', 'yes', 'true'):
            print(dataEntities[0])
        # p.x.get_entity(str(inputfile))
        # questionWeAsked = questionWeAsked.lower()
        # print(questionWeAsked)
        if showGraph in ('y', 'yes', 'true'):
            p.graph.createGraph(dataEntities)
        if questionWeAsked:
            my_answer = p.qna.findanswer(questionWeAsked, numberOfPairs)
            # print("The Answer of the question asked")
            print("------------------------------------------------------------------------------------------------------------")
            print("Question: ",questionWeAsked)
            print("Answer:   ",my_answer)
            print("------------------------------------------------------------------------------------------------------------")
