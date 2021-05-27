# -*- coding: utf-8 -*-
"""
Created on Thu May 27 13:33:54 2021

@author: corber
"""


# -- Patterns for rules based topic classification --


#Exceptions - catching these before they can be incorrectly picked up by another pattern
patterns_exceptions = [
[{'LEMMA': 'social'}, {'LEMMA': 'work'}, ],
[{'LEMMA': 'social'}, {'LEMMA': 'worker'}, ],
[{'LEMMA': 'public'}, {'LEMMA': 'house'}, ],
    ]


#Census
patterns_census = [
[{'LEMMA': 'census'}]
    ]

#Health
patterns_health = [
[{'LOWER': 'nhs'}], #NHS acronym
[{'LOWER': 'gp'}], #GP acronym
[{'LEMMA': 'health'}],
[{'LEMMA': 'healthcare'}],
[{'LEMMA': 'hospital'}],
[{'LEMMA': 'illness'}],
[{'LEMMA': 'sick'}],
[{'LEMMA': 'cancer'}],
[{'LEMMA': 'care'}],
[{'LEMMA': 'disease'}],
[{'LEMMA': 'disabled'}],
[{'LEMMA': 'disability'}],
[{'LEMMA': 'vaccinate'}],
[{'LEMMA': 'vaccination'}],
[{'LEMMA': 'medicine'}],
[{'LEMMA': 'treatment'}],
[{'LEMMA': 'treat'}],
    ]

#COVID-19 - not in 2015-2019 dataset

#Population and Migration
patterns_popmigration = [
[{'LEMMA': 'migration'}],
[{'LEMMA': 'migrant'}],
[{'LEMMA': 'immigrant'}],
[{'LEMMA': 'immigration'}],
[{'LEMMA': 'population'}],
[{'LEMMA': 'refugee'}],
[{'LEMMA': 'visa'}],
    ]


#Economy
patterns_economy = [
[{'LOWER': 'gdp'}], #GDP acronym
[{'LEMMA': 'sme'}], #SME acronym
[{'LEMMA': 'economy'}],
[{'LEMMA': 'borrow'}],
[{'LEMMA': 'finance'}],
[{'LEMMA': 'goods'}],
[{'LEMMA': 'trade'}],
[{'LEMMA': 'product'}],
[{'LEMMA': 'business'}],
[{'LEMMA': 'tourism'}],
[{'LEMMA': 'market'}],
[{'LEMMA': 'export'}],
[{'LEMMA': 'import'}],
[{'LEMMA': 'industry'}],
    ]

#Labour Market
patterns_labourmarket = [
[{'LEMMA': 'job'}],
[{'LEMMA': 'employment'}],
[{'LEMMA': 'employee'}],
[{'LEMMA': 'employer'}],
[{"LEMMA": "work"}],
[{'LEMMA': 'worker'}],
[{'LEMMA': 'redundancy'}],
    ]

#Crime
patterns_crime = [
[{'LEMMA': 'crime'}],
[{'LEMMA': 'criminal'}],
[{'LEMMA': 'police'}],
[{'LEMMA': 'prison'}],
[{'LEMMA': 'prisoner'}],
[{'LEMMA': 'court'}],
[{'LEMMA': 'offence'}],
[{'LEMMA': 'prosecution'}],
[{'LEMMA': 'criminal'}],
[{'LEMMA': 'offender'}],
[{'LEMMA': 'sentence'}],
[{'LEMMA': 'sentencing'}],
[{'LEMMA': 'domestic'}, {'LEMMA': 'violence'}],
[{'LEMMA': 'witness'}],
[{'LEMMA': 'stop'}, {'LEMMA': 'and'}, {'LEMMA': 'search'}],
    ]


#Environment
patterns_environment = [
[{'LEMMA': 'environment'}],
[{'LEMMA': 'climate'}],
[{'LEMMA': 'green'}],
[{'LEMMA': 'carbon'}],
[{'LEMMA': 'fossil'}],
[{'LEMMA': 'oil'}],
[{'LEMMA': 'gas'}],
[{'LEMMA': 'electric'}],
[{'LEMMA': 'coal'}],
[{'LEMMA': 'solar'}],
[{'LEMMA': 'wind'}],
[{'LEMMA': 'energy'}],
[{'LEMMA': 'nature'}],
[{'LEMMA': 'natural'}],
[{'LEMMA': 'recycle'}],
[{'LEMMA': 'fly'}, {'LEMMA': '-'}, {'LEMMA': 'tipping'}],
    ]

#Inequalities/Wellbeing
patterns_inequalwellbeing = [
[{'LOWER': 'lgbt'}], #acronym LGBT
[{'LOWER': 'bme'}], #acronym BME
[{'LOWER': 'bame'}], #acronym BAME
[{'LEMMA': 'equal'}],
[{'LEMMA': 'equality'}],
[{'LEMMA': 'wellbeing'}],
[{'LEMMA': 'minority'}],
[{'LEMMA': 'gender'}],
[{'LEMMA': 'ethnic'}],
[{'LEMMA': 'ethnicity'}],
    ]

# Education
patterns_education = [
[{'LEMMA': 'school'}],
[{'LEMMA': 'education'}],
[{'LEMMA': 'educate'}],
[{'LEMMA': 'teacher'}],
[{'LEMMA': 'teach'}],
[{'LEMMA': 'learn'}],
[{'LEMMA': 'pupil'}],
[{'LEMMA': 'student'}],
[{'LEMMA': 'college'}],
[{'LEMMA': 'university'}],
    ]

# Transport
patterns_transport = [
[{'LOWER': 'main'}, {'LOWER': 'line'}],
[{'LEMMA': 'transport'}],
[{'LEMMA': 'transportation'}],
[{'LEMMA': 'rail'}],
[{'LEMMA': 'train'}],
[{'LEMMA': 'railway'}],
[{'LEMMA': 'bus'}],
[{'LEMMA': 'plane'}],
[{'LEMMA': 'airplane'}],
[{'LEMMA': 'airport'}],
[{'LEMMA': 'fly'}],
[{'LEMMA': 'road'}],
[{'LEMMA': 'motorway'}],
[{'LEMMA': 'car'}],
[{'LEMMA': 'drive'}]
    ]

# Defence

patterns_defence = [
[{'LOWER': 'raf'}], #acronym - RAF
[{'LOWER': 'armed'}, {'LOWER': 'forces'}],
[{'LOWER': 'air'}, {'LOWER': 'force'}],
[{'LEMMA': 'defence'}],
[{'LEMMA': 'war'}],
[{'LEMMA': 'army'}], 
[{'LEMMA': 'navy'}],
[{'LEMMA': 'soldier'}],
[{'LEMMA': 'veteran'}],
[{'LEMMA': 'military'}],
[{'LEMMA': 'security'}],
[{'LEMMA': 'cyber'}],
[{'LEMMA': 'intelligence'}],
[{'LEMMA': 'warhead'}],
    ]


# Foreign Policy

patterns_foreignpolicy = [
[{'LOWER': 'eu'}], #acronym - EU
[{'LEMMA': 'european'}, {'LEMMA': 'union'}],
[{'LEMMA': 'europe'}],
[{'LEMMA': 'withdrawal'}], #i.e. Withdrawal Agreement
[{'LEMMA': 'foreign'}],
    ]
#can use ENT: GPE to identify locations - but need to exclude domestic locations, how to do this?

# Housing

patterns_housing = [
[{'LEMMA': 'house'}],
[{'LEMMA': 'housing'}],
[{'LEMMA': 'landlord'}],
[{'LEMMA': 'tenant'}],
[{'LEMMA': 'rent'}],
[{'LEMMA': 'let'}],
[{'LEMMA': 'mortgage'}],
[{'LEMMA': 'tenant'}],
[{'LEMMA': 'accommodation'}],
    ]

# Tax & Public Spending

patterns_taxspend= [
[{'LEMMA': 'spending'}],
[{'LEMMA': 'tax'}],
[{'LEMMA': 'taxation'}],
[{'LEMMA': 'welfare'}],
[{'LEMMA': 'benefit'}],
    ]

