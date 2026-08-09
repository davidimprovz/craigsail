"""
Command line entry point for craigsail.
"""
import sys
from argparse import ArgumentParser

from .db import CraigsailDB
from .search import Search, Boats, Bikes, RVs, Properties

# Categories with dedicated parsing/cleaning subclasses.
CATEGORY_CLASSES = {
    'boo': Boats,
    'bia': Bikes,
    'rva': RVs,
}


def get_arguments(argv=None):
    parser = ArgumentParser(description='Craigsail multi-city search and asset price tracking')
    parser.add_argument('--search_category', type=str, required=True,
                        help='Craigslist category code, e.g. boo (boats), bia (bikes), rva (RVs)')
    parser.add_argument('--data_path', type=str, required=True,
                        help='Directory to save data into')
    parser.add_argument('--cities', nargs='+', required=True,
                        help='Craigslist site slugs, e.g. sfbay seattle newyork')
    parser.add_argument('--filters', nargs='*', default=[],
                        help='Optional filters as key=value pairs, e.g. max_price=5000')
    parser.add_argument('--db', type=str, default=None,
                        help='Path to the sqlite database. Defaults to <data_path>/craigsail.db')
    parser.add_argument('--csv', action='store_true',
                        help='Also write a dated CSV snapshot alongside the database')
    return parser.parse_args(argv)


def parse_filters(filter_args):
    """
    Turn ['max_price=5000', 'search_titles=true'] into a dict with
    booleans and integers coerced to their real types.
    """
    filters = {}
    for item in filter_args:
        if '=' not in item:
            raise ValueError(f'Filters must be key=value pairs. Got {item!r}.')
        key, value = item.split('=', 1)

        if value.lower() in ('true', 'false'):
            parsed = value.lower() == 'true'
        else:
            try:
                parsed = int(value)
            except ValueError:
                parsed = value

        filters[key] = parsed
    return filters


def main(argv=None):
    args = get_arguments(argv)

    # Fail fast on a mistyped city rather than after a long scrape.
    try:
        cities = Search.validate_cities(args.cities, strict=True)
        filters = parse_filters(args.filters)
    except ValueError as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 2

    search_cls = CATEGORY_CLASSES.get(args.search_category, Search)
    craig_search = search_cls(
        search_category=args.search_category,
        data_path=args.data_path,
        cities=cities,
        filters=filters,
    )

    timespan, results_df = craig_search.get_all_daily_postings()
    print(f'Search completed in {timespan}. {len(results_df)} listings found.')

    db_path = args.db or str(craig_search.SAVE_PATH.joinpath('craigsail.db'))
    db = CraigsailDB(db_path)
    inserted, updated, price_changes = db.save_listings(results_df, category=args.search_category)
    print(f'{db_path}: {inserted} new, {updated} updated, {price_changes} price observations recorded.')

    if args.csv:
        csv_path = craig_search.save_data_as_csv(results_df, 'search_results')
        print(f'CSV snapshot written to {csv_path}.')

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
