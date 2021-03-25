from subprocess import PIPE , Popen

directories = ["./blockchain", 
                "./services/wallet-api", 
                "./services/transaction-api", 
                "./services/users-api", 
                "./services/mining-api"]

for d in directories:
    p = Popen(["cd", d, "&&", "python", "-m", "coverage", "run", "--source=./src", "-m", "pytest", "&&", "python", "-m", "coverage", "report"], shell= True)
    p.communicate()