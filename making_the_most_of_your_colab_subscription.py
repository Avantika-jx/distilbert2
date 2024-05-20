# -*- coding: utf-8 -*-
"""Making the most of your colab subscription

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/notebooks/pro.ipynb

# Making the most of your colab subscription

## Faster GPUs

<p>Users who have purchased one of Colab's paid plans have access to premium GPUs. You can upgrade your notebook's GPU settings in <code>Runtime &gt; Change runtime type</code> in the menu to enable Premium accelerator. Subject to availability, selecting a premium GPU may grant you access to a V100 or A100 Nvidia GPU.</p>
<p>The free-of-charge version of Colab grants access to Nvidia's T4 GPUs subject to quota restrictions and availability.</p>

You can see what GPU you've been assigned at any time by executing the following cell. If the execution result of running the code cell below is 'Not connected to a GPU', you can change the runtime by going to <code>Runtime &gt; Change runtime type</code> in the menu to enable a GPU accelerator, and then re-execute the code cell.
"""

gpu_info = !nvidia-smi
gpu_info = '\n'.join(gpu_info)
if gpu_info.find('failed') >= 0:
  print('Not connected to a GPU')
else:
  print(gpu_info)

"""In order to use a GPU with your notebook, select the <code>Runtime &gt; Change runtime type</code> menu, and then set the hardware accelerator drop-down to GPU.

## More memory

Users who have purchased one of Colab's paid plans have access to high-memory VMs when they are available.
You can see how much memory you have available at any time by running the following code cell. If the execution result of running the code cell below is 'Not using a high-RAM runtime', then you can enable a high-RAM runtime via <code>Runtime &gt; Change runtime type</code> in the menu. Then select High-RAM in the Runtime shape drop-down. After, re-execute the code cell.
"""

from psutil import virtual_memory
ram_gb = virtual_memory().total / 1e9
print('Your runtime has {:.1f} gigabytes of available RAM\n'.format(ram_gb))

if ram_gb < 20:
  print('Not using a high-RAM runtime')
else:
  print('You are using a high-RAM runtime!')

"""## Longer runtimes

All Colab runtimes are reset after some period of time &#40;which is faster if the runtime isn't executing code&#41;. Colab Pro and Pro+ users have access to longer runtimes than those who use Colab free of charge.

## Background execution

Colab Pro+ users have access to background execution, where notebooks will continue executing even after you've closed a browser tab. This is always enabled in Pro+ runtimes as long as you have compute units available.

## Relaxing resource limits in Colab Pro

Your resources are not unlimited in Colab. To make the most of Colab, avoid using resources when you don't need them. For example, only use a GPU when required and close Colab tabs when finished.

If you encounter limitations, you can relax those limitations by purchasing more compute units via pay as you go. Anyone can purchase compute units via <a href="https://colab.research.google.com/signup">pay as you go</a>; no subscription is required.

## Send us feedback!

<p>If you have any feedback for us, please let us know. The best way to send feedback is by using the Help &gt; 'Send feedback…' menu. If you encounter usage limits in Colab Pro consider subscribing to Pro+.</p>
<p>If you encounter errors or other issues with billing &#40;payments&#41; for Colab Pro, Pro+ or pay as you go, please email <a href="mailto:colab-billing@google.com">colab-billing@google.com</a>.</p>

## More resources

### Working with notebooks in Colab
- [Overview of Colaboratory](/notebooks/basic_features_overview.ipynb)
- [Guide to markdown](/notebooks/markdown_guide.ipynb)
- [Importing libraries and installing dependencies](/notebooks/snippets/importing_libraries.ipynb)
- [Saving and loading notebooks in GitHub](https://colab.research.google.com/github/googlecolab/colabtools/blob/main/notebooks/colab-github-demo.ipynb)
- [Interactive forms](/notebooks/forms.ipynb)
- [Interactive widgets](/notebooks/widgets.ipynb)

<a name="working-with-data"></a>
### Working with data
- [Loading data: Drive, Sheets and Google Cloud Storage](/notebooks/io.ipynb)
- [Charts: visualising data](/notebooks/charts.ipynb)
- [Getting started with BigQuery](/notebooks/bigquery.ipynb)

### Machine learning crash course
These are a few of the notebooks from Google's online machine learning course. See the <a href="https://developers.google.com/machine-learning/crash-course/">full course website</a> for more.
- [Intro to Pandas DataFrame](https://colab.research.google.com/github/google/eng-edu/blob/main/ml/cc/exercises/pandas_dataframe_ultraquick_tutorial.ipynb)
- [Linear regression with tf.keras using synthetic data](https://colab.research.google.com/github/google/eng-edu/blob/main/ml/cc/exercises/linear_regression_with_synthetic_data.ipynb)


<a name="using-accelerated-hardware"></a>
### Using accelerated hardware
- [TensorFlow with GPUs](/notebooks/gpu.ipynb)
- [TensorFlow with TPUs](/notebooks/tpu.ipynb)

<a name="machine-learning-examples"></a>

## Machine learning examples

To see end-to-end examples of the interactive machine-learning analyses that Colaboratory makes possible, take a look at these tutorials using models from <a href="https://tfhub.dev">TensorFlow Hub</a>.

A few featured examples:

- <a href="https://tensorflow.org/hub/tutorials/tf2_image_retraining">Retraining an Image Classifier</a>: Build a Keras model on top of a pre-trained image classifier to distinguish flowers.
- <a href="https://tensorflow.org/hub/tutorials/tf2_text_classification">Text Classification</a>: Classify IMDB film reviews as either <em>positive</em> or <em>negative</em>.
- <a href="https://tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization">Style Transfer</a>: Use deep learning to transfer style between images.
- <a href="https://tensorflow.org/hub/tutorials/retrieval_with_tf_hub_universal_encoder_qa">Multilingual Universal Sentence Encoder Q&amp;A</a>: Use a machine-learning model to answer questions from the SQuAD dataset.
- <a href="https://tensorflow.org/hub/tutorials/tweening_conv3d">Video Interpolation</a>: Predict what happened in a video between the first and the last frame.
"""



!pip install accelerate -U

!pip install transformers[torch]

!pip install scikit-learn

import nltk
nltk.download('punkt')

!pip install transformers datasets

import pandas as pd
import random
from collections import Counter
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from transformers import DistilBertTokenizerFast, DistilBertForMaskedLM, Trainer, TrainingArguments
from datasets import Dataset
import torch
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

import pandas as pd
import numpy as np

df =pd.read_excel(  "final_data.xlsx")

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
from datasets import Dataset


dataset = Dataset.from_pandas(df[['CM Remarks', 'CM Decision', 'RIC Remarks']])



train_testvalid = dataset.train_test_split(test_size=0.1)
test_valid = train_testvalid['test'].train_test_split(test_size=0.5)
train_dataset = train_testvalid['train']
test_dataset = test_valid['test']
eval_dataset = test_valid['train']

from transformers import AutoTokenizer, AutoModelForSequenceClassification


tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=2)



def tokenize_function(df):
    # Combine CM Remarks and RIC Remarks
    combined_remarks = [
        f"{cm} {ric if ric else ''}"
        for cm, ric in zip(df["CM Remarks"], df.get("RIC Remarks", [''] * len(df["CM Remarks"])))
    ]
    tokenized_input = tokenizer(combined_remarks, padding="max_length", truncation=True, return_tensors="pt")

    label_map = {"declined": 0, "approved": 1}
    tokenized_input["labels"] = torch.tensor([label_map[label] for label in df["CM Decision"]])

    return tokenized_input


train_dataset = train_dataset.map(
    tokenize_function, batched=True, remove_columns=["CM Remarks", "RIC Remarks", "CM Decision"]
)
eval_dataset = eval_dataset.map(
    tokenize_function, batched=True, remove_columns=["CM Remarks", "RIC Remarks", "CM Decision"]
)
test_dataset = test_dataset.map(
    tokenize_function, batched=True, remove_columns=["CM Remarks", "RIC Remarks", "CM Decision"]
)

training_args = TrainingArguments(
  output_dir="./distilbert-finetuned-OD5",
    num_train_epochs=3,
    per_device_train_batch_size=32,
    per_device_eval_batch_size=32,
    learning_rate=5e-5,
    weight_decay=0.01,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    lr_scheduler_type="linear",
    warmup_ratio=0.1,
    logging_steps=50,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)
trainer.train()

eval_results = trainer.evaluate(eval_dataset=eval_dataset)
print("Evaluation Results:", eval_results)
test_results = trainer.evaluate(eval_dataset=test_dataset)
print("Test Results:", test_results)

import torch
import re

def generate_rm_feedback(application_data, tokenizer, model):
    """
    Generates feedback for relationship managers based on the loan application
    and model prediction.

    Args:
        application_data (dict): A dictionary containing loan application features.
        tokenizer: The tokenizer used for the DistilBERT model.
        model: The fine-tuned DistilBERT model.

    Returns:
        dict: A dictionary containing feedback, missing_info_str, and mitigants_str
    """

    cm_remarks = application_data.get("CM Remarks", "")  # Handle missing remarks
    tokenized_input = tokenizer(cm_remarks, padding="max_length", truncation=True, return_tensors="pt")

    # Model Prediction
    with torch.no_grad():
        outputs = model(**tokenized_input)
        logits = outputs.logits
        predicted_class = logits.argmax().item()
        probability = torch.softmax(logits, dim=1)[0][predicted_class].item()

    # Business Logic Checks
    approval_conditions = {
        "AMC": application_data.get("AMC", 0) > 80000,
        "AMB": application_data.get("AMB", 0) > 10000,
        "Inward cheque bounces": application_data.get("Inward cheque bounces", 0) < 3,
        "Type of Activity": application_data.get("Type of Activity", "") == "Retailer",
        "Eligibility Amount": application_data.get("Eligibility Amount", 0) > 200000,
        "Banking Vintage": application_data.get("Banking Vintage", 0) > 3,
        "CIBIL Score": application_data.get("Consumer Bureau Score", 0) >= 700,
        "Posidex Index": application_data.get("Posidex Index", "").lower() == "good"
    }
    all_conditions_met = all(approval_conditions.values())

    feedback = ""
    missing_info_str = ""
    mitigants_str = ""

    # Detailed Feedback for Approval
    if predicted_class == 1 and all_conditions_met: # Approved
        feedback = (
            f"This application is likely to be approved based on a strong model prediction (Confidence: {probability:.2f}) "
            "and meeting all business rules. The applicant has a good credit history and financial profile. "
            "Based on the provided information, they are a suitable candidate for the loan."
        )
    # Detailed Feedback for Rejection (with mitigations)
    else: # Rejected since either the prediction class is 0 OR prediction class is 1 but all_conditions_met is false
        feedback = f"This application is likely to be rejected. "

        failed_conditions = []
        if predicted_class == 1:
            feedback += f"Model predicts approval (Confidence: {probability:.2f}), but some business rules are not met. "
        else:
            feedback = f"This application is likely to be rejected based on model prediction (Confidence: {probability:.2f}). "

        for condition_name, condition_result in approval_conditions.items():
            if not condition_result:
                if condition_name == "AMC":
                    feedback += f"AMC is {application_data.get('AMC', 0)}, which is below the required 80,000. "
                elif condition_name == "AMB":
                    feedback += f"AMB is {application_data.get('AMB', 0)}, which is below the required 10,000. "
                elif condition_name == "Inward cheque bounces":
                    feedback += f"There have been {application_data.get('Inward cheque bounces', 0)} inward cheque bounces, exceeding the allowed limit of 3. "
                elif condition_name == "Type of Activity":
                    feedback += f"The applicant's type of activity ('{application_data.get('Type of Activity', '')}') is not eligible for this loan. "
                elif condition_name == "Eligibility Amount":
                    feedback += f"The requested eligibility amount of {application_data.get('Eligibility Amount', 0)} is below the minimum requirement of 200,000. "
                elif condition_name == "Banking Vintage":
                    feedback += f"The banking vintage is {application_data.get('Banking Vintage', 0)} years, which is less than the required 3 years. "
                elif condition_name == "CIBIL Score":
                    feedback += f"CIBIL score is {application_data.get('Consumer Bureau Score', 0)}, which is below the recommended 700. "
                elif condition_name == "Posidex Index":
                    feedback += f"The Posidex Index is {application_data.get('Posidex Index','')}, not giving required confidence in application. "

    # Missing Information Check
    missing_info_keywords = {
        "income": ["income", "salary", "earnings", "pay stubs", "tax returns"],
        "employment": ["employment", "job", "work history", "employer", "position"],
        "credit_history": ["credit history", "credit score", "CIBIL score", "repayment history", "credit report"],
        "debt": ["debt", "liabilities","OD","loans", "outstanding balances", "monthly payments"],
        "collateral": ["collateral", "security", "assets", "property", "guarantor"],
        "investigation": ["investigation", "assessment", "review", "further details"],
        "verification": ["verification", "verified", "unable to verify", "document"],
        "business_details": ["business detail", "business profile", "operating since"],
        "posidex": ["posidex"],
        "business_vintage": ["business vintage", "operating history", "business detail", "business profile"],
        "business_financials": ["balance sheet", "profit and loss statement", "cash flow statement", "financial records", "business performance", "tax filings"],
        "personal_financials": ["personal assets", "personal liabilities", "net worth", "savings", "investments", "expenses"],

# ... (add more keywords as needed)
    }

    # Check for missing information but only add if not mentioned in failed_conditions.
    missing_info = []
    for category, keywords in missing_info_keywords.items():
        if not any(re.search(keyword, cm_remarks, re.IGNORECASE) for keyword in keywords):
            if category not in failed_conditions:
                missing_info.append(category)


    # Suggest potential mitigations based on missing info (customize based on your rules)
    mitigants = []
    for missing in missing_info:
        if missing == "income":
            mitigants.append("Provide income verification documents (e.g., recent pay stubs, bank statements).")
        elif missing == "employment":
            mitigants.append("Submit employment verification letter or offer letter, and provide details about job stability and history.")
        elif missing == "credit_history":
            mitigants.append("Obtain a detailed credit report and address any negative items or discrepancies. If CIBIL score is low, explain the reasons for any past credit issues and provide evidence of improved financial responsibility.")
        elif missing == "debt":
            mitigants.append("Submit a comprehensive list of outstanding debts, including balances and monthly payments. Consider debt consolidation or repayment options to improve debt-to-income ratio.")
        elif missing == "collateral":
            mitigants.append("Offer additional assets as collateral (e.g., property, fixed deposits, shares) or consider providing a guarantor.")
        elif missing == "investigation":
            mitigants.append("Conduct a thorough investigation into the areas highlighted for review and provide additional clarifying information or documents.")
        elif missing == "verification":
            mitigants.append("Submit the necessary documents for verification, such as bank statements, proof of address, or business registration documents.")
        elif missing == "business_details":
            mitigants.append("Provide detailed information about the business, including its history, ownership structure, products/services, and financial performance.")
        elif missing == "posidex":
            mitigants.append("Address any negative factors affecting the Posidex score, such as improving financial ratios or resolving outstanding legal issues.")
        elif missing == "business_vintage":
            mitigants.append("If the business is new, provide a detailed business plan and financial projections. Consider alternative loan products designed for newer businesses.")
        elif missing == "business_financials":
            mitigants.append("Submit audited financial statements (balance sheet, profit and loss, cash flow) for the past 2-3 years.")
        elif missing == "personal_financials":
            mitigants.append("Provide details of personal assets and liabilities, including savings, investments, and any outstanding debts.")


    # Prepare the output
    if missing_info:
        missing_info_str = f"Missing information: {', '.join(missing_info)}"
    if mitigants:
        mitigants_str = f"Possible mitigants: {', '.join(mitigants)}"


    return {
        "feedback": feedback,
        "missing_info_str": missing_info_str,
        "mitigants_str": mitigants_str,
    }

from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer, TextClassificationPipeline  # Import all necessary classes

model_path =  "/content/distilbert-finetuned-OD5/checkpoint-5064"

loaded_model = AutoModelForSequenceClassification.from_pretrained(model_path)

pipe = TextClassificationPipeline(
    model=loaded_model,
    tokenizer=tokenizer,
    return_all_scores=True
)

def predict_OD_status_and_feedback(application_data_4):
    """
    Predicts loan status, generates feedback, and returns relevant parameters.

    Args:
        application_data_4 (dict): Dictionary containing loan application features.

    Returns:
        dict: A dictionary containing the predicted label (approved/declined), confidence score,
              feedback, missing_info_str (if any), and mitigants_str (if any).
    """
    try:
        cm_remarks = application_data_4["CM Remarks"]
        prediction = pipe(cm_remarks)[0]

        predicted_label = prediction[0]['label'].replace("LABEL_", "")  # Convert label from "LABEL_0" to "declined" or "LABEL_1" to "approved"
        confidence_score = prediction[0]['score']

        feedback_dict = generate_rm_feedback(application_data_4, tokenizer, loaded_model)

        # Extract and format the relevant information from the feedback dictionary
        feedback_str = feedback_dict.get("feedback", "No feedback available.")
        missing_info_str = feedback_dict.get("missing_info_str", "")
        mitigants_str = feedback_dict.get("mitigants_str", "")

        # Add other relevant parameters to the result dictionary
        return {
            "predicted_label": predicted_label,
            "confidence_score": confidence_score,
            "feedback": feedback_str,
            "missing_info_str": missing_info_str,
            "mitigants": mitigants_str,
        }

    except KeyError as e:
        return {"error": f"Missing key in application data: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

new_application_data_4 = {
    "CM Remarks": "posidex bad base",
    "AMC": 90000,
    "AMB": 9000,
    "Inward cheque bounces":3 ,
    "Type of Activity": "retail",
    "Eligibility Amount": 110000,
    "Banking Vintage": 212,
    "Consumer Bureau Score": 699,
}


result = predict_OD_status_and_feedback(new_application_data_4)
print("\nOD Application Summary:")
for key in result:
    if key in result:
        print(f"{key}: {result[key]}")

pip install streamlit

import streamlit as st
# ... (your existing code)

# ... (your predict_loan_status_and_feedback function) ...
def main():

  st.title("Loan Application Review Assistant")
  # Define input fields
  input_text = st.text_area("Enter Credit Manager's Remarks:", "")
  amc = st.number_input("Enter AMC:")
  amb = st.number_input("Enter AMB:")
  inward_cheque_bounces = st.number_input("Enter Inward Cheque Bounces:")
  type_of_activity = st.selectbox("Type of Activity:", ["retail", "wholesale","service","manufacturer", "Other"])
  eligibility_amount = st.number_input("Enter Eligibility Amount:")
  banking_vintage = st.number_input("Enter Banking Vintage (in years):")
  consumer_bureau_score = st.number_input("Enter Consumer Bureau Score (CIBIL Score):")

  # Create a button for prediction
  if st.button("Predict"):
      # Create a dictionary of input data
      application_data_4 = {
          "CM Remarks": input_text,
          "AMC": amc,
          "AMB": amb,
          "Inward cheque bounces": inward_cheque_bounces,
          "Type of Activity": type_of_activity,
          "Eligibility Amount": eligibility_amount,
          "Banking Vintage": banking_vintage,
          "Consumer Bureau Score": consumer_bureau_score
      }
      result = predict_OD_status_and_feedback(application_data_4)
      st.subheader("Prediction Results:")
      if "error" in result:
        st.error(result["error"])
      else:
        st.write(result)
        st.write("Predicted Label:", result.get('predicted_label', 'N/A'))
        st.write("Confidence Score:", result.get('confidence_score', 'N/A'))
        st.write("Feedback:", result.get('feedback', 'No feedback available.'))
        if result.get('missing_info_str'):
          st.write("Missing Information:")
          st.write(result['missing_info_str'])
        if result.get('mitigants_str'):
          st.write("Possible Mitigants:")
          st.write(result['mitigants_str'])

streamlit run https://colab.research.google.com/drive/1KcFNxHlw68xTeoI9HYCf7wyYUW8-kImX#