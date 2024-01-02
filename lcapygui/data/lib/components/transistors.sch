# Created by lcapy-tk V0.94.dev0
; nodes={1@(1.5, 8), 2@(0.41, 7), 3@(1.5, 6), 4@(3.5, 8), 5@(2.41, 7), 6@(3.5, 6), 7@(5.5, 8), 8@(4.39, 7), 9@(5.5, 6), 10@(7.5, 8), 11@(6.39, 7), 12@(7.5, 6), 13@(9.5, 8), 14@(8.39, 7), 15@(9.5, 6), 16@(11.5, 8), 17@(10.39, 7), 18@(11.5, 6), 19@(0.4, 4.71), 20@(1.5, 4), 21@(2.4, 4.71), 22@(3.5, 4), 23@(8.39, 5), 24@(9.5, 4), 25@(4.39, 5), 26@(5.5, 4), 27@(6.39, 5), 28@(7.5, 4), 29@(10.39, 5), 30@(11.5, 4)}
Q1 1 2 3 npn; right
Q2 6 5 4 pnp; right
M1 7 8 9 nmos; right, kind=nfet
M2 10 11 12 pmos; right, kind=pfet
M3 13 14 15 nmos; right, kind=nfet-bodydiode
M4 16 17 18 pmos; right, kind=pfet-bodydiode
W1 1 4; right
W2 4 7; right
W3 7 10; right
W4 10 13; right
W5 13 16; right
W6 3 6; right
W7 6 9; right
W8 9 12; right
W9 12 15; right
W10 15 18; right
J1 3 19 20 njf; right
J2 6 21 22 pjf; right
W11 20 22; right
M5 9 25 26 nmos; right, kind=nigfete
M6 12 27 28 pmos; right, kind=pigfete
M7 15 23 24 nmos; right, kind=nigfete-bodydiode
M8 18 29 30 pmos; right, kind=pigfete-bodydiode
W12 22 26; right
W13 26 28; right
W14 28 24; right
W15 24 30; right
; draw_nodes=connections, label_nodes=none, style=american, voltage_dir=RP, label_style=split
