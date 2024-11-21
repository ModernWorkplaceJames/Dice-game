import random
from colorama import Fore, Style, init

# Initialize colorama for colored text output
init(autoreset=True)

# Constants for dice
D6 = ["Attack", "Attack", "Attack", "Shield", "Heal", "Blank"]

# Function to roll a die
def roll_dice(dice_faces):
    return random.choice(dice_faces)

# Function to roll multiple dice
def roll_multiple_dice(num_dice, dice_faces):
    return [roll_dice(dice_faces) for _ in range(num_dice)]

# Function to apply dice effects
def apply_dice_effects(dice):
    """
    Process the effects of a list of dice rolls and return the summary of effects.
    """
    total_damage = 0
    total_heal = 0
    effects_summary = []  # Keeps track of effects for future logs or updates

    for roll in dice:
        if roll == "Attack":
            damage = random.randint(1, 6)
            total_damage += damage
            effects_summary.append(Fore.RED + f"Attack! Dealt {damage} damage.")
        elif roll == "Heal":
            heal = random.randint(1, 6)
            total_heal += heal
            effects_summary.append(Fore.GREEN + f"Heal! Restored {heal} HP.")
        elif roll == "Shield":
            # Placeholder for shield logic
            effects_summary.append(Fore.CYAN + "Shield gained! (not implemented yet)")
        else:
            effects_summary.append(Fore.YELLOW + "Blank roll. Nothing happened.")

    return total_damage, total_heal, effects_summary

# Player's turn
def player_turn(num_dice=3, reroll_limit=3):
    """
    Executes the player's turn with a set number of dice and rerolls.
    """
    print(Fore.BLUE + "\n--- Player's Turn ---")

    # Roll initial dice
    dice = roll_multiple_dice(num_dice, D6)
    print(Fore.BLUE + f"Initial roll: {dice}")

    rerolls = reroll_limit

    while rerolls > 0:
        # Ask the player which dice to keep
        keep = input(Fore.YELLOW + f"Enter dice to keep (e.g., 0,2) or press Enter to reroll all: ").strip()
        if keep:
            keep_indices = [int(i) for i in keep.split(",") if i.isdigit()]
            new_dice = []
            for i in range(num_dice):
                if i in keep_indices:
                    new_dice.append(dice[i])  # Keep selected dice
                else:
                    new_dice.append(roll_dice(D6))  # Reroll the others
            dice = new_dice
            rerolls -= 1
            print(Fore.BLUE + f"New roll: {dice} | {rerolls} rerolls left")
        else:
            # Reroll all dice
            dice = roll_multiple_dice(num_dice, D6)
            rerolls -= 1
            print(Fore.BLUE + f"New roll: {dice} | {rerolls} rerolls left")

        # Ask if the player is satisfied with the roll
        satisfied = input(Fore.YELLOW + "Are you satisfied with your roll? (yes/no): ").strip().lower()
        if satisfied == "yes":
            break

    # Apply effects of the final dice roll
    total_damage, total_heal, effects_summary = apply_dice_effects(dice)
    for effect in effects_summary:
        print(effect)
    print(Fore.MAGENTA + f"\nTurn Summary: Total Damage = {total_damage}, Total Heal = {total_heal}")

# Main function
def main():
    """
    Entry point for the game.
    """
    print(Fore.YELLOW + "Welcome to the Dice Game!")
    player_turn()

# Run the game
if __name__ == "__main__":
    main()
