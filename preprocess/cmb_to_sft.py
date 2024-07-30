import argparse
import json
import logging

from datasets import load_dataset
from tqdm import tqdm

"""
{
    "exam_type": "医师考试",
    "exam_class": "执业医师",
    "exam_subject": "口腔执业医师",
    "question": "患者，男性，11岁。近2个月来时有低热（37～38℃），全身无明显症状。查体无明显阳性体征。X线检查发现右肺中部有一直径约0.8cm类圆形病灶，边缘稍模糊，肺门淋巴结肿大。此男孩可能患",
    "answer": "D",
    "question_type": "单项选择题",
    "option": {
        "A": "小叶型肺炎",
        "B": "浸润性肺结核",
        "C": "继发性肺结核",
        "D": "原发性肺结核",
        "E": "粟粒型肺结核"
    }
}
"""


def convert(opts):
    dataset = load_dataset("FreedomIntelligence/CMB", 'exam', split='train')
    formatted_data = []
    for entry in tqdm(dataset):
        prompt = f"该问题源自{entry['exam_type']}，面向{entry['exam_class']}中的{entry['exam_subject']}。\n\n"
        options = eval(entry['option'])
        output = f"答案是{entry['answer']}。"
        question = f"{entry['question']}\n"
        for option in sorted(options.keys()):
            question += f"{option}: {options[option]}\n"

        formatted_entry = dict(instruction=prompt,
                               input=question,
                               output=output)

        formatted_data.append(formatted_entry)

    with open(opts.output_file, 'w', encoding='utf-8') as out_file:
        json.dump(formatted_data, out_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO
    )
    parser = argparse.ArgumentParser(prog='CMB SFT', description='')
    parser.add_argument("--output_file", type=str, default="../../data/cmb.json")
    args = parser.parse_args()
    convert(args)
