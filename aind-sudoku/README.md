# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: Constraint Propagation is all about using local constraints in a space (in the case of Sudoku, the constraints of each square) to dramatically reduce the search space. As we enforce each constraint, it introduces new constraints for other parts of the board that help us further reduce the number of possibilities. The Naked Twins problem is when there are exactly two boxes in the same row or same column or same sub square units which permit the same two digits like say '23'.
When 2 boxes in the same row or column or same square_units permit only the same 2 digits that means those 2 digits are locked in those 2 boxes. We do not know which box contains a "2" and which one contains "3". But one thing we know for sure that no other boxes in the same row, column or sqaure_units can contain those 2 digits. So we iterate over all the boxes in the same unit and eliminate those 2 digits from their possible values.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A:  A regular sudoku consists of a 9x9 grid, and the objective is to fill the grid with digits in such a way that each row, each column, and each of the 9 principal 3x3 subsquares contains all of the digits from 1 to 9.In a diagonal sudoku, in addition to all those constraints there is an additional constraint which states that among the two main diagonals, the numbers 1 to 9 should all appear exactly once. So to calculate the peers of a box we need to see the row, column, subsquare and the diagonals which contains the box. Rest is same. First apply Elimination to eliminate values from peers of each box with a single value. Next we apply elimination using Naked Twins strategy and then we finalize all values that are the only choice for a unit. After that we check if the number of solved boxes increases or not. If it increases we continue with the same process until it is stalled or solved.

### Install

This project requires **Python 3**.

We recommend  install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see our visualization. If you've followed our instructions for setting up our conda environment, you should be all set.
If not, please see how to download pygame [here](http://www.pygame.org/download.shtml)

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py
