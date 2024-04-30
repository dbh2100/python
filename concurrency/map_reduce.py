"""Use multiple processes to add the lengths of all the words in a text file"""

import re
from   functools import partial
import multiprocessing
from   queue import Empty
import time
from   operator import methodcaller


def put_word_length(len_queue, word):
    """The 'map' function: add the word's length to the length queue"""
    len_queue.put(len(word))


def sum_lengths(len_queue, sum_queue):
    """The 'reduce' function: sum the word's lengths"""

    # Get first word length from length queue if this is first sum process
    # Otherwise, get first length from sum queue
    try:
        length1 = sum_queue.get(timeout=5)
    except Empty:
        length1 = len_queue.get(timeout=5)

    # Get second length from length queue if queue is not empty
    try:
        length2 = len_queue.get(timeout=5)
    except Empty:
        length2 = 0

    # Add sum of lengths to sum queue
    # print(length1, length2)
    sum_queue.put(length1 + length2)


def get_num_word_chars(file_name):
    """Find the total number of word characters in a text file"""
    with open(file_name, encoding='utf-8') as fname:
        word_chars = re.findall(r"\w", fname.read())
    return len(word_chars)


if __name__ == '__main__':

    with multiprocessing.Manager() as manager:

        # Initialize queues
        length_queue = manager.Queue()
        total_queue = manager.Queue()

        # Read file
        with open('sample_text_file.txt', encoding='utf-8') as f:
            match_iter = re.finditer(r"\w+", f.read())
            word_iter = map(methodcaller('group', 0), match_iter)

        # Map step
        with multiprocessing.Pool() as map_pool:
            map_pool.map(partial(put_word_length, length_queue), word_iter)

        # Reduce step
        with multiprocessing.Pool(processes=10) as reduce_pool:
            while not length_queue.empty():
                reduce_pool.apply_async(sum_lengths, (length_queue, total_queue))
                reduce_pool.apply_async(time.sleep, (3,))

        # Get final sum from sum queue
        result = 0
        while not total_queue.empty():
            result += total_queue.get()
        print(f'Result: {result}')

    # Find expected result for comaprison by adding file's word characters
    expected_result = get_num_word_chars('sample_text_file.txt')
    print(f'Expected result: {expected_result}')
