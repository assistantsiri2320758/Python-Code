'''Password Generator ->

Randomly generates strong passwords with symbols, numbers, and uppercase/lowercase letters.

And also added option for user to choose length and complexity of the password . '''


import random
import string

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_symbols=True):
    """Generate a random password with specified complexity."""
    
    character_sets = []
    
    if use_uppercase:
        character_sets.append(string.ascii_uppercase)
    if use_lowercase:
        character_sets.append(string.ascii_lowercase)
    if use_digits:
        character_sets.append(string.digits)
    if use_symbols:
        character_sets.append(string.punctuation)
    
    if not character_sets:
        raise ValueError("At least one character set must be selected")
    
    # Ensure at least one character from each selected set
    password = []
    for charset in character_sets:
        password.append(random.choice(charset))
    
    # Fill the rest of the password with random characters from all selected sets
    all_chars = ''.join(character_sets)
    password.extend(random.choices(all_chars, k=length - len(password)))
    
    # Shuffle to avoid predictable patterns
    random.shuffle(password)
    
    return ''.join(password)

def get_user_preferences():
    """Get password generation preferences from the user."""
    
    print("Password Generator\n")
    
    # Get password length
    while True:
        try:
            length = int(input("Enter password length (8-64): "))
            if 8 <= length <= 64:
                break
            print("Please enter a value between 8 and 64.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get complexity options
    print("\nSelect character sets to include:")
    use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
    use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
    use_digits = input("Include digits? (y/n): ").lower() == 'y'
    use_symbols = input("Include symbols? (y/n): ").lower() == 'y'
    
    return {
        'length': length,
        'use_uppercase': use_uppercase,
        'use_lowercase': use_lowercase,
        'use_digits': use_digits,
        'use_symbols': use_symbols
    }

def main():
    """Main function to run the password generator."""
    
    while True:
        try:
            preferences = get_user_preferences()
            password = generate_password(**preferences)
            
            print("\nGenerated Password:")
            print(password)
            
            another = input("\nGenerate another password? (y/n): ").lower()
            if another != 'y':
                break
                
        except ValueError as e:
            print(f"\nError: {e}")
            print("Please select at least one character set.\n")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()