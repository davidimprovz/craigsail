"""
Craigsail
multi-city search and asset price tracking
©2020 Improvz, Inc. All Rights Reserved.

https://github.com/juliomalegria/python-craigslist
"""
from pathlib import Path
import sqlite3
import pandas as pd
from craigslist import CraigslistForSale as clfs
from globals import CRAIGSLIST_CITIES, SALE_CATEGORIES, FILTER_OPTIONS

class Search():
    """
    Generic hooks for the python-craigslist 
    library. Combines that API with pandas 
    and database functionality. Subclass
    this class with one of the search 
    categories provided in the url string
    of any craigslist top-level category. 
    """

    def __init__(
        self, 
        search_category=None,
        data_path=None, 
        *cities, 
        **filters
    ):
        assert isinstance(search_category, str), f'search_category arg should be str. Got {type(search_category)}.'
        assert isinstance(data_path, str), f'data_path must be a string. Got {type(data_path)}.'
        assert Path(data_path).exists(), f'data_path must be a valid directory. Check and run again. {data_path}'

        self.FILTERS = {
            'search_titles':True,
            'has_image':True,
            'bundle_duplicates':True,
        }
        self.CITIES = []
        self.CATEGORY = search_category
        self.SAVE_PATH = Path(data_path)
        
        if len(filters): self.add_filters(**filters)
        if len(cities): self.update_cities(*cities)
    
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
            
    def add_cities(self, new_cities):
        """
        """
        self.CITIES = list(set(self.CITIES) | set(new_cities))
        
    def update_cities(self, new_cities):
        """
		new_cities must be a list of 
		cities that are available in the 
		list of CRAIGSLIST_CITIES.
		"""
		# to do: add a check to make sure 
		# city is an option in CRAIGSLIST_CITIES
        self.CITIES = list(set(new_cities))

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
        
        attr_list = [str(x).split(':') for x in attributes]
        attr_df = pd.DataFrame(attr_list).rename({0:'Attributes',1:'Values'}, axis=1)
        
        return attr_df.set_index('Attributes').T

    def expand_all_attributes(self, df):
        """
        Loop over a set of attributes and 
        call expand_attributes(), combining
        the results in a new df.
        """

        expanded = [self.expand_attributes(row) for _, row in df.iteritems()]
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
        city_items = clfs(site=city, category=self.CATEGORY, filters=self.FILTERS)
        for result in city_items.get_results(sort_by='newest', geotagged=True, include_details=True):
            results.append(result)
        city_df = self.convert_city_dict_to_df(city, results)

        return city_df 

    def get_all_daily_postings(self):

        all_items = list()
        
        start_time = pd.to_datetime('now')
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

        today = pd.to_datetime('today').strftime('%Y-%m-%d')
        save_path = self.SAVE_PATH.joinpath(''.join([filename, today, '.csv']))

        df.to_csv(save_path, index=False)

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

    def combine_city_sailboats_data(self, df, eval_cols=()):
        """
        pass values in as tuples instead of list
        """

        # combine_cols = ['mfg_year', 'año de fabricación',
        # 				'condición','horas del motor (en total)',
        # 				'marca / fabricante', 'nombre / número de modelo', 
        # 				'tipo de propulsión']

        drop_cols = list()
        for col in df.columns:
            if col == 'mfg_year':
                df.loc[:, 'year manufactured'] = df.loc[:, 'year manufactured'].fillna(df[col])
                drop_cols.append(col)
            elif col == 'año de fabricación': # merge all espanol records with english records
                df.loc[:, 'year manufactured'] = df.loc[:, 'year manufactured'].fillna(df[col])
                drop_cols.append(col)
            elif col == 'condición':	
                df.loc[:, 'condition'] = df.loc[:, 'condition'].fillna(df[col])
                drop_cols.append(col)
            elif col == 'horas del motor (en total)':
                df.loc[:, 'engine hours (total)'] = df.loc[:, 'engine hours (total)'].fillna(df[col])
                drop_cols.append(col)
            elif col == 'marca / fabricante':
                df.loc[:, 'make / manufacturer'] = df.loc[:, 'make / manufacturer'].fillna(df[col])
                drop_cols.append(col)
            elif col == 'nombre / número de modelo':
                df.loc[:, 'model name / number'] = df.loc[:, 'model name / number'].fillna(df[col])
                drop_cols.append(col)
            elif col == 'tipo de propulsión':
                df.loc[:, 'boat_propulsion_type'] = df.loc[:, 'boat_propulsion_type'].fillna(df[col])
                drop_cols.append(col)

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
                df[col] = df[col].str.replace('\$|,', '').astype(float)
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