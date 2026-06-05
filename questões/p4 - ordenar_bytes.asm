     goto main
     wb 0
res  ww 0
a    ww 0
v0   ww 0
v1   ww 0
v2   ww 0
v3   ww 0
p    ww 0
q    ww 0

main getb a 0
     mov x v0
     getb a 1
     mov x v1
     getb a 2
     mov x v2
     getb a 3
     mov x v3

     mmov v0 p
     mmov v1 q
     goto c1
e1   mmov v2 p
     mmov v3 q
     goto c2
e2   mmov v0 p
     mmov v2 q
     goto c3
e3   mmov v1 p
     mmov v3 q
     goto c4
e4   mmov v1 p
     mmov v2 q
     goto c5
e5   zera res
     mmov v0 res
     sl8 res
     madd res v1
     sl8 res
     madd res v2
     sl8 res
     madd res v3
     halt

c1   mjz p pz1
     mjz q qz1
     dec p
     dec q
     goto c1
pz1  goto e1
qz1  mmov v0 y
     mmov v1 v0
     mov y v1
     goto e1

c2   mjz p pz2
     mjz q qz2
     dec p
     dec q
     goto c2
pz2  goto e2
qz2  mmov v2 y
     mmov v3 v2
     mov y v3
     goto e2

c3   mjz p pz3
     mjz q qz3
     dec p
     dec q
     goto c3
pz3  goto e3
qz3  mmov v0 y
     mmov v2 v0
     mov y v2
     goto e3

c4   mjz p pz4
     mjz q qz4
     dec p
     dec q
     goto c4
pz4  goto e4
qz4  mmov v1 y
     mmov v3 v1
     mov y v3
     goto e4

c5   mjz p pz5
     mjz q qz5
     dec p
     dec q
     goto c5
pz5  goto e5
qz5  mmov v1 y
     mmov v2 v1
     mov y v2
     goto e5
