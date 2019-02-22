import tkinter
#importing tikinter
import time
#importing time
import threading
from tinydb import TinyDB, Query
db=TinyDB('testworld2.json')


class gameOfLife:
    #making class
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.makeGrid()        
        self.paused = True
        self.updating=True
        self.delay = 0.2
        #class properties

        self.gui = GoLGUI(self)
        #varible


    def clock(self):
        ###timer
        while True:
            if not self.paused:
                self.updating=True
                self.tick()
            self.updating=False
            time.sleep(self.delay)


    def toggletick(self):
        # turns the timer on and of (paused and not paused)
        self.paused = not self.paused
        if self.paused:
            self.gui.window.wm_title("PAUSED x"+str(self.delay))
        else:
            self.gui.window.wm_title("x"+str(self.delay))
            
    def changeSpeed(self, multiplicand):
        ##########speeds up or slows down
        if self.paused:
            if (self.delay * multiplicand) > 0.01 and (self.delay * multiplicand) < 2:
                self.delay *= multiplicand
                if self.paused:
                    self.gui.window.wm_title("PAUSED x"+str(self.delay))
                    #making self.delay a string
                else:
                    self.gui.window.wm_title("x"+str(self.delay))
    
    def reset(self):
    #########resets the grid
        if self.paused:
            self.makeGrid()
            for x in range(self.width):
                for y in range(self.height):
                    self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#FF00FF")
            self.gui.window.update()
            for x in range(self.width):
                for y in range(self.height):
                    self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#000000")
            self.gui.window.update()

    def makeGrid(self):
        ####labels the grid
        #self.grid = {x:{y:False for y in range(self.height)} for x in range(self.width)}
        servergrid = db.all()[0]
        self.grid ={x:{y:False for y in range(self.height)} for x in range(self.width)}


        for x in range(self.width):
            for y in range(self.height):
                self.grid[x][y] = servergrid[str(x)][str(y)]
 
        

        
    def changeState(self, x, y):
        ###change spot on grid
        if self.updating == False:
            self.grid[x][y] = not self.grid[x][y]
            if self.grid[x][y]:
                self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#FFFFFF")
            else:
                self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#000000")


    def tick(self):        
        nextGrid = {x:{y:False for y in range(self.height)} for x in range(self.width)}
        for x in range(self.width):
            for y in range(self.height-1,-1,-1):
                if self.grid.get(x).get(y):                   
                    ##Check if the y position below the current x,y position is = the height of the grid
                    if y+1 < self.height:
                        if nextGrid[x][y+1] == False:
                            nextGrid[x][y]=False
                        else:
                            nextGrid[x][y]=True                         
                    else:
                        nextGrid[x][y]=True                   
                    if nextGrid[x][y] != self.grid[x][y]:
                        self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#000000")
                        db.update(self.grid)
                        
                else:
                    if y+1 < self.height and x < self.width-1 and x > 0:
                        if self.grid[x-1][y+1]==True and self.grid[x][y+1]==True and self.grid[x+1][y+1]==True:
                            nextGrid[x][y]=True                             
                            self.gui.buttonsDict["{0}.{1}".format(x, y)].configure(bg="#FFFFFF")
                            db.update(self.grid)
 


        self.gui.window.update()
        self.grid = nextGrid

class GoLGUI:
    def __init__(self, game):
        self.game = game
        
        self.window = tkinter.Tk()
        self.window.wm_title("PAUSED x"+str(self.game.delay))
        self.window.resizable(False, False)
        self.window.geometry("800x800")

        self.buttonsDict = {}

        for x in range(self.game.width):
            self.window.grid_columnconfigure(x, weight=1)
            for y in range(self.game.height):
                self.window.grid_rowconfigure(y, weight=1)
                buttonCmd = self.buttonCmdGen(x, y)

                if(game.grid.get(x).get(y)):
                    self.buttonsDict["{0}.{1}".format(x, y)] = tkinter.Label(self.window, bg="#FFFFFF")
                else:
                    self.buttonsDict["{0}.{1}".format(x, y)] = tkinter.Label(self.window, bg="#000000")

                
                self.buttonsDict["{0}.{1}".format(x, y)].grid(row=y, column=x, sticky="nesw")
                self.buttonsDict["{0}.{1}".format(x, y)].bind("<Button-1>", buttonCmd)
        
        self.window.bind("[", lambda a:self.game.changeSpeed(2))
        self.window.bind("]", lambda a:self.game.changeSpeed(0.5))
        
        self.window.bind("<Return>", lambda a:self.game.toggletick())
        self.window.bind("<BackSpace>", lambda a:self.game.reset())
        
    def buttonCmdGen(self, x, y):
        return lambda a: self.game.changeState(x, y)

game = gameOfLife(10, 10)
loop = threading.Thread(target=game.clock)
loop.start()
game.gui.window.mainloop()
