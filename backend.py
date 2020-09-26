


"""
parameters
title=request.form['title']
duedate=request.form['duedate']
duedate2=request.form['duedate2']
assignment1=request.form['assignment1']
assignment2=request.form['assignment2']
paste=request.form['paste']



title: hello
duedate1: 04/09/2020
duedate2: 05/09/2020
time1: 9:00 am
time2: 10:00 am
assignment1: Replies
assignment2: Replies
pasted:   hello

If the time is between 12:00 AM and 12:59 AM, we subtract 12 hours.
If the time is between 1:00 AM and 12:59 PM, 24 hour time is same as 12 hour time.
If the time is between 1:00 PM and 11:59 PM, we add 12 hours to input time.
"""
import datetime


def processTime(duedate, time):
    day, month, year = [int(d) for d in duedate.split("/")]
    hourMinute, amOrPm = time.split()
    hour, minute = [int(x) for x in hourMinute.split(":")]

    if amOrPm == "am" and hour == 12:
        hour -= 12
    elif amOrPm == "pm" and (hour in range(1, 12)) and (minute in range(0, 60)):
        hour += 12
    return datetime.datetime(year, month, day, hour, minute)



def run(title, duedate1, duedate2, time1, time2, assignment1, assignment2, paste):
    print("debug: ", title, duedate1, duedate2, time1, time2, assignment1, assignment2)

    
    
    dueDateC = -1
    dueDateR = -1
    if assignment1 == "Comments":
        dueDateC = processTime(duedate1, time1)
    elif assignment2 == "Comments":
        dueDateC = processTime(duedate2, time2)
    if assignment1 == "Replies":
        dueDateR = processTime(duedate1, time1)
    elif assignment2 == "Replies":
        dueDateR = processTime(duedate2, time2)
    #dueDateR = datetime.datetime(2020, 8, 27, 23, 59) #duedate for reply. year, month, day, hour, minute
    #dueDateC = datetime.datetime(2020, 8, 28, 23, 59) #duedate for comment

    d = {}
    open('templates/table.html', 'w').close()

    with open("templates/table-head.html") as f:
        table_head = f.readlines()
    with open("templates/table-foot.html") as f:
        table_foot = f.readlines()

    import schoologyCounter as sc
    f = paste
    d = sc.readData(d, f)







#print("Name".ljust(25)+"|"+"total".ljust(8)+"|"+"on time C".ljust(8)+"|"+"late C".ljust(8)+"|"+"on time R".ljust(8)+"|"+"late R".ljust(9))

#name, total, on time Comments, late Comments, on time Replies, late Replies
    data = []

    loop = False
    ls = []
    for key,value in d.items():
        loop = True
        lateReply = 0
        onTimeReply = 0
        lateComment = 0
        onTimeComment = 0
        for x in value:
            #problem is it reads everthing as comments
            print("debug:", dueDateC, dueDateR)
            print("hmmmm:",  x["timeData"], x["commentType"])
            if x["commentType"] == "reply":
                if dueDateR == -1:
                    pass
                elif dueDateR < x["timeData"]:
                    lateReply += 1
                else:
                    onTimeReply += 1
            elif x["commentType"] == "comment":
                if dueDateC == -1:
                    pass
                elif dueDateC < x["timeData"]:
                    lateComment += 1
                else:
                    onTimeComment += 1
        data.append([key, str(len(value)), str(onTimeComment),  str(lateComment), str(onTimeReply), str(lateReply)])

    if not loop:
        print("there were no stats listed. The pasted text may have been empty")












    table_data = []
    for row in data:
        table_data.append("			<div class=\"table-row\">\n")


        for x in row:
            s = "				<div class=\"table-data\">"
            e = "</div>\n"
            table_data.append(s+str(x)+e)

        table_data.append("			</div>\n")

    with open("templates/table.html", "w") as f:
        table_foot = f.writelines(table_head+table_data+table_foot)
    print("html file has been updated")
