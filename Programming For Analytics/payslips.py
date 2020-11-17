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
    # File name using date, First and Last name, to make it unique
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

