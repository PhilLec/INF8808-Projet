# import module
from numpy import integer
import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean
import numpy as np  
from datetime import date
# read CSV file


  
# count no. of lines
# print("Number of lines present:-", 
#       len(results))

# max=results['Maximum Draugth'].max()
# min=results['Maximum Draugth'].min()

# print('max', max)
# print('min', min)
# print('mean', mean(results['Maximum Draugth']))

# plt.hist(results['Maximum Draugth'],  edgecolor='black', bins=range(int(min), int(max), 1))
# plt.ylabel('Nombre de trajet')
# plt.xlabel("Tirant d'eau du navire (m)")
# plt.show()


#map ship types
trip = pd.read_csv('src/assets/data/TRIP_Cleaned.csv')
# correspondance = pd.read_csv('src/assets/data/Vessel Type Class.csv')

def mapShips(shipType):
      if (shipType in ['Barge Bulk Cargo', 'Barge Chemical','Barge Chips','Barge Derrick','Barge General','Barge Log','Barge Miscellaneous','Barge Oil Drilling Rig', 'Barge Oil/Petroleum', 'Barge Rail/Trailer','Barge Self-Propelled','Barge Towed',"Don't use",'Landing Craft','Logs Raft Section']):
            return 'Barges'
      elif (shipType in ['Excursion Passenger']):
            return 'Excursion'
      elif (['Crab Boat', 'Dragger (Scallop, Clam, etc.)', 'Factory Ship', 'Fishery Patrol', 'Fishing Vessel', 'Gillnetter', 'Groundfish Boat (Open Boat)', 'Lobster Boat', 'Longliner', 'Other Fishing VSL (Open Boat)', 'Seiner', 'Shrimp Boat', 'Trawler', 'Troller']):
            return 'Fishing'
      elif (shipType in ['Cruise', 'Merchant (Dry)', 'Merchant Auto', 'Merchant Bulk', 'Merchant Cement', 'Merchant Coastal', 'Merchant Container', 'Merchant Ferry', 'Merchant General', 'Merchant Lash', 'Merchant Livestock', 'Merchant Ore', 'Merchant Passenger', 'Merchant Rail/Trailer Ferry', 'Merchant Reefer', 'Merchant RO/RO']):
            return 'Merchant'
      elif (shipType in ['Yacht - Pleasure Crafts', 'Yacht Power', 'Yacht Sails']):
            return 'Pleasure Crafts'
      elif(shipType in ['Merchant (Tanker)', 'Merchant Chemical', 'Merchant Chemical/Oil Products Tanker','Merchant Crude','Merchant Gasoline','Merchant Liquified Gas','Merchant Molasses','Merchant Ore/Bulk/Oil','Merchant Super Tanker','Merchant ULCC','Merchant VLCC','Merchant Water']):
            return 'Tanker'
      elif (shipType in ['Tug', 'Tug Fire', 'Tug Harbour', 'Tug Ocean', 'Tug Supply', 'Tugs Workboat']):
            return 'Tugs'
      else :
            return 'Other'


groupes_classes = map(mapShips,trip[:,7])


# Add a list as column
#add_column_in_csv('data/TRIP_Cleaned.csv', 'data/TRIP_Grouped.csv', lambda row, line_num: row.append(groupes_classes[line_num - 1]))
# https://thispointer.com/python-add-a-column-to-an-existing-csv-file/

def convertfromDate(date):
      day = int(date[0:2])
      month = int(date[3:5])
      year = int(date[6:10])
      d0 = date(2011,1,1)
      d1 = date(year,month,day)
      delta = d1-d0
      return(delta.days)

def convertToDate(N):
      d0 = date(2011,1,1)
      d1 = d0+N
      return d1

def typeToCol(shipType):
      if shipType == 'Barges':
            return 1
      elif shipType == 'Excursion':
            return 2
      elif shipType == 'Fishing':
            return 3
      elif shipType == 'Merchant':
            return 4
      elif shipType == 'Pleasure Crafts':
            return 5
      elif shipType == 'Tanker':
            return 6
      elif shipType == 'Tugs':
            return 7
      elif shipType == 'Other':
            return 8


def counter(tripList):
      tab = np.zeroes(3650,9)
      for i in range(3650):
            tab[i,0] = convertToDate(i)
      for line in tripList:
            start = convertfromDate(line[1])
            stop = convertfromDate(line[4])
            col = typeToCol(line[7])
            for j in range(start,stop):
                  tab[j,col] +=1
