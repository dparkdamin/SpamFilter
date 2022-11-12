############################################################
# CMPSC442: Homework 5
############################################################

student_name = "Damin Park"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import email
import io
import math
import os
from collections import defaultdict

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    fileobj = io.open(email_path)
    msg = email.message_from_file(fileobj)
    msgList = list(email.iterators.body_line_iterator(msg))
    wordList = []

    for line in msgList:
        wordList += line.split()
    return wordList

def log_probs(email_paths, smoothing):
    count = {}
    totalWords = 0

    for email_path in email_paths:
        wordList = load_tokens(email_path)
        
        for word in wordList:
            totalWords += 1

            if word not in count:
                count.update({word: 1})
            else:
                count[word] += 1

    dict = defaultdict(lambda: math.log(smoothing / (totalWords + smoothing * (len(count) + 1))))

    for email_path in email_paths:
        wordList = load_tokens(email_path)

        for word in wordList:
            if word not in dict:
                dict.update({word: math.log((count[word] + smoothing) / (totalWords + smoothing * (len(count) + 1)))})
            
    return dict

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spam_paths = os.listdir(spam_dir)
        ham_paths = os.listdir(ham_dir)
        self.logProbSpamDirectory = log_probs(["homework5_data/train/spam/%s" % path for path in spam_paths], smoothing)
        self.logProbHamDirectory = log_probs(["homework5_data/train/ham/%s" % path for path in ham_paths], smoothing)
        self.smoothing = smoothing
        self.spam_prob = len(self.logProbSpamDirectory) / (len(self.logProbSpamDirectory) + len(self.logProbHamDirectory))
        self.ham_prob = len(self.logProbHamDirectory) / (len(self.logProbSpamDirectory) + len(self.logProbHamDirectory))
        self.wordBank = []

        for word in self.logProbHamDirectory:
            if word in self.logProbSpamDirectory:
                if word not in self.wordBank:
                    self.wordBank.append(word)
    
    def is_spam(self, email_path):
        wordList = load_tokens(email_path)
        spamList = []
        hamList = []

        for word in wordList:
            spamList.append(self.logProbSpamDirectory[word])
            hamList.append(self.logProbHamDirectory[word])

        probSpam = math.log(self.spam_prob) + sum(spamList)
        probHam = math.log(self.ham_prob) + sum(hamList)

        if probSpam > probHam:
            return True
        else:
            return False

    def most_indicative_spam(self, n):
        unsortedDict = {}
        for word in self.wordBank:
            unsortedDict[word] = self.logProbSpamDirectory[word] - math.log(math.exp(self.logProbSpamDirectory[word]) * self.spam_prob + math.exp(self.logProbHamDirectory[word]) * self.ham_prob)

        return sorted(unsortedDict, key=unsortedDict.get, reverse=True)[:n]

    def most_indicative_ham(self, n):
        unsortedDict = {}
        for word in self.wordBank:
            unsortedDict[word] = self.logProbHamDirectory[word] - math.log(math.exp(self.logProbHamDirectory[word]) * self.ham_prob + math.exp(self.logProbSpamDirectory[word]) * self.spam_prob)

        return sorted(unsortedDict, key=unsortedDict.get, reverse=True)[:n]


############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
11.5 hours
"""

feedback_question_2 = """
Making sure that I was referring to the right variables and making the formula work correctly was the hardest part.
Because there are many different parts in the formula, it was easy to get lost track of what was referring to what.
"""

feedback_question_3 = """
I liked how there were many different aspects to the homework like reading files and implementing formulas.
"""
