# Trabalho prático de Compiladores
# {
#   Julia Gabriella Corrêa Silva
#   Johnattan Silva Ferreira
#   Henrique Araujo Miranda
# }

class Token:
    TK_IDENTIFICADOR = 0  
    TK_NUMERO        = 1                       
    TK_LITERAL       = 2                       
    TK_PALAVRARE     = 3 
    TK_SIMBOLO       = 4
    TK_OPERACAOA     = 5
    TK_MAIN          = 6 
    TK_CHAR          = 7
    TK_INT           = 8
    TK_IF            = 9       
    TK_ELSE          = 10         
    TK_WHILE         = 11    
    TK_CIN           = 12
    TK_COUT          = 13       
    TK_RETURN        = 14
    TK_OR            = 15    
    TK_AND           = 16      
    TK_NOT           = 17      
    TK_BOOL          = 18
    TK_PIPE          = 19
    TK_ABRPARENTESE  = 20           
    TK_FCHPARENTESE  = 21
    TK_SOMA          = 22
    TK_SUBTRACAO     = 23 
    TK_MULTIPLICACAO = 24           
    TK_DIVISAO       = 25 
    TK_ATRIBUICAO    = 26
    TK_MENOR         = 27
    TK_MAIOR         = 28
    TK_MAIORIGUAL    = 29 
    TK_MENORIGUAL    = 30 
    TK_ABRCOLCHETE   = 31
    TK_FCHCOLCHETE   = 32
    TK_VIRGULA       = 33
    
    def __init__(self, tipo: int, texto: str, linha: int):
        self.tipo = tipo
        self.texto = texto
        self.linha = linha
        self.declaracao = 0
        
    def getTipo(self):
        return self.tipo

    def setTipo(self, tipo):
        self.tipo = tipo
        
    def getLinha(self):
        return self.linha

    def setLinha(self, linha):
        self.linha = linha
    
    def getTexto(self):
        return self.texto
       
    def setTexto(self, texto):
        self.texto = texto
        
    def __str__(self):
        return "Token [tipo: " + str(self.tipo) + ", conteudo: " + self.texto + ", linha: " + str(self.linha) + "]"