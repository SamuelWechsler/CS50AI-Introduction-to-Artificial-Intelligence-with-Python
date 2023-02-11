import os
import random
import re
import sys
import numpy as np

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    output = {}

    # number of all pages
    n = len(corpus.keys())

    # set of all pages
    all_pages = [pg for pg in corpus.keys()]

    # set of all linked pages
    linked_pages = list(corpus[page])

    # add probability that pg gets chosen randomly
    for pg in all_pages:
        output[pg] = round((1 - damping_factor) / n, 5)

    # add probability that pg get chosen as subpage of 
    for pg in linked_pages:
        output[pg] += damping_factor * (1 / len(linked_pages))

    return output

input = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
# ouput = transition_model(input, "1.html", 0.85)

def random_choice(probs):
    """
    Returns a key from probabilities dictionary, with likelihood of
    the corresponding value.
    """
    return random.choices(population=list(probs.keys()), weights=list(probs.values()))[0]

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # create dictionary to count samples
    samples = {}
    for i in corpus.keys():
        samples[i] = 0
    
    # first sample is chosen at random
    sample = random.choice(list(corpus.keys()))
    samples[sample] += 1

    for i in range(n-1):
        # choose sample according to distribution from transition_model
        sample = random_choice(probs=transition_model(corpus, sample, damping_factor))
        samples[sample] += 1
    
    # divide by n to get probability
    for i in samples.keys():
        samples[i] = samples[i] / n

    return samples

# print(sample_pagerank(input, 0.85, 10000))

def pagerank(page, corpus, damping_factor):
    # set of all linked pages
    linked_pages = corpus[page]

    # total number of pages
    n = len(corpus)

    # first part of the PR formula
    result = (1 - damping_factor) / n

    # second part of the PR formula (sum)
    for i in corpus[page]:
        result += damping_factor * pagerank(i, corpus, damping_factor) / len(corpus[i])

    return result

# print(pagerank("1.html", input, 0.85))

def linksTo(page, corpus):
    """
    returns set all pages that link to "page"
    """
    pages = set()

    for pg in list(corpus.keys()):
        # check if page is in linked pages
        if page in corpus[pg]:
            pages.add(pg)

    return pages

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # check if any value is the empty set
    for i in corpus.keys():
        if len(corpus[i]) == 0:
            corpus[i] = set(corpus.keys())

    pageranks = {}

    # total number of pages in corpus
    n = len(corpus)

    # assign 1 / n to each page
    for page in corpus.keys():
        pageranks[page] = 1 / n

    diff = np.inf

    while diff > 0.001:
        #resetting diff to zero
        diff = 0

        for page in corpus.keys():
            # result before adding further iteration
            r1 = pageranks[page]

            # add first sum of formula
            pageranks[page] = (1 - damping_factor) / n
            
            # add second part of formula
            for i in linksTo(page, corpus):
                pageranks[page] += damping_factor * pageranks[i] / len(corpus[i])

            # result after adding further iteration
            r2 = pageranks[page]

            # adding difference to diff
            diff += abs(r2 - r1)
    
    return pageranks

input = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": set()}
print(iterate_pagerank(input, 0.85))

if __name__ == "__main__":
    main()
