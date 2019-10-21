from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.wiki import wiki_search


def search(query):
    # search in database

    # search in wiki
    wiki_search_results = wiki_search(query)

    return wiki_search_results
