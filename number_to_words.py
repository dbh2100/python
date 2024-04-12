'''
Defines function to convert an integer to words

>>> from number_to_words import convert_to_words
>>> convert_to_words(0)
'zero'
>>> convert_to_words(1)
'one'
>>> convert_to_words(3)
'three'
>>> convert_to_words(13)
'thirteen'
>>> convert_to_words(913)
'nine hundred thirteen'
>>> convert_to_words(943)
'nine hundred forty three'
>>> convert_to_words(1943)
'one thousand nine hundred forty three'
>>> convert_to_words(1003)
'one thousand three'
>>> convert_to_words(1000003)
'one million three'
>>> convert_to_words(1020003)
'one million twenty thousand three'
'''


# Words corresponding to the first 19 positive integers
FIRST_19 = [
    None,
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
    'eleven',
    'twelve',
    'thirteen',
    'fourteen',
    'fifteen',
    'sixteen',
    'seventeen',
    'eighteen',
    'nineteen',
]

# Words corresponding to multiples of 10
MUTLIPLES_10 = [
    None,
    None,
    'twenty',
    'thirty',
    'forty',
    'fifty',
    'sixty',
    'seventy',
    'eighty',
    'ninety',
]

# Words corresponding to powers of 1000
POWERS_1000 = [
    None,
    'thousand',
    'million',
    'billion',
    'trillion',
    'quadrillion',
    'quintillion',
    'sextillion',
    'septillion',
    'octillion',
    'nontillion',
    'decillion',
]


def _convert_chunk(chunk):
    '''Returns words associated with chunk separated by comma'''

    # Intialize list
    chunk_words = []

    # Find hundreds, tens, and one digits of chunk
    hundreds, tens, ones = map(int, chunk.zfill(3))

    # Find words corresponding to hundreds digit
    if hundreds > 0:
        chunk_words.append(FIRST_19[hundreds])
        chunk_words.append('hundred')

    # Find words corresponding to tens digit
    if tens > 1:
        chunk_words.append(MUTLIPLES_10[tens])

    # Find words corresponding to ones digit
    if tens == 1:
        ones += 10
    if ones > 0:
        chunk_words.append(FIRST_19[ones])

    # 21 should be rendered as twenty-one
    if tens > 1 and ones > 0:
        ones_word = chunk_words.pop()
        tens_word = chunk_words.pop()
        chunk_words.append('-'.join([tens_word, ones_word]))

    return chunk_words


def convert_to_words(num):
    '''Convert integer num to words'''

    # Base case: the only time "zero" is part of number
    if num == 0:
        return 'zero'

    # Initialize list
    num_words = []

    # Account for a negative number
    if num < 0:
        num_words.append('negative')
        num = -num

    # Convert number into chunks separated by the comma
    chunks = format(num, ',').split(',')

    # The power of 1000 associated with the most significant chunk
    # is the number of chunks - 1
    exp1000 = len(chunks) - 1

    for chunk in chunks:
        num_words.extend(_convert_chunk(chunk))
        if int(chunk) and exp1000 > 0:
            num_words.append(POWERS_1000[exp1000])
        exp1000 -= 1

    return ' '.join(num_words)


if __name__ == '__main__':
    for n in [4, 293947, 1294, 3924803413, -328473, 1000043, 4985747407]:
        print(n, convert_to_words(n), sep=': ')
        print('\n')
