# ETL Pipeline

The **ETL Pipeline** performs several tasks, including: converting Jupyter notebooks and Python scripts to Markdown format, cleaning the code blocks in the Markdown files, removing unnecessary files and directories, and uploading the processed data to a Weaviate instance.

## Data Lake Builder

```gherkin
Feature: Data Lake Builder
  The data lake builder provides the ability to build a data lake from a git repository. It includes features for initializing parameters, creating a backup of existing data, cloning the git repository, and logging actions.

Background:
  Given a git repository URL
  And a directory where the data lake will be built
  And the current date and time

Scenario: Build a new data lake
  When the data lake directory does not exist
  Then the git repository is cloned into the new directory
  And the actions are logged into a log file

Scenario: Build a data lake when a directory with the same name already exists
  Given an existing directory with the same name as the data lake directory
  When the data lake builder is run
  Then the existing directory is moved to a backup directory
  And the git repository is cloned into the new directory
  And the actions are logged into a log file

Scenario: Handle errors during the data lake building process
  When an error occurs during the data lake building process
  Then the error is logged into the log file
```

## IPYNB to MyST Converter

```gherkin
Feature: IPYNB to MyST Converter
  The IPYNB to MyST converter provides the ability to convert Jupyter notebook (.ipynb) files to markdown (.md) files using the jupytext command line tool. It includes features for iterating over a directory of .ipynb files, converting them to .md files, logging conversion results, and handling errors and exceptions.

Background:
  Given a directory where the .ipynb files to be converted are located
  And the current date and time

Scenario: Convert .ipynb files to .md files
  When the IPYNB to MyST converter is run
  Then it iterates over the .ipynb files in the directory
  And it converts each .ipynb file to a .md file
  And it logs the result of each conversion into a log file

Scenario: Handle errors during the .ipynb to .md conversion process
  When an error occurs during the .ipynb to .md conversion process
  Then the error is logged into the log file
  And the error is added to the list of errors

Scenario: Handle exceptions during the .ipynb to .md conversion process
  When an exception occurs during the .ipynb to .md conversion process
  Then the exception is logged into the log file
  And the exception is added to the list of exceptions

Scenario: Write the total counts and lists of errors and exceptions to the log file
  When the IPYNB to MyST converter has finished running
  Then it writes the total number of files processed, successful conversions, errors, and exceptions to the log file
  And it writes the lists of errors and exceptions to the log file
```

## Py to MD Converter

```gherkin
Feature: Py to MD Converter
  The Py to MD converter provides the ability to convert Python (.py) files to markdown (.md) files using the jupytext command line tool. It includes features for iterating over a directory of .py files, converting them to .md files, logging conversion results, and handling errors and exceptions.

Background:
  Given a directory where the .py files to be converted are located
  And the current date and time

Scenario: Convert .py files to .md files
  When the Py to MD converter is run
  Then it iterates over the .py files in the directory
  And it converts each .py file to a .md file
  And it logs the result of each conversion into a log file

Scenario: Handle errors during the .py to .md conversion process
  When an error occurs during the .py to .md conversion process
  Then the error is logged into the log file
  And the error is added to the list of errors

Scenario: Handle exceptions during the .py to .md conversion process
  When an exception occurs during the .py to .md conversion process
  Then the exception is logged into the log file
  And the exception is added to the list of exceptions

Scenario: Write the total counts and lists of errors and exceptions to the log file
  When the Py to MD converter has finished running
  Then it writes the total number of files processed, successful conversions, errors, and exceptions to the log file
  And it writes the lists of errors and exceptions to the log file
```

## Non-MD File Deleter

```gherkin
Feature: Non-MD File Deleter
  The Non-MD File Deleter provides the ability to delete all non-Markdown (.md) files from a specified directory and its subdirectories. It includes features for iterating over a directory of files, deleting non-.md files, and handling exceptions.

Background:
  Given a directory from which non-.md files should be deleted
  And the current date and time

Scenario: Delete non-.md files
  When the Non-MD File Deleter is run
  Then it iterates over the files in the directory
  And it deletes each non-.md file
  And it logs the result of each deletion into a log file

Scenario: Handle exceptions during the deletion process
  When an exception occurs during the deletion process
  Then the exception is logged into the log file
  And the exception is added to the list of exceptions

Scenario: Write the total counts and list of exceptions to the log file
  When the Non-MD File Deleter has finished running
  Then it writes the total number of files processed, successful deletions, and exceptions to the log file
  And it writes the list of exceptions to the log file
```

## Empty Directory Remover

```gherkin
Feature: Empty Directory Remover
  The Empty Directory Remover provides the ability to remove all empty directories from a specified directory and its subdirectories. It includes features for traversing a directory, removing empty directories, and handling exceptions.

Background:
  Given a directory from which empty directories should be removed
  And the current date and time

Scenario: Remove empty directories
  When the Empty Directory Remover is run
  Then it traverses the directory
  And it removes each empty directory
  And it logs the result of each removal into a log file

Scenario: Handle exceptions during the removal process
  When an exception occurs during the removal process
  Then the exception is logged into the log file
  And the exception is added to the list of exceptions

Scenario: Write the total counts and list of exceptions to the log file
  When the Empty Directory Remover has finished running
  Then it writes the total number of directories processed, successful removals, and exceptions to the log file
  And it writes the list of exceptions to the log file
```

## Code Cleanup

```gherkin
Feature: Code Cleanup
  The Code Cleanup tool provides the ability to clean up the code in Markdown (.md) files within a specified directory and its subdirectories. It includes features for traversing a directory, cleaning up code in .md files, and handling exceptions.

Background:
  Given a directory where the .md files to be cleaned up are located
  And the current date and time

Scenario: Clean up code in .md files
  When the Code Cleanup tool is run
  Then it traverses the directory
  And it cleans up the code in each .md file using regular expressions
  And it logs the result of each cleanup operation into a log file

Scenario: Handle exceptions during the cleanup process
  When an exception occurs during the cleanup process
  Then the exception is logged into the log file
  And the exception is added to the list of exceptions

Scenario: Write the total counts and list of exceptions to the log file
  When the Code Cleanup tool has finished running
  Then it writes the total number of files processed, successful cleanups, and exceptions to the log file
  And it writes the list of exceptions to the log file
```

## Jupyter Text Remover

```gherkin
Feature: Jupyter Text Remover
  The Jupyter Text Remover provides the ability to remove Jupyter-specific text from Markdown (.md) files within a specified directory and its subdirectories. It includes features for traversing a directory, removing Jupyter-specific text in .md files, and handling exceptions.

Background:
  Given a directory where the .md files to be cleaned up are located
  And the current date and time

Scenario: Remove Jupyter-specific text from .md files
  When the Jupyter Text Remover is run
  Then it traverses the directory
  And it removes the Jupyter-specific text from each .md file using regular expressions
  And it logs the result of each removal operation into a log file

Scenario: Handle exceptions during the removal process
  When an exception occurs during the removal process
  Then the exception is logged into the log file
  And the exception is added to the list of exceptions

Scenario: Write the total counts and list of exceptions to the log file
  When the Jupyter Text Remover has finished running
  Then it writes the total number of files processed, successful removals, and exceptions to the log file
  And it writes the list of exceptions to the log file
```

## Data Upsertion

```gherkin
Feature: Data Upsertion
  The Data Upsertion tool provides the ability to upsert text data into a Weaviate instance from Markdown (.md) files within a specified directory and its subdirectories. It includes features for traversing a directory, cleaning up code in .md files, splitting text into chunks, and upserting data into Weaviate.

Background:
  Given a directory where the .md files to be cleaned up are located
  And the current date and time

Scenario: Clean up code in .md files
  When the Data Upsertion tool is run
  Then it traverses the directory
  And it removes certain patterns from the text in each .md file using regular expressions
  And it logs the result of each cleanup operation into a log file

Scenario: Split text into chunks
  Given cleaned up text from .md files
  When the text is split into chunks
  Then it uses the RecursiveCharacterTextSplitter to split the text into chunks
  And it logs the result of each split operation into a log file

Scenario: Upsert data into Weaviate
  Given chunks of text
  When the chunks are upserted into Weaviate
  Then it uses the Weaviate client to batch upsert the chunks into Weaviate
  And it logs the result of each upsert operation into a log file

Scenario: Handle exceptions during the cleanup, split, and upsert process
  When an exception occurs during the cleanup, split, or upsert process
  Then the exception is logged into the log file

Scenario: Write the total counts and list of exceptions to the log file
  When the Data Upsertion tool has finished running
  Then it writes the total number of files processed, successful cleanups, successful splits, successful upserts, and exceptions to the log file
```