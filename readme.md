# Lotro Bot V2

---
Lord of the Rings Online is an online MMORPG game that this bot aims to automate.

## Get Started

---

### Usage

For the time being, run main.py.

### Pre-Requisites

The following are pre-requisites this program needs to run:

- Python version 3.9 or higher
- pip
- opencv-python
- numpy

## Dev Notes

---

### Game & Bot Summary

The game this bot will automate is an MMORPG. The goal of the game is to reach endgame (level 130). That will be the
sole mission of this bot

Here are a few of the ways this is currently done:

- Questing
- Farming monsters
- Crafting
- etc.

Our focus is 'Crafting'... more specifically, cooking and farming. In the next
section, we will describe the main features of the game we leverage.

### Game Components

Leveraging the following components in our bot:

- Mini-map
- Full map
- Crafting panel
- Vendor
- Crafting facilities
- Vault

```
-lotro-bot-v2
    - bots
        - movement bot
            - controller.py
            - service.py
        - logging bot
            - controller.py
            - service.py
        - config
        - ai bot
        - mini-map bot
    - data
        - 
```
