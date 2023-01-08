from ui import uiAddCourse, uiShowSchedules
import pygame
from datetime import datetime

# duplicates = []
# nondup = []
# dup = 0
class Course():
    
    def __init__(self, name, startTime, endTime, MWF, section, location, TR):
        
        self.name = name
        self.startTime = startTime
        self.endTime = endTime
        self.MWF = MWF
        self.section = section
        self.location = location
        self.TR = TR

    def machineFit(self, machines):
        # iterate through all the machines 
        # self.endTime
        return

# ESTF
# create new machine if course cannot be scheduled in the existing machines i.e the startTime of the course to be scheduled is < endTime of courses in all machine
# course can be scheduled to a machine if startTime of course to be scheduled is > endTime of a course in a machine


class Machine():
    
    def __init__(self, number):
        self.number = number
        self.valid = False
        self.courses = []

    def addCourse(self, course):
        
        self.courses.append(course)
        return
        
    def checkInsert(self, course):
        # check if the course can fit into the machine
        return

class daySchedule:
    def __init__(self, day):
        self.day = day


def estf(machines, course): # ESTF takes a list of all machines (and the machine contains a list of courses) and a course as input to run ESTF on
    day_dict = {"m" : 0, "t":1, "w": 2, "r": 3, "f": 4}
    
    if course["ls"] == True:
        day_ind = day_dict[course["ls day"]]
        if len(machines[day_ind].courses) == 0:
            machines[day_ind].courses.append(course)
        elif len(machines[day_ind].courses) != 0:
            print("h")
            
            if (machines[0].courses[len(machines[0].courses) - 1]["end"] < course["start"]): 
            # check latest course scheduled on Monday, if it's endTime is < the course to be scheduled's startTime, 
            # schedule this course
                machines[day_ind].courses.append(course)
                
            

    else:

        if (course["mwf"]) == True:
            if len(machines[0].courses) == 0: # check if Monday has a course scheduled, since it is jointly scheduled with Wednesday Friday, we do not need to check the other days
                machines[0].courses.append(course) # add the course to the empty machine (days 0, 2, 4 (MWF)) Monday
                machines[2].courses.append(course) # Wednesday
                machines[4].courses.append(course) # Friday
            elif len(machines[0].courses) != 0:
                # if there are courses in the schedule 

                try:
                    if (machines[0].courses[len(machines.courses) - 1]["end"] < course["start"]): # check latest course scheduled on Monday, if it's endTime is < the course to be scheduled's startTime, schedule this course
                        machines[0].courses.append(course) # Monday
                        machines[2].courses.append(course) # Wednesday
                        machines[4].courses.append(course) # Friday
                except:
                    return -1
            
            # if course["course"] in duplicates:
            #     dup += 1
            #     duplicates.append(course["course"])
            #     nondup.remove(course["course"])
            # else:
            #     nondup.append(course["course"])

                    
        # repeat the same for Tuesday Thursday
        elif (course["tr"]) == True:
            if len(machines[1].courses) == 0: # 
                machines[1].courses.append(course) # Tuesday
                machines[3].courses.append(course) # Thursday
            elif len(machines[1].courses) != 0:
                # if there are courses in the schedule 
                try:
                    if (machines[1].courses[len(machines.courses) - 1]["end"] < course["start"]): 
                        machines[1].courses.append(course) # Tuesday
                        machines[3].courses.append(course) # Thursday
                except:
                    return -1
            # if course["course"] in duplicates:
            #     dup += 1
            #     duplicates.append(course["course"])
            #     nondup.remove(course["course"])
            # else:
            #     nondup.append(course["course"])

# def mult_estf():
#     for i in range(0, dup):
#         for mach in machines:
#             mach.courses.clear()
#         for dups in duplicates:
#             estf(machines, dups)
#         for nondups in nondup:
#             estf(machines, nondups)
    

def userInput():
    
    courseList = []

    stop = False

    while not stop:
        courseName = input("course name: ")
        startTime = input("start time: ")
        endTime = input("end time: ")
        days = input("days of week (mtwhf), separate by comma: ")

        courseList.append(Course(courseName,startTime,endTime, days))
    
        stopword = input("stop? (y/n): ")

        if stopword == "y":
            stop = True
    
        
    return courseList


def main():
    
    choices = uiAddCourse()

    machine1 = Machine(1)
    machine2 = Machine(2)
    machine3 = Machine(3)
    machine4 = Machine(4)
    machine5 = Machine(5)
    machines = [machine1,machine2,machine3,machine4,machine5]
    for i in choices:
        res = estf(machines, i)
        if res == -1:
            break

    pygame.quit()

    if res == -1:
        uiShowSchedules(-1)
    else:
        uiShowSchedules([machine1.courses, machine2.courses, machine3.courses, machine4.courses, machine5.courses])
    
    return

if __name__ == "__main__":
    main()
