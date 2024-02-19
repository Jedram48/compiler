import generate.functions.functions as fun


# class Expressions:
#     def __init__(self, value1, op, value2) -> tuple:
#         if op is None:
#             return self.value(value1, 'a')
#         pass
    
#     @classmethod
#     def value(self, value: int, r: str) -> tuple:
#         return fun.recreate_value(value, r)
    
class Expressions:
    def __init__(self, value1, op, value2) -> None:
        self.value1 = value1
        self.op = op
        self.value2 = value2
        pass
    
    def checkDeclarations(self, generator,proc):
        self.value1.checkDeclarations(generator,proc, False)
        self.value2.checkDeclarations(generator,proc, False)
        
    def getCode(self,r, generator):#TODO WARNING FUCKED UP CODE
        r1 = 'b'
        r2 = 'c'
        if self.op == '+':
           return self.plus(r1, r2, generator)
        elif self.op == '-':
           return  self.minus(r1, r2, generator)
        elif self.op == '*':
           return  self.mult(r1, r2, generator)
        elif self.op == '/': 
            return self.div(r1, r2, generator)
        elif self.op == '%':   
           return  self.mod(r1, r2, generator)
            
    def plus(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        return v1 + v2 +[f"GET {r1}", f"ADD {r2}", f"PUT h", f"RST {r2}"]
    def minus(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)
        v2 = self.value2.getCode(r2, generator)
        return v1 + v2 +[f"GET {r1}", f"SUB {r2}", f"PUT h", f"RST {r2}"]
    def mult(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)#b
        v2 = self.value2.getCode(r2, generator)#c
        jumpToken1 = generator.GetJumpToken()
        jumpToken2 = generator.GetJumpToken()
        r3 = 'e'
        r4 = 'f'
        lines = [
            f"RST {r4}",
            f"GET {r2}",
            f"PUT {r3} ${jumpToken2}$",
            f"SHR {r3}",
            f"SHL {r3}",
            f"SUB {r3}",
            f"JZERO &{jumpToken1}&",          # TODO
            f"GET {r4}",
            f"ADD {r1}",
            f"PUT {r4}",
            f"SHR {r2} ${jumpToken1}$",        # Jump here
            f"SHL {r1}",
            f"GET {r2}",
            f"JPOS &{jumpToken2}&",            # TODO
            f"GET {r4}",
            f"PUT h"
        ]
        return v1+v2+lines
        
    def div(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)#b
        v2 = self.value2.getCode(r2, generator)#c
        jumpToken1 = generator.GetJumpToken()
        jumpToken2 = generator.GetJumpToken()
        jumpToken3 = generator.GetJumpToken()
        jumpToken4 = generator.GetJumpToken()
        r3 = 'e'
        r4 = 'f'
        lines = [
            f"GET {r2}",
            f"JZERO &{jumpToken4}&",#out
            f"RST {r4}",
            f"RST {r3}",
            f"INC {r3}",
            f"SHL {r3} ${jumpToken2}$",#back
            f"SHL {r2}",
            f"GET {r1}",
            f"INC a",
            f"SUB {r2}",
            f"JPOS &{jumpToken2}&",#back
            f"SHR {r3} ${jumpToken3}$",#here
            f"GET {r3}",
            f"JZERO &{jumpToken1}&", #out
            f"SHR {r2}",
            f"GET {r1}",
            f"INC a",
            f"SUB {r2}",
            f"JZERO &{jumpToken3}&",#here
            f"DEC a",
            f"PUT {r1}",
            f"GET {r3}",
            f"ADD {r4}",
            f"PUT {r4}",
            f"JUMP &{jumpToken3}&", #here
            f"RST {r4} ${jumpToken4}$", #out
            f"GET {r4} ${jumpToken1}$",
            f"PUT h"
          ]
        return v1 + v2 + lines
    def mod(self, r1, r2, generator):
        v1 = self.value1.getCode(r1, generator)#b
        v2 = self.value2.getCode(r2, generator)#c
        jumpToken1 = generator.GetJumpToken()
        jumpToken2 = generator.GetJumpToken()
        jumpToken3 = generator.GetJumpToken()
        jumpToken4 = generator.GetJumpToken()
        r3 = 'e'
        r4 = 'f'
        lines = [
            f"GET {r2}",
            f"JZERO &{jumpToken4}&",#out
            f"RST {r3}",
            f"INC {r3}",
            f"SHL {r3} ${jumpToken2}$",#back
            f"SHL {r2}",
            f"GET {r1}",
            f"INC a",
            f"SUB {r2}",
            f"JPOS &{jumpToken2}&",#back
            f"SHR {r3} ${jumpToken3}$",#here
            f"GET {r3}" ,
            f"JZERO &{jumpToken1}&", #out
            f"SHR {r2}",
            f"GET {r1}",
            f"INC a",
            f"SUB {r2}",
            f"JZERO &{jumpToken3}&",#here
            f"DEC a",
            f"PUT {r1}",
            f"GET {r3}",
            f"JUMP &{jumpToken3}&", #here
            f"RST {r1} ${jumpToken4}$", #out
            f"GET {r1} ${jumpToken1}$",
            f"PUT h"
          ]
        return v1 + v2 + lines
class Expression_Value:
    def __init__(self, value) -> None:
        self.value = value
        pass
    
    def checkDeclarations(self, generator,proc):
        self.value.checkDeclarations(generator,proc, False)
        
    def getCode(self, proc, generator):
        return self.value.getCode('h', generator)
        