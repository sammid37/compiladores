# 🦎 Construção de Compiladores I

O seguinte repositório contém a implementação de um compilador para a linguagem de programação pascal desenvolvido para a disciplina de Construção de Compiladores I (período 2023.2). 

O compilador é composto pelo analisador léxico e sintático, sendo o analisador semântico implementado dentro do analisador sintático.

## 🦎 Dependências e Execução

O projeto foi desenvolvido em Python 3.10.x. 

Antes de executar o código principal, por favor baixe as seguintes dependências:

```bash
pip install termcolor # versão 2.4.0
```

Feito isso, execute o comando abaixo.

```bash
python main.py
```

### 🧪 Arquivos de Testes

Os arquivos de testes encontram-se no diretório `/test`.

A execução do programa principal (arquivo `main.py`) faz uso dos 5 arquivos de testes do diretório `/test/syntax_tests`.

Todos eles são executados automaticamente, mas caso um deles falhe no caminho, os demais não serão executados. 

Para realizar mais testes, você pode adicionar mais arquivos no diretório `/test/syntax_tests` portanto que o arquivo siga com o padrão dos demais. Ou seja, `TestX.pas` onde X corresponde a um número igual a 6 ou maior. 

Não esqueça de modificar a seguinte seção do código do arquivo principal:

```python
if __name__ == "__main__":
  print(colored("* * * Projeto de Compiladores", "cyan"))
  test_files_directory = "test/syntax_tests/"
  for i in range(1, 6): # modifique o numéro 6 para 7 ou maior caso tenha mais arquivos de teste
    file_name = os.path.join(test_files_directory, f"Test{i}.pas")
    main(file_name)
```

## 💾 Futuras implementações

- [ ] Concertar o analisador léxico implementado com AFD
- [ ] Permitir a execução dos próximos arquivos de testes caso algum falhe em alguma análise