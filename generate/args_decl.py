class Args_Decl:
    def __init__(self) -> None:
        self.args_decl = []
        pass
    
    def add_identifier(self, pidentifier, T: bool, line) -> None:
        self.args_decl.append((pidentifier, T, line))
        pass
    
    def getDeclarations(self, generaotr, proc):
        result_dict = {}
        for item in self.args_decl:
            if item[0] in result_dict:
                raise Exception(f"Multiple declaration of variable {item[0]} in line {self.item[2]}")
            result_dict[item[0]] = item[1]
            generaotr.addInit(item[0], proc.pidentifier, item[2])
        generaotr.addArgList([item[1] for item in self.args_decl],proc.pidentifier)
        generaotr.addArgIdList([item[0] for item in self.args_decl],proc.pidentifier)
        return result_dict