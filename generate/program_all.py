
class Program_All:
    def __init__(self, procedures, main) -> None:
        self.procedures = procedures
        self.main = main
        pass
    def GetDeclarations(self,generator):
        mainDecl = self.main.getDeclarations(generator)
        procDecl = self.procedures.getDeclarations(generator)
        procArgs = self.procedures.getArgs(generator)
        pDecLines = self.procedures.getDeclLines()
        generator.generateMemoryMap(mainDecl,procDecl,procArgs,pDecLines)
    def checkDeclarations(self,generator):
        self.procedures.checkDeclarations(generator)
        self.main.checkDeclarations(generator)
        
    def getCode(self,generator):
        # TODO
        return self.main.getCode(generator)
        