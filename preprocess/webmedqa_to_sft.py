import argparse
import json
import logging
import re
import pandas as pda


def convert(opts):
    data = []
    # Read question data into a DataFrame
    for l in open(f"{opts.data_dir}/medQA.train.txt"):
        items = l.split('\t')
        data.append(items)

    train_df = pda.DataFrame(data, columns=['department', 'is_answer', 'question_id', 'question', 'option'])
    train_df = train_df[train_df.is_answer == '1']
    print(train_df.head())

    # Convert grouped DataFrame to a list of JSON entries
    sft_entries = []
    for index, row in train_df.iterrows():
        sft_entry = {
            "instruction": row.question,
            "input": "",
            "output": re.sub(r'\d{4}-\d{2}-\d{4}:\d{2}', "", row.option)  # list of content from cMedQA_A.csv
        }
        sft_entries.append(sft_entry)

    # Save JSON data to output file
    with open(opts.output_file, 'w', encoding='utf-8') as json_file:
        json.dump(sft_entries, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )
    parser = argparse.ArgumentParser(prog='webMedQA SFT', description='')
    parser.add_argument("--data_dir", type=str, default="")
    parser.add_argument("--output_file", type=str, default="../../data/webmedqa.json")
    # Initialize arguments
    args = parser.parse_args()
    convert(args)
