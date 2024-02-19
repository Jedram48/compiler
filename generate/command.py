

class Assign:
    def __init__(self, identifier, expression) -> None:
        self.identifier = identifier
        self.expression = expression
        pass
    
    def checkDeclarations(self, generator,proc):
        self.identifier.checkDeclarations(generator,proc, True)
        self.expression.checkDeclarations(generator,proc)
        
    def getCode(self,generator):
        c1 = self.identifier.getAddr("g",generator)
        c2 = self.expression.getCode("h",generator)
        return c1+c2+[f"GET h", f"STORE g", f"RST g", f"RST a"]
        
        

class IfThenElse:
    def __init__(self, condition, if_commands, else_commands) -> None:
        self.condition = condition
        self.if_commands = if_commands
        self.else_commands = else_commands
        pass
    
    def checkDeclarations(self, generator,proc):
        self.condition.checkDeclarations(generator,proc)
        self.if_commands.checkDeclarations(generator,proc)
        self.else_commands.checkDeclarations(generator,proc)
    def getCode(self,generator):
        cond = self.condition.getCode('b', 'c', generator)
        jumpToken1 = generator.GetJumpToken()
        jumpToken2 = generator.GetJumpToken()
        lines = cond + [f"RST b", f"RST c", f"GET f", f"JZERO &{jumpToken1}&"]
        lines += self.if_commands.getCode(generator) + [f"JUMP &{jumpToken2}&"]
        lines += [f"RST a", f"RST f ${jumpToken1}$"]
        lines += self.else_commands.getCode(generator) + [f"RST a ${jumpToken2}$"]
        return lines

class IfThen:
    def __init__(self, condition, commands) -> None:
        self.condition = condition
        self.commands = commands
        pass
    
    def checkDeclarations(self, generator,proc):
        self.condition.checkDeclarations(generator,proc)
        self.commands.checkDeclarations(generator,proc)
    def getCode(self,generator):
        cond = self.condition.getCode('b', 'c', generator)
        jumpToken = generator.GetJumpToken()
        lines = cond + [f"RST b", f"RST c", f"GET f", f"JZERO &{jumpToken}&"]
        lines += self.commands.getCode(generator)
        lines += [f"RST a", f"RST f ${jumpToken}$"]
        return lines
    
class WhileDo:
    def __init__(self, condition, commands) -> None:
        self.condition = condition
        self.commands = commands
        pass
    
    def checkDeclarations(self, generator,proc):
        self.condition.checkDeclarations(generator,proc)
        self.commands.checkDeclarations(generator,proc)
    def getCode(self,generator):
        jumpToken1 = generator.GetJumpToken()
        jumpToken2 = generator.GetJumpToken()
        cond = [f"RST a ${jumpToken1}$"] + self.condition.getCode('b', 'c', generator)
        lines = cond + [f"GET f", f"JZERO &{jumpToken2}&"]
        lines += self.commands.getCode(generator) + [f"JUMP &{jumpToken1}&", f"RST a", f"RST f ${jumpToken2}$"]
        return lines
    
class RepeatUntil:
    def __init__(self, commands, condition) -> None:
        self.condition = condition
        self.commands = commands
        pass
    
    def checkDeclarations(self, generator,proc):
        self.condition.checkDeclarations(generator,proc)
        self.commands.checkDeclarations(generator,proc)
    def getCode(self,generator):
        jumpToken1 = generator.GetJumpToken()
        lines = [f"RST a ${jumpToken1}$"] + self.commands.getCode(generator)
        lines += self.condition.getCode('b', 'c', generator) + [f"GET f", f"JZERO &{jumpToken1}&", f"RST a", f"RST f", f"RST b", f"RST c"]
        return lines
    
class Proc_Call:
    def __init__(self, proc_call) -> None:
        self.proc_call = proc_call
        pass
    
    def checkDeclarations(self, generator,proc):
        self.proc_call.checkDeclarations(generator,proc)
    def getCode(self,generator):
        return self.proc_call.getCode(generator)
        
    
class Read:
    def __init__(self, identifier) -> None:
        self.identifier = identifier
        pass
    
    def checkDeclarations(self, generator,proc):
        self.identifier.checkDeclarations(generator,proc, True)
    def getCode(self,generator):
        return self.identifier.getAddr("g",generator) + [f"READ", f"STORE g", "RST a", "RST g"]
    
class Write:
    def __init__(self, value) -> None:
        self.value = value
        pass
    
    def checkDeclarations(self, generator,proc):
        self.value.checkDeclarations(generator,proc, False)
    def getCode(self,generator):
        r = 'h'
        return self.value.getCode(r,generator) + [f"GET {r}", f"WRITE", "RST a", f"RST {r}"]