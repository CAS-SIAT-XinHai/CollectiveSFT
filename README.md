# CollectiveSFT

Office Code Repository of CollectiveSFT: Scaling Large Language Models for Chinese Medical Benchmark with Collective Instructions in Healthcare.

[![arXiv](https://img.shields.io/badge/arXiv-2407.19705-b31b1b.svg)](https://arxiv.org/abs/2407.19705) [![Model on HF](https://huggingface.co/datasets/huggingface/badges/resolve/main/model-on-hf-md.svg)](https://huggingface.co/CAS-SIAT-XinHai/CollectiveSFT)

🎉 **Congratulations!** We have achieved an outstanding score on the CMB [leaderboard](https://cmedbenchmark.llmzoo.com/static/leaderboard.html) with CollectiveSFT.

## Preprocessing

In the `preprocess` folder, you will find all conversion scripts used to transform datasets into the Alpaca format. Feel free to use them, but please note that you may need to apply for access to some datasets before they can be utilized.

## Train

Our training configuration is available in the `train` folder. You can train the model yourself using the [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory/) repository. Please install the llamafactory-cli first, then run the following command to start training. If you encounter any issues during the training stage, please refer to the original repository for assistance. Remember to replace the `dataset_info.json` and ensure all required data is in the `data` folder before running the train command.

```sh
FORCE_TORCHRUN=1 llamafactory-cli train train/collectivesft.yaml
```

## Eval

You can use the [CMB](https://github.com/FreedomIntelligence/CMB) repository to generate answers. Follow the setup instructions in the repository to configure the evaluation code. We have provided some useful scripts in the `eval` folder to help you validate and score the results more quickly than submitting them to the official website.

## Citation

If you find our work helpful in your research, please cite the following paper:

```tex
@misc{zhu2024collectivesftscalinglargelanguage,
      title={CollectiveSFT: Scaling Large Language Models for Chinese Medical Benchmark with Collective Instructions in Healthcare}, 
      author={Jingwei Zhu and Minghuan Tan and Min Yang and Ruixue Li and Hamid Alinejad-Rokny},
      year={2024},
      eprint={2407.19705},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2407.19705}, 
}
```