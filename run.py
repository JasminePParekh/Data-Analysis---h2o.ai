#!/usr/bin/env python
# coding: utf-8

import click
import application as app

@click.group()
def main():
	pass

@main.command()
@click.argument('file')

def graph(file):
	'''Driver for this script
	1. Run regex on log file provided by user to create dataframes
	2. Dataframes reformatted to be suitable for graphing
	3. Three graph with annotations are produced and saved for the user

	@param: file - directory pathway for specific log file the user wishes to analyze - obtained from cli input
  	@type: String

  	@return: None

  	@generates: Three dynamic graphs

  	@saves: Three .png files of the graphs
	'''
	df_one, df_two, df_three, df_four = app.runRegex(file)
	df_one, df_two, df_three, df_four = app.reformat(df_one, df_two, df_three, df_four)
	df_one, df_two, df_three, df_four= app.graph(df_one, df_two, df_three, df_four)
	click.echo('Graph Done')

if __name__ == '__main__':
	main()