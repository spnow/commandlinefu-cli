YELLOWC = "\033[93m"
CYANC   = "\033[36m"
ENDC    = "\033[0m"

import sys
import getopt
from urllib2 import urlopen, URLError
from base64 import b64encode
from json import loads

def main():
    opt = 0
    rjson  = "[]"
    if(len(sys.argv)<2):
        usage()
        sys.exit(1)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hac:t", ["help", "all", "command=", "tagged"])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(1)
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif o in ("-a", "--all"):
            opt = 1
        elif o in ("-c", "--command"):
            command = a
            opt  = 2
        elif o in ("-t", "--tagged"):
            command = a
            opt  = 3
    if opt == 1:
        try:
            rjson = urlopen("http://www.commandlinefu.com/commands/browse/sort-by-votes/json")
            rjson = rjson.read()
        except URLError, err:
            print str(err)
            sys.exit(1)
    elif opt == 2:
        try:
            rjson = urlopen("http://commandlinefu.com/commands/matching/"+command
                            +"/"+b64encode(command)+"/json")
            rjson = rjson.read()
        except URLError, err:
            print str(err)
            sys.exit(1)
    elif opt == 3:
        try:
            rjson = urlopen("http://commandlinefu.com/commands/tagged/163/"+command
                            +"/json")
            rjson = rjson.read()
        except URLError, err:
            print str(err)
            sys.exit(1)
    if rjson == "[]":
        print "[-] command not found"
        sys.exit(1)
    print_json(rjson)

def print_json(rjson):
    try: data = loads(rjson)
    except ValueError, err: return
    for i in range(0,len(data)):
        votes   = data[i]["votes"]
        cmd     = data[i]["command"]
        summary = data[i]["summary"]
        print "%s%d) %s (votes:%s)\n\t%s%s%s%s" % (CYANC, i+1, summary,
                                                 votes, ENDC, YELLOWC, cmd, ENDC)
def usage():
    commands = {
        "-c <command>":"\tSearch for specific command",
        "-t <command>":"\tSearch for tagged commands",
        "-a":"\t\tShow latest commandlinefu submissions",
        "-h":"\t\tShow help"
        }
    print "Usage : %s" % sys.argv[0]
    for options in commands:
        print "\t%s%s" % (options, commands[options])

if __name__ == "__main__":
    main()
