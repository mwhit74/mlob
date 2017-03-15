
This program calculates the shear and moment induced in a simply supported beam
with a constant moment of area (moment of inertia) along the span length. Each
axle is placed at each node (critial section) and the location of the other axles
is calculated. The shear on each side of the node is calculated and the moment at each node is
calculated. 

By placing the axle at each node it ensures that the maximum forces are
calculated at those nodes. 

This program uses a functional porgramming paradigm approach. 

The program in this branch is incomplete. The program was started by
incrementally stepping the axles across the span and calculating for each step
the shear and moment at each node. 

This approach does not ensure that the maximum forces are calculated. It can be
overcome by decreaing the increment such that the axle step is refined enough to
ensure an accurate calculation. 

This code was saved because it is a valid approach if it is executed properly
and may be useful in the future.
