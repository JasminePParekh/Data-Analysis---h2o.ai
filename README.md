# H2O Internship Project - Log File Analysis
###### By Jasmine Parekh 


#### To Run Data Analysis

- Open zip file (h2oPackage.zip)
- To run the CLI, go to the terminal and change directory to h2oPackage
```Linux
cd /Users/jasmineparekh/Desktop/h2oPackage
```

- To install all the dependencies needed for the program to run successfully
```Linux
python setup.py develop
```

- Now, you can run the program using this command
```Linux
python run.py graph /Users/jasmineparekh/Downloads/h2oPackage/h2oai_server_anonymized.log
```

#### To Run Unit Tests

-To run the unit test file (test_cli.py) make sure you are in the h2oPackage directory and then type the following command
```Linux
py.test
```

#### Quick Facts

- Graphs will be saved in the same host folder after the program has finished running

- Graphs produced on your screen are interactable. You can zoom and move around the graph to get a better view of things

- Annotations are the vertical lines made over the graph. Their color or pattern can be used with the legend to find out what the annotation means





