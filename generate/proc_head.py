class Proc_Head:
    def __init__(self, pidentifier, args_decl, line) -> None:
        self.pidentifier = pidentifier
        self.args_decl = args_decl
        self.line = line
        pass
    
    def getDeclarations(self,generator):
        return self.args_decl.getDeclarations(generator, self.pidentifier)
    def getDeclLine(self):
        return self.pidentifier.line