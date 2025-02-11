# Trabalho prático de Compiladores
# {
#   Julia Gabriella Corrêa Silva
#   Johnattan Silva Ferreira
#   Henrique Araujo Miranda
# }

from Token import Token

class AnalisadorLexico:
    def __init__(self, filename):
        self.posArquivo = 0
        self.linha = 1
        try:
            with open(filename, encoding='utf-8') as file:
                txtConteudo = file.read()
                print()
                print('------------------------')
                print(txtConteudo) 
                print('------------------------')
                print()
                self.conteudo = list(txtConteudo) # converte para lista
        except Exception as ex:
            print(f'Ocorreu um erro: {ex}')
            exit()

    def numero(self, c):
        return c is not None and (c >= '0' and c <= '9')

    def caracterMa(self, c):
        return c is not None and (c >= 'A' and c <= 'Z')

    def caracterMi(self, c):
        return c is not None and (c >= 'a' and c <= 'z')

    def espaco(self, c):
        return (c == ' ') or (c == '\t') or (c == None) 

    def simbolo(self, c):
        return (c == '|') or (c == '(') or (c == ')') or (c == '[') or (c == ']') or (c == ',') or (c =='?') or (c == ';')  or (c == ':') or (c == '.')  or (c == '{')  or (c == '}')

    def operadorAr(self, c):
        return (c == '+') or (c == '-') or (c == '*') or (c == '/')

    def EOF(self):
        return self.posArquivo >= len(self.conteudo)
    
    def proximoChar(self): 
        if self.EOF():
            return None
               
        aux = self.conteudo[self.posArquivo]
        self.posArquivo += 1
        return aux

    def proximoToken(self):
        if self.EOF():
            return None
    
        self.charAtual = ''
        self.termo = ''
        self.estado = 0    
        while(True):
            
            self.charAtual = self.proximoChar()
            
            if self.estado == 0:
                if self.caracterMi(self.charAtual):
                    self.termo += self.charAtual
                    self.estado = 1
                    if self.EOF():
                        token = Token(Token.TK_IDENTIFICADOR, self.termo, self.linha)
                        return token
            
                elif self.numero(self.charAtual):   
                    self.termo += self.charAtual
                    self.estado = 3
                    if self.EOF():
                        token = Token(Token.TK_NUMERO, self.termo, self.linha)
                        return token
                        
                elif self.charAtual == '"':
                    self.termo += self.charAtual
                    self.estado = 5
                    
                elif self.caracterMa(self.charAtual):
                    self.termo += self.charAtual
                    self.estado = 7
                    if self.EOF():
                        return self.palavraRes(self.termo)
                
                elif self.charAtual == '\n':
                    self.linha += 1
            
                elif self.espaco(self.charAtual):
                    self.charAtual = ''
                    self.termo = ''
                    self.estado = 0  
                    if self.EOF():
                        return None                          
                    
                elif self.charAtual == '!':
                    self.termo += self.charAtual
                    self.estado = 9
                    
                elif self.simbolo(self.charAtual):
                    self.termo += self.charAtual
                    self.estado = 11
                    if self.EOF():
                        return self.simboloEsp(self.termo)
                
                elif self.operadorAr(self.charAtual):
                    self.termo += self.charAtual
                    self.estado = 12
                    if self.EOF():
                        return self.operadorAri(self.termo)
                    
                elif self.charAtual == '=':
                    self.termo += self.charAtual
                    self.estado = 18
                    
                elif self.charAtual == '>':
                    self.termo += self.charAtual
                    self.estado = 14
                
                elif self.charAtual == '<':
                    self.termo += self.charAtual
                    self.estado = 13
                
            elif self.estado == 1:
                if (self.caracterMi(self.charAtual) or self.caracterMa(self.charAtual) or self.numero(self.charAtual)):
                    self.termo += self.charAtual
                    self.estado = 1
                    
                else: # Estado 2
                    if self.EOF():
                        token = Token(Token.TK_IDENTIFICADOR, self.termo, self.linha)
                    else:
                        self.posArquivo -= 1
                        token = Token(Token.TK_IDENTIFICADOR, self.termo, self.linha)
                    return token
            
            elif self.estado == 3:
                if (self.numero(self.charAtual)):
                    self.termo += self.charAtual
                    self.estado = 3
                    if self.EOF():
                        token = Token(Token.TK_NUMERO, self.termo, self.linha)
                        return token
                    
                else: # Estado 4
                    self.posArquivo -= 1
                    token = Token(Token.TK_NUMERO, self.termo, self.linha)
                    return token
                
            elif self.estado == 5:
                if (self.caracterMi(self.charAtual) or self.caracterMa(self.charAtual) or self.numero(self.charAtual) or self.charAtual == ' '):
                    self.termo += self.charAtual
                    self.estado = 5
                elif self.charAtual == '"':
                    self.termo += self.charAtual
                    self.estado = 6
                else: 
                    print("ERRO LÉXICO LINHA:", self.linha, "- ESPERAVA (\") OU CARACTERE INVÁLIDO INSERIDO")
                    exit()
            
            elif self.estado == 6:
                if self.EOF():
                    token = Token(Token.TK_LITERAL, self.termo, self.linha)
                else:
                    self.posArquivo -= 1 
                    token = Token(Token.TK_LITERAL, self.termo, self.linha)
                return token

            elif self.estado == 7:
                if self.caracterMa(self.charAtual):
                    self.termo += self.charAtual
                    self.estado = 7
                else:
                    if self.EOF():
                        return self.palavraRes(self.termo)
                    
                    else: #ESTADO 8
                        self.posArquivo -= 1
                        token = self.palavraRes(self.termo)
                        self.termo = ''
                        self.estado = 0
                        return token
           
            elif self.estado == 9:
                if (self.charAtual != "\n"):
                    self.estado = 9 
                else:
                    self.linha += 1
                    if self.EOF():
                        return None
                    
                    else: #ESTADO 10
                        self.charAtual = ''
                        self.termo = ''
                        self.estado = 0

            elif self.estado == 11:
                self.posArquivo -= 1 
                return self.simboloEsp(self.termo)
            
            elif self.estado == 12:
                self.posArquivo -= 1 
                return self.operadorAri(self.termo)
            
            elif self.estado == 18:
                self.posArquivo -= 1 
                token = Token(Token.TK_ATRIBUICAO, self.termo, self.linha)
                return token
            
            elif self.estado == 13:
                if self.charAtual == '=':
                    self.termo += self.charAtual
                    self.estado = 16
                        
                else:
                    self.posArquivo -= 1 
                    token = Token(Token.TK_MENOR, self.termo, self.linha)
                    return token
            
            elif self.estado == 14:
                if self.charAtual == '=':
                    self.termo += self.charAtual
                    self.estado = 16
                        
                else:
                    self.posArquivo -= 1 
                    token = Token(Token.TK_MAIOR, self.termo, self.linha)
                    return token

            elif self.estado == 16:
                if self.charAtual == '>=':
                    self.posArquivo -= 1 
                    token = Token(Token.TK_MAIORIGUAL, self.termo, self.linha)
                    return token
                else:
                    self.posArquivo -= 1
                    token = Token(Token.TK_MENORIGUAL, self.termo, self.linha)
                    return token
            
    def palavraRes(self, termo):
        if termo == 'SATUS':      # MAIN
            return Token(Token.TK_MAIN, termo, self.linha)
        elif termo == 'NUMERUS':  # INT
            return Token(Token.TK_INT, termo, self.linha)
        elif termo == 'LITTERAE': # CHAR
            return Token(Token.TK_CHAR, termo, self.linha)
        elif termo == 'SI':       # IF
            return Token(Token.TK_IF, termo, self.linha)
        elif termo == 'ALIUD':    # ELSE
            return Token(Token.TK_ELSE, termo, self.linha)
        elif termo == 'DUM':      # WHILE
            return Token(Token.TK_WHILE, termo, self.linha)
        elif termo == 'LEGERE':   # CIN
            return Token(Token.TK_CIN, termo, self.linha)
        elif termo == 'SCRIBERE': # COUT
            return Token(Token.TK_COUT, termo, self.linha)
        elif termo == 'REDITUS':  # RETURN
            return Token(Token.TK_RETURN, termo, self.linha)          
        elif termo == 'AUT':      # OR
            return Token(Token.TK_OR, termo, self.linha)
        elif termo == 'ET':       # AND
            return Token(Token.TK_AND, termo, self.linha)
        elif termo == 'NO':       # NOT
            return Token(Token.TK_NOT, termo, self.linha)
        elif termo == 'VERUM':    # TRUE
            return Token(Token.TK_BOOL, termo, self.linha)
        elif termo == 'FALSUS':   # FALSE
            return Token(Token.TK_BOOL, termo, self.linha)
        else:
            print("ERRO LÉXICO LINHA:", self.linha, "- PALAVRA RESERVADA:",self.termo)
            exit()
            
    def simboloEsp(self, termo):
        if termo == '|': # PONTO E VERGULA
            return Token(Token.TK_PIPE, termo, self.linha)
        elif termo == '(':
            return Token(Token.TK_ABRPARENTESE, termo, self.linha)
        elif termo == ')':
            return Token(Token.TK_FCHPARENTESE, termo, self.linha)
        elif termo == '[':
            return Token(Token.TK_ABRCOLCHETE, termo, self.linha)
        elif termo == ']':
            return Token(Token.TK_FCHCOLCHETE, termo, self.linha)
        elif termo == ',': 
            return Token(Token.TK_VIRGULA, termo, self.linha)
        else:
            print("ERRO LÉXICO LINHA:", self.linha, "- SIMBOLO ESPECIAL:",self.termo)
            exit()
        
    def operadorAri(self, termo):
        if termo == '+':
            return Token(Token.TK_SOMA, termo, self.linha)
        elif termo == '-':
            return Token(Token.TK_SUBTRACAO, termo, self.linha)
        elif termo == '*':
            return Token(Token.TK_MULTIPLICACAO, termo, self.linha)
        elif termo == '/':
            return Token(Token.TK_DIVISAO, termo, self.linha)
        
    def operadorRel(self, termo):
        if termo == '>':
            return Token(Token.TK_MAIOR, termo, self.linha)
        elif termo == '<':
            return Token(Token.TK_MENOR, termo, self.linha)
        elif termo == '>=':
            return Token(Token.TK_MAIORIGUAL, termo, self.linha)
        elif termo == '<=':
            return Token(Token.TK_MENORIGUAL, termo, self.linha)