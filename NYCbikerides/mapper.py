#!/usr/bin/python
  
# import sys because we need to read and write data to STDIN and STDOUT
import sys
import csv
  
# reading entire line from STDIN (standard input)
reader = csv.reader(sys.stdin, delimiter=',')
for line in reader:
    
    # split the line into values
    #ride_id, rideable_type, started_at, ended_at, start_station_name, start_station_id, end_station_name, end_station_id, start_lat, start_lngend_lat, end_lng, member_casual = line
    #if(len(line) == 13)
    start_station_name = line[4]
    #words = line.split()
      
    # we are looping over the words array and printing the word
    # with the count of 1 to the STDOUT
    #for word in words:
        # write the results to STDOUT (standard output);
        # what we output here will be the input for the
        # Reduce step, i.e. the input for reducer.py
    print('%s\t%s' % (start_station_name, 1))