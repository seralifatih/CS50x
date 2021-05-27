from cs50 import get_string

def main():
    text = get_string("Text: ")
    letters = count_letters(text)
    words = count_words(text)
    sentences = count_sentences(text)
    preindex = 0.0588 * (letters * 100.0) / words - 0.296 * (sentences * 100.0) / words - 15.8
    index = round(preindex)
    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")

def count_letters(text):
    counter = 0
    for i in range(len(text)):
        if text[i].isalpha():
            counter += 1
    return counter

def count_words(text):
    word_counter = 1
    for i in range(len(text)):
        if text[i].isspace():
            word_counter += 1
    return word_counter

def count_sentences(text):
    sentence_counter = 0
    for i in range(len(text)):
        if text[i] == "." or text[i] == "?" or text[i] == "!":
            sentence_counter += 1
    return sentence_counter


main()