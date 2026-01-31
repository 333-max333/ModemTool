import subprocess
import re

def get_mac_address():
    # 执行 arp -a 命令并获取输出
    try:
        result = subprocess.run(['arp', '-a'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout
    except Exception as e:
        return None
    
    # 使用正则表达式提取 192.168.1.1 的 MAC 地址
    match = re.search(r'192\.168\.1\.1\s+([0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2}[-:][0-9a-fA-F]{2})', output)
    
    if match:
        # 将 MAC 地址中的 `-` 和 `:` 去掉
        mac = match.group(1).replace('-', '').replace(':', '').upper()
        return mac
    return None

def generate_a1(hex_str):
    cts = [
        'QbNUTaMecPWVSKdCgXIJRrsfYXwyqpvnDHWzQuPmAGtAxRTphBcwBnNkjbFmvVMqaFkEutSrDCxsCKjBzEyDEUJTZfHZghMHYFdeASGNaUgFtdbYRkshJHkFNXMcKdfw',
        'NXMcKdfwRkshJHkFaUgFtdbYYFdeASGNZfHZghMHzEyDEUJTDCxsCKjBaFkEutSrjbFmvVMqhBcwBnNkAGtAxRTpDHWzQuPmYXwyqpvngXIJRrsfcPWVSKdCQbNUTaMe',
        'eMaTUNbQCdKSVWPcfsrRJIXgnvpqywXYmPuQzWHDpTRxAtGAkNnBwcBhqMVvmFbjrStuEkFaBjKCsxCDTJUEDyEzHMhgZHfZNGSAedFYYbdtFgUaFkHJhskRwfdKcMXN',
        'CbntTaMGFPWTSkdCtXIYRrsfaXyyqpvRbHWAJuPSAGtacRTpVKcmBnNevbFMvSMPDFkEuRSDXCssCKjszEyDEUJCZfckghBHYFseASaNaUgFPfbYRLSubTkFKXMcKdfH',
        'gXIJRrsfNXMcKdfwYXwZqpvnQuPmDHWzAGtQxRTpjbFmvVMqDCxsjBCKzEyDEUJTHbCwBnIkZfHZghMHYASGFdeNcPWVSKdCaUgFtdbYRkshJHkF'+'QbNUTaMeaFkLutSr'
    ]
    hex_clean = ''.join(c for c in hex_str.upper() if c in '0123456789ABCDEF')
    if len(hex_clean) < 12: return "MAC错误"
    v19 = [ord(c) for c in reversed(hex_clean[-8:])]
    v10 = next(((c-48|j) for j,c in enumerate(v19) if 49<=c<=57), 5)
    results = [[] for _ in range(len(cts))]
    for k in range(len(v19)):
        v15 = v19[k] & v19[7-k] if k <4 else v19[k] | v19[k-4]
        v16 = v15 + v10
        if v16 > 127: v16, v10 = k, k
        for i in range(len(cts)): results[i].append(cts[i][v16])
        v10 += max(k, 1)
    
    # 添加注释
    annotated_results = [
        ''.join(results[0]) + "  # 电信版",
        ''.join(results[1]) + "  # 电信版",
        ''.join(results[2]) + "  # 特艺光猫的",
        ''.join(results[3]) + "  # 联通的博通版",
        ''.join(results[4]) + "  # 海思版"
    ]
    
    # 每个结果都独占一行，前面加上16个空格
    result_line1 = "                " + annotated_results[0]
    result_line2 = "                " + annotated_results[1]
    result_line3 = "                " + annotated_results[2]
    result_line4 = "                " + annotated_results[3]
    result_line5 = "                " + annotated_results[4]
    
    return '\n'.join([result_line1, result_line2, result_line3, result_line4, result_line5])

def format_mac(mac_str):
    # 去除输入中的所有非十六进制字符（如: `:` 或 `-`），并确保其大写
    return ''.join(c for c in mac_str.upper() if c in '0123456789ABCDEF')

def validate_mac(mac_str):
    # 校验 MAC 地址是否有效
    return len(mac_str) == 12

if __name__ == "__main__":
    while True:
        # 获取 arp -a 输出的 MAC 地址
        mac_from_arp = get_mac_address()
        
        if mac_from_arp:
            print(f"从 ARP 获取到的 MAC 地址（192.168.1.1）：{mac_from_arp}")
        else:
            print("无法从 ARP 获取到 192.168.1.1 的 MAC 地址。")
        
        # 用户输入 MAC 地址
        mac_address = input("请输入 MAC 地址（格式可以是 AA:AA:AA:AA:AA:AA 或者 AAAAAAAAAAAA）：")
        
        # 格式化和验证 MAC 地址
        formatted_mac = format_mac(mac_address)
        
        if not validate_mac(formatted_mac):
            print("无效的 MAC 地址，请重新输入。")
            continue
        
        print(generate_a1(formatted_mac))
        
        # 提示用户是否继续
        user_choice = input("是否继续输入新的 MAC 地址？(y/n)：")
        if user_choice.lower() != 'y':
            print("退出程序。")
            break
