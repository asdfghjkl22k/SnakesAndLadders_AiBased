# 🎲 AI-Enhanced Snakes and Ladders

A modern twist on the classic Snakes and Ladders game — now featuring AI, dynamic storytelling, power-ups, sound effects, and more!

https://github.com/user-attachments/assets/bb1d6288-ac1e-49b5-856f-bc5bdbcb7f8a

## 📄 Project Report

📥 [Download Project Report](https://docs.google.com/document/d/1fuR7QJ8ziTzRAgGvOQPcMSSUF33P8HKgX1A8F6pcf0w/edit?usp=sharing)


---
## 📌 Features

- 🤖 Human vs AI gameplay
- 🐍 Dynamically regenerating snakes and ladders every 3 turns
- ⚡ Power-Ups: "Boost" and "Challenge" tiles
- 📜 NLP-style storytelling log with scrollable UI
- 🔊 Real-time sound effects (dice roll, snake, ladder, win)
- 🧠 Simple rule-based AI logic with responsive animations
- 🎨 Smooth token movement animation

---

## 🎮 How to Play

- Press **Spacebar** to roll the dice on your turn.
- Watch the AI automatically play its move.
- Land on:
  - 🐍 Snake: Slide down.
  - 🪜 Ladder: Climb up.
  - ⚡ Power-Up: Trigger boost or quiz challenge.

---

## 📂 Folder Structure
SnakesAndLadders_AiBased/
├── game/
│ ├── board.py
│ ├── dice.py
│ ├── player.py
│ ├── ai_agent.py
│ └── init.py
├── sounds/
│ ├── dice_roll.wav
│ ├── snake.wav
│ ├── ladder.wav
│ └── win.wav
├── assets/
│ └── dice_faces/ (images 1.png to 6.png)
├── main.py
└── README.md

---

## 🚀 Getting Started

### 🔧 Requirements
- Python 3.11+
- [Pygame](https://www.pygame.org/)

### 📦 Installation
```bash
git clone https://github.com/your-username/snakes-and-ladders-ai.git
cd snakes-and-ladders-ai
pip install pygame
python main.py

