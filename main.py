import random
from colorama import Fore, Style, init
import sys

# Initialize colorama for colored text output
init(autoreset=True)

# Constants for action types
ATTACK = "Attack"
HEAL = "Heal"
SHIELD = "Shield"
MANA = "Mana"
BLANK = "Blank"

# Constants for spell names
FIREBALL = "Fireball"
HEALING_WAVE = "Healing Wave"
SHIELD_WALL = "Shield Wall"
MANA_SURGE = "Mana Surge"
ESSENCE_DRAIN = "Essence Drain"

# Spell Class
class Spell:
    def __init__(self, name, cost, effect):
        """
        Initialize a spell with a name, mana cost, and effect function.
        """
        self.name = name
        self.cost = cost
        self.effect = effect  # Function to execute the spell's effect

    def cast(self, caster, target):
        """
        Cast the spell, executing its effect.
        """
        return self.effect(caster, target)

# Die Class
class Die:
    def __init__(self, name, sides, faces):
        """
        Initialize a die with a given name, number of sides, and faces.
        Each face is an action type.
        """
        self.name = name
        self.sides = sides
        if len(faces) != sides:
            raise ValueError("Number of faces provided does not match the number of sides.")
        self.faces = faces  # List of action types

    def roll(self):
        return random.choice(self.faces)

# Player Class
class Player:
    def __init__(self, name, health=50, max_health=50):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.shield = 0
        self.mana = 0  # Introduce mana

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

    def add_mana(self, amount):
        self.mana += amount

# Game Class
class Game:
    def __init__(self):
        # Define the dice
        self.available_dice = {
            1: Die(
                name='d4',
                sides=4,
                faces=[ATTACK, ATTACK, HEAL, SHIELD]
            ),
            2: Die(
                name='d6',
                sides=6,
                faces=[ATTACK, ATTACK, HEAL, SHIELD, MANA, BLANK]
            ),
            3: Die(
                name='d8',
                sides=8,
                faces=[ATTACK, ATTACK, ATTACK, HEAL, HEAL, SHIELD, SHIELD, MANA]
            ),
            4: Die(
                name='d10',
                sides=10,
                faces=[ATTACK]*4 + [HEAL]*2 + [SHIELD]*2 + [MANA, BLANK]
            ),
            5: Die(
                name='d12',
                sides=12,
                faces=[ATTACK]*5 + [HEAL]*3 + [SHIELD]*2 + [MANA, BLANK]
            ),
            6: Die(
                name='d20',
                sides=20,
                faces=[ATTACK]*8 + [HEAL]*5 + [SHIELD]*3 + [MANA]*2 + [BLANK]*2
            )
        }
        # Initialize player and AI with default health
        self.player = Player("Player")
        self.ai = Player("AI")
        # Player and AI dice inventories
        self.player_dice = []
        self.ai_dice = []
        # Initialize spells
        self.spells = self.initialize_spells()
        # Start the dice selection phase
        self.dice_selection_phase()

    def initialize_spells(self):
        """
        Initialize the initial set of spells.
        """
        spells = {
            FIREBALL: Spell(FIREBALL, 3, self.spell_fireball),
            HEALING_WAVE: Spell(HEALING_WAVE, 2, self.spell_healing_wave),
            SHIELD_WALL: Spell(SHIELD_WALL, 3, self.spell_shield_wall),
            MANA_SURGE: Spell(MANA_SURGE, 2, self.spell_mana_surge),
            ESSENCE_DRAIN: Spell(ESSENCE_DRAIN, 4, self.spell_essence_drain)
        }
        return spells

    # Spell Effects
    def spell_fireball(self, caster, target):
        """
        Fireball: Deals 8-12 damage to the opponent.
        """
        damage = random.randint(8, 12)
        blocked = target.apply_damage(damage)
        return Fore.RED + f"{caster.name} casts Fireball! Deals {damage} damage. Blocked: {blocked}. Damage Dealt: {damage - blocked}."

    def spell_healing_wave(self, caster, target):
        """
        Healing Wave: Restores 5-10 HP to the caster.
        """
        heal = random.randint(5, 10)
        caster.add_health(heal)
        return Fore.GREEN + f"{caster.name} casts Healing Wave! Restores {heal} HP."

    def spell_shield_wall(self, caster, target):
        """
        Shield Wall: Grants 5-10 shield points to the caster.
        """
        shield = random.randint(5, 10)
        caster.add_shield(shield)
        return Fore.CYAN + f"{caster.name} casts Shield Wall! Gains {shield} shield points."

    def spell_mana_surge(self, caster, target):
        """
        Mana Surge: Grants 3-5 additional mana points to the caster.
        """
        mana = random.randint(3, 5)
        caster.add_mana(mana)
        return Fore.MAGENTA + f"{caster.name} casts Mana Surge! Gains {mana} mana points."

    def spell_essence_drain(self, caster, target):
        """
        Essence Drain: Deals 5-8 damage to the opponent and heals the caster for half the damage dealt.
        """
        damage = random.randint(5, 8)
        blocked = target.apply_damage(damage)
        actual_damage = damage - blocked
        heal = actual_damage // 2
        caster.add_health(heal)
        return Fore.MAGENTA + f"{caster.name} casts Essence Drain! Deals {actual_damage} damage and heals for {heal} HP."

    def dice_selection_phase(self):
        """
        Allows the player and AI to select their dice at the start of the game.
        """
        print(Fore.YELLOW + "\n--- Dice Selection Phase ---")
        print("You can choose 3 dice for your inventory.")
        print("Available dice:")
        for idx, die in self.available_dice.items():
            # Count the number of each action type on the die
            action_counts = {}
            for action in die.faces:
                action_counts[action] = action_counts.get(action, 0) + 1
            # Create a string representation of action counts
            actions_str = ", ".join([f"{action}: {count}" for action, count in action_counts.items()])
            print(f"{idx}. {die.name} (Sides: {die.sides}) - Actions: {actions_str}")

        # Let the player choose their dice
        for i in range(3):
            while True:
                try:
                    choice = int(input(Fore.YELLOW + f"Choose die {i + 1} by number: "))
                    if choice in self.available_dice:
                        self.player_dice.append(self.available_dice[choice])
                        print(Fore.GREEN + f"Added {self.available_dice[choice].name} to your inventory.")
                        break
                    else:
                        print(Fore.RED + "Invalid selection. Please choose a number from the list.")
                except ValueError:
                    print(Fore.RED + "Invalid input. Please enter a number.")

        # AI selects dice randomly
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
        Returns a list of effect summaries.
        """
        effects_summary = []

        for die_info in dice:
            roll = die_info["face"]
            die = die_info["die"]
            sides = die.sides
            # Action values based on die size
            if roll == ATTACK:
                damage = random.randint(1, max(1, sides // 2))
                blocked = opponent.apply_damage(damage)
                effects_summary.append(
                    Fore.RED + f"{user.name} attacks! Deals {damage} damage. Blocked: {blocked}. Damage Dealt: {damage - blocked}."
                )
            elif roll == HEAL:
                heal = random.randint(1, max(1, sides // 3))
                user.add_health(heal)
                effects_summary.append(
                    Fore.GREEN + f"{user.name} heals! Restores {heal} HP."
                )
            elif roll == SHIELD:
                shield = random.randint(1, max(1, sides // 4))
                user.add_shield(shield)
                effects_summary.append(
                    Fore.CYAN + f"{user.name} gains shield! Increases shield by {shield}."
                )
            elif roll == MANA:
                mana = random.randint(1, max(1, sides // 5))
                user.add_mana(mana)
                effects_summary.append(
                    Fore.MAGENTA + f"{user.name} gains mana! Increases mana by {mana}."
                )
            elif roll == BLANK:
                effects_summary.append(Fore.YELLOW + f"{user.name} rolls a Blank. Nothing happens.")
            else:
                # Handle any other special faces
                pass

        return effects_summary

    def player_turn(self, reroll_limit=3):
        """
        Executes the player's turn using their selected dice and rerolls.
        """
        print(Fore.BLUE + f"\n--- {self.player.name}'s Turn ---")
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

        # After dice effects, offer spell casting
        self.cast_spells_phase(self.player, self.ai)

    def ai_turn(self, reroll_limit=3):
        """
        Executes the AI's turn using its selected dice.
        """
        print(Fore.RED + f"\n--- {self.ai.name}'s Turn ---")
        # Roll initial dice from the AI's inventory
        dice = self.roll_multiple_dice(self.ai_dice)
        print(Fore.RED + f"{self.ai.name}'s initial roll:")
        self.display_dice(dice)

        rerolls = reroll_limit

        # AI's strategy: reroll blanks or less useful actions
        while rerolls > 0:
            rerolled = False
            for die_info in dice:
                face = die_info["face"]
                die = die_info["die"]
                # Reroll strategy based on AI's needs
                if face == BLANK:
                    die_info["face"] = die.roll()
                    rerolled = True
                elif face == HEAL and self.ai.health >= self.ai.max_health - 10:
                    die_info["face"] = die.roll()
                    rerolled = True
            if not rerolled:
                break  # Exit if no rerolls were made
            rerolls -= 1

        print(Fore.RED + f"{self.ai.name}'s final roll:")
        self.display_dice(dice)

        # Apply effects of the final dice roll
        effects_summary = self.apply_dice_effects(dice, self.ai, self.player)
        for effect in effects_summary:
            print(effect)

        # AI casts spells if it has enough mana
        self.cast_spells_phase(self.ai, self.player, ai_turn=True)

    def cast_spells_phase(self, caster, target, ai_turn=False):
        """
        Allows the caster to cast spells if they have enough mana.
        For players, prompts for input. For AI, uses strategy.
        """
        if caster.mana < min(spell.cost for spell in self.spells.values()):
            return  # Not enough mana to cast any spell

        if ai_turn:
            # AI spell casting strategy
            # Prioritize offensive spells, then defensive, then utility
            spell_priority = [FIREBALL, ESSENCE_DRAIN, SHIELD_WALL, HEALING_WAVE, MANA_SURGE]
            for spell_name in spell_priority:
                spell = self.spells[spell_name]
                if caster.mana >= spell.cost:
                    # Simple strategy: cast the first spell they can afford
                    caster.mana -= spell.cost
                    effect_message = spell.cast(caster, target)
                    print(effect_message)
                    return  # Cast one spell per turn
        else:
            # Player spell casting
            print(Fore.YELLOW + "\n--- Spell Casting Phase ---")
            available_spells = [spell for spell in self.spells.values() if spell.cost <= caster.mana]
            if not available_spells:
                print(Fore.YELLOW + "No spells available to cast.")
                return

            print("Available Spells:")
            for idx, spell in enumerate(available_spells, 1):
                print(f"{idx}. {spell.name} (Cost: {spell.cost} Mana)")

            print(f"{len(available_spells)+1}. Skip casting")

            while True:
                try:
                    choice = int(input(Fore.YELLOW + "Choose a spell to cast by number: "))
                    if 1 <= choice <= len(available_spells):
                        selected_spell = available_spells[choice - 1]
                        caster.mana -= selected_spell.cost
                        effect_message = selected_spell.cast(caster, target)
                        print(effect_message)
                        break
                    elif choice == len(available_spells) + 1:
                        print(Fore.YELLOW + "Skipping spell casting.")
                        break
                    else:
                        print(Fore.RED + "Invalid selection. Please choose a valid number.")
                except ValueError:
                    print(Fore.RED + "Invalid input. Please enter a number.")

    def game_loop(self):
        """
        Main game loop for player vs AI combat.
        """
        turn = 1
        while self.player.health > 0 and self.ai.health > 0:
            print(Fore.MAGENTA + f"\n=== Turn {turn} ===")
            print(Fore.CYAN + f"{self.player.name}: Health = {self.player.health}/{self.player.max_health}, Shield = {self.player.shield}, Mana = {self.player.mana}")
            print(Fore.RED + f"{self.ai.name}: Health = {self.ai.health}/{self.ai.max_health}, Shield = {self.ai.shield}, Mana = {self.ai.mana}")

            # Player's turn
            self.player_turn()

            # Check if AI is defeated
            if self.ai.health <= 0:
                print(Fore.GREEN + f"\n{self.player.name} wins!")
                break

            # AI's turn
            self.ai_turn()

            # Check if Player is defeated
            if self.player.health <= 0:
                print(Fore.RED + f"\n{self.ai.name} wins!")
                break

            turn += 1

# Main function
if __name__ == "__main__":
    print(Fore.YELLOW + "Welcome to the Dice RPG Game!")
    game = Game()
    game.game_loop()
