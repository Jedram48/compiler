class Num:
    def __init__(self, num) -> None:
        self.num = num
        pass
    def checkDeclarations(self, generator,proc, init):
         pass
    
    def getCode(self, r ,generator):
        if self.num == 0:
            return [f"RST {r}"]
        lines = []
        while self.num > 1:
            if self.num % 2 == 1:
                lines.append(f"INC {r}")
                self.num -= 1
            else:
                lines.append(f"SHL {r}")
                self.num /= 2
        lines.append(f"INC {r}")
        lines.append(f"RST {r}")
        return lines[::-1]
    
class Identifier:
    def __init__(self, identifier, line) -> None:
        self.identifier = identifier
        self.line = line
        pass
    def checkDeclarations(self, generator,proc, init):
        self.identifier.checkDeclarations( generator,proc, init)
        pass
    def getCode(self, r,generator):
        return self.identifier.getCode( r,generator)
    
    def getAddr(self, r,generator):
        return self.identifier.getAddr( r,generator)