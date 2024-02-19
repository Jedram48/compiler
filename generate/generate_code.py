from generate.commands import *
from generate.expressions import *

class Generator():
        
    def __init__(self):
        self.variables = dict()
        self.free_space = [0]
        self.cmd = []
        self.register = {'a': True, 'b': True, 'c': True, 'd': True, 'e': True, 'f': True, 'g': True, 'h': True}
        self.main_start = 2
        self.memoryMapMain = {}
        self.memoryMapProcedures = {}
        self.procArgs = {}
        self.procaArgLists = {}
        self.procaArgIdLists = {}
        self.varTypes = {}
        self.procDecLine = {}
        self.initDict = {}
        self.accDict = {}
        self.callStack = []
        self.remapStack = []
        self.procedureCommands = {}
        self.lastJumpToken = 0
        
    def addArgList(self,arglist,proc):
        self.procaArgLists[proc] = arglist
        
    def GetJumpToken(self):
         self.lastJumpToken += 1
         return  self.lastJumpToken-1
        
    def  addArgIdList(self,argidlist,proc):
        self.procaArgIdLists[proc] = argidlist
         
    def getAddr(self,idnt):
        if len(self.callStack) == 0:
            return self.memoryMapMain[idnt]
        if(idnt in self.memoryMapProcedures[self.callStack[-1]]):
            return self.memoryMapProcedures[self.callStack[-1]][idnt]
        return self.remapStack[-1][idnt]
        
    def GetInline(self,proc,args_list):
        self.addToCallStack(proc, args_list)    # TODO 
        lines = self.procedureCommands[proc].getCode(self)
        self.removeFromCallStack()
        return lines
        
    def addToCallStack(self,proc,idList):
        argidList = self.procaArgIdLists[proc]
        idMap = {}
        for i in range(len(argidList)):
            idMap[argidList[i]] = self.getAddr(idList[i]) # TODO
        self.remapStack.append(idMap)
        self.callStack.append(proc)
    
    def removeFromCallStack(self):
        self.callStack.pop()
        self.remapStack.pop()
        
        
    def addAccess(self, identifier, proc, line):
        if proc not in self.accDict:
            self.accDict[proc] = {}
        if identifier not in self.accDict[proc]:
            self.accDict[proc][identifier] = line
        self.accDict[proc][identifier] = min(self.accDict[proc][identifier],line)
        
    def addInit(self, identifier, proc, line):
        if proc not in self.initDict:
            self.initDict[proc] = {}
        if identifier not in self.initDict[proc]:
            self.initDict[proc][identifier] = line
        self.initDict[proc][identifier] = min(self.initDict[proc][identifier],line)
        
    def getMemoryMap(self,proc):
       
        if(proc == "") :
            return  self.memoryMapMain
        return self.memoryMapProcedures[proc] | self.procArgs[proc]
    
    def getDeclType(self,proc):
        if proc == "":
            return self.varTypes[proc]
        return self.varTypes[proc] | self.procArgs[proc]
        
    def generate(self, main):
        main.GetDeclarations(self)
        main.checkDeclarations(self)
        self.checkForInitError()
        rawCMD = main.getCode(self)
        pos= {}
        for cmdLine in range(len(rawCMD)):
            sp = rawCMD[cmdLine].split("$")
            for idx in range(1,len(sp),2):
                pos[int(sp[idx])] = cmdLine
            rawCMD[cmdLine] = ''.join([sp[idx] for idx in range(0,len(sp),2)])
            
        for cmdLine in range(len(rawCMD)):
            sp = rawCMD[cmdLine].split("&")
            for idx in range(1,len(sp),2):
                rawCMD[cmdLine] = sp[0]+ f"{pos[int(sp[idx])]}"
            
        rawCMD.append("HALT")
        return rawCMD
        
        
    def checkForInitError(self):
        for proc in self.accDict:
            for acc in self.accDict[proc]:
                if proc not in self.initDict or acc not in self.initDict[proc] or self.accDict[proc][acc]<=  self.initDict[proc][acc]:
                    raise Exception(f"Access to unitialized variable {acc} at line {self.accDict[proc][acc]}")
            
    
    
    def generateMemoryMap(self,mainDecls,procDecls,procArgs,procDecLine):
        addr = 0
        self.varTypes[""] = {}
        for decl in mainDecls:
            self.memoryMapMain[decl] = addr
            addr += mainDecls[decl]
            self.varTypes[""][decl] = mainDecls[decl] > 1
        for procDecl in procDecls:
            self.varTypes[procDecl] = {}
            self.memoryMapProcedures[procDecl] = {}
            for decl in procDecls[procDecl]:
                self.memoryMapProcedures[procDecl][decl] = addr
                self.varTypes[procDecl][decl] = procDecls[procDecl][decl] > 1
                addr += procDecls[procDecl][decl]
        for procArg in procArgs:
            self.procArgs[procArg] = {}
            for arg in procArgs[procArg]:
                self.procArgs[procArg][arg] = procArgs[procArg][arg]
        self.procDecLine = procDecLine
                    
        
    def free_register_a(self):
        if self.register['a']:
            return
        key = self.get_free_register()
        self.register['a'] = True
        self.register[key] = False
        return [f"PUT {key}", "RST a"]
            
    def get_free_register(self):
        items = list(self.register.items())
        for key, value in items[1:]:
            if value:
                return key

    def add_variable(self, id):
        self.variables[id] = self.free_space[-1]
        if len(self.free_space) < 2: self.free_space[0] += 1
        else: del self.free_space[-1]
        
    def get_variable(self, id):
        if id in self.variables:
            return self.variables[id]
        return -1
    
    def value(self, value):
        r = 'a' if self.register['a'] else self.get_free_register()
        self.register[r] = False
        if type(value) is int:
            self.cmd.append(Expressions.value(value, r))
        elif type(value) is str:
            if value not in self.variables:
                return -1
            lines = tuple(Expressions.value(self.variables[value], r) + tuple([f"LOAD {r}", f"PUT {r}"]))
            if r != 'a':
                r2 = self.get_free_register()
                start = tuple([f"PUT {r2}"])
                end = tuple([f"GET {r2}", f"RST {r2}"])
                lines = start + lines + end
            self.cmd.append(lines)
        return r
    
    def expression(self, r1: str, op, r2: str):
        if op is None:
            if r1 != 'a':
                self.cmd.append(tuple([f"GET {r1}", f"RST {r1}"]))
        return 'a'
    
    def assign(self, id: str):
        if id not in self.variables:
            return -1
        r2 = self.get_free_register()
        self.cmd.append(tuple(Commands.assign(self.variables[id], r2)))
        self.register['a'] = True
        
    def write(self):
        self.cmd.append(Commands.write_value())
        self.register['a'] = True