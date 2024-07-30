import argparse
import json
import logging

from datasets import load_dataset
from more_itertools import chunked
from tqdm.auto import tqdm


def convert(opts):
    # with open(f"{opts.data_dir}/empathetic_dialogues-test.json", 'r', encoding='utf-8') as file:
    #     dataset = json.load(file)

    # dataset_en = load_dataset("medical_dialog", split='en')
    dataset = load_dataset("medical_dialog", 'processed.zh', split='train')

    sft_entries = []
    for i, entry in enumerate(tqdm(dataset)):
        if i == 0:
            print(entry)
        conversations = entry['utterances']
        history = []
        for i, d in enumerate(chunked(conversations, n=2)):
            conv1, conv2 = d

            assert conv1.startswith("病人：")
            assert conv2.startswith("医生：")

            conv1 = conv1.replace("病人：", "")
            conv2 = conv2.replace("医生：", "")
            sft_entry = {
                "instruction": conv1,
                "input": "",
                "output": conv2,
                "history": history.copy()
            }
            sft_entries.append(sft_entry)

            history.append([conv1, conv2])

    with open(opts.output_file, 'w', encoding='utf-8') as out_file:
        json.dump(sft_entries, out_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )
    parser = argparse.ArgumentParser(prog='MedicalDialogue', description='')
    parser.add_argument("--output_file", type=str, default="../../data/medicaldialogue.json")
    opts = parser.parse_args()
    convert(opts)
