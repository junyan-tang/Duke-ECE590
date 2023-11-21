For each problem, solve it first without dynamic programming, measure the per-formance, then add dynamic programming (this should not 
require a major code rewrite—if you followed my advice, it is adding/removing @cache), then measure the performance with dynamic programming.

1. For your first problem, there is a dragon in a magical treasure vault that is laid out like a grid. 
The dragon enters the vault at the south eastern corner and can only move North or West from any given room. The dragon may never go South nor East (because of the magic of the vault). Once the dragon leave the vault, she may not return. Each room in the vault contains an integer number of gold coins.
The dragon is aware of the number of gold coins in each room before she starts her journey.

2.  For this problem, you are going to select the order in which you perform matrix multiplications to reduce the total number of
operations (in mat.py). Recall that multiplying an NxM matrix by an MxR matrix results in an NxR matrix. Doing this multiplication takes O(NMR) work—which we will just call N*M*R operations.
As matrix multiplication is associative, you can choose the order in which you multiply the matrices.

3. This problem will work with binary search trees (in tree.py). If you aren’t familiar with binary search tress, you will learn a LOT more about them in 551 soon. However, for what we are going to do here, you only need to know a few things.
A binary search tree is a way to store and retrieve data. It is based on the idea that “everything larger goes right and everything smaller goes left”. This property means that when searching for
a particular item, the algorithm can choose the right direction, ideally discarding half the tree at once. In the general case (which is what we will cover in 551), we want our tree to be nicely balanced like the one shown, as that minimizes the average search time for an arbitrary element. However, if we knew a priori that certain elements would be searched with much higher probability than others, we would want a different arrangement.
