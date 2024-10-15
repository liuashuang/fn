import hashlib
from tqdm import tqdm
import logging
from multiprocessing import Pool, Manager

# 设置日志配置
logging.basicConfig(filename='process.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def md5_hash(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()

def load_plaintexts(plaintext_file):
    with open(plaintext_file, 'r') as f:
        return [line.strip() for line in f.readlines()]

def check_passwords(args):
    salt, ciphertext, plaintexts, username = args
    for plaintext in plaintexts:
        if md5_hash(salt + md5_hash(plaintext)) == ciphertext:
            logging.info(f'Match found for {username} with salt {salt}: {plaintext}')
            return f"{salt}:{ciphertext}:{plaintext}"
    logging.info(f'No match for {username} with salt {salt}')
    return f"{salt}:{ciphertext}:-"

def main(input_file, output_file, plaintext_file):
    plaintexts = load_plaintexts(plaintext_file)
    logging.info(f'Loaded {len(plaintexts)} plaintext passwords.')

    with open(input_file, 'r') as f:
        lines = f.readlines()

    results = []

    with Pool() as pool:
        for line in tqdm(lines, desc="Processing", unit="line"):
            line = line.strip()
            username, *ciphertexts = line.split(',')
            
            output = [username]
            tasks = [(salt, c, plaintexts, username) for ciphertext in ciphertexts for salt, c in [ciphertext.split(':')]]
            matches = pool.map(check_passwords, tasks)
            
            output.extend(matches)
            
            # 如果没有任何匹配的结果，则不写入
            if any(":-" not in entry for entry in output[1:]):
                results.append(','.join(output))
    
    # 写入到新的文件
    with open(output_file, 'w') as f:
        for result in results:
            f.write(result + '\n')
    
    logging.info('Processing complete. Results written to output file.')

if __name__ == "__main__":
    main('input.txt', 'output.txt', 'plaintexts.txt')
