from lcapy import Iac, R, L, C

net = Iac('Is') | (R('R') + (L('L') | C('C')))
net.draw()
