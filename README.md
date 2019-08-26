# Robot Motion Planning Project

### Table of Contents
1. [Installation](#installation)
2. [File Structure](#file-structure)
3. [Project Motivation](#project-motivation)
4. [Project Details](#project-details)
5. [Licensing](#licensing)

## Installation
The project uses Python version 2.7.16 and numpy library.

To run the tester, use the following command: 
`python tester.py test_maze_01.txt`

And to run the maze visualization use this command:
`python showmaze.py test_maze_01.txt`
The script uses the turtle module to visualize the maze. You can click on the window with the visualization after drawing is complete to close the window.

## File Structure
The project contains these files:

    robot.py - This script establishes the robot class.                       
    maze.py - This script contains functions for constructing the maze and for checking for walls upon robot movement or sensing.
    tester.py - This script will be run to test the robot’s ability to navigate mazes.
    showmaze.py - This script can be used to create a visual demonstration of what a maze looks like.
    test_maze_##.txt - These files provide three sample mazes upon which to test your robot.
    free_form_maze.txt - This file has an additional maze used for evaluation purpose.

## Project Motivation
Navigation is a major task for mobile robots. In real applications, this task can be really complicated with a lot of elements such as obstacle avoidance, object recognition and path planning. Handling all of these tasks at once is quite tough. In this project, we only deal with finding the optimum path which could be integrated later with a more complex project.    

## Project Details
I encourge you to read this article for more details about the project: https://medium.com/@yasirghunaim/plot-and-navigate-a-virtual-maze-capstone-project-9c21bb4f2698

## Licensing
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
