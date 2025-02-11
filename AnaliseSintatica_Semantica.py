# Trabalho prático de Compiladores
# {
#   Julia Gabriella Corrêa Silva
#   Johnattan Silva Ferreira
#   Henrique Araujo Miranda
# }

from AnaliseLexica import AnalisadorLexico
from Token import Token

class AnalisadorSintatico:

    def __init__(self, scanner: AnalisadorLexico):
        self.scanner = scanner  
        self.token = None 
        self.lista_id = []
        
    # AO TENTAR DECLARAR UMA VARIAVEL DUAS VEZES
    def verificaDeclara(self, id): 
        for i in self.lista_id:
            if i.getTexto() == id.getTexto(): 
                print("ERRO SEMANTICO LINHA:", self.token.getLinha(), "- ESSA VARIAVEL JÁ EXISTE:", self.token.getTexto())
                exit() 
        self.lista_id.append(id)
    
    # AO CHAMAR UMA VARIAVEL
    def existeVar(self, id): 
        existe = False
        for i in self.lista_id: 
            if i.getTexto() == id.getTexto(): 
                existe = True
        if not existe:
            print("ERRO SEMANTICO LINHA:", self.token.getLinha(), "- ESSA VARIAVEL NÃO EXISTE:", self.token.getTexto())
            exit()
    
    # LITTERAE NAO RECEBE NUMERUS E VICE-VERSA
    def verificaTipoVar(self, var, tipo):
        if tipo == 1:
            if not var == tipo:
                print("ERRO SEMANTICO LINHA:", self.token.getLinha(), "- ESSA VARIAVEL NÃO É NUMERUS")
                exit() 
        if tipo == 2:
            if not var == tipo: 
                print("ERRO SEMANTICO LINHA:", self.token.getLinha(), "- ESSA VARIAVEL NÃO É LITTERAE")
                exit()   
        
    
    # MAIN -> SATUS '(' DECLARA BLOCO ')'
    def MAIN(self):
        self.token = self.scanner.proximoToken()
        if self.token.getTipo() == Token.TK_MAIN:                 
            self.token = self.scanner.proximoToken()
            if self.token.getTipo() == Token.TK_ABRPARENTESE:     
                self.token = self.scanner.proximoToken()
                self.DECLARA()
                self.BLOCO()
                if self.token.getTipo() == Token.TK_FCHPARENTESE:  
                    self.token = self.scanner.proximoToken()
                    if self.token == None:
                        print("COMPILAÇÃO BEM SUCEDIDA!")
                        print()
                        print('------------------------')
                    else:
                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- CONTEÚDO FORA DE ESCOPO ")
                        exit() 
                else:
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA ')' ")
                    exit()
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA '(' ")
                exit()
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: SATUS ")
            exit()
    
    # DECLARA -> VAR DECLARA | ε
    def DECLARA(self):
        while self.token.getTipo() == Token.TK_CHAR or self.token.getTipo() == Token.TK_INT: 
            if self.token.getTipo() == Token.TK_CHAR:
                self.token = self.scanner.proximoToken()
                self.token.declaracao = 2
            if self.token.getTipo() == Token.TK_INT:
                self.token = self.scanner.proximoToken()
                self.token.declaracao = 1
            self.VAR()
            self.DECLARA() 

    # BLOCO -> CMD BLOCO | ε    
    def BLOCO(self):
        while self.token.getTipo() != Token.TK_FCHPARENTESE:
            self.CMD()
            self.BLOCO()
    
    # CMD -> IN | OUT | LOOP | IF | EXP | ATR
    def CMD(self):
        if self.token.getTipo() == Token.TK_CIN: 
            self.token = self.scanner.proximoToken()
            self.IN()
        elif self.token.getTipo() == Token.TK_COUT or self.token.getTipo() == Token.TK_RETURN:
            self.OUT()
        elif self.token.getTipo() == Token.TK_WHILE: 
            self.token = self.scanner.proximoToken()
            self.LOOP()
        elif self.token.getTipo() == Token.TK_IF: 
            self.token = self.scanner.proximoToken()
            self.IF()
        elif self.token.getTipo() == Token.TK_IDENTIFICADOR:
            self.existeVar(self.token)
            self.token = self.scanner.proximoToken() 
            if self.token.getTipo() == Token.TK_ATRIBUICAO:
                self.token = self.scanner.proximoToken()
                self.ATR()
        else: 
            print ("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: COMANDO")
            exit()
    
    # IN -> LEGERE [ ID ] '|'
    def IN(self): 
        if self.token.getTipo() == Token.TK_ABRCOLCHETE: 
            self.token = self.scanner.proximoToken() 
            if self.token.getTipo() == Token.TK_IDENTIFICADOR:
                self.existeVar(self.token)
                self.token = self.scanner.proximoToken()
                if self.token.getTipo() == Token.TK_FCHCOLCHETE: 
                    self.token = self.scanner.proximoToken()
                    if self.token.getTipo() == Token.TK_PIPE: 
                        self.token = self.scanner.proximoToken()
                    else:
                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '|' ")
                        exit()
                else:
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ']' ")
                    exit() 
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: IDENTIFICADOR ")
                exit()  
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '[' ")
            exit()       

    # OUT -> SCRIBERE [ ID | TEXTO ] '|' | REDITUS [ ID ] '|'
    def OUT(self): 
        # SCRIBERE [ ID | TEXTO ] '|'
        if self.token.getTipo() == Token.TK_COUT:
            self.token = self.scanner.proximoToken()
            if self.token.getTipo() == Token.TK_ABRCOLCHETE: 
                self.token = self.scanner.proximoToken() 
                if self.token.getTipo() == Token.TK_IDENTIFICADOR or self.token.getTipo() == Token.TK_LITERAL:
                    if self.token.getTipo() == Token.TK_IDENTIFICADOR:
                        self.existeVar(self.token)
                    self.token = self.scanner.proximoToken()
                    if self.token.getTipo() == Token.TK_FCHCOLCHETE: 
                        self.token = self.scanner.proximoToken()
                        if self.token.getTipo() == Token.TK_PIPE: 
                            self.token = self.scanner.proximoToken()
                        else:
                            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '|' ")
                            exit()
                    else:
                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ']' ")
                        exit() 
                else:
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: IDENTIFICADOR OU TEXTO ")
                    exit()  
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '[' ")
                exit()  
                
        # REDITUS [ ID ] '|'
        elif self.token.getTipo() == Token.TK_RETURN:
            self.token = self.scanner.proximoToken()
            if self.token.getTipo() == Token.TK_ABRCOLCHETE: 
                self.token = self.scanner.proximoToken() 
                if self.token.getTipo() == Token.TK_IDENTIFICADOR:
                    self.existeVar(self.token)
                    self.token = self.scanner.proximoToken()
                    if self.token.getTipo() == Token.TK_FCHCOLCHETE: 
                        self.token = self.scanner.proximoToken()
                        if self.token.getTipo() == Token.TK_PIPE: 
                            self.token = self.scanner.proximoToken()
                        else:
                            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '|' ")
                            exit()
                    else:
                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ']' ")
                        exit() 
                else:
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: IDENTIFICADOR ")
                    exit()  
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '[' ")
                exit()  
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: SCRIBERE OU REDITUS ")
            exit()    
        
    # LOOP -> DUM [ EXP OP EXP | BOOL ] '(' BLOCO ')'
    def LOOP(self): 
        if self.token.getTipo() == Token.TK_ABRCOLCHETE:
            self.token = self.scanner.proximoToken() 
            if self.token.getTipo() == Token.TK_NUMERO or self.token.getTipo() == Token.TK_ABRPARENTESE or self.token.getTipo() == Token.TK_IDENTIFICADOR: #arrumar o if por algum funcional
                if self.token.getTipo() == Token.TK_IDENTIFICADOR:
                    self.existeVar(self.token)
                self.EXP()
                self.OP()
                self.EXP()
            elif(self.token.getTipo() == Token.TK_BOOL):
                self.token = self.scanner.proximoToken() 
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: EXPRESSAO OU BOOL ")
                exit()
            if self.token.getTipo() == Token.TK_FCHCOLCHETE:
                self.token = self.scanner.proximoToken() 
                if self.token.getTipo() == Token.TK_ABRPARENTESE:
                    self.token = self.scanner.proximoToken() 
                    self.BLOCO()
                    if self.token.getTipo() == Token.TK_FCHPARENTESE:
                        self.token = self.scanner.proximoToken()         
                    else: 
                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ')' ")
                        exit()                
                else: 
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '(' ")
                    exit()                   
            else: 
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ']' ")
                exit()
        else: 
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '[' ")
            exit()
        
    # LOOP -> DUM [ EXP OP EXP | BOOL ] '(' BLOCO ')'
    def IF(self): 
        if self.token.getTipo() == Token.TK_ABRCOLCHETE:
            self.token = self.scanner.proximoToken() 
            if self.token.getTipo() == Token.TK_NUMERO or self.token.getTipo() == Token.TK_ABRPARENTESE or self.token.getTipo() == Token.TK_IDENTIFICADOR: #arrumar o if por algum funcional
                self.EXP()
                self.OP()
                self.EXP()
                if self.token.getTipo() == Token.TK_FCHCOLCHETE:
                    self.token = self.scanner.proximoToken() 
                    if self.token.getTipo() == Token.TK_ABRPARENTESE:
                        self.token = self.scanner.proximoToken() 
                        self.BLOCO()
                        if self.token.getTipo() == Token.TK_FCHPARENTESE:
                            self.token = self.scanner.proximoToken() 
                            if self.token.getTipo() == Token.TK_ELSE: 
                                self.token = self.scanner.proximoToken() 
                                if self.token.getTipo() == Token.TK_ABRPARENTESE:
                                    self.token = self.scanner.proximoToken() 
                                    self.BLOCO()
                                    if self.token.getTipo() == Token.TK_FCHPARENTESE:
                                        self.token = self.scanner.proximoToken() 
                                    else: 
                                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ')' ")
                                        exit()
                                else: 
                                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '(' ")
                                    exit()             
                        else: 
                            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ')' ")
                            exit()                
                    else: 
                        print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '(' ")
                        exit()                   
                else: 
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ']' ")
                    exit()
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: EXPRESSÃO ")
                exit()
        else: 
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '[' ")
            exit()
                        
    # OP -> LOGICO | ARITMETICO | RELACIONAL
    def OP(self): 
        if self.token.getTipo() == Token.TK_OR or self.token.getTipo() == Token.TK_AND or self.token.getTipo() == Token.TK_NOT:
            self.token = self.scanner.proximoToken()
        elif self.token.getTipo() == Token.TK_SOMA or self.token.getTipo() == Token.TK_SUBTRACAO or self.token.getTipo() == Token.TK_DIVISAO or self.token.getTipo() == Token.TK_MULTIPLICACAO:
            self.token = self.scanner.proximoToken()
        elif self.token.getTipo() == Token.TK_MAIOR or self.token.getTipo() == Token.TK_MENOR or self.token.getTipo() == Token.TK_MAIORIGUAL or self.token.getTipo() == Token.TK_MENORIGUAL:
            self.token = self.scanner.proximoToken()
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: OPERADOR ")
            exit()  

    # VAR -> TYPE ID (, ID)* '|' | TYPE ATR     
    def VAR(self):
        aux = self.token.declaracao
        tipo = 0
        if self.token.getTipo() == Token.TK_IDENTIFICADOR:
            self.verificaDeclara(self.token)
            self.token = self.scanner.proximoToken()
            if self.token.getTipo() == Token.TK_VIRGULA:
                while(self.token.getTipo() == Token.TK_VIRGULA): 
                    self.token = self.scanner.proximoToken()
                    self.ID()
                if self.token.getTipo() == Token.TK_PIPE:
                    self.token = self.scanner.proximoToken()
                else:
                    print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '|' ou ',' ")
                    exit()
            elif self.token.getTipo() == Token.TK_ATRIBUICAO:
                self.token = self.scanner.proximoToken()
                if self.token.getTipo() == Token.TK_NUMERO or self.token.getTipo() == Token.TK_ABRPARENTESE or self.token.getTipo() == Token.TK_IDENTIFICADOR:
                    tipo = 1
                    self.verificaTipoVar(aux, tipo)
                elif self.token.getTipo() == Token.TK_LITERAL:
                    tipo = 2
                    self.verificaTipoVar(aux, tipo)
                self.ATR()
            elif self.token.getTipo() == Token.TK_PIPE:
                self.token = self.scanner.proximoToken()
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '|' ou ',' ")
                exit()
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: IDENTIFICADOR OU ATRIBUIÇÃO ")
            exit()         
            
    # ID -> (a..z)(A..Z | a..z | 0..9)*
    def ID(self):
        if self.token.getTipo() == Token.TK_IDENTIFICADOR:
            self.verificaDeclara(self.token)
            self.token = self.scanner.proximoToken()
        else: 
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: IDENTIFICADOR ")
            exit()
                    
    # ATR -> ID = (TEXTO | EXP) '|'    
    def ATR(self):
        if self.token.getTipo() == Token.TK_LITERAL:
            self.token = self.scanner.proximoToken()
        elif self.token.getTipo() == Token.TK_NUMERO or self.token.getTipo() == Token.TK_IDENTIFICADOR or self.token.getTipo() == Token.TK_ABRPARENTESE:
            self.EXP()
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: TEXTO OU EXPRESSÃO ")
            exit()
        if self.token.getTipo() == Token.TK_PIPE: 
            self.token = self.scanner.proximoToken()
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: '|' ")
            exit()
    
    # EXP -> TERM EXP'
    def EXP(self): 
        self.TERM()
        self.EXPL()
        
    # EXP' -> N0 EXP | ε
    def EXPL(self):
        if self.token.getTipo() == Token.TK_SOMA or self.token.getTipo() == Token.TK_SUBTRACAO:
            self.token = self.scanner.proximoToken()
            self.EXP()
    
    # TERM -> FATOR TERM'
    def TERM(self):
        self.FATOR()
        self.TERML()
        
    # TERM' -> N1 TERM | ε
    def TERML(self):
        if self.token.getTipo() == Token.TK_MULTIPLICACAO or self.token.getTipo() == Token.TK_DIVISAO:
            self.token = self.scanner.proximoToken()
            self.TERM()
        
    # FATOR -> NUMERO | ID | '(' EXP ')'
    def FATOR(self):
        if self.token.getTipo() == Token.TK_NUMERO or self.token.getTipo() == Token.TK_IDENTIFICADOR:
            if self.token.getTipo() == Token.TK_IDENTIFICADOR:
                self.existeVar(self.token)
            self.token = self.scanner.proximoToken()
        elif self.token.getTipo() == Token.TK_ABRPARENTESE: 
            self.token = self.scanner.proximoToken()
            self.EXP()
            if self.token.getTipo() == Token.TK_FCHPARENTESE:
                self.token = self.scanner.proximoToken()
            else:
                print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: ')' ")
                exit()
        else:
            print("ERRO SINTATICO LINHA:", self.token.getLinha(), "- ESPERAVA: NUMERO | ID | EXPRESSÃO ")
            exit()
    