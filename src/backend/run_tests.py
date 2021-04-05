from subprocess import Popen

directories = ["./blockchain", 
                "./services/wallet-api", 
                "./services/transaction-api", 
                "./services/users-api", 
                "./services/mining-api"]

change_directory = ["cd"]
run_coverage_pytest = ["python", "-m", "coverage", "run", "--source=./src", "-m", "pytest"]
get_coverage_report = ["python", "-m", "coverage", "report"]
_and = ["&&"]

for d in directories:
    p = Popen( change_directory + [d] + _and + run_coverage_pytest + _and + get_coverage_report, shell= True)
    p.communicate()