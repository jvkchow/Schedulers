import pygame
from datetime import datetime

class DaysButton:
       
    def __init__(self, x, y, width, height, color, surface,day):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = pygame.Color(color)
        self.surface = surface
        self.day = day
    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)
    def change_color(self,color):
        self.color = pygame.Color(color)
    def handleEvents(self,event):
        return(self.rect.collidepoint(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN)
            


class SystemButton:
    
    def __init__(self,x, y, width, height, surface, type):
        self.rect = pygame.Rect(x, y, width, height)
        self.surface = surface
        self.colour = pygame.Color("black")
        self.type = type
        self.font = pygame.font.SysFont("", 35)
        self.active = False

        if self.type == "add":
            self.text = "ADD"
        elif self.type == "done":
            self.text = "DONE"
        elif self.type == "ls":
            self.text = "YES"

        self.textSurface = self.font.render(self.text, True, self.colour)
        
    def handleEvents(self, event):
        if self.type == "ls":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
            if self.active:
                self.colour = pygame.Color("red")
            else:
                if self.active or self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.colour = pygame.Color("red")
                else:
                    self.colour = pygame.Color("black")
            return self.active

        else:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.colour = pygame.Color("red")
            else:
                self.colour = pygame.Color("black")   

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                    return True

    def draw(self, surface):
        surface.blit(self.textSurface, (self.rect.x + 15, self.rect.y + 17))
        pygame.draw.rect(surface, self.colour, self.rect, 2)

class TextBox:

    def __init__(self, x, y, width, height, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.colour = pygame.Color("black")
        self.text = text
        self.font = pygame.font.SysFont("", 35)
        self.textSurface = self.font.render(self.text, True, self.colour)
        self.active = False

    def renderText(self):
        self.textSurface = self.font.render(self.text, True, self.colour)

    def handleEvents(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            if self.active:
                self.colour = pygame.Color((122, 122, 122))
            else:
                self.colour = pygame.Color("black")
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.renderText()

    def update(self):
        # still needs work
        width = max(200, self.textSurface.get_width() + 10)
        self.rect.w = width

    def draw(self, surface):
        surface.blit(self.textSurface, (self.rect.x + 15, self.rect.y + 17))
        pygame.draw.rect(surface, self.colour, self.rect, 2)

class CourseAddApp():

    def __init__(self, surface):

        self.surface = surface
        self.bgColour = pygame.Color("white")
        self.closeClicked = False
        self.textFont = pygame.font.SysFont("", 40)
        self.textColour = pygame.Color("black")
        self.ls = False
        self.add = False
        self.done = False
        self.dataList = []
        self.day = ''
        self.inputError = False

    def createTextBoxes(self):
        self.courseBox = TextBox(15, 62, 700, 60)
        self.sectionBox = TextBox(15, 197, 700, 60)
        self.locationBox = TextBox(15, 332, 700, 60)
        self.startBox = TextBox(15, 467, 250, 60)
        self.endBox = TextBox(300, 467, 250, 60)

        self.textBoxes = [self.courseBox, self.sectionBox, self.locationBox, self.startBox, self.endBox]

    def createDayButtons(self):
        self.mwfButton = DaysButton(600,467,50,50,"red",self.surface,'mwf')
        self.thButton = DaysButton(700,467,50,50,"red",self.surface,'tr')
        self.mButton = DaysButton(750,467,50,50,"red",self.surface,'m')
        self.tButton = DaysButton(825,467,50,50,"red",self.surface,'t')
        self.wButton = DaysButton(900,467,50,50,"red",self.surface,'w')
        self.hButton = DaysButton(975,467,50,50,"red",self.surface,'t')
        self.fButton = DaysButton(1050,467,50,50,"red",self.surface,'f')

        self.lecButtons = [self.mwfButton, self.thButton]
        self.lsButtons = [self.mButton,self.tButton,self.wButton,self.hButton,self.fButton]

    def createSystemButtons(self):
        self.addButton = SystemButton(350, 700, 200, 60, self.surface, "add")
        self.doneButton = SystemButton(600, 700, 200, 60, self.surface, "done")
        self.lsButton = SystemButton(900, 62, 100, 60, self.surface, "ls")

        self.systemButtons = [self.addButton, self.doneButton, self.lsButton]

    def resetData(self):

        for box in self.textBoxes:
            box.text = ""
            box.active = False
            box.renderText()
            box.draw(self.surface)
        
        for lecButton in self.lecButtons:
            lecButton.color = pygame.Color("red")
        for lsButton in self.lsButtons:
            lsButton.color = pygame.Color("red")

        self.ls = False
        self.add = False
        self.done = False
        self.day = ''
        self.lsButton.active = False

    def dateValidation(self, date):
        if ":" not in date:
            return False
        
        numbers = date.split(":")
        if len(numbers) > 2 or not numbers[0].isdigit() or not numbers[1].isdigit() or int(numbers[0]) < 0 or int(numbers[0]) > 24 or int(numbers[1]) < 0 or int(numbers[1]) > 59 or date == "":
            return False

        return True

    def dataValidation(self):

        allDataValid = True

        if not self.dateValidation(self.startBox.text) or not self.dateValidation(self.endBox.text) or (datetime.strptime(self.endBox.text, "%H:%M") < datetime.strptime(self.startBox.text, "%H:%M")):

            self.startBox.text = ""
            self.endBox.text = ""
            self.startBox.renderText()
            self.endBox.renderText()
            self.startBox.draw(self.surface)
            self.endBox.draw(self.surface)

            self.startBox.colour = pygame.Color("red")
            self.endBox.colour = pygame.Color("red")
            allDataValid = False

        if self.courseBox.text == "":
            self.courseBox.text = ""
            self.courseBox.renderText()
            self.courseBox.draw(self.surface)
            self.courseBox.colour = pygame.Color("red")
            allDataValid = False

        if self.sectionBox.text == "":
            self.sectionBox.text = ""
            self.sectionBox.renderText()
            self.sectionBox.draw(self.surface)
            self.sectionBox.colour = pygame.Color("red")
            allDataValid = False

        if self.locationBox.text == "":
            self.locationBox.text = ""
            self.locationBox.renderText()
            self.locationBox.draw(self.surface)
            self.locationBox.colour = pygame.Color("red")
            allDataValid = False

        if self.day == '':
            allDataValid = False

        return allDataValid

    def addData(self):

        if self.dataValidation():

            if self.ls:
                data = {"course": self.courseBox.text, 
                        "section": self.sectionBox.text,
                        "location": self.locationBox.text, 
                        "start": datetime.strptime(self.startBox.text, "%H:%M"), 
                        "end": datetime.strptime(self.endBox.text, "%H:%M"),
                        "mwf": False, 
                        "tr": False, 
                        "ls": self.ls,
                        "ls day": self.day}

            else:
                data = {"course": self.courseBox.text, 
                        "section": self.sectionBox.text,
                        "location": self.locationBox.text, 
                        "start": datetime.strptime(self.startBox.text, "%H:%M"), 
                        "end": datetime.strptime(self.endBox.text, "%H:%M"),
                        "mwf": self.day == "mwf", 
                        "tr": not self.day == 'mwf', 
                        "ls": self.ls,
                        "ls day": False}                

            self.dataList.append(data)
            self.resetData()

    def runAddCourses(self):

        self.createTextBoxes()
        self.createSystemButtons()
        self.createDayButtons()

        while not self.closeClicked and not self.done:
            self.handleEvents()
            self.draw()

            if self.done:
                return self.dataList

    def handleEvents(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.closeClicked = True

            for box in self.textBoxes:
                box.handleEvents(event)

            if not self.ls:
                for box in self.lecButtons:
                    if box.handleEvents(event):
                        for metabox in self.lecButtons:
                            metabox.change_color("red")
                        for metabox in self.lsButtons:
                            metabox.change_color("red")
                        box.change_color("green")
                        self.day = box.day
            
            else:
               for box in self.lsButtons:
                    if box.handleEvents(event):
                        for metabox in self.lecButtons:
                            metabox.change_color("red")
                        for metabox in self.lsButtons:
                            metabox.change_color("red")
                        box.change_color("green")
                        self.day = box.day



            self.ls = self.lsButton.handleEvents(event)
            self.add = self.addButton.handleEvents(event)

            if self.add:
                self.addData()

            self.done = self.doneButton.handleEvents(event)

            if self.done:
                self.done = True

    def draw(self):
        self.surface.fill(self.bgColour)
        self.drawText()
        self.drawDayButtons()

        for box in self.textBoxes:
            box.draw(self.surface)

        for button in self.systemButtons:
            button.draw(self.surface)

        pygame.display.update()

    def drawText(self):

        clsInstr1 = "(Enter labs and seminars separately!)"
        clsInstr1Image = pygame.font.SysFont("", 25).render(clsInstr1, True, pygame.Color("red"))
        self.surface.blit(clsInstr1Image, (220, 20))

        clsInstr2 = "(If Lab/Seminar: Prefix with LAB/SEM with LAB/SEM section here)"
        clsInstr2Image = pygame.font.SysFont("", 25).render(clsInstr2, True, pygame.Color("red"))
        self.surface.blit(clsInstr2Image, (150, 155))

        courseText = "Course Name"
        courseTextImage = self.textFont.render(courseText, True, self.textColour)
        self.surface.blit(courseTextImage, (15, 15))

        sectionText = "Section"
        sectionTextImage = self.textFont.render(sectionText, True, self.textColour)
        self.surface.blit(sectionTextImage, (15, 150))

        locationText = "Location"
        locationTextImage = self.textFont.render(locationText, True, self.textColour)
        self.surface.blit(locationTextImage, (15, 285))

        startText = "Start"
        startTextImage = self.textFont.render(startText, True, self.textColour)
        self.surface.blit(startTextImage, (15, 420))

        endText = "End"
        endTextImage = self.textFont.render(endText, True, self.textColour)
        self.surface.blit(endTextImage, (300, 420))

        daysText = "Days of the Week"
        daysTextImage = self.textFont.render(daysText, True, self.textColour)
        self.surface.blit(daysTextImage, (585, 420))

        lsText = "Lab/Seminar?"
        lsTextImage = self.textFont.render(lsText, True, self.textColour)
        self.surface.blit(lsTextImage, (865, 15))

        if self.ls:
            
            mText = "M"
            mTextImage = self.textFont.render(mText, True, self.textColour)
            self.surface.blit(mTextImage, (750,520 ))

            tText = "T"
            tTextImage = self.textFont.render(tText, True, self.textColour)
            self.surface.blit(tTextImage, (825, 520))
            
            wText = "W"
            wTextImage = self.textFont.render(wText, True, self.textColour)
            self.surface.blit(wTextImage, (900,520 ))

            rText = "R"
            rTextImage = self.textFont.render(rText, True, self.textColour)
            self.surface.blit(rTextImage, (975, 520))
            
            fText = "F"
            fTextImage = self.textFont.render(fText, True, self.textColour)
            self.surface.blit(fTextImage, (1050,520 ))


        else:

            mwfText = "MWF"
            mwfTextImage = self.textFont.render(mwfText, True, self.textColour)
            self.surface.blit(mwfTextImage, (600,520 ))

            trText = "TR"
            trTextImage = self.textFont.render(trText, True, self.textColour)
            self.surface.blit(trTextImage, (700, 520))
            
    def drawDayButtons(self): # :) :} :c
        if not self.ls:
            self.mwfButton.draw()
            self.thButton.draw()
            
        else:
            self.mButton.draw()
            self.tButton.draw()
            self.wButton.draw()
            self.hButton.draw()
            self.fButton.draw()
        

class ScheduleApp():
    
    def __init__(self, schedule, surface):
        self.schedule = schedule
        self.surface = surface
        self.closeClicked = False

    def runSchedules(self):
        while not self.closeClicked:
            self.handleEvents()

            if self.schedule == -1:
                self.drawNoSchedule()
            else:
                self.draw()

    def drawNoSchedule(self):
        self.surface.fill(pygame.Color("white"))
        noText = "No schedules can be made from the current courses, try adding fewer courses."
        noTextImage = pygame.font.SysFont("", 40).render(noText, True, pygame.Color("red"))
        self.surface.blit(noTextImage, (50, 250))
        pygame.display.update()

    def draw(self):
        self.surface.fill(pygame.Color("white"))
        self.drawHeaders()
        self.drawCourses()

        pygame.display.update()

    def drawHeaders(self):

        baseFont = pygame.font.SysFont("", 30)
        fontColour = pygame.Color((0, 89, 10))
        font = baseFont
        font.set_underline(True)

        monHeader = "MONDAY:"
        monHeaderImage = font.render(monHeader, True, fontColour)
        self.surface.blit(monHeaderImage, (15, 15))

        tuesHeader = "TUESDAY:"
        tuesHeaderImage = font.render(tuesHeader, True, fontColour)
        self.surface.blit(tuesHeaderImage, (250, 15))

        wedHeader = "WEDNESDAY:"
        wedHeaderImage = font.render(wedHeader, True, fontColour)
        self.surface.blit(wedHeaderImage, (500, 15))

        thursHeader = "THURSDAY:"
        thursHeaderImage = font.render(thursHeader, True, fontColour)
        self.surface.blit(thursHeaderImage, (750, 15))

        friHeader = "FRIDAY:"
        friHeaderImage = font.render(friHeader, True, fontColour)
        self.surface.blit(friHeaderImage, (1000, 15))

    def drawCourses(self):

        font = pygame.font.SysFont("", 25)
        xpos = None
        dayCounter = 0
        for day in self.schedule:

            ypos = 50

            if dayCounter == 0:
                xpos = 15
            elif dayCounter == 1:
                xpos = 250
            elif dayCounter == 2:
                xpos = 500
            elif dayCounter == 3:
                xpos = 750
            elif dayCounter == 4:
                xpos = 1000

            if len(day) == 0:
                noneText = "NO CLASSES"
                noneTextImage = font.render(noneText, True, pygame.Color("red"))
                self.surface.blit(noneTextImage, (xpos, 50))

            else:

                for course in day:
                    # time
                    timeText = course.get("start").strftime("%H:%M") + " - " + course.get("end").strftime("%H:%M")
                    timeTextImage = font.render(timeText, True, pygame.Color("black"))
                    self.surface.blit(timeTextImage, (xpos, ypos))
                    
                    # course name
                    timeText = course.get("course")
                    timeTextImage = font.render(timeText, True, pygame.Color("black"))
                    self.surface.blit(timeTextImage, (xpos, ypos+30))

                    # section
                    sectionText = course.get("section")
                    sectionTextImage = font.render(sectionText, True, pygame.Color("black"))
                    self.surface.blit(sectionTextImage, (xpos, ypos+60))       

                    # location
                    locationText = course.get("location")
                    locationTextImage = font.render(locationText, True, pygame.Color("black"))
                    self.surface.blit(locationTextImage, (xpos, ypos+90))

                    ypos += 150

            dayCounter += 1


    def handleEvents(self):

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.closeClicked = True

def uiAddCourse():

    pygame.init()
    pygame.display.set_mode([1200, 800])
    pygame.display.set_caption("SlayTracks")
    surface = pygame.display.get_surface() 
    prog = CourseAddApp(surface)
    courses = prog.runAddCourses()

    return courses

def uiShowSchedules(schedules):

    pygame.init()
    pygame.display.set_mode([1200, 800])
    pygame.display.set_caption("SlayTracks")
    surface = pygame.display.get_surface()
    schedApp = ScheduleApp(schedules, surface)
    schedApp.runSchedules()
    pygame.quit()

    return
