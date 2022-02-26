{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Weather API processing"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "In this project, I will construct a Workflow to process the weather extracted data using API to query the data for different cities as well as provide analytical dataset as per the requirements"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The data source is from https://openweathermap.org/"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Project Architecture"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "I used Python to build my whole project and stored data using Postgres. My whole project was built on windows so anyone would like to use the docker image should still use windows otherwise reading the files/directories may not work"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "My work has been summarized as below:\n",
    "1. First, I create account on Openweather, it tooks a while till my account got activated.\n",
    "2. I found the API to query the 5 last days taking only co-ordinates. I wanted some conveniance so I created a module that taked the popular cities name and return the co-ordinates. For this I used geopy library. I save those values for later use when I run the API\n",
    "3. I then constructed a list of timestamp so I loop over to query several days calls as the API can return only 1 day hourly data\n",
    "4. Now my data is ready so I used them to construct the APIs and the response content got stored in the staging_data folder\n",
    "5. I then process each JSON and store the information I found needed later in the database. I faced one issue that the timezone where not storing properly which would affect my calculation later so I have altered the whole DB time zone to be UTC\n",
    "6. Last step is to construct the 2 required dataset, I developed the queries first and tested on the PgAdmin and then automate the run within the main program script."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The folder Structure:"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Project Output"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "2 Datasets were required as part of the project delivery"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Dataset 1"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A dataset containing the location, date and temperature of the highest temperatures reported by location and month."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The dataset was executed as part of the main program and can be availble in the dataset1_data directory"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Dataset 2"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "A dataset containing the average temperature, min temperature, location of min temperature, and location of max temperature per day."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "The dataset was executed as part of the main program and can be availble in the dataset2_data directory"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
