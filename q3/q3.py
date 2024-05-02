from mrjob.job import MRJob
from mrjob.step import MRStep
from nltk.corpus import stopwords
import re

WORD_RE = re.compile(r"[\w']+")

class MRMostUsedWords(MRJob):

    def mapper_get_words(self, _, line):
        '''
        Yields tuples of non-stop words in lowercase and the count 1 from a given line of text.
        '''
        stop_words = set(stopwords.words('english'))
        words = WORD_RE.findall(line)
        for word in words:
            lower_word = word.lower()
            if lower_word not in stop_words:
                yield (lower_word, 1)

    def combiner_count_words(self, word, counts):
        '''
        Sum all of the words available so far
        '''
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        '''
        Arrive at a total count for each word in the 5 star reviews
        '''
        yield None, (sum(counts), word)

    def reducer_find_top_words(self, _, word_counts):
        sorted_words = sorted(word_counts, reverse=True)[:10]
        for count, word in sorted_words:
            yield (word, count)

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_top_words)
        ]


if __name__ == '__main__':
    MRMostUsedWords.run()


'''
Use "python q3.py descriptions.txt > output.txt" to run locally
with a python version under 3.12.
'''