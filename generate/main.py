class Progam_Decl:
    def __init__(self, declarations, commands) -> None:
        self.declarations = declarations
        self.commands = commands
        pass
    def getDeclarations(self,generator):
        return self.declarations.getDeclarations(generator)
    
    def checkDeclarations(self, generator):
        self.commands.checkDeclarations(generator,"")
        
    def getCode(self,generator):
        return  self.commands.getCode(generator)

class Program:
    def __init__(self, commands) -> None:
        self.commands = commands
        pass
    def getDeclarations(self):
        return {}
    def checkDeclarations(self, generator):
        self.commands.checkDeclarations(generator,"")
    def getCode(self,generator):
        return  self.commands.getCode(generator)
