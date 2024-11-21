import random
from colorama import Fore, Style, init
import sys

# Initialize colorama for colored text output
init(autoreset=True)

# Constants for die faces
ATTACK = "Attack"
HEAL = "Heal"
SHIELD = "Shield"
BLANK = "Blank"

# Die Class
class Die:
    def __init__(self, sides=6, faces=None):
        """
        Initialize a die with a given number of sides.
        If faces are provided, use them; otherwise, generate numerical faces.
        """
        self.sides = sides
        if faces is not None:
            if len(faces) != sides:
                raise ValueError("Number of faces provided does not match the number of sides.")
            self.faces = faces
        else:
            # Generate numerical faces starting from 1
            self.faces = list(range(1, sides + 1))

    def roll(self):
        return random.choice(self.faces)

# Player Class
class Player:
    def __init__(self, name, health=20, max_health=20):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.shield = 0

    def apply_damage(self, damage):
        """
        Applies damage to the player, considering the shield.
        Returns the amount of damage blocked.
        """
        blocked = 0
        if self.shield > 0:
            blocked = min(self.shield, damage)
            self.shield -= blocked
            damage -= blocked
        self.health = max(self.health - damage, 0)
        return blocked

    def add_health(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def add_shield(self, amount):
        self.shield += amount

# Game Class
class Game:
    def __init__(self):
        # Define available dice (similar to D&D dice)
        self.available_dice = {
            'd4': Die(sides=4),
            'd6': Die(sides=6),
            'd8': Die(sides=8),
            'd10': Die(sides=10),
            'd12': Die(sides=12),
            'd20': Die(sides=20),
            # You can customize dice with special faces if desired
            # 'custom_d8': Die(sides=8, faces=[1, 2, 3, 4, HEAL, SHIELD, ATTACK, BLANK]),
        }
        # Initialize player and AI with default health
        self.player = Player("Player")
        self.ai = Player("AI")
        # Player and AI dice inventories
        self.player_dice = []
        self.ai_dice = []
        # Start the dice selection phase
        self.dice_selection_phase()

    def dice_selection_phase(self):
        """
        Allows the player and AI to select their dice at the start of the game.
        """
        print(Fore.YELLOW + "\n--- Dice Selection Phase ---")
        print("You can choose 3 dice for your inventory.")
        print("Available dice:")
        for key in self.available_dice:
            print(f"- {key}")

        # Let the player choose their dice
        for i in range(3):
            while True:
                chosen_die = input(Fore.YELLOW + f"Choose die {i + 1}: ").strip().lower()
                if chosen_die in self.available_dice:
                    self.player_dice.append(self.available_dice[chosen_die])
                    break
                else:
                    print(Fore.RED + "Invalid die selection. Please choose from the available dice.")

        # For simplicity, AI selects dice randomly
        self.ai_dice = random.choices(list(self.available_dice.values()), k=3)
        print(Fore.RED + "\nAI has selected its dice.")

    def roll_multiple_dice(self, dice_list):
        """
        Rolls a list of dice and returns a list of roll results with indices.
        """
        return [{"index": i + 1, "face": die.roll(), "die": die} for i, die in enumerate(dice_list)]

    def display_dice(self, dice):
        """
        Displays the rolled dice faces with their indices.
        """
        display = ", ".join([f"[{die['index']}] {die['face']}" for die in dice])
        print(Fore.BLUE + f"Dice: {display}")

    def apply_dice_effects(self, dice, user, opponent):
        """
        Processes the effects of a list of dice rolls and updates user/opponent stats.
        """
        effects_summary = []

        for die_info in dice:
            roll = die_info["face"]
            die = die_info["die"]
            # Check if roll is a special face or a number
            if isinstance(roll, str):
                if roll == ATTACK:
                    damage = random.randint(1, die.sides)
                    blocked = opponent.apply_damage(damage)
                    effects_summary.append(
                        Fore.RED + f"Attack! Dealt {damage} damage. Blocked: {blocked}."
                    )
                elif roll == HEAL:
                    heal = random.randint(1, die.sides)
                    user.add_health(heal)
                    effects_summary.append(Fore.GREEN + f"Heal! Restored {heal} HP.")
                elif roll == SHIELD:
                    shield = random.randint(1, die.sides // 2)
                    user.add_shield(shield)
                    effects_summary.append(Fore.CYAN + f"Shield gained! Added {shield} shield.")
                elif roll == BLANK:
                    effects_summary.append(Fore.YELLOW + "Blank roll. Nothing happened.")
                else:
                    # Handle any other special faces
                    pass
            elif isinstance(roll, int):
                # Treat numerical rolls as damage
                damage = roll
                blocked = opponent.apply_damage(damage)
                effects_summary.append(
                    Fore.RED + f"Attack! Rolled {roll}. Blocked: {blocked}. Damage dealt: {damage - blocked}."
                )
            else:
                # Handle unexpected roll types
                pass

        return effects_summary

    def player_turn(self, reroll_limit=3):
        """
        Executes the player's turn using their selected dice and rerolls.
        """
        print(Fore.BLUE + "\n--- Player's Turn ---")
        # Roll initial dice from the player's inventory
        dice = self.roll_multiple_dice(self.player_dice)
        self.display_dice(dice)

        rerolls = reroll_limit

        while rerolls > 0:
            # Prompt the player
            reroll_input = input(
                Fore.YELLOW + f"Enter the indices of dice to reroll (e.g., 1,3), press Enter to keep all, or type 'q' to quit: "
            ).strip().lower()

            if reroll_input == 'q':
                print(Fore.RED + "Game terminated by user.")
                sys.exit()
            elif reroll_input == '':
                # Keep all current dice
                break
            else:
                # Parse and validate indices to reroll
                try:
                    reroll_indices = {int(i) for i in reroll_input.split(",") if i.isdigit()}
                    if any(i < 1 or i > len(dice) for i in reroll_indices):
                        print(Fore.RED + "Invalid indices. Please enter valid indices separated by commas.")
                        continue
                except ValueError:
                    print(Fore.RED + "Invalid input. Please enter valid indices separated by commas.")
                    continue

                # Reroll selected dice
                for die_info in dice:
                    if die_info["index"] in reroll_indices:
                        die_info["face"] = die_info["die"].roll()
                rerolls -= 1
                self.display_dice(dice)
                print(Fore.BLUE + f"Rerolls left: {rerolls}")

        # Apply effects of the final dice roll
        effects_summary = self.apply_dice_effects(dice, self.player, self.ai)
        for effect in effects_summary:
            print(effect)

    def ai_turn(self, reroll_limit=3):
        """
        Executes the AI's turn using its selected dice.
        """
        print(Fore.RED + "\n--- AI's Turn ---")
        # Roll initial dice from the AI's inventory
        dice = self.roll_multiple_dice(self.ai_dice)
        print(Fore.RED + f"AI's initial roll:")
        self.display_dice(dice)

        rerolls = reroll_limit

        # AI's strategy: reroll blanks or low numbers
        while rerolls > 0:
            rerolled = False
            for die_info in dice:
                face = die_info["face"]
                die = die_info["die"]
                if isinstance(face, str) and face == BLANK:
                    die_info["face"] = die.roll()
                    rerolled = True
                elif isinstance(face, int) and face < die.sides // 2:
                    # Reroll low numerical rolls
                    die_info["face"] = die.roll()
                    rerolled = True

            if not rerolled:
                break  # Exit if no rerolls were made
            rerolls -= 1

        print(Fore.RED + f"AI's final roll:")
        self.display_dice(dice)

        # Apply effects of the final dice roll
        effects_summary = self.apply_dice_effects(dice, self.ai, self.player)
        for effect in effects_summary:
            print(effect)

    def game_loop(self):
        """
        Main game loop for player vs AI combat.
        """
        turn = 1
        while self.player.health > 0 and self.ai.health > 0:
            print(Fore.MAGENTA + f"\n=== Turn {turn} ===")
            print(Fore.CYAN + f"Player: Health = {self.player.health}, Shield = {self.player.shield}")
            print(Fore.RED + f"AI: Health = {self.ai.health}, Shield = {self.ai.shield}")
            
            # Player's turn
            self.player_turn()

            # Check if AI is defeated
            if self.ai.health <= 0:
                print(Fore.GREEN + "\nYou win!")
                break

            # AI's turn
            self.ai_turn()

            # Check if Player is defeated
            if self.player.health <= 0:
                print(Fore.RED + "\nThe AI wins!")
                break

            turn += 1

# Main function
if __name__ == "__main__":
    print(Fore.YELLOW + "Welcome to the Dice RPG Game!")
    game = Game()
    game.game_loop()
