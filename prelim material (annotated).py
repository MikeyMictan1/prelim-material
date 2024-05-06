#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

import random
import os

def Main():
    """
    Function Description:
    ---------------------
    Asks user for what puzzle they want to run, and runs that puzzle using the
    puzzle() class

    Parameters
    ---------------------
    None

    returns
    ---------------------
    None
    """
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()

class Puzzle():
    def __init__(self, *args):
        """
        Function Description:
        ---------------------
        Initialises the Puzzle class, adding all the initial parameters needed

        Parameters
        ---------------------
        Score: int
            The users score based on their performance in the game
        SymbolsLeft: int
            The number of symbols left to place
        GridSize: int
            The size of the playable grid for the puzzle
        Grid: list
            The actual grid the game is played on, created as a list
        AllowedPatterns: list
            A list of the patterns allowed for points
        AllowedSymbols: list
            A list of the symbols the user is allowed to play in the game

        returns
        ---------------------
        None
        """
        self.args = args
        if len(args) == 1:
            self.args = args[0]
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            # WILDCARD -------------
            wildcard_count = 0
            while wildcard_count != 3:
                random_cell = random.randint(0, len(self.__Grid))
                grid_space = self.__Grid[random_cell]

                if grid_space.GetSymbol() != "*":
                    grid_space.ChangeSymbolInCell("*")
                    wildcard_count += 1
            # WILDCARD -------------


            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")

            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")

            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

            # adding additional symbols
            Lpattern = Pattern("L", "L***LLLL")
            self.__AllowedPatterns.append(Lpattern)
            self.__AllowedSymbols.append("L")

            self.__AllowedSymbols.append("B")

    def __LoadPuzzle(self, Filename):
        """
        Function Description:
        ---------------------
        Opens the file of the puzzle text file that the user wants to play

        Parameters
        ---------------------
        Filename: str
            The name of the file of the puzzle that the user wants to play

        returns
        ---------------------
        None
        """
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range (1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range (1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        """
        Function Description:
        ---------------------
        Runs when the user wants to play a puzzle, holds their score and lets the user put symbols
        into the playing grid to earn points.

        Parameters
        ---------------------
        None

        returns
        ---------------------
        score: int
            returns the users score after the game finishes
        """
        Finished = False
        times_ran = 0
        undo = ""

        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False

            # Undoing the last move ----------------------------------
            previous_score = self.__Score
            previous_symbols_left = self.__SymbolsLeft

            if times_ran > 0:
                undo = input("Do you want to undo? y/n:")

            if undo == "y":
                Index = (self.__GridSize - previous_row) * self.__GridSize + previous_column - 1
                self.__Grid[Index] = Cell()
                self.__Score = previous_score
                self.__SymbolsLeft = previous_symbols_left
                self.DisplayPuzzle()

            times_ran += 1
            # --------------------------------------------------------



            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass


            Column = -1
            Valid = False


            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass


            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            CurrentCell = self.__GetCell(Row, Column)

            # Undoing the last move ----------------------------------
            previous_row = Row
            previous_column = Column
            # --------------------------------------------------------

            # Blowing up blocked tiles -------------------------------
            if type(CurrentCell) == BlockedCell and Symbol == "B":
                Index = (self.__GridSize - Row) * self.__GridSize + Column - 1  # from get cell function
                self.__Grid[Index] = Cell()

            elif CurrentCell.CheckSymbolAllowed(Symbol) and Symbol != "B":
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)

                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            # --------------------------------------------------------



            # saving a puzzle if it is not the standard
            if len(self.args) == 1:
                self.save_game(self.args)
                pass

            else:
                self.save_game("standard_puzzle_saved.txt")
                pass

            if self.__SymbolsLeft == 0:
                Finished = True

        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        """
        Function Description:
        ---------------------
        Gets one "tile" of the playable grid, from the specified row and column

        Parameters
        ---------------------
        row: int
            The row number of the cell that will be retrieved
        column: int
            The column number of the cell that will be retrieved

        returns
        ---------------------
        Grid[index]: str
            The value of the cell at the specified row and column number
        """
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()


    def CheckforMatchWithPattern(self, Row, Column):
        """
        Function Description:
        ---------------------
        Checks if there is a matching pattern, starting from a specific row and column.

        Parameters
        ---------------------
        row: int
            The row number of the cell that will be retrieved
        column: int
            The column number of the cell that will be retrieved

        returns
        ---------------------
        value: int
            the value that will be added to score if there is a pattern match
        """
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = ""
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        """
        Function Description:
        ---------------------
        Obtains a valid symbol input from the user, to be placed onto the grid

        Parameters
        ---------------------
        None

        returns
        ---------------------
        Symbol: str
            returns the symbol string that the user inputted, once it is confirmed to be valid
        """
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        """
        Function Description:
        ---------------------
        Creates a horizontal line, used in between the puzzle grid lines, to make the formatting of
        the puzzle nicer.

        Parameters
        ---------------------
        None

        returns
        ---------------------
        Line: str
            The horizontal line of "-"
        """
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        """
        Function Description:
        ---------------------
        Displays the puzzle grid in the current state of play
        Parameters
        ---------------------
        None

        returns
        ---------------------
        None
        """
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

    def save_game(self, filename):
        with open(filename, "w") as saved_game_file:

            # writing allowed symbols
            saved_game_file.write(f"{len(self.__AllowedSymbols)}\n")
            for symbol in self.__AllowedSymbols:
                saved_game_file.write(f"{symbol}\n")

            # writing allowed patterns
            saved_game_file.write(f"{len(self.__AllowedPatterns)}\n")
            for pattern in self.__AllowedPatterns:
                sequence = pattern.GetPatternSequence()
                saved_game_file.write(f"{max(sequence)},{sequence}\n")


            # writing other stuff
            saved_game_file.write(f"{self.__GridSize}\n")

            for symbol in self.__Grid:
                if f"{symbol.GetSymbol()}" == "-":
                    saved_game_file.write(f",\n")

                else:
                    saved_game_file.write(f"{symbol.GetSymbol()}, \n")



            saved_game_file.write(f"{self.__Score}\n")
            saved_game_file.write(f"{self.__SymbolsLeft}\n")


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        """
        Function Description:
        ---------------------
        Initialisation function for the "pattern" class

        Parameters
        ---------------------
        SymbolToUse: str
            Symbol to be used in the pattern
        PatternString: str
            A symbol pattern, in the form of one string


        returns
        ---------------------
        None
        """
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

    def MatchesPattern(self, PatternString, SymbolPlaced):
        """
        Function Description:
        ---------------------
        Checks of a pattern matches a valid pattern

        Parameters
        ---------------------
        PatternString: str
            The pattern that must be checked
        SymbolPlaced:
            The symbol that was last placed on the puzzle grid

        returns
        ---------------------
        True or False: bool
            returns true or false depending on if the pattern has a match

        """
        # WILDCARD ------------------
        if SymbolPlaced != self.__Symbol and self.__Symbol != "*":
            return False

        for Count in range(0, len(self.__PatternSequence)):
            try:
                if (self.__PatternSequence[Count] == self.__Symbol or self.__PatternSequence[Count] == "*") and (PatternString[Count] != self.__Symbol and self.__Symbol != "*"):
                    return False

            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")

        return True
        # WILDCARD ------------------

    def GetPatternSequence(self):
        """
        Function Description:
        ---------------------
        Gets a sequence for a certain pattern for the puzzle

        Parameters
        ---------------------
        None

        returns
        ---------------------
        PatternSequence: str
            Returns the pattern sequence as a string
        """
        return self.__PatternSequence

class Cell():
    def __init__(self):
        """
        Function Description:
        ---------------------
        Initialisation funciton for the cell class

        Parameters
        ---------------------
        Symbol: str
            Symbol to be placed on the grid
        SymbolsNotAllowed: list
            List, that will contain all symbols that aren't allowed to be used in the puzzle

        returns
        ---------------------
        None
        """
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        """
        Function Description:
        ---------------------
        Gets the symbol in a cell

        Parameters
        ---------------------
        None

        returns
        ---------------------
        Symbol or -: str
            returns the contents of the symbol in a cell
        """
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol
    
    def IsEmpty(self):
        """
        Function Description:
        ---------------------
        Checks if a cell is empty

        Parameters
        ---------------------
        None

        returns
        ---------------------
        True or False: bool
            returns true or false depending on if the cell is empty or not

        """
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        """
        Function Description:
        ---------------------
        Changes a symbol in a cell with a new symbol

        Parameters
        ---------------------
        NewSymbol: str
            The string for the new symbol that will be inputted into the puzzle grid


        returns
        ---------------------
        None
        """
        if self.IsEmpty() == False:
            self._Symbol = self._Symbol

        else:
            self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Function Description:
        ---------------------
        Checks if a symbol, that will be inputted in the grid, is allowed

        Parameters
        ---------------------
        SymbolToCheck: str
            The symbol in question to check if it is allowed to be in the puzzle grid


        returns
        ---------------------
        True or False: bool
            returns True or False depending on if the symbol is allowed to be in the puzzle grid
        """
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        """
        Function Description:
        ---------------------
        Adds a symbol to the list of symbols that aren't allowed in the puzzle grid

        Parameters
        ---------------------
        SymbolToAdd: str
            The symbol to be added to the SymbolsNotAllowed list


        returns
        ---------------------
        None
        """
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        """
        Function Description:
        ---------------------
        Updates a cell

        Parameters
        ---------------------
        None

        returns
        ---------------------
        None
        """
        pass

class BlockedCell(Cell):
    def __init__(self):
        """
        Function Description:
        ---------------------
        Initialisation

        Parameters
        ---------------------
        parameter: type
            parameter description


        returns
        ---------------------
        thing: type
            description of type returned value

        """
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
        Function Description:
        ---------------------
        Checks if a symbol is allowed to go into a blocked cell

        Parameters
        ---------------------
        SymbolToCheck: str
            the symbol to check if it is allowed


        returns
        ---------------------
        False: bool
            Always returns false (broken)
        """
        return False

if __name__ == "__main__":
    Main()