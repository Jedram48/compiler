class Commands:
    def __init__(self) -> None:
        self.commands = []
        pass
    
    def add_command(self, command) -> None:
        self.commands.append(command)
        pass
    
    
    def checkDeclarations(self, generator, proc):
        for command in self.commands:
            command.checkDeclarations(generator,proc)
            
    def getCode(self,generator):
        return  sum([command.getCode(generator) for command in self.commands], [])
            
            
            
    