"""
This file contains functions that analyze and plot
the data in the PayScale and BLS datasets
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Question 1 :What are the fastest growing and declining
# occupations in the next coming years ?


def plot_employment_growth(data):
    # Employment Change 2019 - 29, potential number of jobs
    # that will be added in the from 2019 - 2029

    growing_job = data.sort_values('Employment Change, 2019-29',
                                   ascending=False).head(10)

    job_name_employment = list(growing_job['occupation_name'])
    Employment_growth = list(growing_job['Employment Change, 2019-29'])

    fig, ax = plt.subplots(figsize=(10, 10))

    plt.bar(job_name_employment, Employment_growth)
    plt.xticks(rotation=270)
    plt.title('Top 10 Careers with Largest Number of Job Growth')
    plt.ylabel('Number of Job Grow')
    plt.tick_params(axis="x", labelsize=12)
    plt.tight_layout()
    plt.savefig('Employment_growth_plot')


def plot_employment_decline(data):
    # The fastest declinging job depending on the number of job
    # oppotunities that will disappear between year 2019 - 2029
    declining_job = data.sort_values('Employment Change, '
                                     '2019-29').head(10)

    job_name_decline = declining_job['occupation_name'].tolist()
    Employment_decline = data['Employment Change, 2019-29'].tolist()
    Employment_decline = sorted(Employment_decline, reverse=True)

    fig, ax = plt.subplots(figsize=(10, 10))

    plt.bar(job_name_decline, declining_job['Employment Change, 2019-29'])
    plt.xticks(rotation=270)
    plt.title('Top 10 Careers with Largest Number of Job Decline')
    plt.ylabel('Number of Job Will Disappear')
    plt.tight_layout()

    plt.savefig('Employment_decline_plot')


def plot_job_outlook(data):
    # Job Outlook 2019-29 represent the growth rate of the job in
    # from 2019 - 2029, the ones higher percentage represent the
    # faster growing rate

    # pre data wrangling for the testing, delete all strings
    # in Job Outlook, 2019-29 column
    data['Job Outlook, 2019-29'] = data['Job Outlook, '
                                        '2019-29'].str.replace(r' \(.*\)', '')

    data['Job Outlook, 2019-29'] = data['Job Outlook, '
                                        '2019-29'].str.replace('%', '')

    data['Job Outlook, 2019-29'] = pd.to_numeric(data['Job Outlook, 2019-29'])

    # Table of information for top 10 highest rate of Job Outlook jobs
    growing_ratio = data.sort_values('Job Outlook, 2019-29',
                                     ascending=False).head(10)

    # Bar Graph for the top 10 highest rate of Job Outlook jobs
    job_name = growing_ratio['occupation_name'].tolist()
    Job_outlook = growing_ratio['Job Outlook, 2019-29'].tolist()

    fig, ax = plt.subplots(figsize=(10, 10))

    plt.bar(job_name, Job_outlook)
    plt.xticks(rotation=270)
    plt.title('Top 10 Careers with Highest Growth rate ')
    plt.ylabel('Growth Rate %')
    plt.tick_params(axis="x", labelsize=12)
    plt.tight_layout()

    plt.savefig('Job_Outlook_growth_plot')


# Question 4

def clean_data_1(data):
    """
    This method takes in the Payscale
    dataset to clear out any unnessary
    phrases in each cell of the required
    columns for further analysis. It also
    ranks the Early Career Pay and Mid Career
    Pay columns and sums up their scores
    together. It returns a modified version of
    the original dataset with ranked scores of
    the Early Career Pay, the Mid Career Pay, and
    the sum of these two scores in three new columns.
    """

    data['Major'] = data['Major'].str.replace('Major:', '')
    data['Major'] = data['Major'].str.replace(r' \(.*\)', '')
    data['Early Career Pay'] = data['Early Career Pay'].map(
                                                lambda x: x.lstrip(
                                                    'Early Career Pay:$'))
    data['Early Career Pay'] = data['Early Career Pay'].str.replace(',', '')
    data['Early Career Pay'] = pd.to_numeric(data['Early Career Pay'])
    data['Mid-Career Pay'] = data['Mid-Career Pay'].map(
                                                lambda x: x.lstrip(
                                                    'Mid-Career Pay:$'))
    data['Mid-Career Pay'] = data['Mid-Career Pay'].str.replace(',', '')
    data['Mid-Career Pay'] = pd.to_numeric(data['Mid-Career Pay'])
    data['Early Career Pay Rank'] = data['Early Career Pay'].rank(method='max')
    data['Mid-Career Pay Rank'] = data['Mid-Career Pay'].rank(method='max')
    sum_rankings = data['Early Career Pay Rank'] + data['Mid-Career Pay Rank']
    data['Resultant Score'] = sum_rankings
    return data


def uw(file_name, data):
    """
    This method takes in the cleaned Payscale
    dataset and the file dataset of every
    known UW major offered and checks to
    see if the Payscale dataset contains each
    major found in the file. It returns a modified
    version of the cleaned Payscale dataset that
    details the the majors found at UW and the
    information about them.
    """
    uw_majors_list = []
    with open(file_name) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            uw_majors_list.append(line)
    uw_majors = data['Major'].isin(uw_majors_list)
    uw_majors.name = 'At UW?'
    data = pd.concat([data, uw_majors], axis=1)
    data = data[data['At UW?']]
    return data


def top_10(data):
    """
    This method takes in the Payscale
    dataset that contains information
    about each major offered at UW and
    creates a clustered bar plot that
    details the ten majors with the highest
    Early and Mid-Career Salaries.
    """
    top_10 = data.sort_values(by=['Resultant Score'], ascending=False).head(10)
    top_10_e = top_10['Early Career Pay'].tolist()
    top_10_m = top_10['Mid-Career Pay'].tolist()
    top_10_labels = top_10['Major'].tolist()
    x = np.arange(len(top_10_labels))
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(x - width/2, top_10_e, width, label='Early')
    ax.bar(x + width/2, top_10_m, width, label='Mid')
    ax.set_ylabel('Pay Amount')
    ax.set_title('Top 10 Highest Paying Majors At UW')
    ax.set_xticks(x)
    ax.set_xticklabels(top_10_labels)
    plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig('Highest_Paying_Majors')


def bottom_10(data):
    """
    This method takes in the Payscale
    dataset that contains information
    about each major offered at UW and
    creates a clustered bar plot that
    details the ten majors with the lowest
    Early and Mid-Career Salaries.
    """
    bottom_10 = data.sort_values(by=['Resultant Score']).head(10)
    bottom_10_e = bottom_10['Early Career Pay'].tolist()
    bottom_10_m = bottom_10['Mid-Career Pay'].tolist()
    bottom_10_labels = bottom_10['Major'].tolist()
    x = np.arange(len(bottom_10_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(15, 20))
    ax.bar(x - width/2, bottom_10_e, width, label='Early')
    ax.bar(x + width/2, bottom_10_m, width, label='Mid')
    ax.set_ylabel('Pay Amount')
    ax.set_title('Top 10 Lowest Paying Majors At UW')
    ax.set_xticks(x)
    ax.set_xticklabels(bottom_10_labels)
    ax.legend()
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig('Lowest_Paying_Majors')

# Question 2


def clean_data_2(data):
    """
    This method takes in the occupation
    dataset to clear out any unnessary
    phrases in each cell of the required
    columns for further analysis. It returns a
    modified version of the original dataset with
    all cells in the 2019 Median Pay column
    all turned into integers for the purpose of
    analyzing the pay amount salary.
    """
    data = data.dropna()
    pay = data['2019 Median Pay']
    data['2019 Median Pay'] = pay.str.replace('$', '')
    data['2019 Median Pay'] = pay.str.replace(',', '')
    data['2019 Median Pay'] = pay.str.extract(r'(\d+)', expand=False)
    data['2019 Median Pay'] = pd.to_numeric(pay)
    return data


def bach_10(data):
    """
    This method takes in the cleaned occupation
    dataset that contains information
    about the 2019 Median Pay for jobs that
    require a Bachelor's degree for entry level
    and creates a bar plot showing the top 10
    highest paying occupations for the Bachelor's
    degree and their respective salaries.
    """
    data = data[data['Typical Entry-Level Education'] == 'Bachelor\'s degree']
    highest_paying_bach = data.sort_values(by=['2019 Median Pay'],
                                           ascending=False).head(10)
    highest_paying_bach = highest_paying_bach.head(10)
    bach_10 = highest_paying_bach['2019 Median Pay'].tolist()
    bach_10_labels = highest_paying_bach['occupation_name'].tolist()
    x = np.arange(len(bach_10_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(30, 30))
    ax.bar(x, bach_10, width)
    ax.set_ylabel('Mean Annual Salary')
    ax.set_title('Highest Paying Bachelor\'s Degree Occupations')
    ax.set_xticks(x)
    ax.set_xticklabels(bach_10_labels)
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig('Highest_Paying_Bach')


def master_10(data):
    """
    This method takes in the cleaned occupation
    dataset that contains information
    about the 2019 Median Pay for jobs that
    require a Master's degree for entry level
    and creates a bar plot showing the top 10
    highest paying occupations for the Master's
    degree and their respective salaries.
    """
    data = data[data['Typical Entry-Level Education'] == 'Master\'s degree']
    highest_paying_master = data.sort_values(by=['2019 Median Pay'],
                                             ascending=False).head(10)
    highest_paying_master = highest_paying_master.head(10)
    master_10 = highest_paying_master['2019 Median Pay'].tolist()
    master_10_labels = highest_paying_master['occupation_name'].tolist()
    x = np.arange(len(master_10_labels))
    width = 0.35
    fig, ax = plt.subplots(figsize=(15, 20))
    ax.bar(x, master_10, width)
    ax.set_ylabel('Mean Annual Salary')
    ax.set_title('Highest Paying Master\'s Degree Occupations')
    ax.set_xticks(x)
    ax.set_xticklabels(master_10_labels)
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig('Highest_Paying_Master')


def doct_10(data):
    """
    This method takes in the cleaned occupation
    dataset that contains information
    about the 2019 Median Pay for jobs that
    require a Doctorate or Professional degree for
    entry level and creates a bar plot showing the top 10
    highest paying occupations for the Doctorate and
    Professional degree and their respective salaries.
    """
    data = data[data['Typical Entry-Level Education']
                == 'Doctoral or professional degree']
    highest_paying_doct = data.sort_values(by=['2019 Median Pay'],
                                           ascending=False).head(10)
    highest_paying_doct = highest_paying_doct.head(10)
    doct_10 = highest_paying_doct['2019 Median Pay'].tolist()
    doct_10_labels = highest_paying_doct['occupation_name'].tolist()
    labels = ['Pediatrician', 'Physcian',
              'Family Medicine\n Physician',
              'Psychiatrists', 'Obstetricians\n and gynecologist',
              'Surgeons\n except ophthalmologist',
              'Anesthesiologists', 'General internal\n medicine physician',
              'Dentists', 'Oral and maxillofacial surgeons']
    x = np.arange(len(doct_10_labels))
    width = 0.35
    fig, ax = plt.subplots()
    ax.bar(x, doct_10, width)
    ax.set_ylabel('Mean Annual Salary')
    ax.set_title('Highest Paying Doctorate or Professional Degree Occupations')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    plt.xticks(rotation=-90)
    plt.tight_layout()
    plt.savefig('Highest_Paying_Doct')


# Question 3: What are the average salaries for different levels of education?
def get_average_salary_education_level(data):
    """
    This method takes in the cleaned occupation dataset that includes
    information about the 2019 Median Pay for different levels of education
    and calculates the average salary for those levels of education
    """
    data = \
        data.groupby('Typical Entry-Level Education')['2019 Median Pay'].mean()

    return data


def plot_average_salary_education_level(data):
    """
    This method takes in the data calculated by
    get_average_salary_education_level and plots into a bar chart.
    """
    labels = ["Associate's\n degree", "Bachelor's\n degree",
              "Doctoral\n or professional\ndegree",
              "High school\n diploma\n or equivalent",
              "Master's\n degree", "No formal\n education\n credential",
              "Postsecondary\n nondegree\n award", "Vocational\n Education",
              "Some college,\n no degree"]
    plt.figure(figsize=(10, 10))
    plt.bar(labels, data.tolist(), width=0.25)
    plt.title('Average Salaries for Different Education Levels')
    plt.ylabel('Mean Annual Salary')
    plt.xticks(rotation=45)
    plt.savefig('average_salary_education')


def main():
    data_question_1 = pd.read_csv('./occupation_data.csv')

    plot_employment_decline(data_question_1)
    plot_employment_growth(data_question_1)
    plot_job_outlook(data_question_1)

    data_question_4 = pd.read_csv('Final Project Dataset.csv',
                                  encoding='cp1252')
    data_question_4 = clean_data_1(data_question_4)
    data_question_4 = uw('UW Majors.txt', data_question_4)
    top_10(data_question_4)
    bottom_10(data_question_4)

    data_question_2 = pd.read_csv('occupation_data.csv', encoding='cp1252')
    data_question_2 = clean_data_2(data_question_2)
    bach_10(data_question_2)
    master_10(data_question_2)
    doct_10(data_question_2)

    average_salary_data = get_average_salary_education_level(data_question_2)
    plot_average_salary_education_level(average_salary_data)


if __name__ == '__main__':
    main()
