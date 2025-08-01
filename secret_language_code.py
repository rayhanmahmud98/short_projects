import random

# Function to generate random characters
def random_chars(length=3):
    letters = 'abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choice(letters) for _ in range(length))

# Function to encode a word
def encode_word(word):
    if len(word) >= 3:
        # Remove the first letter, append it at the end, and add random characters at the start and end
        word = word[1:] + word[0]
        encoded_word = random_chars() + word + random_chars()
    else:
        # Simply reverse the word if it's less than 3 characters
        encoded_word = word[::-1]
    return encoded_word

# Function to decode a word
def decode_word(word):
    if len(word) < 3:
        # Reverse the word if it's less than 3 characters
        decoded_word = word[::-1]
    else:
        # Remove the random characters and move the last letter to the beginning
        word = word[3:-3]  # Remove the first and last 3 characters
        decoded_word = word[-1] + word[:-1]  # Move the last letter to the front
    return decoded_word

# Function to process the entire message
def process_message(message, action):
    words = message.split()  # Split the message into words
    processed_words = []

    for word in words:
        if action == 'encode':
            processed_words.append(encode_word(word))
        elif action == 'decode':
            processed_words.append(decode_word(word))
    
    return ' '.join(processed_words)

# Main program
def main():
    action = input("Do you want to 'encode' or 'decode' the message? ").strip().lower()
    
    if action not in ['encode', 'decode']:
        print("Invalid option. Please choose 'encode' or 'decode'.")
        return

    message = input("Enter your message: ").strip()

    # Process the message based on the action (encode or decode)
    result = process_message(message, action)
    
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
