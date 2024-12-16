## Assassin's Creed 2 Memory Modifier

A Python script that allows you to modify various aspects of the game Assassin's Creed 2 in real-time by manipulating the memory. 

The main features include enabling God Mode, modifying the player's money value, and more. 

This script interacts with the game's memory using pymem to read and write values such as health and money.

# Features

- God Mode: Automatically restores the player's health to a specified value, making them invincible.
- Money Modifier: Modify the player's money value in real-time during gameplay.
# Requirements

```
Python 3.x
pymem: Python library to interact with the memory of running processes.
Assassin's Creed II running on your PC.
```
```pip install pymem```

## How It Works

This script utilizes memory manipulation techniques to modify the player's health and money values in *Assassin's Creed 2*. The process of finding the correct memory addresses and offsets involves scanning the game's memory, modifying in-game values, and performing iterative pointer scans. Here's how it works:

### Finding Pointers and Offsets

1. **Health Value**:
   - Since the exact address of the player's health is unknown, we begin by performing an "unknown initial value" scan.
   - To locate the health address, you need to take damage or heal in the game and scan for the corresponding changes in value. 
   - Continue scanning for increased or decreased values as you modify the health in-game until you identify the correct memory location.
   - The health value is typically stored as a 4-byte integer, and a common starting value is 20.

2. **Money Value**:
   - Finding the money pointer is simpler. You can loot, spend, or pickpocket in the game, and then perform a memory scan to detect changes in the amount of money you have (also stored as a 4-byte integer).
   - Scan before and after performing an action that affects the money value to locate the correct memory address.

3. **Generating Stable Pointers**:
   - Once you find the memory addresses for health and money, it's important to generate a pointer map.
   - Restart the game and repeat the scanning process to ensure the addresses remain the same.
   - Perform this process 2-3 times to find consistent memory addresses.
   - After identifying stable addresses, conduct a final pointer scan to ensure the memory addresses are reliable and persistent across different game sessions.
  
# Enabling God Mode

- The script continuously checks and updates the player's health to 20 (or any specified value), ensuring the player remains invincible. The God Mode is toggled on and off via the menu system.

# Memory Manipulation

- Reading values: The script uses pm.read_int() and pm.read_uint() to read integers from specific memory addresses.

- Writing values: To change the money or health values, the script uses pm.write_int() to overwrite values at the target memory addresses.
