1. Highlight selected component ?

2. Add misc operations: poles, zeros, etc.

3. Show current through component.  For wires this is tricky and will
require some Lcapy magic.  Need to sum all the currents coming into
the branch node.  This requires recursion if connected to other wires.
Stop if reach one of the branch nodes

4. Redo...

5. Move components

6. Rotate components?  Perhaps just delete and re-enter but lose
attributes unless clever

7. Configuration file

8. User levels to hide many options

9. Add numerical analysis

10. Add node in middle of wire?   Need to delete wire or split into two.

11. Draw nodes after drawing cpts (for port nodes)

12. Close/quit

13. Add labels, voltage labels, current labels to cpt attributes

14. Connect opamp negative output node to ground

15. Name opamps E1, E2, etc

17. Make Lcapy more robust to nodes being changed when node positions
    are defined

18. Improve opamp label placement

19. Add frequency and phase to AC sources

20. Fill open nodes so not transparent to wire underneath

21. Fix Lcapy to simplify condition expression for t >= 0

22. Reposition component labels to match circuitikz

23. Fix fullscreen

24. Fix transistor menagerie if base/gate offset

25. Add transfer function dialog (transimpedance, transadmittance)
