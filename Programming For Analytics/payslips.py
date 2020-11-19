# QUESTION 1

import pandas as pd

def generate_payslip(series):
    """Generates payslip and output it to a .txt file.

    Parameters
    ----------
    series : Pandas.Series
        this function is meant to be used with DataFrame.apply,
        since it will use a full row to generate the payslip file. 
    """
    # Convert DataFrame into Series. Less typing
    s = series
    # Avoid "/" to create multiple txt files based on date and Full Name 
    date = s['Date'].strftime('%d-%m-%Y')

    file_name = '{}-{} {}.txt'.format(date, s['First Name'], s['Surname'])
    with open(file_name, 'w') as f:
        f.write('PAYSLIP\n\n')
        f.write('{:12}{}\n'.format('StaffID: ', s['StaffID']))
        f.write('{:12}{} {}\n'.format(
            'Staff Name: ',
            s['First Name'],
            s['Surname']
        ))
        f.write('{:12}{}\n'.format('PPSN: ', s['PPS Number']))
        f.write('{:12}{}\n\n'.format('Date: ', date))
        f.write('{:18} | {:^8} | {:^8} | {:^8}\n'.format(
            '',
            'Hours',
            'Rate',
            'Total'
        ))
        f.write('{:18} | {:8,.2f} | {:8,.2f} | {:8,.2f}\n'.format(
            'Regular',
            s['Regular'],
            s['Hourly Rate'],
            s['Regular Pay']
        ))
        f.write('{:18} | {:8,.2f} | {:8,.2f} | {:8,.2f}\n\n'.format(
            'Overtime',
            s['Overtime'],
            s['Overtime Rate'],
            s['Overtime Pay']
        ))
        f.write('{:18} {:8,.2f}\n\n'.format('Gross Pay', s['Gross Pay']))
        f.write('{:18}   {:^8} | {:^8} | {:^8}\n'.format(
            '',
            '',
            'Rate',
            'Total'
        ))
        f.write('{:18} | {:8,.2f} | {:8.0%} | {:8,.2f}\n'.format(
            'Standard Band',
            s['StandardBand'],
            s['StandardRate'],
            s['Regular Tax']
        ))
        f.write('{:18} | {:8,.2f} | {:8.0%} | {:8,.2f}\n\n'.format(
            'Higher Rate',
            s['Higher Rate Pay'],
            s['HigherRate'],
            s['HigherRate Tax']
        ))
        f.write('{:18} | {:8,.2f} |\n'.format(
            'Total Deductions',
            s['Total Deductions']
        ))
        f.write('{:18} | {:8} | {:8,.2f}\n'.format(
            'Tax Credit',
            '',
            s['TaxCredit']
        ))
        f.write('{:18} | {:8,.2f} |\n'.format(
            'Net Deductions',
            s['Net Deductions']
        ))
        f.write('{:18}   {:8,.2f}'.format('Net Pay', s['Net Pay']))
    print('{} created.'.format(file_name))

# import Hours.txt
hrs = pd.read_csv('Hours.txt', sep='\t')
hrs['Date'] = pd.to_datetime(hrs['Date'])

# import Employees.txt
emp = pd.read_csv('Employees.txt', sep='\t')

# import Tax Rate
tax = pd.read_csv('Taxrates.txt', sep='\t')

# Merge Employee information onto Hours
hrs = hrs.merge(emp, on='StaffID', how='left')

# Values are in percentage, without the % sign
hrs['StandardRate'] = tax.loc[0, 'Standard Rate'] / 100
hrs['HigherRate'] = tax.loc[0, 'Higher Rate'] / 100

# Checking if there are overtime hours
hrs['Regular'] = hrs.apply(
    lambda x: x['Hours'] if
              x['Hours'] <= x['Standard Hours'] 
              else x['Standard Hours'],
    axis=1
)

hrs['Overtime'] = hrs.apply(
    lambda x: x['Hours'] - x['Standard Hours'] if
              x['Hours'] >= x['Standard Hours'] 
              else 0,
    axis=1
)

hrs['Regular Pay'] = hrs['Regular'] * hrs['Hourly Rate']
hrs['Overtime Pay'] = hrs['Overtime'] * hrs['Overtime Rate']
hrs['Gross Pay'] = hrs['Regular Pay'] + hrs['Overtime Pay']

# Higher rate Tax will be applied only after StandardBand amount
hrs['Higher Rate Pay'] = hrs.apply(
    lambda x: x['Gross Pay'] - x['StandardBand'] if 
              x['Gross Pay'] > x['StandardBand'] 
              else 0,
    axis=1
)

hrs['Regular Tax'] = hrs.apply(
    lambda x: x['Gross Pay'] * x['StandardRate'] if
              x['Gross Pay'] <= 700 
              else x['StandardBand'] * x['StandardRate'],
    axis=1
)

hrs['HigherRate Tax'] = hrs.apply(
    lambda x: (x['Gross Pay'] - x['StandardBand']) * x['HigherRate'] if
              x['Gross Pay'] > 700 
              else 0,
    axis=1
)

hrs['Total Deductions'] = hrs['Regular Tax'] + hrs['HigherRate Tax']

hrs['Net Deductions'] = hrs['Total Deductions'] - hrs['TaxCredit']
hrs['Net Pay'] = hrs['Gross Pay'] - hrs['Net Deductions']

hrs.apply(generate_payslip, axis=1)

# QUESTION 2

def pay_report(dataframe, n=6):
    """Generates a pay report with weekly average gross pay,
    and n-week rolling average gross pay.

    Parameters
    ----------
    dataframe : Pandas.DataFrame
        this is the DataFrame that contains all the payslips
    n : integer
        number of weeks to apply the rolling average
    """
    # Filter DF because we only need 3 columns for report
    df = dataframe[['Date', 'StaffID', 'Gross Pay']]
    
    # Reset Index to avoid Multilevel indexing
    pay_average = df.groupby('StaffID').mean().reset_index()
    
    # Renaming to better present information
    pay_average.rename(columns={'Gross Pay': 'Average Gross Pay'}, inplace=True)
    
    # Create empty df to store rolling average values 
    # to then merge with main df
    rolling_av_df = pd.DataFrame(columns=['StaffID', 'Gross Pay'])
    for i in df['StaffID'].unique():
        filtered_df = hrs[['StaffID', 'Gross Pay']].loc[hrs['StaffID'] == i]
        # if pay dates less than n, then no value will appear.
        if len(filtered_df) >= n:
            # Because of rolling average, we can take only the last n rows.
            rolling_average = filtered_df.tail(n).groupby(
                'StaffID'
            ).mean().reset_index()
            
            # append to df
            rolling_av_df = pd.concat([rolling_av_df, rolling_average])

    df_report = pay_average.merge(rolling_av_df, on='StaffID', how='left')
    
    df_report.rename(columns={
        'Gross Pay':'Rolling Average Pay ({} wks)'.format(n)
    }, inplace=True)

    df_report.to_csv('Pay Report.txt', sep='\t', index=False, header=True)
    return df_report
            
pay_report(hrs)