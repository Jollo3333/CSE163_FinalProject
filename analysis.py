import pandas as pd
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

    fig, ax = plt.subplots(1)

    plt.bar(job_name_employment, Employment_growth)
    plt.xticks(rotation=270)
    plt.title('Top 10 Careers with Largest Number of Job Growth')
    plt.ylabel('Number of Job Grow')

    plt.savefig('Employment_growth_plot')


def plot_employment_decline(data):
    # The fastest declinging job depending on the number of job
    # oppotunities that will disappear between year 2019 - 2029
    declining_job = data.sort_values('Employment Change, '
                                     '2019-29').head(10)

    job_name_decline = declining_job['occupation_name'].tolist()
    Employment_decline = data['Employment Change, 2019-29'].tolist()
    Employment_decline = sorted(Employment_decline, reverse=True)

    fig, ax = plt.subplots(1)

    plt.bar(job_name_decline, declining_job['Employment Change, 2019-29'])
    plt.xticks(rotation=270)
    plt.title('Top 10 Careers with Largest Number of Job Decline')
    plt.ylabel('Number of Job Will Disappear')

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

    fig, ax = plt.subplots(1)

    plt.bar(job_name, Job_outlook)
    plt.xticks(rotation=270)
    plt.title('Top 10 Careers with Highest Growth rate ')
    plt.ylabel('Growth Rate %')

    plt.savefig('Job_Outlook_growth_plot')


def main():
    data = pd.read_csv('./occupation_data.csv')

    plot_employment_decline(data)
    plot_employment_growth(data)

    plot_job_outlook(data)


if __name__ == '__main__':
    main()