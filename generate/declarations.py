class Declarations:
    def __init__(self) -> None:
        self.declarations = []
        pass
    
    def add_identifier(self, pidentifier, line) -> None:
        self.declarations.append(ID(pidentifier, line))
        pass
    
    def add_array(self, pidentifier, num, line) -> None:
        self.declarations.append(Array(pidentifier, num, line))
        pass
    
    def getDeclarations(self,_):
        decls = {}
        size = 0
        idnt = ""
        for decl in self.declarations:
      
            if isinstance(decl, ID):
                idnt = decl.identifier
                size = 1
            elif isinstance(decl, Array):
                idnt = decl.pidentifier
                size = decl.num
            if(idnt in decls): 
                 raise Exception(f"Multiple declarations of variable {idnt} line {self.declarations[decl].line}")
            decls[idnt] = size
        return decls

    
class ID:
    def __init__(self, identifier, line) -> None:
        self.identifier = identifier
        self.line = line
        pass
    
class Array:
    def __init__(self, pidentifier, num, line) -> None:
        self.pidentifier = pidentifier
        self.num = num
        self.line = line
        pass