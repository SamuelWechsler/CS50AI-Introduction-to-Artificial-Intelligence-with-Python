import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for file in os.listdir(directory):
        if file.endswith(".txt"):
            with open(os.path.join(os.getcwd(), directory, file)) as f:
                files[file] = " ".join(f.readlines())

    return files

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document)
    word_tokens = [
        word.lower() for word in tokens
        if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")
    ]
    return word_tokens

def idf(word, docs):
    num_occurences = 0
    for words in docs.values():
        num_occurences += words.count(word)
    num_docs = len(docs)

    return math.log(num_docs / num_occurences)



def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = {}
    docs = documents.keys()

    for doc in docs:
        for word in documents[doc]:
            idfs[word] = idf(word, documents)
    
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    ranking = []
    mapped_words = idfs.keys()

    for file in files.keys():
        sum_tfidf = 0
        doc_words = files[file]

        for word in query:
            if word in mapped_words:
                sum_tfidf += idfs[word] * doc_words.count(word)

        ranking.append((file, sum_tfidf))

    ranking = sorted(ranking, key=lambda tup: tup[1])

    return [ele[0] for ele in ranking][:n]

# docs = load_files("corpus")
# words = tokenize(docs["python.txt"])
# print(compute_idfs({"python.txt" : words}))

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    ranking = []

    for sentence in sentences.keys():
        sum_idf = 0
        lst_sentence = sentences[sentence]
        qry_term_density = len([word for word in lst_sentence if word in query]) / len(lst_sentence)

        
        for word in query:
            if word in lst_sentence:
                sum_idf += idfs[word]
        
        ranking.append((sentence, sum_idf, qry_term_density))
    
    ranking = sorted(ranking, key=lambda tup: (tup[1], tup[2]), reverse=True)

    for i in range(10):
        print(ranking[i])

    return [ele[0] for ele in ranking][:n]


if __name__ == "__main__":
    main()
