from main import mainFunc
import sys, getopt

class Main:
    """docstring for Main."""

    def __init__(self):
        super(Main, self).__init__()

    def main(self, argv):
        inputfile = ''
        try:
            # print("Here")
            opts, args = getopt.getopt(argv, "hi:", ["ifile="])
            # print(opts, args)
            if opts == [] and args == []:
                print("ERROR")
                print ("Help:","python",'init.py -i <TextFileName>')
        except getopt.GetoptError as err:
            sys.exit(2)

        for opt, arg in opts:
            if opt == '-h':
                print ('test.py -i <inputfile>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg

        # print ('Input file is "', inputfile,'"')
        return inputfile


if __name__ == "__main__":
    p = Main()
    inputfile = p.main(sys.argv[1:])
    if inputfile:
        x = mainFunc()
        x.get_entity(str(inputfile))
