# Train an AI bot to play Flappy Bird

In this project, I have re-created the simple single player game Flappy bird from scratch. In the original game the main aim is to pass as many pipes as possible by jumping/flying the bird. 

The user tries to understand the dynamics by trial to see how large the birds jump and how fast it drops if stopped flapping. In this project, instead of user input, I utilized NEAT package to create many birds to learn the dynamics of the game with genetic algorithm, where each genetic iteration the bird reaches farther. 

\bin:
  * - Bird, pipe and base classes to create different parts of the game
  * - Constants: The constants and images used in the game
  * -  Utils: The functions that are utilized for the implementation of the game

- config.txt : Configuration file for the NEAT package
- environment.yml : Package versions used in the conda environment
- main.py : The main function to run once the repo is cloned to train the AI
- all_in_one.py: Since this is a relatively small project, everything is combined into a single python file for interested parties. 
