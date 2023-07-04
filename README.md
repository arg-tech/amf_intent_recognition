# AMF Intent Recognition

![GitHub repo size](https://img.shields.io/github/repo-size/arg-tech/amf_intent_recognition)
![GitHub contributors](https://img.shields.io/github/contributors/arg-tech/amf_intent_recognition)
![GitHub last commit](https://img.shields.io/github/last-commit/arg-tech/amf_intent_recognition)
![GitHub](https://img.shields.io/github/license/arg-tech/amf_intent_recognition)

This repository contains the AMF Intent Recognition project, which focuses on recognizing and classifying user intents from natural language input in the context of argument mining and analysis. The intent recognition model provided in this repository is specifically designed to understand user intentions related to argumentation and discourse.

## Features

- Preprocessing: This repository doesn't contain the preprocessing steps.
- Training: It includes training scripts and utilities to build and train an intent recognition model using various machine learning algorithms.
- Evaluation: The repository contains evaluation scripts to assess the performance of the intent recognition model on argumentation-specific datasets.
- Inference: It provides utilities and examples for deploying the trained model to perform intent recognition on new inputs related to argumentation.
- Examples: The repository includes example code and datasets to help you get started with intent recognition in the context of argument mining and analysis.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/arg-tech/amf_intent_recognition.git
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```
3. In palce of step 2, you can just build the image by running the docker file:

   ```bash
   docker-compose up --build
   ```

## Usage

1. Prepare your dataset: Follow the guidelines provided in the repository's documentation to prepare your intent recognition dataset in the context of argumentation.
2. Preprocess the data: Use the preprocessing utilities provided in the repository to preprocess your dataset and convert it into a suitable format for training.
3. Train the model: Utilize the training scripts and utilities to train an intent recognition model on your preprocessed data, considering the argumentation-specific context.
4. Evaluate the model: Employ the evaluation scripts to assess the performance of your trained model on argumentation-specific test datasets or cross-validation sets.
5. Perform inference: Deploy the trained model and utilize the provided inference utilities to perform intent recognition on new user inputs related to argumentation.

## Web Services (REST APIS)

1. http://amfws-intentifier.arg.tech/amf_ts : Intent classification for argument framework with timestamps generation.
2. http://amfws-intentifier.arg.tech/amf_nts : Intent classification for argument framework with no timestamps generation.
3. http://amfws-intentifier.arg.tech/signature_ts : Intent classification for xaif jsons with timestamps generation.
4. http://amfws-intentifier.arg.tech/signature_nts : Intent classification for xaif jsons with no timestamps generation.


## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. Make sure to follow the repository's code of conduct.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- The AMF Intent Recognition project acknowledges the contributions of the ARG-Tech research group and their ongoing efforts in the field of argument mining and analysis.

## References

Budzynska, K., Janier, M., Reed, C., & Saint-Dizier, P. (2016). Theoretical foundations for illocutionary structure parsing. Argument & Computation, 7(1), 91-108.

Chesnevar, C., Modgil, S., Rahwan, I., Reed, C., Simari, G., South, M., ... & Willmott, S. (2006). Towards an argument interchange format. The knowledge engineering review, 21(4), 293-316.

Foulis, M., Visser, J., & Reed, C. (2020). Dialogical Fingerprinting of Debaters. Computational Models of Argument, 465–466. https://doi.org/10.323
