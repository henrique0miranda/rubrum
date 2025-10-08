# Linguagem 

A linguagem de programação Rubrum utiliza o idioma latim como base para as palavras reservada.
Para iniciar um programa na linguagem Rubrum, é necessário adicionar a palavra-chave STATUS e em seguida parênteses. Dentro deles, todo o escopo do
código será descrito. Os comentários podem ser adicionados utilizando o símbolo “!” no início da frase.

## Tokens

MAIN       -> SATUS '(' DECLARA BLOCO ')' \
DECLARA    -> VAR DECLARA | ε \
VAR        -> TYPE ID (, ID)* '|' | TYPE ATR \
TYPE       -> LITTERAE | NUMERUS \
ATR        -> ID = (TEXTO | EXP) '|' \
BLOCO      -> CMD BLOCO | ε \
CMD        -> IN | OUT | LOOP | IF | EXP | ATR \
IN         -> LEGERE [ ID ] '|' \
OUT        -> SCRIBERE [ ID | TEXTO ] '|' | REDITUS [ ID ] '|' \
LOOP       -> DUM [ EXP OP EXP | BOOL ] '(' BLOCO ')' \
IF         -> SI [ EXP OP EXP ] '(' BLOCO ')' ( ALIUD BLOCO )? \
OP         -> LOGICO | ARITMETICO | RELACIONAL\
LOGICO     -> AUT | ET | NO \
ARITMETICO -> N0 | N1 \
N0         -> - | + \
N1         -> * | / \
RELACIONAL -> > | < | >= | <= \
EXP        -> TERM EXP' \
EXP'       -> N0 EXP | ε \
TERM       -> FATOR TERM' \
TERM'      -> N1 TERM | ε \
FATOR      -> NUMERO | ID | '(' EXP ')' \
TEXTO      -> " (LETRA | NUMERO)* " \
LETRA      -> (a..z | A..Z)* \
ID         -> (a..z)(A..Z | a..z | 0..9)* \
NUMERO     -> (0..9)+ \ 
BOOL       -> VERUM | FALSUS  \

ESPECIFICAÇÕES 

V NÃO DECLARAR DUAS VARIAVEIS COM O MESMO ID \
V DECLARAR ANTES DE USAR  \
V CHAR NÃO RECEBE NUM E NUM NÃO RECEBE CHAR NA DECLARACAO \
