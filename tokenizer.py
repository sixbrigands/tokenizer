

# Helper function to replace punctuation with whitespace. Allows for exceptions.
# Based on https://www.geeksforgeeks.org/python-remove-punctuation-from-string/
def remove_punctuation(string, exception = ' '):
    punctuation = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
    for v in string:
        if v in punctuation and v not in exception:
            string = string.replace(v, ' ')
    return string

# Checks if a string looks like an initilaism.
def is_initialism(string):
    dot_check = False
    if len(string) > 3:
        for v in string:
            if not dot_check and v.isalpha():
                dot_check = not dot_check
                continue
            if dot_check and v == '.':
                dot_check = not dot_check
                continue
            else:
                return False
        if dot_check == False:        
            return True
    return False

# Checks if string contains a vowel.
def contains_vowel(string):
    vowels = {'a', 'e', 'i', 'o', 'u'}
    for v in string:
        if v in vowels:
            return True
    return False

# Helper function for porter stemmer
def porter_helper(string):
    if string.endswith('at') or string.endswith('bl') or string.endswith('iz') or len(string) < 4:
        return string + 'e'
    if len(string) > 2:
        if string[-1] == string[-2] and string[-1] != 'l' and string[-1] != 's' and string[-1] != 'z':
            return string[:-1]
    return string
    
# Initial tokenization.
def tokenize(user_input):
    with open(user_input, 'r') as file:
        data = remove_punctuation(file.read().replace('\n', ' ').lower(), '.')
        word_list = data.split()
        tokens = []
        for word in word_list:
            if is_initialism(word):
                tokens.append(word.replace('.', ''))
                continue
            for sub_word in remove_punctuation(word).split():
                tokens.append(sub_word)
        return tokens

# Remove stopwords.
def remove_stopwords(tokens):
    with open('stopwords.txt', 'r') as file:
        stopwords = file.read().splitlines();
        for token in tokens[:]:
            if token in stopwords:
                tokens.remove(token)

# Implement the first 2 steps of Porter stemming
def stem(tokens):

    stemmed_tokens = []
    for token in tokens:

        if token.endswith('sses'):
            stemmed_tokens.append(token[:-4] + 'ss')
            continue
        
        if token.endswith('s') and not token.endswith('us') and not token.endswith('ss') and contains_vowel(token):
            if not contains_vowel(token[len(token) - 2]): #if the second to last char is not a vowel
                stemmed_tokens.append(token[:-1])         #remove the 's'
                continue

        if token.endswith('ied') or token.endswith('ies'):
            if len(token) < 5:
                stemmed_tokens.append(token[:-3] + 'ie')
                continue
            else:
                stemmed_tokens.append(token[:-3] + 'i')
                continue

        if 'eed' in token or 'eedly' in token:
            i = token.index('eed')
            if i >= 2:
                if not contains_vowel(token[i - 1]) and contains_vowel(token[i - 2]):
                    if 'eedly' in token:
                        stemmed_tokens.append(token.replace("eedly", "ee", 1))
                        continue
                    if 'eed' in token:
                        stemmed_tokens.append(token.replace("eed", "ee", 1))
                        continue
        
        if token.endswith('ed') and not token.endswith('eed'):
            token_copy = token[:-2]
            if contains_vowel(token_copy):
                stemmed_tokens.append(porter_helper(token_copy))
                continue

        if token.endswith('edly'):
            token_copy = token[:-4]
            if contains_vowel(token_copy):
                stemmed_tokens.append(porter_helper(token_copy))
                continue

        if token.endswith('ing'): 
            token_copy = token[:-3]
            if contains_vowel(token_copy):
                stemmed_tokens.append(porter_helper(token_copy))
                continue

        if token.endswith('ingly'):
            token_copy = token[:-5]
            if contains_vowel(token_copy):
                stemmed_tokens.append(porter_helper(token_copy))
                continue

        stemmed_tokens.append(token)
    return stemmed_tokens    

# This outpts the top 200 words as 'terms.txt' and the vocabulary growth data as 'graph_data.csv'
# https://stackabuse.com/how-to-sort-dictionary-by-value-in-python/
def token_stats(tokens):
    with open('graph_data.csv', 'w') as graph_data:
        token_dict = {}
        total_words =  0
        unique_words = 0
        for token in tokens:
            if token in token_dict:
                token_dict[token] += 1
            else:
                token_dict[token] = 1 
                unique_words += 1
            total_words += 1
            graph_data.write(str(total_words) + ',' + str(unique_words) + '\n')
        with open('terms.txt', 'w') as terms:  
            sorted_tokens= sorted(token_dict, key=token_dict.get, reverse=True)
            limit = len(sorted_tokens) if len(sorted_tokens) < 200 else 200
            for i in range(limit):
                terms.write(sorted_tokens[i] + ': ' + str(token_dict[sorted_tokens[i]]) + '\n')

if __name__ == '__main__':
    user_input = input('What file should I tokenize? ')
    user_output = input('What should I call the output file? ')
    tokens = tokenize(user_input + '.txt')
    remove_stopwords(tokens)
    tokens = stem(tokens)
    file = open(user_output + '.txt', "w") 
    for token in tokens:
        file.write(token + '\n')
    user_input = input('Done. Would you like the term statistics as well? y/n: ')
    if user_input.lower().startswith('y'):
        token_stats(tokens)
    file.close() 
