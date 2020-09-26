import datetime
dueDateR = datetime.datetime(2020, 8, 26, 23, 59) #duedate for reply. year, month, day, hour, minute
dueDateC = datetime.datetime(2020, 8, 25, 23, 59) #duedate for comment
#Hey Mr. Clarke! Please edit this to fix the duedate:


#format of dictionary:
#{name:[{timeData:??, timeDisplay:??, content:??},{},{}....],name...}
#dictionary of lists of dictionaries


#Today thing
d = {}

months = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"
months = months.split()

def readData(d, f):

    """
    Stages are small steps taken in this process

    loop:
        Condition: if it says "Hide All n Replies" OR "hide 1 reply" set replyChain = n
        Stage 1: if it says Profile picture, store name
            #Note: Override stage even if stage is different
        Stage 2: then look at next line with date, edit it, and store date and time values
            #Note: if the above fails, go back to stage 1
        Stage 3: then read all the lines until the next "Reply" is reached
        if replyChain > 0:
            replyChain -= 1
    """

    i = 0
    replyChain = 0
    d = {}
    stage = 1
    for x in f.splitlines():
        #print("=============================")
        #print(d)
        if (x.startswith("Hide All")) and (x.endswith("Replies") or x[:-1].endswith("Replies") or x[:-2].endswith("Replies")):
            replyChain = int(x.split()[2])
            print(replyChain)
        elif  (x == "Hide 1 reply\n") or (x.endswith("Hide 1 reply")) or (x[:-2] == "Hide 1 reply"):
            replyChain = 1

            
        elif x.startswith("Profile picture"):
            #store username
            name = " ".join(x.split()[3:])
            stage = 2
            #print(name)

        elif stage==2 and x.startswith(name):
            try:
                
                time = x.replace(",", "").replace(name, "").replace("Edited · ", "").split()
                if "Today" in time:
                    now = datetime.datetime.now().date()
                    month = now.month
                    year = now.year
                    day = now.day
                    hour, minute = [int(x) for x in time[2].split(":")]
                    period = time[3] #period means am/pm
                else:
                
                    #W is for word, while no W is for number
                    dayW = time[0]
                    monthW = time[1]
                    month = months.index(monthW)+1
                    day = int(time[2])
                    year = int(time[3])
                    hour, minute = [int(x) for x in time[5].split(":")]
                    period = time[6] #period means am/pm
#Ashlee Nicole TugadeToday at 8:20 pm
#normal
#Shivani ChoudharyTue Aug 25, 2020 at 8:12 pm

                if period == "pm" and hour < 12:
                    hour += 12
                content = ""
                stage = 3
                #large to small: (year, month, day, hour, minute)
                timeData = datetime.datetime(year, month, day, hour, minute)
                timeDisplay = "%s %s %s %s %s:%s %s" % (dayW, monthW, day, year, hour, minute, period)
            except:
                stage = 1
                print("WARNING, THE FOLLOWING NAME WAS IGNORED:")
                print(name)

        elif stage==3:
            if x == "Reply":
                #heres the code for storing all the information in the dictionary

                #if name doesnt alr exist
                if not(name in d):
                    d[name] = []
                commentType = "comment"
                if replyChain > 0:
                    commentType = "reply"

                comment = {"content":content, "commentType":commentType, "timeDisplay":timeDisplay,"timeData":timeData}
                d[name].append(comment)
                if replyChain > 0:
                    replyChain -= 1

            else:
                content += x


        i += 1
    if i == 0:
        print("WARNING: the file was empty!")
    nd = {k: d[k] for k in sorted(d)}
    return nd

def printData(d):
    print("===========================================================================")
    for key, value in d.items():
        for x in value:
            name = key
            timeDisplay = x["timeDisplay"]
            content = x["content"]
            print("----------------------------------------------------")
            print(name)
            print(timeDisplay)
            print("\n"+content)
            print("----------------------------------------------------")
    print("===========================================================================")

def searchName(d, name):
    if not (name in d):
        for key, value in d.items():
            if name.lower() in key.lower():
                print("did you mean %s?" % key)
        print("the name you specified does not exist in the data")
        return
    comments = len(d[name])
    print("user has made %s comments" % comments)

def listStats(d, dueDateR, dueDateC):
    print("----------------------------------------------------------------------------------------")
    print("Name".ljust(25)+"|"+"total".ljust(8)+"|"+"on time C".ljust(8)+"|"+"late C".ljust(8)+"|"+"on time R".ljust(8)+"|"+"late R".ljust(9))
    print("----------------------------------------------------------------------------------------")
    loop = False
    ls = []
    for key,value in d.items():
        loop = True
        lateReply = 0
        onTimeReply = 0
        lateComment = 0
        onTimeComment = 0
        for x in value:
            if x["commentType"] == "reply":
                if dueDateR < x["timeData"]:
                    lateReply += 1
                else:
                    onTimeReply += 1
            elif x["commentType"] == "comment":
                if dueDateC < x["timeData"]:
                    lateComment += 1
                else:
                    onTimeComment += 1
        print(key.ljust(25), str(len(value)).ljust(9), str(onTimeComment).ljust(9), str(lateComment).ljust(9), str(onTimeReply).ljust(9), str(lateReply).ljust(9))
    print("----------------------------------------------------------------------------------------")
    if not loop:
        print("there were no stats listed. Please type `load` if you forgot to load the file")


def helper():
    print("----------------------------------------------------")
    print("""
    SETUP: Go to the schoology discussion page. ctrl A + ctrl C. Then, ctrl V into `input.txt`

    STEP 1: open the python file and change the lines 2-3 to set the default duedates. if you have this program running in this process, make sure your re-run it to update your changes.
    STEP 2: type "load" This will process data from the text file "input.txt"
    STEP 3: type "stats"

    ---------
    other commands--:
    help: Leads you to this place
    search [name]: search for a name in the list of submissions
    print: Print data. This won't really be of much use
    read file [fileName]: read a file. You must do this before doing stats
    duedateR [date]: (look at NOTE below for date format) set duedate for replies
    duedateC [date]: (look at NOTE below for date format) set duedate for comments
    ---------

    *NOTE: date format must be: "mm/dd/yyyy hh:mm" (24 hour clock)
    example: 08/27/2020 23:59
            """)
    print("----------------------------------------------------")
