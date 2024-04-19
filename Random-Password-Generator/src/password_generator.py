import random
import string

class PasswordGenerator:
    def __init__(self,Pass_create_label, length=8, easy_chars=False, medium_chars=False, hard_chars=False, vhard_chars=False, complexity_level="Easy"):
        self.length = length
        self.easy_chars = easy_chars
        self.medium_chars = medium_chars
        self.hard_chars = hard_chars
        self.vhard_chars = vhard_chars
        self.complexity_level = complexity_level
        self.Pass_create_label=Pass_create_label

    def generate_password(self):
        complexity_ratios = {
            "Easy": 0.2,
            "Medium": 0.35,
            "Hard": 0.5,
            "Very Hard": 0.75
        }

        num_non_alphanumeric = int(self.length * complexity_ratios[self.complexity_level])

        characters = string.ascii_letters + string.digits
        special_characters = ''
        if self.easy_chars:
            special_characters += "!$@#"
        if self.medium_chars:
            special_characters += "%^?*"
        if self.hard_chars:
            special_characters += "_-+="
        if self.vhard_chars:
            special_characters += "~`|/"

        while num_non_alphanumeric > len(special_characters):
            special_characters += special_characters

        password_special = ''.join(random.choice(special_characters) for _ in range(num_non_alphanumeric))
        password_alpha = ''.join(random.choice(characters) for _ in range(self.length - num_non_alphanumeric))
        password = password_special + password_alpha

        generated_password = 'Generated Password: '
        generated_password += ''.join(random.sample(password, len(password)))
        self.Pass_create_label.setText(generated_password)
        print(generated_password)

if __name__ == "__main__":
    # Example usage
    generator = PasswordGenerator(length=12, easy_chars=True, medium_chars=True, hard_chars=True, vhard_chars=True, complexity_level="Very Hard")
    generator.generate_password()
