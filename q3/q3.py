from mrjob.job import MRJob
from mrjob.step import MRStep
import re
import nltk

nltk.download('stopwords')

WORD_RE = re.compile(r"[\w']+")

class MRMostUsedWords(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper_get_words,
                   combiner=self.combiner_count_words,
                   reducer=self.reducer_count_words),
            MRStep(reducer=self.reducer_find_top_words)
        ]

    def mapper_get_words(self, _, line):
        from nltk.corpus import stopwords
        stop_words = set(stopwords.words('english'))
        words = WORD_RE.findall(line)
        for word in words:
            lower_word = word.lower()
            if lower_word not in stop_words:
                yield (lower_word, 1)

    def combiner_count_words(self, word, counts):
        yield (word, sum(counts))

    def reducer_count_words(self, word, counts):
        yield None, (sum(counts), word)

    def reducer_find_top_words(self, _, word_counts):
        sorted_words = sorted(word_counts, reverse=True)[:10]
        for count, word in sorted_words:
            yield (word, count)


if __name__ == '__main__':
    MRMostUsedWords.run()

'''
Use "python most_used_words.py descriptions.txt > output.txt" to run locally
with a python version under 3.12.
'''