class Token:
  def __init__(self, token_type, value, line):
    self.type = token_type
    self.value = value
    self.line = line
    
  def __str__(self):
    return f"({self.value}, {self.type}, linha {self.line})"