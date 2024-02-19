class Args:
    def __init__(self) -> None:
        self.args = []
        pass
    
    def add_identifier(self, pidentifier) -> None:
        self.args.append(pidentifier)
        pass
    
    def checkDeclarations(self, generator,proc):
        for arg in self.args:
            arg.checkDeclarations(generator,proc,True,True)
    
    def checkArgs(self, generator, procPin,procParent):
        argList = generator.procaArgLists[procPin.pidentifier]
        if len(self.args) != len(argList):
            raise Exception(f"Number of variables don't match {procPin.pidentifier} in line {procPin.line}")
        decltypes =  generator.getDeclType(procParent)
        for i in range(0,len(self.args)):
           if decltypes[self.args[i].pidentifier] != argList[i]:
                raise Exception(f"inapropriate usage of an argument {self.args[i].pidentifier} in line {procPin.line}")
        