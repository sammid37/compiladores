# Construção de Compiladores
# Implementação de Estrutura Pilha para a Análise Semântica
# Enthony e Samantha
class Pilha:
  def __init__(self):
    self.items = []

  def vazia(self):
    return len(self.items) == 0

  def empilhar(self, item):
    self.items.append(item)

  def desempilhar(self):
    if not self.vazia():
      return self.items.pop()
    else:
      return None

  def topo(self):
    if not self.vazia():
      return self.items[-1]
    else:
      return None

  def tamanho(self):
    return len(self.items)
  
  def __iter__(self):
    """Iterando em ordem inversa, como se estivéssimos desempilhando"""
    return iter(self.items[::-1])
  
  def exbirPilhaIdentificadores(self):
    for i in self.items:
      print(f"Conteúdo da pilha: {i}")

  def exibirPilhaIdsTipados(self):
    for identificadorTipado in self.items:
      print(f"Identificador: {identificadorTipado.identificador}, Tipo: {identificadorTipado.tipo}")


# # Exemplo de uso da pilha
# pilha = Pilha()

# pilha.empilhar("Elemento 1")
# pilha.empilhar("Elemento 2")
# pilha.empilhar("Elemento 3")
# pilha.empilhar("Elemento 4")

# # Lendo e removendo os elementos da pilha
# while not pilha.vazia():
#   elemento = pilha.desempilhar()
#   print("Elemento lido:", elemento)
