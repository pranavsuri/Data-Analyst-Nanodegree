# P5: Identifying Fraud from Enron Email Dataset
> With the help of machine learning techniques, a classification model is built to identify Enron Employees who may have committed fraud based on the public Enron financial and email dataset.

## About
In 2000, Enron was one of the largest companies in the United States. By 2002, it had collapsed into bankruptcy due to widespread corporate fraud. In the resulting federal investigation, a significant amount of typically confidential information entered into the public record, including tens of thousands of emails and detailed financial data for top executives.

In this project, Enron employees who may have committed fraud are identified using machine learning algorithms on the email dataset.

#### The activities implemented in this project are:
1. **Exploring the Enron Dataset:** This involves data cleaning, outlier removal and analyzing.

2. **Feature Processing of the Enron Dataset:** Includes creation, scaling, selection and transforming of features.

3. **Choosing the Algorithm(s):** Multiple classification models are trained and tuned.

4. **Evaluation:** Involves validation and overall performance check.

## Learning Outcome
This project provided an excellent platform to apply machine learning on a real dataset. One of the challenges was to optimize the algorithm for a small and skewed dataset which made me learn a great deal about model validation and tuning it for optimum performance.

## Files
- `Enron_61702_Insiderpay.pdf` – Reference data.

- `Report.ipynb` – iPython Report for the project.

- `Report.html` – HTML export of the Jupyter notebook.

- `poi_id.py` – Main project file.

- `tester.py` – Script to test the algorithm performance.

- All other files in this directory are helper codes/data.

###### Data Files
- `my_classifier.pkl` – Developed classification model.
- `my_dataset.pkl` – Modified dataset (during the analysis).
- `my_feature_list.pkl` – List of features in classifier.
- `final_project_dataset.pkl` – The dataset for the project.

## Requirements
This project requires **Python 3** with `NumPy`, `Pandas`, `Seaborn` and `scikit-learn`.

It is recommended to use [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.

## License
[Modified MIT License © Pranav Suri](/License.txt)
