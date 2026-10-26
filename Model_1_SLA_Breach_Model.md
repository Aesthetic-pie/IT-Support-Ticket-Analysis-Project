# Model 1: SLA Breach Logistic Regression Model

## Overview

This model analyses IT Support Tickets and predicts the probability of the tickets experiencing an SLA breach. SLA (Service Level Agreement) in simple terms is the targeted number of hours that the Support team must resolve the ticket by, and if the target hours pass without the ticket getting resolved, that is considered an SLA breach.

For instance, say we have a medium priority ticket that is queued. Say the target number of hours to resolve a medium priority ticket is 16 hours. If the 16 hours pass without the ticket getting resolved, that is considered an SLA breach. This model is more focused on analysing the responsiveness of the IT Support tickets to see if the SLA target was reached or not.

> **NB:** The model is a logistic regression model because it examines patterns in the data to estimate the risk probability of an SLA breach on the tickets, specifically the resolved tickets.

## Where I got the dataset & the preprocessing steps

I got the dataset from Kaggle, but it was stated that it is synthetic data that was generated using a Python model to resemble real cyber problems.

![Model 1 Preprocesing](Model%201%20Preprocesing.png)

Before I built the model, I checked that the dataset was clean and removed features that were not going to help the model predict, as seen in the screenshot above, because we were looking to predict SLA breach risk.

![Model 1 One hot encoding](Model%201%20One%20hot%20encoding.png)

I then used one-hot encoding to turn categorical data into numerical values. I used one-hot encoding specifically so that the machine doesn't rank the categorical data according to its importance during its prediction. For features like the SLA plan (standard, gold, platinum), I used numerical ranking so that the machine can analyse the tickets according to their importance.

## Python Libraries Used

- Pandas
- NumPy
- Scikit-Learn

## Challenges Faced while Building the Model

![Challenge 1](Challenge%201.png)

![Challenge 1 solved.](Challenge%201%20solved..png)

### Challenge 1: Defining the target (Y)

One of the challenges I faced while building the model was ***defining the target (Y)***. In machine learning, knowing how to define a target is one of the most precise yet difficult things to do. The dataset I was working with didn't have a probability field. I had to create a new field for the SLA breach, which was going to be the target (Y).

At first glance, I defined the target with very precise and refined criteria (for instance: `df["resolution_time_hours"] <= 24`) as seen in the first screenshot of three screenshots, and I ran the whole code with no errors, only to realise that when I reached the performance metrics to evaluate the model, I was getting an F1-score, recall, accuracy and precision of all 1.0, which means it was 100%. This was very suspicious because no realistic machine learning model gets an accuracy of 100%.

I knew that something was wrong with my code but I couldn't figure out where exactly, so I explained to AI what was happening and it advised me on what the problem could be, and I found out that what I did was ***overfitting***. My mistake was that I overfed the model too much information on how it should predict. Instead of giving it a few main examples and letting it figure out the rest, I fed it everything, each and every column, which made it cram answers and cheat to get 100% accuracy. What I did was like giving a student the memorandum before they write a test.

So I rewrote the less specific code with fewer examples to resolve the problem, and that stabilised the performance metrics to a reasonable percentage, as seen on the last two screenshots of three screenshots.

### Challenge 2: Imbalance

The other challenge I faced was ***imbalance***. During the `train_test_split`, I split the data using only tickets that were resolved, because that is where we can determine whether a ticket experienced an SLA breach, after it is resolved.

When it was time to evaluate the performance of the model using the performance metrics, it gave me an error stating that it couldn't calculate the metrics because of an imbalance between the train and `y_prob` data. When I checked the error, the problem was that I hadn't defined `y_prob`, which was the probability. So I went back to define it, and that is how I resolved the problem and got the performance metrics.

## Performance Metrics of the Model (Findings)

> **NB:** The dataset has 100 000 rows. I used 15 040 rows to test the model. The 15 040 rows were tickets that were resolved, since I was looking to analyse those resolved tickets.

I chose these performance metrics because they help me evaluate how well the model performed in predicting the risk probability of an SLA breach.

I found that for tickets that did not experience an SLA breach (**0**), meaning they were resolved on time, the model predicted less accurately, because the dataset used to train the model had fewer tickets that were solved on time. For tickets that experienced an SLA breach (**1**), the model predicted more accurately because it had more tickets that experienced an SLA breach.

### Classification report

|  | precision | recall | f1-score | support |
| --- | --- | --- | --- | --- |
| 0 | 0.68 | 0.75 | 0.72 | 6300 |
| 1 | 0.81 | 0.75 | 0.78 | 8700 |
| **accuracy** |  |  | 0.75 | 15040 |
| **macro avg** | 0.75 | 0.75 | 0.75 | 15040 |
| **weighted avg** | 0.76 | 0.75 | 0.75 | 15040 |

### What the metrics mean

- **Accuracy:** How often was the model correct?
- **Precision:** When the model predicts a risk, how often is it right?
- **Recall:** Of all the tickets actually breached / not breached, how many did the model find?
- **F1-score:** How well does my model balance precision and recall?

### Confusion matrix

|  | Predicted 0 | Predicted 1 |
| --- | --- | --- |
| **Actual 0** | 4754 | 1546 |
| **Actual 1** | 2205 | 6535 |

In this matrix, the model made 11 289 correct predictions out of 15 040 tickets and 3 751 incorrect predictions. This gives us an accuracy of 75%.

## Limitations of the Model

The model may struggle with complex relationships since it was trained on refined features like ticket priority, resolution time hours and SLA plan. If additional features are added, the model may struggle to adjust its algorithm to predict based on the additional factors.

## How the Model is Relevant to Solving the Real Problem at Hand

This model was designed to explore further the problem described in the statement on the first page of the whole project. It stated that some employees in certain companies complain that their IT Support departments are not resolving tickets on time, so the model evaluates and analyses exactly that delay in resolving tickets, using synthetic data to explore the idea.

This model will help teams review their overall performance for the month or week to see whether they managed to solve the majority of tickets in time to reach the SLA target, and if not, what can be done to improve their performance to hit the target.

In Model 2, we explored the IT Support department solution further.
