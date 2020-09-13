import pygame, sys
from settings import *
from buttonClass import *


class App:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Sudoku")
        self.running = True
        self.grid = testBoard
        self.grid_solved = testBoard_solved
        self.mousePos = None
        self.selected = None
        self.state = "playing"
        self.finished = False
        self.playingButtons = []
        self.lockedCells = []
        self.wrongInput = []
        self.cntMistakes = 0
        self.font = pygame.font.SysFont("arial", cellSize//2, )
        self.load()


    def run(self):
        while self.running:

            if self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
        pygame.quit()
        sys.exit()

    #### playing state func #####

    def playing_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selected = self.mouseOnGrid()
                if self.selected:
                    print(self.selected)
                else:
                    #for button in self.playingButtons:
                        #if button.highlighted:
                        #button.click()
                    self.selected = None

            if event.type == pygame.KEYDOWN:
                if self.selected is not None and self.selected not in self.lockedCells:
                    if self.isInt(event.unicode):
                        self.grid[self.selected[1]][self.selected[0]] = int(event.unicode)
                        if self.grid_solved[self.selected[1]][self.selected[0]] != int(event.unicode):
                            self.cntMistakes = self.cntMistakes + 1
                            if self.selected not in self.wrongInput:

                                self.wrongInput.append(self.selected)
                        else:
                            if self.selected in self.wrongInput:
                                self.wrongInput.remove(self.selected)
                if event.key == pygame.K_SPACE:
                    solve(self.grid)



    def playing_update(self):
        self.mousePos = pygame.mouse.get_pos()
        for button in self.playingButtons:
            button.update(self.mousePos)

    def playing_draw(self):
        if self.cntMistakes >= 11:
            self.writeGameOver(self.window)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        self.window.fill(WHITE)

        for button in self.playingButtons:
            button.draw(self.window)


        if self.selected:
            self.drawSelection(self.window, self.selected)
        self.shadeLockedCells(self.window, self.lockedCells)
        self.shadeWrongCells(self.window, self.wrongInput)


        self.drawNumbers(self.window)
        self.drawGrid()
        self.mistakeCounter(self.window)
        if not find_empty(self.grid) and len(self.wrongInput) == 0:
            self.writeCongrats(self.window)
            pygame.display.update()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
        pygame.display.update()

    ##### Helper Functions #####

    '''def displayGUI(self, window):
        solve(self.grid)
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                pos = [xidx*cellSize+gridPos[0], yidx*cellSize+gridPos[1]]
                self.textToScreen(window, str(num), pos)'''
    def writeGameOver(self, window):
        text = "Game Over!"
        font = pygame.font.SysFont("arial", 30, bold=1)
        text = font.render(text, False, (0, 0, 0))
        width, height = text.get_size()

        text_rect = text.get_rect()
        text_rect.center = (100, 5)
        window.blit(text, ((WIDTH - width) // 2, 0))

    def mistakeCounter(self, window):
        text = "Mistakes: {}/10".format(str(self.cntMistakes))
        font = pygame.font.SysFont("arial", 15, bold=1)
        text = font.render(text, False, (0, 0, 0))
        width, height = text.get_size()
        window.blit(text, (10, HEIGHT -height-5 ))

        text = "Press space bar to get the Solution"
        font = pygame.font.SysFont("arial", 15, bold=1)
        text = font.render(text, False, (0, 0, 0))
        width, height = text.get_size()
        window.blit(text, (WIDTH - width-5, HEIGHT -height-5))

    def writeCongrats(self, window):
        text = "Congrats! You have Solved"
        font = pygame.font.SysFont("arial", 30, bold=1)
        text = font.render(text, False, (0, 0, 0))
        width, height = text.get_size()

        text_rect = text.get_rect()
        text_rect.center = (100, 5)
        window.blit(text, ((WIDTH - width)//2, 0))


    def shadeWrongCells(self, window, wrong):
        for cell in wrong:
            pygame.draw.rect(window, WRONGCELLCOLOUR, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    def shadeLockedCells(self, window, locked):
        for cell in locked:
            pygame.draw.rect(window, LOCKEDCELLCOLOUR, (cell[0]*cellSize+gridPos[0], cell[1]*cellSize+gridPos[1], cellSize, cellSize))

    def drawNumbers(self, window):
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num!=0:
                    pos = [xidx*cellSize+gridPos[0], yidx*cellSize+gridPos[1]]
                    self.textToScreen(window, str(num), pos)


    def drawSelection(self, window, pos):
        pygame.draw.rect(window, LIGHTBLUE,
                         (pos[0] * cellSize + gridPos[0], pos[1] * cellSize + gridPos[1], cellSize, cellSize))

    def drawGrid(self):
        pygame.draw.rect(self.window, BLACK, (gridPos[0], gridPos[1], WIDTH - 150, HEIGHT - 150), 2)
        for i in range(9):
            pygame.draw.line(self.window, BLACK, (gridPos[0] + i * cellSize, gridPos[1]),
                                 (gridPos[0] + i * cellSize, gridPos[1] + 450), 2 if i % 3 == 0 else 1)
            pygame.draw.line(self.window, BLACK, (gridPos[0], gridPos[1] + i * cellSize),
                                 (gridPos[0] + 450, gridPos[1] + i * cellSize), 2 if i % 3 == 0 else 1)


    def mouseOnGrid(self):
        if self.mousePos[0] < gridPos[0] or self.mousePos[1] < gridPos[1] or self.mousePos[0] > gridPos[0] + gridSize or \
                self.mousePos[1] > gridPos[1] + gridSize:
            return False
        return ((self.mousePos[0] - gridPos[0]) // cellSize, (self.mousePos[1] - gridPos[1]) // cellSize);

    def loadButtons(self):

        self.playingButtons.append(Button(  140, 40, WIDTH//7, 40,
                                            colour=(117,172,112),
                                            params="1",
                                            text="Easy"))
        self.playingButtons.append(Button(  WIDTH//2-(WIDTH//7)//2, 40, WIDTH//7, 40,
                                            colour=(204,197,110),
                                            params="2",
                                            text="Medium"))
        self.playingButtons.append(Button( 380, 40, WIDTH//7, 40,
                                            colour=(199,129,48),
                                            params="3",
                                            text="Hard"))


    def textToScreen(self, window, text, pos):
        font = self.font.render(text, False, BLACK)
        fontWidth = font.get_width()
        fontHeight = font.get_height()
        pos[0]+=(cellSize-fontWidth) //2
        pos[1] += (cellSize - fontHeight) // 2
        window.blit(font, pos)

    def load(self):
        self.loadButtons()
        for yidx, row in enumerate(self.grid):
            for xidx, num in enumerate(row):
                if num!=0:
                    self.lockedCells.append((xidx, yidx))

        #print(self.lockedCells)

    def isInt(self, string):

        try:
                int(string)
                return True
        except:
                return False