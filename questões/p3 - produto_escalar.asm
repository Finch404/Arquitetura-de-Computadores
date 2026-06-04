     goto main
     wb 0
res  ww 0
a    ww 134480385
b    ww 33686018
a0   ww 0
b0   ww 0
a1   ww 0
b1   ww 0
a2   ww 0
b2   ww 0
a3   ww 0
b3   ww 0

main getb a 0
     mov x a0
     getb a 1
     mov x a1
     getb a 2
     mov x a2
     getb a 3
     mov x a3

     getb b 0
     mov x b0
     getb b 1
     mov x b1
     getb b 2
     mov x b2
     getb b 3
     mov x b3

     mmov a0 x
mul0 jz x set1
     madd res b0
     dec x
     goto mul0

set1 mmov a1 x
mul1 jz x set2
     madd res b1
     dec x
     goto mul1

set2 mmov a2 x
mul2 jz x set3
     madd res b2
     dec x
     goto mul2

set3 mmov a3 x
mul3 jz x fim
     madd res b3
     dec x
     goto mul3

fim  halt