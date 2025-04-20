import pandas as pd
import streamlit as st 

violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')

def top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    #Create a pivot table to sum the amount of violations by location
    amount_by_location = violations_df.pivot_table(
        index='location',
        values='amount',
        aggfunc='sum'
    ).sort_values(by='amount', ascending=False)

    #setting location equal to the index
    amount_by_location['location'] = amount_by_location.index

    #reset the index
    amount_by_location.reset_index(drop=True, inplace=True)

    #return any rows that meet the threshold
    return amount_by_location[amount_by_location['amount'] >= threshold]


def top_locations_mappable(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    #Get the top locations
    top_locations_df = top_locations(violations_df, threshold)

    #Get the lat and lon columns
    violations_pre_merge_df = violations_df[['location', 'lat', 'lon']].drop_duplicates(subset=['location'])

    #convert location to string
    top_locations_df['location'] = top_locations_df['location'].astype(str)
    violations_pre_merge_df['location'] = violations_pre_merge_df['location'].astype(str)

    #Merge the top locations with the lat and lon columns
    merged = pd.merge(top_locations_df, violations_pre_merge_df, on='location', how='left')

    return merged.drop_duplicates()


def tickets_in_top_locations(violations_df : pd.DataFrame, threshold=1000) -> pd.DataFrame:
    #Get the top locations
    top_locations_df = top_locations(violations_df)

    #convert location to string
    top_locations_df['location'] = top_locations_df['location'].astype(str)
    violations_df['location'] = violations_df['location'].astype(str)

    #Merge the top locations with the violations data
    merged = pd.merge(top_locations_df[['location']], violations_df, on='location')

    #Return the merged data
    return merged


if __name__ == '__main__':
    '''
    Main ETL job. 
    '''
    st.write("Running ETL job...")
    st.write("Reading violations data from ./cache/final_cuse_parking_violations.csv")
    violations_df = pd.read_csv('./cache/final_cuse_parking_violations.csv')
    top_locations_df = top_locations(violations_df)
    st.write("Writing top locations to ./cache/top_locations.csv")
    top_locations_df.to_csv('./cache/top_locations.csv', index=False)
    top_locations_mappable_df = top_locations_mappable(violations_df)
    st.write("Writing mappable top locations to ./cache/top_locations_mappable.csv")
    top_locations_mappable_df.to_csv('./cache/top_locations_mappable.csv', index=False)
    tickets_in_top_locations_df = tickets_in_top_locations(violations_df, top_locations_df)
    st.write("Writing tickets in top locations to ./cache/tickets_in_top_locations.csv")
    tickets_in_top_locations_df.to_csv('./cache/tickets_in_top_locations.csv', index=False)

    st.write("Top locations:")
    st.dataframe(top_locations_df)
    st.write("Top locations mappable:")
    st.dataframe(top_locations_mappable_df)
    st.write("Top locations:")
    st.dataframe(tickets_in_top_locations_df)