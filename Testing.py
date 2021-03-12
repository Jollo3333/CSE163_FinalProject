from cse163_utils import assert_equals
import pandas as pd


def test_fastest_growing_job(data):
    """
    test the data set for the job with the highest
    Job Outlook rate 2019-29
    """

    assert_equals(61.0, data['Job Outlook, 2019-29'].max())


def test_employment_declining(data):
    """
    test the data set for the job that has the highest number
    of loss 2019-29
    """

    assert_equals(-327400.0, data['Employment Change, 2019-29'].min())


def test_employment_growing(data):
    """
    test the data set for the job that has the highest number
    of growth 2019-29
    """

    assert_equals(1159500.0, data['Employment Change, 2019-29'].max())


def main():
    data = pd.read_csv('./occupation_data.csv')

    # pre data wrangling for the testing, delete all strings
    # in Job Outlook, 2019-29 column
    data['Job Outlook, 2019-29'] = data['Job Outlook, '
                                        '2019-29'].str.replace(r' \(.*\)', '')

    data['Job Outlook, 2019-29'] = data['Job Outlook, '
                                        '2019-29'].str.replace('%', '')

    data['Job Outlook, 2019-29'] = pd.to_numeric(data['Job Outlook, 2019-29'])

    test_fastest_growing_job(data)
    test_employment_declining(data)
    test_employment_growing(data)


if __name__ == '__main__':
    main()