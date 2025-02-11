# Trabalho prático de Compiladores
# {
#   Julia Gabriella Corrêa Silva
#   Johnattan Silva Ferreira
#   Henrique Araujo Miranda
# }

from AnaliseLexica import AnalisadorLexico
from AnaliseSintatica_Semantica import AnalisadorSintatico

scanner = AnalisadorLexico("input.txt")
parser = AnalisadorSintatico(scanner)
parser.MAIN()