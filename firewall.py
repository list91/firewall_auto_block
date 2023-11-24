import ipaddress
import win32com.client

import subprocess
rule_name = "BlockRDPBruteForce"
# command = 'netsh advfirewall firewall set rule name="BlockRDPBruteForce" new remoteip=111.111.1.100,222.222.2.200,333.333.3.300'

def run_command(ip_list):
    ip_line = ""
    for ip in ip_list:
        if ip_line == "":
            d = ""
        else:
            d = ","
        ip_line += d + ip
    command = f'netsh advfirewall firewall set rule name="{rule_name}" new remoteip={ip_line}'
    # print(command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode == 0:
        print("Команда успешно выполнена")
    else:
        print(f"Ошибка выполнения команды: {error.decode()}")

def find_firewall_rule_by_name(rule_name):
    firewall = win32com.client.Dispatch("HNetCfg.FwPolicy2")
    rules = firewall.Rules

    for rule in rules:
        if rule.Name == rule_name:
            return rule

    return None

# print(get_list_addresses_diapazone())
"""получение промежуточных адресов"""
def get_intermediate_ips(start_ip, end_ip):
    start = ipaddress.ip_address(start_ip)
    end = ipaddress.ip_address(end_ip)

    # Проверяем условия: стартовый и конечный адреса не равны друг другу,
    # а также стартовый адрес не больше конечного адреса
    if start > end:
        return []
    elif start == end:
        return [start_ip]

    intermediate_ips = []
    current_ip = start + 1  # Начинаем с первого промежуточного адреса

    while current_ip < end:
        intermediate_ips.append(str(current_ip))
        current_ip += 1

    return intermediate_ips
def clear_mask(ip):
    if "/" in ip:
        return ip.split("/")[0]
    return ip
def get_list_addresses_firewall():
    addresses = []
    # rule_name = "BlockRDPBruteForce"
    rule = find_firewall_rule_by_name(rule_name)

    if rule is not None:
        # print(rule.RemoteAddresses)
        remote_addresses = rule.RemoteAddresses.split(",") if rule.RemoteAddresses else []
        print(f"Удаленные IP-адреса для правила '{rule_name}':")
        # remote_addresses.append('77.238.102.220-77.238.102.226')
        for address in remote_addresses:
            address = address.strip()
            if "-" in address:
                # Обработка диапазона адресов
                ip_range = address.split("-")
                start_ip = ip_range[0].strip()
                end_ip = ip_range[1].strip()
                result_list = get_intermediate_ips(start_ip, end_ip)
                if len(result_list) != 0:
                    for adr in result_list:
                        addresses.append(clear_mask(adr))
                # network = ipaddress.ip_network(f"{start_ip}/{end_ip}", strict=False)
                # addresses.extend([str(ip) for ip in network.hosts()])
            else:
                # Отдельный IP-адрес
                addresses.append(clear_mask(address))
                # print(address)
    else:
        print(f"Правило '{rule_name}' не найдено.")
    return addresses
# for i in get_list_addresses_fireval():
#     # i = i.split("/")[0]
#     print(i) 

# run_command(get_list_addresses())

