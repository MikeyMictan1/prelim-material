# Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed in the Python 3.9.4 programming environment

import random
import os


def Main():
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
        if len(args) == 1:
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
            # ADDITIONAL SYMBOL ADDED TO GAME -------------------------------------------------------------------------
            Lpattern = Pattern("L", "L***LLLL")
            self.__AllowedPatterns.append(Lpattern)
            self.__AllowedSymbols.append("L")
            # ADDITIONAL SYMBOL ADDED TO GAME -------------------------------------------------------------------------
            # WILDCARDS -----------------------------------------------------------------------------------------------
            wildcard_count = 0
            while wildcard_count != 3:
                random_cell = random.randint(0, len(self.__Grid))
                grid_space = self.__Grid[random_cell]

                if grid_space.GetSymbol() != "*":
                    grid_space.ChangeSymbolInCell("*")
                    wildcard_count += 1
            # WILDCARDS -----------------------------------------------------------------------------------------------

            # BLOW UP A BLOCKED CELL ----------------------------------------------------------------------------------
            self.__AllowedSymbols.append("B")
            # BLOW UP A BLOCKED CELL ----------------------------------------------------------------------------------

    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())

                for Count in range(1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())

                NoOfPatterns = int(f.readline().rstrip())

                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)

                self.__GridSize = int(f.readline().rstrip())

                for Count in range(1, self.__GridSize * self.__GridSize + 1):
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
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
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
            # UNDO MOVE -----------------------------------------------------------------------------------------------
            previous_score = self.__Score
            previous_cell = CurrentCell.GetSymbol()
            # UNDO MOVE -----------------------------------------------------------------------------------------------

            # BLOW UP A BLOCKED CELL ----------------------------------------------------------------------------------
            if type(CurrentCell) == BlockedCell and Symbol == "B":
                Index = (self.__GridSize - Row) * self.__GridSize + Column - 1  # from get cell function
                CurrentCell.UpdateCell()
                CurrentCell.ChangeSymbolInCell("-")

            elif CurrentCell.CheckSymbolAllowed(Symbol) and Symbol != "B":
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)

                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            # BLOW UP A BLOCKED CELL ----------------------------------------------------------------------------------

            # UNDO MOVE -----------------------------------------------------------------------------------------------
            self.DisplayPuzzle()
            undo_move = input("Would you like to undo move? Y/N: ")
            if undo_move.upper() == "Y":
                self.__Score = previous_score
                self.__SymbolsLeft += 1
                if previous_cell == "@":  # IF PREVIOUSLY A BLOCKED CELL, MAKE IT BLOCKED AGAIN
                    CurrentCell.UpdateBlockedCell()

                CurrentCell.ChangeSymbolInCell(previous_cell)
            # UNDO MOVE -----------------------------------------------------------------------------------------------

            if self.__SymbolsLeft == 0:
                Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
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
                    # ROTATED PATTERNS --------------------------------------------------------------------------------
                    rotate_acw = PatternString[2:8] + PatternString[:2] + PatternString[8]
                    rotate_180 = PatternString[4:8] + PatternString[:4] + PatternString[8]
                    rotate_cw = PatternString[6:8] + PatternString[:6] + PatternString[8]
                    rotations_lst = [PatternString, rotate_acw, rotate_180, rotate_cw]

                    for P in self.__AllowedPatterns:
                        for rotation in rotations_lst:
                            CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                            if P.MatchesPattern(rotation, CurrentSymbol):
                                # ROTATED PATTERNS --------------------------------------------------------------------
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
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
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


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString
        # WILDCARDS -----------------------------------------------------------------------------------------------
        self.wildcard_symbol = "*"
        # WILDCARDS -----------------------------------------------------------------------------------------------

    def MatchesPattern(self, PatternString, SymbolPlaced):
        # WILDCARDS -----------------------------------------------------------------------------------------------
        if SymbolPlaced != self.__Symbol and SymbolPlaced != self.wildcard_symbol:
            return False

        for Count in range(0, len(self.__PatternSequence)):
            try:
                # if real pattern[0] matches with the real symbol, and the players 3*3 grid is NOT the correct symbol
                if (self.__PatternSequence[Count] == self.__Symbol
                        and PatternString[Count] != self.__Symbol
                        and PatternString[Count] != self.wildcard_symbol):
                    return False

            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        # WILDCARDS -----------------------------------------------------------------------------------------------
        return True

    def GetPatternSequence(self):
        return self.__PatternSequence


class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        if self.IsEmpty():
            return "-"

        else:
            return self._Symbol

    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True

        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False

        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        # BLOCKED CELL UPDATING ---------------------------------------------------------------------------------------
        self.__class__ = Cell
        # BLOCKED CELL UPDATING ---------------------------------------------------------------------------------------

    # BLOCKED CELL UPDATING ---------------------------------------------------------------------------------------
    def UpdateBlockedCell(self):
        self.__class__ = BlockedCell
    # BLOCKED CELL UPDATING ---------------------------------------------------------------------------------------


class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        return False


if __name__ == "__main__":
    Main()
