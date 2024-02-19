class Procedures:
    def __init__(self) -> None:
        self.procadures = []
        pass
    def addProcadure(self,procaedure) -> None:
        self.procadures.append(procaedure)
        
    def getDeclLines(self):
        return {proc.proc_head.pidentifier.pidentifier:proc.getDeclLine() for proc in self.procadures}
        
    # def getDeclarations(self):
    #     procs = {}
    #     decl = {}
    #     idnt = ""
    #     for proc in self.procadures:
    #         decl = proc.getDeclarations()
    #         if(idnt in decls): 
    #             return {}# TODO throw error
    #         decls[idnt] = size
    #     return decls
    #      return { procedure.Name():procedure.getDeclarations() for procedure in self.procadures}
    def getArgs(self, generator):
        result_dict = {}
        for proc in self.procadures:
            if proc.proc_head.pidentifier in result_dict:
                raise ValueError(f"Multiple declarations{proc.proc_head.pidentifier.pidentifier}") # TODO throw error
            result_dict[proc.proc_head.pidentifier.pidentifier] = proc.getArgs(generator)
        return result_dict
    def getDeclarations(self,generator):
        result_dict = {}
        for proc in self.procadures:
            if proc.proc_head.pidentifier in result_dict:
                raise ValueError(f"Duplicate key found: {proc.proc_head.pidentifier.pidentifier}") # TODO throw error
            result_dict[proc.proc_head.pidentifier.pidentifier] = proc.getDeclarations(generator)
        return result_dict
    def checkDeclarations(self,generator):
        for procedure in self.procadures:
            procedure.checkDeclarations(generator)
    

    
    
   

    
class Procedure:
    def __init__(self, proc_head, commands, end) -> None:
        self.proc_head = proc_head
        self.commands = commands
        self.end = end
        pass
    def getDeclarations(self,generaotr):
        generaotr.procedureCommands[self.proc_head.pidentifier.pidentifier] = self.commands
        self.proc_head.getDeclarations(generaotr)
        return {}
    def getArgs(self, generaotr):
        return self.proc_head.getDeclarations(generaotr)
    
    def getDeclLine(self):
        
        # return self.proc_head.getDeclLine()
        return self.end
    def checkDeclarations(self, generator):
        self.commands.checkDeclarations(generator, self.proc_head.pidentifier.pidentifier)
         
    
class Procedure_Decl:
    def __init__(self, proc_head, declarations, commands, end) -> None:
        self.proc_head = proc_head
        self.declarations = declarations
        self.commands = commands
        self.end = end
        pass
    def checkDeclarations(self, generator):
        self.commands.checkDeclarations(generator, self.proc_head.pidentifier.pidentifier)
    def getDeclLine(self):
        # return self.proc_head.getDeclLine()
        return self.end
    def getArgs(self, generator):
        return self.proc_head.getDeclarations(generator)
    def getDeclarations(self,generator):
        generator.procedureCommands[self.proc_head.pidentifier.pidentifier] = self.commands
        argsDecls =  self.proc_head.getDeclarations(generator)
        decls = self.declarations.getDeclarations(generator)
        for decl in argsDecls:
            if(decl in decls):
                raise Exception(f"Multiple declaration of variable {decl} in line {self.proc_head.line}")
        return decls
    