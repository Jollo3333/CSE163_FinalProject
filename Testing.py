from cse163_utils import assert_equals
import analysis
import pandas as pd


def test_fastest_growing_job(data):
    """
    The function test the data set for the job with the highest
    Job Outlook rate 2019-29, it indicates the highest predicting
    rate of occupation growing from 2019 to 2029
    """

    assert_equals(61.0, data['Job Outlook, 2019-29'].max())


def test_employment_declining(data):
    """
    The function test the data set for the job that has the highest number
    of loss 2019-29. It takes the dataset's Employment change column
    and calculate the higest number of lost job from 2019 to 2029
    """

    assert_equals(-327400.0, data['Employment Change, 2019-29'].min())


def test_employment_growing(data):
    """
    The function test the data set for the job that has the highest number
    of growth 2019-29. It takes the dataset's Employment change column
    and calculate the higest number of new job from 2019 to 2029
    """

    assert_equals(1159500.0, data['Employment Change, 2019-29'].max())


def test_clean_data(data, data2):
    """
    This function dictates if plugging
    in the given values will give a certain
    determined result to tell if the clean_data
    function in Research_Question_4.py works as expected.
    Should all tests pass, it will print nothing.
    On the other hand, if one of these tests fails,
    it will show an error message.
    """
    expect_major = ['Physics',
                    'Computer Science & Engineering', 'Applied Mathematics']
    expect_pay = [62300, 74000, 64400]
    expect_2019_pay = [107510, 92030, 122220]
    assert_equals(expect_major, data['Major'].tolist())
    assert_equals(expect_pay, data['Early Career Pay'].tolist())
    assert_equals(expect_2019_pay, data2['2019 Median Pay'].tolist())


def test_uw(data):
    """
    This function dictates if plugging
    in the given values will give a certain
    determined result to tell if the uw
    function in Research_Question_4.py works as expected.
    Should all tests pass, it will print nothing.
    On the other hand, if one of these tests fails,
    it will show an error message.
    """
    expect_uw_majors = ['Physics', 'Applied Mathematics']
    given = analysis.uw('UW Majors.txt', data)
    assert_equals(expect_uw_majors, given['Major'].tolist())


def main():
    # Question 1 testing
    data_question_1 = pd.read_csv('./occupation_data.csv')

    # pre data wrangling for the testing, delete all strings
    # in Job Outlook, 2019-29 column
    data_question_1['Job Outlook, 2019-29'] = data_question_1['Job Outlook, '
                                        '2019-29'].str.replace(r' \(.*\)', '')
    data_question_1['Job Outlook, 2019-29'] = data_question_1['Job Outlook, '
                                        '2019-29'].str.replace('%', '')
    data_question_1['Job Outlook, 2019-29'] = pd.to_numeric(data_question_1['Job Outlook, 2019-29'])

    test_fastest_growing_job(data_question_1)
    test_employment_declining(data_question_1)
    test_employment_growing(data_question_1)

    # Question 2/4 testing
    data_question_4 = pd.read_csv('Payscale Test.csv', encoding='cp1252')
    data_question_2 = pd.read_csv('occupation Test.csv', encoding='cp1252')
    cleaned = analysis.clean_data_1(data_question_4)
    cleaned2 = analysis.clean_data_2(data_question_2)
    test_clean_data(cleaned, cleaned2)
    test_uw(cleaned)


if __name__ == '__main__':
    main()