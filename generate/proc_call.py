class Proc_Call:
    def __init__(self, pidentifier, args) -> None:
        self.pidentifier = pidentifier
        self.args = args
        pass
    
    def checkDeclarations(self, generator,proc):
        if self.pidentifier.pidentifier not in generator.memoryMapProcedures or self.pidentifier.line <  generator.procDecLine[self.pidentifier.pidentifier]:  # TODO
            raise Exception(f"Undeclared procedure call {self.pidentifier.pidentifier} in line {self.pidentifier.line}")
        self.args.checkDeclarations(generator,proc)
        self.args.checkArgs(generator, self.pidentifier,proc)
        
    def getCode(self,generator):
        return generator.GetInline(self.pidentifier.pidentifier,[arg.pidentifier for arg in self.args.args])