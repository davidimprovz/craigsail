from argparse import ArgumentParser
import search as craigsearch

def get_arguments():
    arguments = {}
    # Process a specific search 
    # Add to / update db 
    # Output 
    return arguments


if __name__ == '__main__':
    # Handle arguments
    arguments = get_arguments()
    craig_search = craigsearch.Search(**arguments)
    craig_search.run()
    # Output results


