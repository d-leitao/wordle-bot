import os
import random

class Wordle:
    def __init__(self, dictionary_path, random_seed=None):
        random.seed(random_seed)
        self.dictionary = self.__get_dictionary(dictionary_path)
        self.answer = self.__draw_answer()

        self.current_round = 0
        self.guesses = [["" for _ in range(5)] for _ in range(6)]
        self.feedback = [[None for _ in range(5)] for _ in range(6)]

    def play(self):
        os.system("cls")
        print("Wordle")
        while self.current_round < 6:
            guess = self.__receive_guess()
            self.guesses[self.current_round] = list(guess)

            if guess != self.answer:
                self.feedback[self.current_round] = self.__get_feedback(guess)
                self.__update_screen()
            else:
                print(f"You won! The answer was {self.answer}.")
                return self.current_round
            
            self.current_round += 1

        else:
            print(f"You lost. The answer was {self.answer}.")
            return self.current_round + 1

    def __update_screen(self):
        os.system("cls")
        UNDERLINE = "\033[4m"  # ANSI escape code for bold
        RESET = "\033[0m"
        for r in range(self.current_round+1):
            guess = self.guesses[r]
            feedback = self.feedback[r]
            guess_str = f"{r+1}: "
            for ix, char in enumerate(guess):
                if feedback[ix] == 0:
                    guess_str += char.lower()
                elif feedback[ix] == 1:
                    guess_str += char.upper()
                elif feedback[ix] == 2:
                    guess_str += UNDERLINE + char.upper() + RESET
            print(guess_str)

    def __get_feedback(self, guess):
        # Initialize feedback with all greys (0)
        feedback = [0] * len(guess)

        # Mark greens (2) and track the counts of letters in the answer for yellows
        letter_counts_in_answer = {}
        for ix, (g_letter, a_letter) in enumerate(zip(guess, self.answer)):
            if g_letter == a_letter:
                feedback[ix] = 2
            else:
                letter_counts_in_answer[a_letter] = letter_counts_in_answer.get(a_letter, 0) + 1

        # Mark yellows (1)
        for ix, g_letter in enumerate(guess):
            if feedback[ix] == 0 and letter_counts_in_answer.get(g_letter, 0) > 0:
                feedback[ix] = 1
                letter_counts_in_answer[g_letter] -= 1

        return feedback

    def __receive_guess(self) -> str:
        while True:
            guess = input(f"{self.current_round + 1}: ").lower()
            if self.__is_valid_guess(guess):
                return guess

    def __is_valid_guess(self, guess) -> bool:
        if len(guess) != 5:
            print(f"Guess a five-letter word. Your word has {len(guess)} letter(s).")
            return False
        elif guess not in self.dictionary:
            print(f"{guess} is not a valid word according to our dictionary.")
            return False
        else:
            return True

    def __draw_answer(self) -> str:
        return random.choice(self.dictionary)
        
    @staticmethod
    def __get_dictionary(path) -> list:
        with open(path, "r") as file:
            all_words = [line.strip() for line in file]
        
        valid_words = [
            w.lower() for w in all_words
            if len(w) == 5
                and w.islower()  #  not an acronym or proper name
                and all("a" <= l <= "z" for l in w)  # only standard English letters
        ]

        with open("dictionaries/valid_words.txt", "w", encoding="utf-8") as file:
            file.write("\n".join(valid_words))

        return valid_words

w = Wordle(dictionary_path="dictionaries/portuguese.txt")
print(w.play())