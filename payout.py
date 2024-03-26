import subprocess

spl_executable = r'C:\Users\MEMEdev\.local\share\solana\install\active_release\bin\spl-token.exe'
contract_address = 'Bc4itdH5eAJU2WN9h7uSZ8i9RZXSbNrVdUkaedFTHyDc'  # mini btc ca


def fund_user(user, amount):
    # command = ["solana","config","get"]
    command = [spl_executable, 'transfer', contract_address, amount, user]
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout  # return soon

# fund_user('G12Gw8DWHLL4ADUsumZTh2AsvVCpWJ6whpPmLYP1x8px', '50000')
# come back later
