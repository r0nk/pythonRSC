JMP start

; Variables

var1: BE
var2: 9E
somevariable32: 3E

start:
    LDAC var1 ;a stored variable
    MOVAC
    LDAC var2
    ADD
    OUT

    HALT