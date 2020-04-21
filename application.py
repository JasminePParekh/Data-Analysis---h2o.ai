#!/usr/bin/env python
# coding: utf-8
import click
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dt
import matplotlib.lines as mlines
import sys


def runRegex(file):
  ''' Data Gathering Stage - Regex through log file
  Regex lines provided will take file given by user and capture important information. 
  Each regex line (4 in total) will capture different information and convert it into 4 different dataframes - df_one, df_two, df_three, df_four

  @param: file - directory pathway for specific log file the user wishes to analyze - obtained from cli input
  @type: String

  @return: df_one, df_two, df_three, df_four
  
  *df_one: contains all basic info from lines of the log file such as cpu memory, io, cpu utilization, etc. - primaraily used for graphing 
  *df_two: contains all instances of iteration starts within the log file - used for iteration annotation
  *df_three: contains all instances of mutations such as the start and end of mutations - used for mutation annotation
  *df_four: contains all instances of experiments such as the start and end of experiments - used for experiment annotation
  
  '''

  log_file_path = file
  log_file_bool = False

  regex = '(\d{4}-.+\d{2} .+\d{2}),.*D:(.+) M:(.+) \d+ [A-Z]+  : Ping from experiment (\w+). CPU memory usage: (.+), max: (.+) CPU: \s* (\d+)% Procs:.*GPU memory usage: (.+), max: (.+) GPUs usage:.*(\d+)% OpenFiles:\s*(\d+)\/\s*\d+'
  regexTwo = '(\d{4}-.+\d{2} .+\d{2}),\d{3}.*Starting Iteration: (\d.*)'
  regexThree = '(\d{4}-.+\d{2} .+\d{2}),\d{3}.*DEBUG  : (.*): (Duration|mutation_rate).*\.'
  regexFourA = '(\d{4}-.+\d{2} .+\d{2}),\d{3}.*: Temporary directory:.*experiment_(.*)'
  regexFourB = '(\d{4}-.+\d{2} .+\d{2}),\d{3}.*: Experiment (.*) FINISHED'

  read_line = True

  name_list = ["date-time", "disk-space", "memory", "experiment","cpu-memory", "cpu-max", "cpu-usage","gpu-memory", "gpu-max", "gpu-usage", "io"]
  name_two_list = ["date-time", "iteration-number"]
  name_three_list = ["date-time", "mutation-stage"]
  name_four_list = ["date-time", "experiment"]
  try:
    with open(log_file_path, "r") as file:
      match_list = []    
      match_list2 = []
      match_list3 = []
      match_list4 = []

      if read_line == True:
        for line in file:
          for match in re.finditer(regex, line):
            log_file_bool = True;
            list = []
            for a in range(0,11):
              list.append(match.group(a+1))
            match_list.append(list) 

          for match in re.finditer(regexTwo, line):
            list = []
            for a in range(0,2):
              list.append(match.group(a+1))
            match_list2.append(list) 

          for match in re.finditer(regexThree, line):
            list = []
            for a in range(0,2):
              list.append(match.group(a+1))
            match_list3.append(list)
          for match in re.finditer(regexFourA, line):
            list = []
            for a in range(0,2):
              if(a == 1):
                list.append(match.group(a+1) + ' Start')
              else:
                list.append(match.group(a+1))
            match_list4.append(list)
          for match in re.finditer(regexFourB, line):
            list = []
            for a in range(0,2):
              if(a == 1):
                list.append(match.group(a+1) + ' End')
              else:
                list.append(match.group(a+1))
            match_list4.append(list)


    df_one = pd.DataFrame(match_list,columns=name_list)
    df_two = pd.DataFrame(match_list2,columns=name_two_list)
    df_three = pd.DataFrame(match_list3,columns=name_three_list)
    df_four = pd.DataFrame(match_list4,columns=name_four_list)
    file.close()
  except FileNotFoundError:
    click.echo('FileNotFoundError')
    sys.exit('ERROR: Please provide a valid log file pathway')
  if log_file_bool == False:
    click.echo('Not a log file')
    sys.exit('ERROR: Please provide a valid log file')
  else:
    return df_one, df_two, df_three, df_four

def reformat(df_one, df_two, df_three, df_four):
  '''Intermediary Stage - Preparing dataframes for graphing
  
  Converts "cpu memory" data from string to float and then from MB, GB, or TB to just MB - in df_one
  Converts "io" data from string to integer - in df_one
  Converts "cpu usage" data from string to integer - in df_one
  Converts "date and time" data from string to datetime - in df_one, df_two, df_three, df_four

  @param: df_one
  @type: pandas dataframe
  @param: df_two
  @type: pandas dataframe
  @param: df_three
  @type: pandas dataframe
  @param: df_four
  @type: pandas dataframe

  @return: df_one, df_two, df_three, df_four

  *all formatted to correct object types for graphing
  
  '''
  df_one['cpu-memory-new'] = df_one['cpu-memory'].astype(str).str[:-2].astype(np.float64)
  df_one.loc[df_one['cpu-memory'].str.contains("GB"),'cpu-memory-new'] = df_one['cpu-memory-new']*1000
  df_one.loc[df_one['cpu-memory'].str.contains("TB"),'cpu-memory-new'] = df_one['cpu-memory-new']*1000000
  df_one['io'] = df_one['io'].astype(int)
  df_one['cpu-usage'] = df_one['cpu-usage'].astype(int)
  df_one['date-time'] = pd.to_datetime(df_one['date-time'], format="%Y-%m-%d %H:%M:%S")
  df_one['date-time-num']= dt.date2num(df_one['date-time'])

  df_two['date-time'] = pd.to_datetime(df_two['date-time'], format="%Y-%m-%d %H:%M:%S")
  df_two['date-time-num']= dt.date2num(df_two['date-time'])

  df_three['date-time'] = pd.to_datetime(df_three['date-time'], format="%Y-%m-%d %H:%M:%S")
  df_three['date-time-num']= dt.date2num(df_three['date-time'])

  df_four['date-time'] = pd.to_datetime(df_four['date-time'], format="%Y-%m-%d %H:%M:%S")
  df_four['date-time-num']= dt.date2num(df_four['date-time'])
  
  return df_one, df_two, df_three, df_four


def graph(df_one, df_two, df_three, df_four):
  '''Plotting Stage - three plots graphed  
  Three plots are created, annotated, saved as .png files (in the same location as this file) for later use, 
  and showed to the user temporarily for dynamic use

  @param: df_one
  @type: pandas dataframe
  @param: df_two
  @type: pandas dataframe
  @param: df_three
  @type: pandas dataframe
  @param: df_four
  @type: pandas dataframe

  @return: df_one, df_two, df_three, df_four
  
  *all passed on for graph annotation

  ''' 
  plt.figure(figsize=(15, 5))
  plt.plot(df_one['date-time'], df_one['cpu-memory-new'], marker = 'o')
  plt.suptitle('Cpu Memory Utilization vs. Time', fontsize = 14, fontweight = 'bold')
  plt.xlabel('Time')
  plt.ylabel('Cpu Memory Usage (MB)')
  annotate(df_one, df_two, df_three, df_four)
  plt.savefig('cpu_memory_vs_time.png')
  plt.show()
  
  plt.figure(figsize=(15, 5))
  plt.plot(df_one['date-time'], df_one['io'], marker = 'o')
  plt.suptitle('Number of Opened Files vs. Time', fontsize = 14, fontweight = 'bold')
  plt.xlabel('Time')
  plt.ylabel('Number of Opened Files (files)')
  annotate(df_one, df_two, df_three, df_four)
  plt.savefig('io_vs_time.png')
  plt.show()

  
  plt.figure(figsize=(15, 5))
  plt.plot(df_one['date-time'], df_one['cpu-usage'], marker = 'o')
  plt.suptitle('Cpu Utilization vs. Time', fontsize = 14, fontweight = 'bold')
  plt.xlabel('Time')
  plt.ylabel('Cpu Usage (%)')
  annotate(df_one, df_two, df_three, df_four)
  plt.savefig('cpu_usage_vs_time.png')
  plt.show()

  return df_one, df_two, df_three, df_four


def annotate(df_one, df_two, df_three, df_four):
  '''Annotation Stage - annotating interesting events onto the graphs
  Legend is created to help user identify interesting events plotted 
  Annotation are made by vertical line to indicate point in time where event as occured
    Iterations have a number attached to the line to indicate the specific iteration number of this event
    Experiments have a name and stage indicator attached to the line to identify which experiment and what stage (start or end) it is at
    Mutations are either green or red lines that indicate mutation start and mutation end, respectively

    @param: df_one
    @type: pandas dataframe
    @param: df_two
    @type: pandas dataframe
    @param: df_three
    @type: pandas dataframe
    @param: df_four
    @type: pandas dataframe

    @return: None

  ''' 
  experiment_line = mlines.Line2D([], [], color='black', linestyle ='-',markersize=15, label='Experiment')
  iteration_line = mlines.Line2D([], [], color='black', linestyle =':',markersize=15, label='Starting Iteration (Iteration # labeled on graph)')
  mutation_start_line = mlines.Line2D([], [], color='green', linestyle ='--',markersize=15, label='Mutation Start')
  mutation_end_line = mlines.Line2D([], [], color='red', linestyle ='--',markersize=15, label='Mutation End')
   
  xmin, xmax, ymin, ymax = plt.axis()
  for i in range(0,len(df_four)):
      x_line_annotation = df_four['date-time-num'][i]
      x_text_annotation = df_four['date-time-num'][i]
      plt.axvline(x=x_line_annotation, linestyle='-', alpha=0.5, color='black')
      plt.text(x=x_text_annotation, y=ymax*2/3, s= df_four['experiment'][i], alpha=0.7, backgroundcolor = 'black',horizontalalignment ='center', color='yellow')

  for i in range(0,len(df_three)):
      x_line_annotation = df_three['date-time-num'][i]
      x_line_annotationn = df_three['date-time-num'][i]
      x_text_annotation = df_three['date-time-num'][i]
      if(df_three['mutation-stage'][i] == 'mutating'):
          plt.axvline(x=x_line_annotation, linestyle = '--',alpha=0.5, color='green')
      if(df_three['mutation-stage'][i] == 'end mutating'):
          plt.axvline(x=x_line_annotation, linestyle='--', alpha=0.5, color='red')
  for i in range(0,len(df_two)):
      x_line_annotation = df_two['date-time-num'][i]
      x_text_annotation = df_two['date-time-num'][i]
      plt.axvline(x=x_line_annotation, linestyle=':', alpha=0.5, color='black')
      plt.text(x=x_text_annotation, y=ymax*1/4, s= df_two['iteration-number'][i], alpha=0.7, backgroundcolor = 'black',horizontalalignment ='center', color='cyan')
      plt.legend(handles=[experiment_line, iteration_line, mutation_start_line, mutation_end_line], loc = 'best')
      
  #mplcursors.cursor().connect("add", lambda sel: sel.annotation.set_text(df_one['date-time'][sel.target.index]))  
