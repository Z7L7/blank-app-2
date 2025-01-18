import streamlit as st
import gdelt 
import pandas as pd
import datetime

def gdelt_wrapper(country, keyword):
    crisis_cameo_codes = {
        "earthquake": ["0233"],  # Appeal for humanitarian aid
        "flood": ["0233", "0234"],  # Appeal for humanitarian aid, Appeal for military protection or peacekeeping
        "famine": ["0233"],  # Appeal for humanitarian aid
        "drought": ["0233"],  # Appeal for humanitarian aid
        "wildfire": ["0233"],  # Appeal for humanitarian aid
        "tornado": ["0233"],  # Appeal for humanitarian aid
        "hurricane": ["0233", "0234"],  # Appeal for humanitarian aid, Appeal for military protection
        "tsunami": ["0233"],  # Appeal for humanitarian aid
        "landslide": ["0233"],  # Appeal for humanitarian aid
        "volcanic eruption": ["0233"],  # Appeal for humanitarian aid
        "economic crisis": ["0231", "1031"],  # Appeal and Demand for economic aid
        "financial crisis": ["0231", "1031"],  # Appeal and Demand for economic aid
        "health crisis": ["0233"],  # Appeal for humanitarian aid
        "pandemic": ["0233", "0234"],  # Appeal for humanitarian aid, Appeal for military protection
        "epidemic": ["0233"],  # Appeal for humanitarian aid
        "civil unrest": ["145", "172"],  # Protest violently, Impose administrative sanctions
        "protests": ["143", "144"],  # Conduct strike or boycott, Obstruct passage
        "riots": ["145"],  # Protest violently
        "military conflict": ["190", "193", "195"],
        # Use conventional military force, Fight with small arms, Employ aerial weapons
        "war": ["190", "195", "200"],
        # Use conventional military force, Employ aerial weapons, Use unconventional mass violence
        "terrorist attack": ["1383", "180"],  # Threaten unconventional attack, Use unconventional violence
        "cyber attack": ["176"],  # Attack cybernetically
        "hostage situation": ["181"],  # Abduct, hijack, take hostage
        "kidnapping": ["181"],  # Abduct, hijack, take hostage
        "blockade": ["191"],  # Impose blockade
        "embargo": ["163"],  # Impose embargo, boycott, or sanctions
        "political instability": ["120", "130"],  # Reject, Threaten
        "martial law": ["1724"],  # Impose state of emergency or martial law
        "state of emergency": ["1724"],  # Impose state of emergency or martial law
        "environmental disaster": ["0233"],  # Appeal for humanitarian aid
        "chemical spill": ["2041"],  # Use chemical weapons
        "nuclear incident": ["2042"],  # Detonate nuclear weapons
        "biological threat": ["2041"],  # Use biological weapons
        "violent repression": ["175"],  # Use tactics of violent repression
        "ethnic cleansing": ["203"]  # Engage in ethnic cleansing
    }
    country_code = {
        'Afghanistan': 'AF',
        'Albania': 'AL',
        'Algeria': 'AG',
        'Antarctica': 'AY',
        'Antigua And Barbuda': 'AC',
        'Argentina': 'AR',
        'Australia': 'AS',
        'Austria': 'AU',
        'Azerbaijan': 'AJ',
        'Bahamas': 'BF',
        'Bahrain': 'BA',
        'Bangladesh': 'BG',
        'Barbados': 'BB',
        'Belize': 'BH',
        'Belgium': 'BE',
        'Benin': 'BN',
        'Bermuda': 'BD',
        'Bhutan': 'BT',
        'Bolivia': 'BL',
        'Bosnia-Herzegovina': 'BK',
        'Botswana': 'BW',
        'Brazil': 'BR',
        'Brunei': 'BX',
        'Bulgaria': 'BU',
        'Burundi': 'BY',
        'Cambodia': 'CB',
        'Cameroon': 'CM',
        'Canada': 'CA',
        'Chad': 'CD',
        'Chile': 'CI',
        'China': 'CH',
        'Colombia': 'CO',
        'Congo': 'CF',
        'Cook Islands': 'CW',
        'Cuba': 'CU',
        'Cyprus': 'CY',
        'Denmark': 'DA',
        'Djibouti': 'DJ',
        'Dominican Republic': 'DR',
        'Ecuador': 'EC',
        'Egypt': 'EG',
        'El Salvador': 'ES',
        'Eritrea': 'ER',
        'Estonia': 'EN',
        'Ethiopia': 'ET',
        'Finland': 'FI',
        'France': 'FR',
        'Gambia': 'GA',
        'Gaza Strip': 'GZ',
        'Germany': 'GM',
        'Ghana': 'GH',
        'Gibraltar': 'GI',
        'Greece': 'GR',
        'Grenada': 'GJ',
        'Guam': 'GQ',
        'Guatemala': 'GT',
        'Guinea': 'GV',
        'Guyana': 'GY',
        'Haiti': 'HA',
        'Honduras': 'HO',
        'Hong Kong': 'HK',
        'Hungary': 'HU',
        'India': 'IN',
        'Indonesia': 'ID',
        'Iran': 'IR',
        'Iraq': 'IZ',
        'Ireland': 'EI',
        'Israel': 'IS',
        'Italy': 'IT',
        'Jamaica': 'JM',
        'Japan': 'JA',
        'Jersey': 'JE',
        'Jordan': 'JO',
        'Kazakhstan': 'KZ',
        'Kenya': 'KE',
        'Kyrgyzstan': 'KG',
        'Laos': 'LA',
        'Latvia': 'LG',
        'Lebanon': 'LE',
        'Libya': 'LY',
        'Malawi': 'MI',
        'Malaysia': 'MY',
        'Maldives': 'MV',
        'Mali': 'ML',
        'Malta': 'MT',
        'Mauritania': 'MR',
        'Mexico': 'MX',
        'Moldova': 'MD',
        'Mongolia': 'MG',
        'Montenegro': 'MJ',
        'Morocco': 'MO',
        'Namibia': 'WA',
        'Nepal': 'NP',
        'Netherlands': 'NL',
        'New Zealand': 'NZ',
        'Nicaragua': 'NU',
        'Nigeria': 'NI',
        'Niue': 'NE',
        'North Korea': 'KN',
        'Norway': 'NO',
        'Pakistan': 'PK',
        'Palau': 'PS',
        'Panama': 'PM',
        'Papua New Guinea': 'PP',
        'Peru': 'PE',
        'Philippines': 'RP',
        'Poland': 'PL',
        'Portugal': 'PO',
        'Qatar': 'QA',
        'Rwanda': 'RW',
        'Saudi Arabia': 'SA',
        'Serbia': 'RI',
        'Singapore': 'SN',
        'South Africa': 'SF',
        'South Korea': 'KS',
        'South Sudan': 'OD',
        'Spain': 'SP',
        'Sri Lanka': 'CE',
        'Sudan': 'SU',
        'Sweden': 'SW',
        'Switzerland': 'SZ',
        'Syria': 'SY',
        'Taiwan': 'TW',
        'Tanzania': 'TZ',
        'Thailand': 'TH',
        'Tonga': 'TN',
        'Turkey': 'TU',
        'Turkmenistan': 'TX',
        'Uganda': 'UG',
        'Ukraine': 'UP',
        'United Arab Emirates': 'AE',
        'United Kingdom': 'UK',
        'United States': 'US',
        'Uzbekistan': 'UZ',
        'Venezuela': 'VE',
        'Vietnam': 'VM',
        'West Bank': 'WE',
        'Yemen': 'YM',
        'Zambia': 'ZA',
        'Zimbabwe': 'ZI'
    }

    try:
        # Query GDELT data
        results = gd2.Search([datetime.today().strftime('%Y %m %d')], table='events', coverage=False)

        if len(results) == 0:
            st.write("No results found.")
            return pd.DataFrame()

        filtered_df = pd.DataFrame(results)

        # Validate the keyword and country inputs
        if keyword not in crisis_cameo_codes:
            st.error(f"Keyword '{keyword}' not found in CAMEO mappings.")
            return pd.DataFrame()

        if country not in country_code:
            st.error(f"Country '{country}' not recognized.")
            return pd.DataFrame()

        # Check if the EventCode exists in the data
        matching_event_codes = filtered_df['EventCode'].isin(crisis_cameo_codes[keyword]).any()

        if matching_event_codes:
            # Filter by both country and event codes
            gdelt_df = filtered_df.loc[
                (filtered_df.ActionGeo_CountryCode == country_code[country]) &
                (filtered_df.EventCode.isin(crisis_cameo_codes[keyword]))
                ]

            if gdelt_df.shape[0] == 0:
                gdelt_df = filtered_df.loc[
                    (filtered_df.ActionGeo_CountryCode == country_code[country])
                ]
        else:
            # Filter only by country if no matching event codes
            gdelt_df = filtered_df.loc[
                (filtered_df.ActionGeo_CountryCode == country_code[country])
            ]

        # Return relevant columns
        gdelt_df[[
            'SOURCEURL', 'ActionGeo_FullName', 'CAMEOCodeDescription', 'GoldsteinScale',
            'Actor1Name', 'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode', 'NumMentions', 'NumArticles'
        ]].to_csv('gdelt.csv')
        return gdelt_df[[
            'SOURCEURL', 'ActionGeo_FullName', 'CAMEOCodeDescription', 'GoldsteinScale',
            'Actor1Name', 'Actor1CountryCode', 'Actor2Name', 'Actor2CountryCode', 'NumMentions', 'NumArticles'
        ]]
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return pd.DataFrame()

