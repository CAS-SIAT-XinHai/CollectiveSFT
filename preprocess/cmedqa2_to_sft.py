# -*- coding: utf-8 -*-
# @Time    : 2023/8/30 9:50
# @Author  : TimLeo
# @FileName: cmedqa2_to_sft.py
# @Software: PyCharm

import argparse
import json
import logging

import pandas as pd


def convert(opts):
    # Read question data into a DataFrame
    questions_df = pd.read_csv(f"{opts.data_dir}/question.zip", compression='zip', encoding='utf-8')

    # Read train candidates into a DataFrame
    train_df = pd.read_csv(f"{opts.data_dir}/train_candidates.zip", compression='zip', encoding='utf-8')

    questions_df = questions_df[questions_df.question_id.isin(train_df.question_id.unique())]

    # Read answer data into a DataFrame
    answers_df = pd.read_csv(f"{opts.data_dir}/answer.zip", compression='zip', encoding='utf-8')

    # Merge question and answer data based on question_id
    merged_df = pd.merge(answers_df, questions_df, on='question_id', how='inner')
    print(merged_df.head())

    # Group answers by question_id and aggregate content
    grouped = merged_df.groupby('question_id')['content_x'].apply(list).reset_index(name='output')

    # Convert grouped DataFrame to a list of JSON entries
    sft_entries = []
    for index, row in grouped.iterrows():
        question_content = questions_df[questions_df['question_id'] == row['question_id']]['content'].iloc[0]
        for item in row['output']:
            sft_entry = {
                "instruction": question_content,  # content from cMedQA_Q.csv
                "input": "",
                "output": item,  # list of content from cMedQA_A.csv
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
    parser = argparse.ArgumentParser(prog='cMedQA2 SFT', description='')
    parser.add_argument("--data_dir", type=str, default="")
    parser.add_argument("--output_file", type=str, default="../../data/cmedqa2.json")
    # Initialize arguments
    args = parser.parse_args()
    convert(args)
