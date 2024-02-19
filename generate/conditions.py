class Contidion:
    def __init__(self, value1, op, value2) -> None:
        self.value1 = value1
        self.op = op
        self.value2 = value2
        pass
    
    def checkDeclarations(self, generator,proc):
        self.value1.checkDeclarations(generator,proc, False)
        self.value2.checkDeclarations(generator,proc, False)
        
    def getCode(self,r1, r2, generator):
        if self.op == '=':
           return self.equal(r1, r2, generator)
        elif self.op == '!=':
            return self.not_equal(r1, r2, generator)
        elif self.op == '>':
            return self.greater(r1, r2, generator)
        elif self.op == '<': 
            return self.less(r1, r2, generator)
        elif self.op == '>=':   
            return self.greater_or_equal(r1, r2, generator)
        elif self.op == '<=':
            return self.less_or_equal(r1, r2, generator)
            
    def equal(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        jumpToken1 = generator.GetJumpToken()
        jumpToken2 = generator.GetJumpToken()
        lines = [
            f"RST f",
            f"INC f",
            f"GET {r1}",
            f"SUB {r2}",
            f"JPOS &{jumpToken1}&",
            f"RST a",
            f"GET {r2}",
            f"SUB {r1}",
            f"JPOS &{jumpToken1}&",
            f"JUMP &{jumpToken2}&",
            f"RST {r1} ${jumpToken1}$",
            f"DEC f",
            f"RST {r2}",
            f"RST a ${jumpToken2}$"
        ]
        return v1+v2+lines
        
    def not_equal(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        jumpToken1 = generator.GetJumpToken()
        lines = [
            f"RST f",
            f"INC f",
            f"GET {r1}",
            f"SUB {r2}",
            f"JPOS &{jumpToken1}&",
            f"RST a",
            f"GET {r2}",
            f"SUB {r1}",
            f"JPOS &{jumpToken1}&",
            f"DEC f",
            f"RST {r1} ${jumpToken1}$",
            f"RST {r2}",
            f"RST a"
        ]
        return v1+v2+lines
    
    def greater(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        lines = [
            f"RST f",
            f"GET {r1}",
            f"SUB {r2}",
            f"PUT f",
            f"RST a"
        ]
        return v1+v2+lines
        
    def less(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        lines = [
            f"RST f",
            f"GET {r2}",
            f"SUB {r1}",
            f"PUT f",
            f"RST a"
        ]
        return v1+v2+lines
        
    def greater_or_equal(self, r1, r2, generator):#_
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        lines = [
            f"RST f",
            f"GET {r1}",
            f"DEC {r2}",
            f"SUB {r2}",
            f"PUT f",
            f"RST a"
        ]
        return v1+v2+lines
        
    def less_or_equal(self, r1, r2, generator): #+
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        lines = [
            f"RST f",
            f"GET {r2}",
            f"DEC {r1}",
            f"SUB {r1}",
            f"PUT f",
            f"RST a"
        ]
        return v1+v2+lines
