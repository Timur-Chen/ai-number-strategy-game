# AI Number Strategy Game

A Python-based strategy game where a human player competes against an AI opponent.

The AI uses classical **Artificial Intelligence search algorithms** such as **Minimax** and **Alpha-Beta pruning** to determine the optimal move.

This project demonstrates how **game trees** and **heuristic evaluation functions** can be used to build intelligent decision-making systems.

---

# Project Overview

This game starts with a number between **20 and 30**.

Players take turns multiplying the current number by:

- ×3
- ×4
- ×5

The objective is to reach **3000 or more**.

Each move affects the score depending on whether the number is **even or odd**, and additional **bank points** may be collected.

The computer player uses AI algorithms to analyze possible future states and choose the best move.

---

# AI Algorithms Used

This project implements two classical AI algorithms:

## Minimax Algorithm
The Minimax algorithm simulates all possible moves and assumes that the opponent will always play optimally.

It evaluates the game tree and chooses the move that maximizes the player's chances of winning.

## Alpha-Beta Pruning
Alpha-Beta pruning is an optimized version of Minimax.

It eliminates branches in the game tree that cannot affect the final decision, allowing the AI to search deeper and faster.

---

# Game Tree Search

The AI builds a **game tree** where each node represents a game state.

Example:

Start: 25

25  
├── 75 (×3)  
├── 100 (×4)  
└── 125 (×5)

Each branch represents a possible move.  
The AI explores these branches up to a selected **search depth**.

---

# Game Features

✔ Human vs Computer gameplay  
✔ Tkinter graphical user interface  
✔ Adjustable AI search depth  
✔ Minimax algorithm implementation  
✔ Alpha-Beta pruning optimization  
✔ Move history tracking  
✔ Game tree visualization  
✔ AI statistics (nodes visited, computation time)

---

# User Interface

The game is built using **Tkinter**, Python’s standard GUI toolkit.

The interface includes:

- Player selection (Human or Computer starts)
- Algorithm selection (Minimax / Alpha-Beta)
- Adjustable search depth
- Start number input
- Move buttons (×3, ×4, ×5)
- Move history log
- Game statistics display

---

# Technologies Used

This project was built using:

- Python
- Tkinter
- Game Tree Search
- Minimax Algorithm
- Alpha-Beta Pruning
- Object-Oriented Programming

---

# How to Run the Project

Clone the repository:

```bash
git clone https://github.com/Timur-Chen/ai-number-strategy-game.git
```
---
# Navigate to the project folder:

```bash
cd ai-number-strategy-game
```

# Run the game:

```bash
python main.py
```