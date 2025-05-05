from pepfunn.library import Library
import os
import csv
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def generate_random_library():
    lib = Library()
    peptides = lib.generate_random_population()
    return peptides

def read_uploaded_sequences(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip() and not line.startswith(">")]

def generate_from_uploaded_file(file_path):
    lib = Library()
    with open(file_path, 'r') as f:
        lines = f.readlines()

    seed_seqs = [line.strip() for line in lines if line.strip() and not line.startswith(">")]

    lib.seeds = seed_seqs
    lib.mode_scan = 'random'  # 或根据用户输入设置为 'all'
    lib.positions = list(range(1, len(seed_seqs[0]) + 1))  # 假设每条长度相同，或使用最长那条

    population = lib.generate_single_population()
    return population


def save_results_csv(sequences, output_path):
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sequence'])
        for seq in sequences:
            writer.writerow([seq])

def run_module1(mode='random', file_path=None):
    if mode == 'random':
        peptides = generate_random_library()
    elif mode == 'upload' and file_path:
        peptides = generate_from_uploaded_file(file_path)
    else:
        raise ValueError("Invalid mode or missing file")

    filename = 'peptides_result.csv'
    csv_path = os.path.join(RESULT_FOLDER, filename)
    save_results_csv(peptides, csv_path)

    summary = f"共生成 {len(peptides)} 条肽序列。"
    download_link = f"/download/{filename}"
    return summary, download_link






def save_and_summarize(sequences):
    filename = 'peptides_result.csv'
    csv_path = os.path.join(RESULT_FOLDER, filename)
    save_results_csv(sequences, csv_path)
    summary = f"共生成 {len(sequences)} 条肽序列。"
    download_link = f"/download/{filename}"
    return summary, download_link

def generate_mutated_sequences(file_path, mutation_mode, positions=None):
    lib = Library()

    with open(file_path, 'r') as f:
        lines = f.readlines()
    seed_seqs = [line.strip() for line in lines if line.strip() and not line.startswith(">")]

    lib.seeds = seed_seqs

    if mutation_mode == 'all':
        lib.mode_scan = 'all'
        lib.positions = list(range(1, len(seed_seqs[0]) + 1))
        lib.pairs = [(pos, aa) for pos in lib.positions for aa in lib.list_aa]
    elif mutation_mode == 'random':
        lib.mode_scan = 'random'
        lib.positions = list(range(1, len(seed_seqs[0]) + 1))
    elif mutation_mode == 'custom' and positions:
        lib.mode_scan = 'random'
        lib.positions = positions
    else:
        raise ValueError("突变模式不合法或缺失必要参数")

    return lib.generate_single_population()
