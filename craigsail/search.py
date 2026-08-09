"""
Craigsail
multi-city search and asset price tracking

https://github.com/juliomalegria/python-craigslist
"""
from pathlib import Path
import pandas as pd
from .globals import CRAIGSLIST_CITIES, SALE_CATEGORIES, FILTER_OPTIONS

# `craigslist.base` fetches the list of all craigslist sites over the network
# at import time. Import lazily so that importing craigsail (and running the
# test suite) does not require network access.
clfs = None


def _load_clfs():
    """
    Import CraigslistForSale on first use. Returns the class.
    Raises a clear error if the dependency is missing.
    """
    global clfs
    if clfs is None:
        try:
            from craigslist import CraigslistForSale
        except ImportError as exc:
            raise ImportError(
                'python-craigslist is required to fetch listings. '
                'Install it with `pip install python-craigslist`.'
            ) from exc
        clfs = CraigslistForSale
    return clfs

class Search():
    """
    Generic hooks for the python-craigslist 
    library. Combines the API with pandas 
    and database functionality. Subclass
    with one of the search categories provided 
    in the url string of any craigslist 
    top-level category.
    """

    def __init__(
        self,
        search_category=None,
        data_path=None,
        cities=None,
        filters=None,
    ):
        """
        cities is a list of craigslist site slugs (e.g. ['sfbay', 'seattle']).
        filters is a dict of python-craigslist filter options, merged over
        the defaults below.
        """
        assert isinstance(search_category, str), f'search_category arg should be str. Got {type(search_category)}.'
        assert isinstance(data_path, str), f'data_path must be a string. Got {type(data_path)}.'

        self.FILTERS = {
            'search_titles': True,
            'has_image': True,
            'bundle_duplicates': True,
        }
        self.CITIES = []
        self.CATEGORY = search_category
        self.SAVE_PATH = Path(data_path)

        if filters:
            self.add_filters(**filters)
        if cities:
            self.update_cities(cities)
    
    def get_category(self):
        return self.CATEGORY

    def set_category(self, category):
        assert isinstance(category, str), f'category arg should be string. Got type {type(category)}.'
        self.CATEGORY = category

    def add_filters(self, **filters):
        self.FILTERS |= filters

    def remove_filters(self, **filters):
        keys = set(self.FILTERS) - set(filters)
        self.FILTERS = {key: val for key,val in self.FILTERS.items() if key in keys}    
            
    @staticmethod
    def validate_cities(cities, strict=False):
        """
        Normalise a list of craigslist site slugs (strip + lowercase).

        With strict=True the slugs are additionally checked against the
        authoritative site list from python-craigslist and a ValueError is
        raised for any that do not exist. That check costs a network request,
        so it is opt-in and used at the CLI boundary rather than on every
        instantiation. Checking is skipped silently if the site list cannot
        be reached, so offline use still works.
        """
        assert not isinstance(cities, str), 'cities must be a list of city slugs, not a single string.'

        cleaned = [str(city).strip().lower() for city in cities]

        if not strict:
            return cleaned

        try:
            from craigslist.base import ALL_SITES
        except Exception:
            return cleaned  # offline / dependency missing - accept as given

        if not ALL_SITES:
            return cleaned

        unknown = sorted(set(cleaned) - set(ALL_SITES))
        if unknown:
            raise ValueError(
                f'Unknown craigslist site(s): {unknown}. '
                'Use the site subdomain (e.g. "sfbay", "seattle", "newyork"). '
                'See craigsail.globals.CRAIGSLIST_CITIES for cities by state.'
            )
        return cleaned

    def add_cities(self, new_cities):
        """
        Add cities to the existing search list.
        """
        self.CITIES = sorted(set(self.CITIES) | set(self.validate_cities(new_cities)))

    def update_cities(self, new_cities):
        """
        Replace the search list with new_cities.
        """
        self.CITIES = sorted(set(self.validate_cities(new_cities)))

    def remove_cities(self, cities):
        self.CITIES = list(set(self.CITIES) - set(cities))
        if not len(self.CITIES):
            print(f'there are no more cities to search.')

    # def set_search_term(self, term):
    # to do: fix to work on filters instead
    # 	assert isinstnace(term, str), f'argument term must be a str. Got {type(term)}.'
    # 	self.SEARCH_TERM = term

    # def get_search_term(self):
    # 	return self.SEARCH_TERM

    def convert_city_dict_to_df(
        self, 
        city, 
        city_data
    ):
        """
        Convert each list to a Series and
        concat all records into a dataframe. 
        Use the city as a feature.
        """
        
        df = pd.DataFrame(city_data) # 
        df['city'] = city
        return df.reset_index(drop=True)

    def expand_attributes(self, attributes):
        """
        Convert a list with colon 
        delimited values into an
        individual df format for 
        concatination.
        """
        
        if attributes is None or (not isinstance(attributes, (list, tuple, pd.Series)) and pd.isna(attributes)):
            return pd.DataFrame(index=[0])

        # Split on the first colon only - values such as
        # "engine hours (total):1:30" would otherwise spill into extra columns.
        attr_list = [str(x).split(':', 1) for x in attributes]
        attr_list = [pair for pair in attr_list if len(pair) == 2]
        if not attr_list:
            return pd.DataFrame(index=[0])

        attr_df = pd.DataFrame(attr_list).rename({0: 'Attributes', 1: 'Values'}, axis=1)

        return attr_df.set_index('Attributes').T

    def expand_all_attributes(self, df):
        """
        Loop over a set of attributes and 
        call expand_attributes(), combining
        the results in a new df.
        """

        # Accept either the `attrs` Series itself or a single-column frame
        # holding it. Each element is a list of "key:value" strings.
        if isinstance(df, pd.DataFrame):
            assert df.shape[1] == 1, (
                f'expand_all_attributes expects the attrs Series or a '
                f'single-column DataFrame. Got {df.shape[1]} columns.'
            )
            attrs = df.iloc[:, 0]
        else:
            attrs = df

        # `.iteritems()` was removed in pandas 2.0; `.items()` is the successor.
        expanded = [self.expand_attributes(row) for _, row in attrs.items()]
        expanded_df = pd.concat(expanded).reset_index(drop=True)

        return expanded_df

    def clean_str_columns(self, df):
        stripped_df = df.copy().stack().str.strip().unstack()
        return stripped_df

    def strip_nan_columns(self, df):
        """
        Loop over each col and check if 
        all values NaN. Remove col from 
        df if so. 
        """

        for col in df.columns: 
            if df[col].isnull().all():
                df = df.drop(col, axis=1)
        return df 

    def get_city_items(self, city):
        """
        Fetch data from craigslist using 
        the cities and filters.
        """
        
        results = list()
        search_cls = _load_clfs()
        city_items = search_cls(site=city, category=self.CATEGORY, filters=self.FILTERS)
        for result in city_items.get_results(sort_by='newest', geotagged=True, include_details=True):
            results.append(result)
        city_df = self.convert_city_dict_to_df(city, results)

        return city_df 

    def get_all_daily_postings(self):

        all_items = list()
        
        start_time = pd.to_datetime('now')
        # to do..async with reactivex
        for city in self.CITIES:
            all_items.append(self.get_city_items(city)) # control search with filters Query 
        finish_time = pd.to_datetime('now')

        df = pd.concat(all_items).reset_index(drop=True)
        timespan = finish_time - start_time
        
        return timespan, df

    def save_data_as_csv(self, df, filename):
        """
        Use the save_path supplied at 
        instantiation to write a csv
        to disk. 
        """

        self.SAVE_PATH.mkdir(parents=True, exist_ok=True)

        today = pd.to_datetime('today').strftime('%Y-%m-%d')
        save_path = self.SAVE_PATH.joinpath(f'{filename}_{today}.csv')

        df.to_csv(save_path, index=False)

        return save_path

    def send_to_sqlitedb(self, df, conn, table_name):
        """
        Save a pandas dataframe to a sqlite3 db. 
        If the table already exists, update it. 
        Otherwise, create a new table.
        """
        assert isinstance(df, pd.DataFrame), "df must be a pandas DataFrame"
        assert isinstance(table_name, str), "table_name must be a string"

        df.to_sql(table_name, conn, if_exists='append', index=False)

    def filter_feature_space(self, df, keep_cols):
        """
        Use a list of sub-strings to filter for 
        columns containing those sub strings.  
        """
        assert isinstance(df, pd.DataFrame)
        assert isinstance(keep_cols, list)
        
        return df.loc[:, df.columns.str.contains('|'.join(keep_cols))]

    def merge_multiple_csvs(
        self, 
        path_to_files, 
        merge_col, 
        keep_cols=[]
    ):
        """
        Glob the csvs in a path and load 
        them, merging a specified col. 
        """

        assert isinstance(path_to_files, str)
        assert Path(path_to_files).exists()
        assert isinstance(merge_col, str)

        # load files
        data_path = Path(path_to_files)
        data_files = [pd.read_csv(item) for item in data_path.glob('*.csv')]
        assert merge_col in data_files[0], 'The specified merge column was not found in the dataframes. Try again.'
            
        # perform merging
        merged_df = pd.DataFrame()
        for df in data_files:
            if merged_df.empty: merged_df = df.copy()
            else: merged_df = merged_df.merge(df, on=merge_col, how='outer')
            
        # filter feature space
        if len(keep_cols):
            merged_df = self.filter_feature_space(merged_df, keep_cols)

        return merged_df
    
class Boats(Search):
    """
    Parsing and cleaning functionality
    for the 'boo' search category.

    # to do: use LangChain to format data
    # to remove need for if>then.
    """

    # Craigslist serves attribute names in the poster's language, so the same
    # field arrives under several keys. Map each alias onto its canonical
    # english column name.
    COLUMN_ALIASES = {
        'mfg_year': 'year manufactured',
        'año de fabricación': 'year manufactured',
        'condición': 'condition',
        'horas del motor (en total)': 'engine hours (total)',
        'marca / fabricante': 'make / manufacturer',
        'nombre / número de modelo': 'model name / number',
        'tipo de propulsión': 'boat_propulsion_type',
    }

    def combine_city_sailboats_data(self, df, eval_cols=()):
        """
        Coalesce aliased/spanish attribute columns into their canonical
        english counterparts, then drop the aliases. Returns a new DataFrame.
        """

        df = df.copy()
        drop_cols = []

        for alias, canonical in self.COLUMN_ALIASES.items():
            if alias not in df.columns:
                continue

            if canonical in df.columns:
                df[canonical] = df[canonical].fillna(df[alias])
            else:
                # Target absent for this batch of listings - promote the alias.
                df[canonical] = df[alias]

            drop_cols.append(alias)

        return df.drop(drop_cols, axis=1)

    def clean_city_sailboats_data(self, df, clean_up=[]):
        """
        Pass values to clean in as list
        """
        
        assert isinstance(df, pd.DataFrame), f'df argument must be a pd.DataFrame. Got {type(df)}.'
        # assert isinstance(clean_cols, list)
        # assert all(col in df.columns for col in clean_cols)

        # clean_cols = ['year manufactured',
        # 				'mfg_year','price', 
        # 				'id','datetime', 'last_updated',
        # 				'created','has_image',
        # 				'length overall (LOA)',
        # 				'engine hours (total)', 
        # 				'condition']
        
        for col in df.columns: 
            if col == 'year manufactured': # extract year from name
                years = df['name'].str.strip().str.extract(r'(?P<Year>\s{0,1}[1-2]\d{2,3}\s*)')
                df[col] = df[col].fillna(years.squeeze())
                # df[col] = pd.to_datetime(df[col]).dt.year
            elif col == 'price': # remove all special chars
                # pandas 2.0 made regex=False the default for Series.str.replace
                df[col] = (
                    df[col].astype(str)
                    .str.replace(r'[^\d.]', '', regex=True)
                    .replace('', pd.NA)
                    .astype(float)
                )
            elif col == 'id': # id as int
                df[col] = df[col].astype(int)
            elif col in ['datetime', 'last_updated','created']: # date as datetime
                df[col] = pd.to_datetime(df[col])
            elif col == 'has_image': # has image as bool 
                df[col] = df[col].astype(bool)
            elif col in ['length overall (LOA)','engine hours (total)']: # to float
                df[col] = df[col].astype(float)
                # [geotag, 'longitud total']

        # extract length from name
        # df['name'].str.strip().str.extract(r'(?P<Length>\d{2,3}\s*)')

        # remove records that don't make sense 
        # df['lengths'] = df['name'].str.extract(r'(\d{1,})', expand=True).reset_index(drop=True).astype(float)
        
        # drop dup cols
        return df.loc[:,~df.columns.duplicated()] 

    def prep_daily_sailboats_data(self):
    
        # current_df = craigslist_sailboats.get_city_items('keys')		
        download_time, current_df = self.get_all_daily_postings()
            
        attribute_df = self.expand_all_attributes(current_df['attrs'])
        expanded_df = pd.concat([current_df, attribute_df], axis=1).drop('attrs', axis=1)
        
        combined_df = self.combine_city_sailboats_data(expanded_df)
        cleaned_df = self.clean_city_sailboats_data(combined_df)
        
        # strip_cols = ['repost_of', 'name', 'url', 'where', 'body', 
        # 		  'condition', 'boat_propulsion_type', 'make / manufacturer', 
        # 		  'propulsion type', 'model name / number']
        # cleaned_df[strip_cols] = self.clean_str_columns(cleaned_df[strip_cols])
        
        stripped_df = self.strip_nan_columns(cleaned_df)
        
        return download_time, stripped_df

class Bikes(Search):
    """
    Parsing and cleaning for the 
    'bia' search category.
    """

    def combine_city_bike_data(self, df, eval_cols=()):
        """
        """

        pass

    def clean_city_bike_data(self, df, clean_up=[]):
        """
        """
        
        pass

    def prep_daily_bike_data(self):
        """
        """

        pass

class RVs(Search):
    """
    Parsing and cleaning functionality
    for the 'rva' search category.
    """

    def combine_city_rv_data(self, df, eval_cols=()):
        """
        """

        pass

    def clean_city_rv_data(self, df, clean_up=[]):
        """
        """

        pass

    def prep_daily_rv_data(self):
        """
        """

        pass


# let gpt observe the data and suggest 
# the appropriate code to handle


# to add a new class of search, simply 
# copy / paste the class template 
# there will be some trial / error 
# to get the aggregate search results
# formatted properly as it appears 
# craigslist does not enforce strict
# output standards. 



class Properties(Search):
    """
    Parsing and cleaning functionality
    for the 'properties' search category.
    """

    def combine_city_property_data(self, df, eval_cols=()):
        """
        """

        pass

    def clean_city_property_data(self, df, clean_up=[]):
        """
        """

        pass

    def prep_daily_property_data(self):
        """
        """

        pass

# to do: take best of github and incorporate it

# web app


# mapping 

# craigslist
# https://github.com/jccoulson/craigslist-price-tracker
# https://github.com/irahorecka/craigslist-housing-miner
# https://github.com/irahorecka/auto-craigslist-housing
# https://github.com/vadimsaroka/craigslist_scraper
# https://github.com/mjhea0/Scrapy-Samples
# https://github.com/gjreda/craigslist-checker

# data science
# https://github.com/ryanirl/CraigslistScraper