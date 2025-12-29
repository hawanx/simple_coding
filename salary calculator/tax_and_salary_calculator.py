import json

standard_deduction = 75000 # fixed

def calculate_tax(salary):
    # URL and payload structure from the example
    url = "https://lma.co.in/resources/Calculators/Tax_Calculator/Call_WebService.asmx/gettax"
    payload = f"{{txtSalary: \"{salary}\",txtIFHProperty: \"0\",txtBIncome: \"0\",txtOthers: \"0\",txtOtherIncome: \"0\",txtDUs80: \"0\",txtChild: \"0\",txtParent: \"0\",txtOtherDeduction: \"0\",txt20Tax: \"0\",txt10Tax: \"0\",txtSOWSTTaxpaid: \"0\",txtWFCountries: \"0\",txtAIncome: \"0\",rdoLstStatus: \"Individual\",rdoLstComType: \"Domestic\",rdoIndstatus: \"O\",fyear: \"2025\",ded80tta: \"-99999\",TURNOVER: \"0\",txtnew20Taxshort: \"0\",txtnew12Taxlong: \"0\",flag1: 0,flag2: 0,sflag1: \"\",sflag2: \"\"\r\n}}"

    headers = {'content-type': 'application/json; charset=UTF-8', }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)["d"].split(",")
    total_tax = float(data[0]) + float(data[8]) - float(data[-2]) # Tax + Health and Education Cess

    # Calculate net annual salary (salary + 75000 - total tax)
    net_annual_salary = float(salary) + standard_deduction - total_tax

    # Calculate net monthly salary
    net_monthly_salary = net_annual_salary / 12

    return total_tax, net_annual_salary, net_monthly_salaryw


import requests

monthly_salary = 110000
epf_amount = 1800
lwf = 0

total_salary = monthly_salary
annual_salary = 12 * total_salary

total_tax, net_annual_salary, net_monthly_salary = calculate_tax(annual_salary-standard_deduction)

print(f"Total Tax: {total_tax:.0f}")
print(f"Net Monthly Salary: {net_monthly_salary - lwf - epf_amount:.0f}")
print(f"Net money : {net_monthly_salary - lwf:.0f}")
