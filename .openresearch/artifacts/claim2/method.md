# Claim 2 method

The primary checker performs integer-exact resource accounting at
power-of-two boundaries and very large `n`. A separately implemented checker
exhausts every integer `n` from 2 through 8192. Both derive the minimal address
width, multiplexor sum, parameter count, and constructive depth without curve
fitting. Deliberately weakened width, depth, and layer-count constructions
must be rejected.
