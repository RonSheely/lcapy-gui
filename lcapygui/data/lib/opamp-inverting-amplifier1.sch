# Created by lcapy-tk V0.6.dev0
; nodes={1@(15, 11), 0@(0, 0), 4@(10, 10), 3@(10, 12), 5@(7, 12), 6@(10, 14), 7@(15, 14), 9@(17, 8), 8@(17, 11), 10@(10, 8), 11@(7, 8)}
E1 1 0 opamp 4 3 E1 0 0; right=2.5, mirror
R1 3 5; left=1.5
W1 3 6; up
R2 6 7; right=2.5
W2 7 1; down=1.5
W4 9 0; down=0, sground
W3 1 8; right
P1 8 9; down=1.5
W5 10 4; up
W6 10 0; down=0, sground
V1 5 11; down=2
W7 11 0; down=0, sground
; draw_nodes=connections, label_nodes=all, style=american, voltage_dir=RP, label_ids=false, label_values=true
