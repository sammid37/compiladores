class Token:
  def __init__(self, token_type, value, line, erro_sintatico = None):
    self.type = token_type
    self.value = value
    self.line = line
    self.erro_sintatico = erro_sintatico

  def __str__(self):
    if(self.erro_sintatico): 
      return f"({self.value}, {self.type}, linha {self.line}, erro sintático: '{self.erro_sintatico}')"
    else:
      return f"({self.value}, {self.type}, linha {self.line})"
