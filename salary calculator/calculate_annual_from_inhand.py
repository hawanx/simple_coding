from tax_and_salary_calculator import calculate_tax

standard_deduction = 75000
epf = 1800


def binary_search(in_hand_salary, lo=1000000, hi=10000000):
    mid = (lo+hi)/2
    tax = calculate_tax(mid-standard_deduction)[0]
    derived_in_hand_salary = int(mid)/12 - int(tax)/12 - epf
    if derived_in_hand_salary == in_hand_salary:
        return mid
    elif derived_in_hand_salary > in_hand_salary:
        hi = mid-1
    else:
        lo = mid+1
    return binary_search(in_hand_salary, lo, hi)

salary = 1345000

print(f"Annual Salary would be = {binary_search(salary):.0f}")