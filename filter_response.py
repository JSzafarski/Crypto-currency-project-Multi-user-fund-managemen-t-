import random


def filter_msg(message):
    word_list = message.split()
    sentences_array = []
    temp_sentence = ""
    for word in word_list:
        if "!" in word or "." in word:
            temp_sentence += " " + str(word)
            sentences_array.append(temp_sentence)
            temp_sentence = ""
        else:
            temp_sentence += " " + str(word)
    if temp_sentence != "":  # incase the last is hash-tag
        sentences_array.append(temp_sentence)
    # remove sentences until character limit is under 280
    total = 0
    while True:
        total = 0
        for sentence in sentences_array:
            total += len(sentence)
        if total > 280:
            random_sentence = random.randint(0, len(sentences_array) - 1)
            if "#mBTC" not in sentences_array[random_sentence]:
                sentences_array.pop(random_sentence)
            # randomly remove sentence and repeat but it must include hashtag
        else:
            break
    return ''.join(sentences_array)

