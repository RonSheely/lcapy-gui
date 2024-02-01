# Created by lcapy-tk V0.94.dev0
; nodes={1@(11, 5), 0@(3, 2), 4@(6, 4), 3@(6, 6), 5@(3, 6), 6@(6, 8), 7@(11, 8), 9@(13, 2), 8@(13, 5), 10@(6, 2), 11@(3, 2)}
E1 1 0 opamp 4 3 A 0 0; right, mirror
R1 3 5; left=1.5
W1 3 6; up
R2 6 7; right=2.5
W2 7 1; down=1.5
W4 9 0; down=0, sground
W3 1 8; right
P1 8 9; down=1.5, v=V_o
W5 10 4; up
W6 10 0; down=0, sground
V1 5 11; down=2
W7 11 0; down=0, sground
; draw_nodes=connections, label_nodes=all, style=american, voltage_dir=RP, label_style=value
