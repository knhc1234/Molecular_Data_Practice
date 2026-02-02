import lmdb
import pickle
import numpy as np
import pandas as pd

# 1. 파일 경로 설정 (split.lmdb가 들어있는 폴더 경로)
lmdb_path = "./data/valid.lmdb"     # From MoleBLEND(Uni-Mol) Valid/Test data 
output_csv = "./data/MoleBlend_clintox_val.csv"

# 2. LMDB 환경 열기
env = lmdb.open(lmdb_path, subdir=False, readonly=True, lock=False, readahead=False, meminit=False)
test_num = 0

extracted_rows = []

with env.begin() as txn:
    print(f"--- LMDB 탐색 시작 (전체 엔트리 수: {txn.stat()['entries']}) ---")
    
    # 0번부터 50번까지 넉넉하게 확인
    for i in range(500):
        key = str(i).encode()
        raw_data = txn.get(key)
        
        if not raw_data:
            continue
            
        try:
            sample = pickle.loads(raw_data)
        except Exception:
            continue

        # 데이터의 타입과 길이를 먼저 확인 (KeyError 방지)
        sample_type = type(sample)
        sample_len = len(sample) if hasattr(sample, '__len__') else "N/A"
        
        print(f"Key: {i:<3} | Type: {str(sample_type):<18} | Len: {sample_len}")

        # 만약 길이가 5 이상이고, 진짜 데이터셋 구조라면 상세 출력
        if isinstance(sample, (list, tuple)) and len(sample) >= 5:
            # Index 4가 'target' 문자열이 아닌 실제 값일 때 출력
            target_val = sample[4]
            if not isinstance(target_val, str) or target_val != 'target':
                print(f"  ▶ [데이터 발견!] Target: {target_val} (Type: {type(target_val)})")
                if len(sample) > 2:
                    print(f"  ▶ SMILES: {sample[2]}")
                print("-" * 50)
                # 진짜 데이터를 하나 찾았으면 종료하거나 더 보고 싶으면 계속 진행
                # break 
        else:
            # 데이터가 리스트가 아니거나 짧은 경우 (메타데이터일 확률 높음)
            data = sample["smi"]
            extracted_rows.append(data)
            print(f"  ▶ 내용 요약: {data}...")
            test_num +=1 

env.close()
print(test_num)

df = pd.DataFrame(extracted_rows)
df.to_csv(output_csv, index=False, encoding='utf-8-sig')

print(f"--- 변환 완료 ---")
print(f"추출된 데이터 수: {len(extracted_rows)}")
print(f"저장된 파일명: {output_csv}")
