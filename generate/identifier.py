
def genNum(num,r):
    lines = []
    if num > 0:
        while num > 1:
            if num % 2 == 1:
                lines.append(f"INC {r}")
                num -= 1
            else:
                lines.append(f"SHL {r}")
                num /= 2
        lines.append(f"INC {r}")
    lines.append(f"RST {r}")
    return lines[::-1]


class Pidentifier:
    def __init__(self, pidentifier, line) -> None:
        self.pidentifier = pidentifier
        self.line = line
        pass
    
    def checkDeclarations(self, generator, proc, init: bool, omit = False):
        dectype = generator.getDeclType(proc)
        if not omit:
            if self.pidentifier not in dectype:
                raise Exception(f"Undifined variable {self.pidentifier} in line {self.line}")
            if dectype[self.pidentifier]:
                raise Exception(f"Wrong type of variable {self.pidentifier} in line {self.line}")
        if init: generator.addInit(self.pidentifier, proc, self.line)
        else: generator.addAccess(self.pidentifier, proc, self.line)
        
    def getCode(self, r,generator):
        lines = self.getAddr(r,generator)
        lines.append(f"LOAD {r}")
        lines.append(f"PUT {r}")
        lines.append("RST a")
        return lines
    
    def getAddr(self, r,generator):
        mem = generator.getAddr(self.pidentifier)
        return genNum(mem,r)
    
class Array_Num:
    def __init__(self,pidentifier, num, line) -> None:
        self.pidentifier = pidentifier
        self.num = num
        self.line = line
        pass
    
    def checkDeclarations(self, generator,proc, init: bool):
        dectype = generator.getDeclType(proc)
        if self.pidentifier not in dectype:
            raise Exception(f"Undifined variable {self.pidentifier} in line {self.line}")
        if not dectype[self.pidentifier]:
            raise Exception(f"Wrong type of variable {self.pidentifier} in line {self.line}")
    def getCode(self, r, generator):
        lines = self.getAddr(r,generator)
        lines.append(f"LOAD {r}")
        lines.append(f"PUT {r}")
        lines.append("RST a")
        return lines
    
    def getAddr(self, r,generator):
        mem = generator.getAddr(self.pidentifier) + self.num
        return genNum(mem,r)
        
    
class Array_ID:
    def __init__(self, pidentifier, pidentifier_index, line) -> None:
        self.pidentifier = pidentifier
        self.index = pidentifier_index
        self.line = line
        pass
    
    def checkDeclarations(self, generator,proc, init: bool):
        generator.addAccess(self.index, proc, self.line)
        dectype = generator.getDeclType(proc)
        if self.pidentifier not in dectype:
            raise Exception(f"Undifined variable {self.index} in line {self.line}")
        if not dectype[self.pidentifier]:
            raise Exception(f"Wrong type of variable {self.index} in line {self.line}")
        if self.index not in dectype:
            raise Exception(f"Undifined variable {self.index} in line {self.line}")
        if dectype[self.index]:
            raise Exception(f"Wrong type of variable {self.index} in line {self.line}")
        
    def getCode(self, r, generator):
        lines = self.getAddr(r,generator)
        lines.append(f"LOAD {r}")
        lines.append(f"PUT {r}")
        lines.append("RST a")
        return lines
    
    def getAddr(self, r,generator):
        mem = generator.getAddr(self.pidentifier)
        memId = generator.getAddr(self.index)
        lines = genNum(memId,r)
        lines.append(f"LOAD {r}")
        lines.append(f"PUT {r}")
        lines.append("RST a")
        lines += genNum(mem,"a")
        
        lines += [f"ADD {r}", f"PUT {r}","RST a"]
        return lines