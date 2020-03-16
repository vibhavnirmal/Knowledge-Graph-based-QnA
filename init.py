# from getentitypair import GetEntity
import sys, getopt
from getentitypair import GetEntity
from qna import QuestionAnswer
from exportPairs import exportToJSON

class Main:
    """docstring for Main."""

    def __init__(self):
        super(Main, self).__init__()
        self.qna = QuestionAnswer()
        self.x = GetEntity()
        self.exp = exportToJSON()

    def main(self, argv):
        inputfile = ''
        inputQue = ''
        try:
            # print("Here")
            opts, args = getopt.getopt(argv, "hi:q:", ["ifile=", "question="])
            # print(opts, args)
            if opts == [] and args == []:
                print("ERROR")
                print("Help:")
                print("python init.py -i <TextFileName> -q <Question>")
        except getopt.GetoptError as err:
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print ('test.py -i <inputfile> -q <question>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-q", "--question"):
                inputQue = arg
                # print(inputQue)
            else:
                assert False, "unhandled option"

        # print ('Input file is "', inputfile,'"')
        return inputfile, inputQue


if __name__ == "__main__":
    p = Main()
    inputfile, questionWeAsked = p.main(sys.argv[1:])
    dataEntities = p.x.get_entity(str(inputfile))
    # print(questionWeAsked)
    if inputfile:
        p.exp.dumpdata(dataEntities[0])
        # p.x.get_entity(str(inputfile))
        p.qna.findanswer(questionWeAsked)
