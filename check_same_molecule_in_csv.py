import pandas as pd
from rdkit import Chem

def compare_smiles_sets(file1_path, file2_path):
    # 1. CSV 파일 읽기
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # 첫 번째 컬럼 추출
    smi_col1 = df1.iloc[:, 0]
    smi_col2 = df2.iloc[:, 0]

    def get_canonical_set(smi_list, file_name):
        can_set = set()
        error_count = 0
        for i, smi in enumerate(smi_list):
            mol = Chem.MolFromSmiles(str(smi))
            if mol:
                # 표준화된 SMILES로 변환하여 집합에 추가
                can_set.add(Chem.MolToSmiles(mol, canonical=True))
            else:
                print(f"[{file_name}] Row {i+1}: SMILES 해석 오류 - {smi}")
                error_count += 1
        return can_set, error_count

    print("--- 파일 1 표준화 진행 중... ---")
    set1, err1 = get_canonical_set(smi_col1, "File1")
    
    print("--- 파일 2 표준화 진행 중... ---")
    set2, err2 = get_canonical_set(smi_col2, "File2")

    print("\n--- 비교 결과 요약 ---")
    print(f"File 1: 총 {len(smi_col1)}개 행 -> 고유 화합물 {len(set1)}개 (오류 {err1}개)")
    print(f"File 2: 총 {len(smi_col2)}개 행 -> 고유 화합물 {len(set2)}개 (오류 {err2}개)")

    # 두 집합 비교
    if set1 == set2:
        print("\n결과: 두 파일은 순서와 관계없이 [완벽하게 동일한 화합물들]로 구성되어 있습니다.")
    else:
        only_in_1 = set1 - set2
        only_in_2 = set2 - set1
        
        print("\n결과: 두 파일의 구성 성분이 다릅니다.")
        if only_in_1:
            print(only_in_1)
            print(f"  - File 1에만 있는 화합물: {len(only_in_1)}개")
        if only_in_2:
            print(only_in_2)
            print(f"  - File 2에만 있는 화합물: {len(only_in_2)}개")
            
        # 차이가 나는 샘플을 일부 출력해보고 싶다면 아래 주석 해제
        # print(f"예시 (File 1에만 존재): {list(only_in_1)[:3]}")

# 실행
compare_smiles_sets('./data/0202_Clintox_Test.csv', './data/MoleBlend_clintox_test.csv')