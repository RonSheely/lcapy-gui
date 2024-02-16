% markdown-cleanup-list-numbers

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

7. User levels to hide many options

8. Add numerical analysis

9. Add node in middle of wire?   Need to delete wire or split into two.

10. Draw nodes after drawing cpts (for port nodes)

11. Close/quit

12. Add labels, voltage labels, current labels to cpt attributes

13. Connect opamp negative output node to ground

14. Make Lcapy more robust to nodes being changed when node positions
    are defined

15. Add frequency and phase to AC sources

16. Fill open nodes so not transparent to wire underneath

17. Fix Lcapy to simplify condition expression for t >= 0

18. Reposition component labels to match circuitikz

19. Fix fullscreen

20. Fix transistor menagerie if base/gate offset

21. Add voltage, current, and flow labels

22. Add generic labels

23. Use suffixes for component values (u, p, M, etc)

24. Handle exception when creating circuitiz image

25. Fix circuitikz image creation to use node positions

26. Fix invert for opamp

27. Add label position modifiers

28. Add U components

29. Check if opamp has node 0 as output reference and warn if have no
    other node 0.

30. Add mutual inductance (could associate with a transformer but
    would need to output two inductors and a mutual inductance; this
    will be hard to interpret).  Probably need to modify TF in Lcapy
    to have arguments for the two self-inductances and the coupling
    coefficient.  In the interim, have a coupling dialog (edit/couplings)
    that specifies the couplings, e.g., `L1 L2 1`.

31. Remove opts field from components

32. Better labels for transformers (show turns ratio)

33. History of operations (perhaps convert to Python script)

34. Show symbol pins for debugging

35. Add network synthesis

36. Stretch transformer

37. Tooltips for menu items

38. Fix selection of connections that are smaller than the grid

39. Add multiple component select

40. Expand grid

41. Rejoin nodes after moves
