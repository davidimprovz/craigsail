from argparse import ArgumentParser
import search as craigsearch

def get_arguments():
    parser = ArgumentParser(description="Craigsail multi-city search and asset price tracking")
    parser.add_argument('--search_category', type=str, required=True, help='The search category to use')
    parser.add_argument('--data_path', type=str, required=True, help='The path to save data')
    parser.add_argument('--cities', nargs='+', required=True, help='List of cities to search')
    parser.add_argument('--filters', nargs='*', help='Optional filters for the search', default={})
    return vars(parser.parse_args())

if __name__ == '__main__':
    # Handle arguments
    arguments = get_arguments()
    craig_search = craigsearch.Search(
        search_category=arguments['search_category'],
        data_path=arguments['data_path'],
        cities=arguments['cities'],
        filters=dict(arg.split('=') for arg in arguments['filters'])
    )
    timespan, results_df = craig_search.get_all_daily_postings()
    print(f"Search completed in {timespan}.")
    print("Results:")
    print(results_df)
    # Optionally save results
    craig_search.save_data_as_csv(results_df, 'search_results')
