from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)

standard_deduction = 75000

def calculate_tax(salary):
    url = "https://lma.co.in/resources/Calculators/Tax_Calculator/Call_WebService.asmx/gettax"
    payload = f"{{txtSalary: \"{salary}\",txtIFHProperty: \"0\",txtBIncome: \"0\",txtOthers: \"0\",txtOtherIncome: \"0\",txtDUs80: \"0\",txtChild: \"0\",txtParent: \"0\",txtOtherDeduction: \"0\",txt20Tax: \"0\",txt10Tax: \"0\",txtSOWSTTaxpaid: \"0\",txtWFCountries: \"0\",txtAIncome: \"0\",rdoLstStatus: \"Individual\",rdoLstComType: \"Domestic\",rdoIndstatus: \"O\",fyear: \"2025\",ded80tta: \"-99999\",TURNOVER: \"0\",txtnew20Taxshort: \"0\",txtnew12Taxlong: \"0\",flag1: 0,flag2: 0,sflag1: \"\",sflag2: \"\"\r\n}}"
    headers = {'content-type': 'application/json; charset=UTF-8'}

    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        data = json.loads(response.text)["d"].split(",")
        total_tax = float(data[0]) + float(data[8]) - float(data[-2])

        net_annual_salary = float(salary) + standard_deduction - total_tax
        net_monthly_salary = net_annual_salary / 12

        return total_tax, net_monthly_salary
    except Exception as e:
        print(f"error in requesting as {e}")
        return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        monthly_salary = float(request.form.get('monthly_salary', 0))
        epf_amount = float(request.form.get('epf', 1800))
        lwf = float(request.form.get('lwf', 0))

        annual_salary = 12 * monthly_salary
        total_tax, net_monthly_salary = calculate_tax(annual_salary - standard_deduction)

        if total_tax is not None:
            result = {
                "total_tax": round(total_tax),
                "net_monthly": round(net_monthly_salary - lwf - epf_amount),
                "gross_monthly": round(net_monthly_salary - lwf)
            }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)