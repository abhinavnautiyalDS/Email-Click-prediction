![image](https://github.com/user-attachments/assets/01660e33-262d-447b-9e4f-461cebfcc43f)

# **Smart Email Marketing: Predicting and Boosting Click-Through Rates**

# **Problem Statement**

The marketing team of an e-commerce site has launched an email campaign. This site has email addresses from all the users who created an account in the past.
They have chosen a random sample of users and emailed them. The email lets the user know about a new feature implemented on the site. From the marketing team perspective, success is if the user clicks on the link inside of the email. This link takes the user to the company site.
You are in charge of figuring out how the email campaign performed and were asked the following questions:
What percentage of users opened the email and what percentage clicked on the link within the email?

The VP of marketing thinks that it is stupid to send emails in a random way. Based on all the information you have about the emails that were sent, ***can you build a model to optimize in future how to send emails to maximize the probability of users clicking on the link inside the email?***

# **Datasets**

1. **email_table** - info about each email that was sent. 

- **email_id** : the Id of the email that was sent. It is unique by email.
- **email_text** : there are two versions of the email: one has “long text” (i.e. has 4 paragraphs) and one has “short text” (just two paragraphs)
- **email_version** : some emails were “personalized” (i.e. they had the name of the user receiving the email in the incipit, such as “Hi John”), while some emails were “generic” (the incipit was just “Hi,”).
- **hour** : the local time on which the email was sent.
- **weekday** : the day on which the email was sent.
- **user_country** : the country where the user receiving the email was based. It comes from the user ip address when she created the account.
- **user_past_purchases** : how many items in the past were bought by the user receiving the email

2. **email_opened_table** - the id of the emails that were opened at least once.

- **email_id** : the id of the emails that were opened, i.e. the user clicked on the email and, supposedly, read it.
  
3. **link_clicked_table** - the id of the emails whose link inside was clicked at least once.
- **email_id** : if the user clicked on the link within the email, then the id of the email shows up on this table.


## ** Data Undertanding and Feature engineering**

- The Email_table contains 100,000 rows and 7 columns, email_opened_table contains 10,345 rows and 1 column, and link_clicked_table contains 2,119 rows.

- First, I merged Email_table with email_opened_table to get the users who opened the email. Let’s call this merged DataFrame df1.

- Then, I created a new column in link_clicked_table named "click" and assigned it a value of 1 to indicate a click.

- Next, I performed a left join between df1 and link_clicked_table on a common key (e.g., user ID or email ID), and filled the missing values in the "click" column with 0.
  
= This resulted in a binary target feature click, where 1 indicates the user clicked the link and 0 means they did not.

- the result dataframe have no null and no duplicate rows.
- 



## **Exploratory Data Analysis**

1. **Distribution of Categorical Features**:

   ![image](https://github.com/user-attachments/assets/a53bc3e3-f8a9-4331-aea3-335b80bbb184)

   **Insights**:
   
- **Distribution of email_text**
  Short emails account for 55.7%, while long emails make up 44.3%.
  This suggests a slight preference toward sending shorter emails, which could imply an assumption that users engage better with concise content.

- **Distribution of email_version**
  Personalized emails dominate at 61.5%, whereas generic emails represent 38.5%.
  The emphasis on personalization aligns with best practices in email marketing, suggesting the team is already trying to optimize for engagement.

- **Distribution of weekday**
  Email distribution is fairly evenly spread across weekdays, with each day from Monday to Thursday having ~16% share.
  Friday (10.2%), Saturday (12.3%), and Sunday (12.2%) have comparatively fewer emails sent.
  This might indicate that marketing efforts are more focused on weekdays, possibly due to higher expected engagement during workdays.

- **Distribution of user_country**
  The majority of users are from the US (69.1%), followed by the UK (23.2%). France (3.9%) and Spain (3.8%) form smaller segments.

  The campaign is heavily skewed towards the US and UK markets, indicating a primary audience focus on English-speaking regions.

2. **Distribution of Numerical Features**

   ![image](https://github.com/user-attachments/assets/f05949cd-3ac7-4e70-bbb2-8d64ed2b65d3)

   **Insights**
   
  1. email_id:
  The distribution is uniform, indicating that email_id is just a unique identifier without any predictive power. It doesn’t carry meaningful information for modelling and should be excluded from training features to avoid introducing noise.
  
  2. hour:
  The distribution is right-skewed, with a peak between 8 AM and 12 PM, especially around 10 AM. This suggests emails are most frequently sent in the morning, possibly to maximise visibility and engagement — a business-driven choice likely based on user behaviour.
  
  3. user_past_purchases:
  The distribution is heavily right-skewed, where most users have made fewer than 5 purchases, and very few have high purchase counts. This indicates a typical long-tail effect common in e-commerce or marketing datasets, reflecting that only a small portion of users are highly active customers.
  
  4. click:
  The distribution is extremely imbalanced, with the majority of values being 0 (no click) and very few 1s (clicks). This highlights a class imbalance issue in the target variable, which can negatively impact model performance if not addressed through methods like resampling, class weighting, or appropriate evaluation metrics.


![image](https://github.com/user-attachments/assets/deff161c-b63c-4f20-85f2-dab83b8320b3)

![image](https://github.com/user-attachments/assets/f8281709-8b68-45f3-91ee-a5a104f0d9ea)



3. **How does the number of clicks vary across different weekdays?**

  **Insights**
  
  Click behaviour varies significantly by weekday:
  The highest number of clicks occurs on Wednesday (383), followed closely by Tuesday and Thursday (346 each), while Friday (187) shows the lowest engagement. This suggests users are most responsive to emails during the midweek, likely due to higher availability or work-related engagement. Click activity dips on weekends, possibly due to reduced work-related screen time and attention. Email campaigns may perform best when scheduled for midweek delivery

4. **How does the email version impact the number of clicks?**

  ![image](https://github.com/user-attachments/assets/4e37bc64-1908-4f49-b43c-f40828d57c22)

  **Insights**
  Personalized emails received significantly more clicks (1340) than generic ones (729), showing nearly 84% higher engagement. This suggests that customising content for recipients—such as using their names or tailored recommendations—increases relevance, trust, and encourages action. Generic emails may feel impersonal or spammy, reducing user interaction.


5. **Does the length of the email impact the number of clicks?**

![image](https://github.com/user-attachments/assets/7901526a-1d0f-47b8-a29e-44b58b1d9d71)

Yes. Short emails generated more clicks (1165) compared to long emails (904). This suggests that concise messaging is more effective in grabbing users’ attention and prompting action. Readers likely prefer quick, scannable content over lengthy text, especially in crowded inboxes.


6. **What is the best time of day to send emails for maximum clicks?**

![image](https://github.com/user-attachments/assets/7523e8d8-5617-4e48-8a9e-cfe19ef71267)

![image](https://github.com/user-attachments/assets/bf75eee8-fb42-4ceb-bcea-61d0cd96802b)


The highest number of clicks occurred at 10 AM (226 clicks), followed by 9 AM (215) and 11 AM (197). This indicates that late morning hours (9–11 AM) are the peak engagement window.
Clicks steadily rise from early morning and drop sharply after noon, suggesting that early distribution maximises engagement


7. **How does the user's country affect the number of clicks?**

![image](https://github.com/user-attachments/assets/e0687df8-e31b-4efb-946a-486508e1a2c3)
The US had the highest number of clicks (1,650), followed by the UK (738). The relatively fewer clicks from countries like France (98) and Spain (87) suggest that users from the US and UK are more likely to engage with the emails.
This could be due to factors such as localisation, familiarity with the brand, or higher engagement rates in these markets, suggesting that focusing more on these regions might boost campaign effectiveness.

8. **How does the number of past purchases influence the likelihood of clicking on the email link?**

![image](https://github.com/user-attachments/assets/8be90412-062a-4104-b69f-f27007de1f4e)

Users with higher past purchases tend to have higher click-through rates, as seen in the distribution. This suggests that more engaged or loyal customers are more likely to respond to email campaigns.
It could also indicate that these users are more familiar with the brand and may trust the content of the email more, leading to increased interaction with the email’s link. Targeting these users for special offers or personalised content might boost clicks even further.


## **Business Recommendations to Increase Email Click-Through Rates**

1. **Send Emails During Peak Times:**

Schedule emails between 9 AM and 11 AM, as this is when engagement is highest.

Avoid sending emails late in the afternoon or on weekends, as these tend to have lower click-through rates.

2. **Personalise the Emails:**

Use personalised versions of the emails (e.g., using the user’s name in the subject line or body), as personalised emails significantly outperform generic ones in terms of clicks.

Customised content makes the email feel more relevant, fostering trust and prompting action.

3. **Keep the Email Content Short:**

Opt for shorter email text (2 paragraphs instead of 4), as users engage better with concise, scannable content.

A brief and clear message with a direct call-to-action is more likely to encourage clicks than lengthy emails.

4. **Target High-Engagement Countries:**

Focus your efforts on regions like the US and UK, where users show higher engagement and click-through rates.

Localise the content to suit the preferences and language of specific regions to increase the likelihood of users clicking the link.

5. **Segment Users by Past Purchases:**

Target users with higher past purchases as they are more likely to click on the email links.

You could even create specific campaigns or promotions for these loyal customers, such as special offers or new product updates that cater to their interests.

6. **Optimize the Email Design for Mobile Devices:**

Ensure that the email is mobile-friendly since many users may access the email on their phones. A well-optimised design improves the chances of a click.

7. **A/B Test Email Versions:**

Continuously test both email versions (personalised vs. generic) and email text length (short vs. long) to identify the best-performing combination.

Make iterative improvements based on performance data to maximise click rates.


## **Data Preprocessing**

- I perform label encoding to encode categorical column

**Imbalanced dataset**
  Target feature in my dataset is imbalaned and if i trained model on this dataset then model prediction will based towards majority classes
![image](https://github.com/user-attachments/assets/7c885288-deef-4a23-9d66-fbfdc42e77f3)
  
  so , to Handle this problem i use **SMOTE** technique
![image](https://github.com/user-attachments/assets/7a0f535f-7c4e-480d-8019-b85ca59e3106)


## **Feature Selection**

for feature selection i have used sparsity property of lasso regression , Lasso regression is a kind of regularisation and what do we mean by regularistaion , regurisation is a technique which is used to reduce overfitting by adding extra term during a training of our model. there is a paramter in lasso regresion called alpha and if we increase the value of alpha then it makes the coefficients of less important features to zero , so those features left which are important for prediction.

## **Model Building**

#### **Data Splitting**:
I have split my dataset into three parts: Training set, Validation set, and Testing set, with a splitting ratio of 70:20:10. Now, I am going to train my model using the Training set and then check its performance using the Validation set. After that, I will perform hyperparameter tuning using the Validation set to find the best parameters. Once I find the best parameters, I will retrain my model using the Training set with these optimal parameters and evaluate its performance using evaluation metrics. Finally, I will test how my model performs on the unseen Testing set, which will give me an unbiased assessment of its performance

#### **Hyperparameter Tuning**

I have used two techniques for Hyperparamter Tuning
1. HalvingRandomSearchCV
2. RandomizedSearchCV

#### **Evauluation metrics**

When evaluating a classification model, several metrics can be used to assess its performance comprehensively. Below are key metrics and their significance:

1. **Accuracy Score**: This metric indicates the proportion of correct predictions made by the model out of the total number of predictions. While accuracy is straightforward and intuitive, it has a significant limitation: it does not provide information about the types of errors the model is making.

2. **Confusion Matrix**: The confusion matrix addresses the shortcomings of the accuracy score by detailing the types of errors. It provides a breakdown of the following:

3. **True Positive (TP)**: The model correctly predicts a positive class (e.g., predicting cancer when the patient actually has cancer).
False Positive (FP): The model incorrectly predicts a positive class (e.g., predicting cancer when the patient does not have cancer).
True Negative (TN): The model correctly predicts a negative class (e.g., predicting no cancer when the patient does not have cancer).
False Negative (FN): The model incorrectly predicts a negative class (e.g., predicting no cancer when the patient actually has cancer).
Ideally, the number of false positives and false negatives should be zero or close to zero.

4. **Precision (P)**: This metric measures the proportion of predicted positive cases that are actually positive:

       Precision=TP/(TP+FP)
Ideally, the precision value should be 1, indicating no false positives.

5. **Recall (R)**: Also known as sensitivity, recall measures the proportion of actual positive cases that are correctly classified:

Recall=TP/(TP+FN)
Ideally, the recall value should be 1, indicating no false negatives.

6. **F1 Score**: The F1 score is the harmonic mean of precision and recall, providing a single metric that balances both:

F1_Score =2 Precision * Recall/(Precision+Recall)


7. **ROC AUC**: The area under the ROC AUC curve (Receiver Operating Characteristic - Area Under the Curve) is a metric used to evaluate the performance of a classification model. It measures how well your model is able to distinguish between different classes



#### **Model Training**

For this task, I trained three models—logistic regression, decision tree, and random forest—and found that random forest achieved the highest accuracy among them.

![image](https://github.com/user-attachments/assets/3a0b5ea7-501e-4b7b-a5a9-edb400c9f19c)

![image](https://github.com/user-attachments/assets/51b4654f-5bab-475f-bfd5-c6f2654bf5a8)


## **Conclusion** :
The email marketing campaign analysis provides valuable insights and actionable strategies for improving future campaigns. Based on the exploratory data analysis and feature engineering, we identified key factors that influence user engagement and click-through rates.

- **Optimal Email Content**: Personalized emails, concise in length, significantly outperform generic and longer emails. This highlights the importance of tailoring content to each user and ensuring it is brief and direct.

- **Timing of Campaigns**: Emails sent during late morning hours (9 AM - 11 AM) have the highest click-through rates, emphasizing the need to schedule campaigns during peak engagement times.

- **Targeting High-Engagement Regions**: Focusing on countries like the US and UK, where user engagement is notably higher, could drive better results. Localization of email content is essential to boost relevance and engagement.

- **Customer Segmentation**: Targeting users with a higher number of past purchases proved effective in improving click rates, underscoring the importance of segmenting users based on past behavior and engagement.

- **Model Optimization**: Through feature selection using Lasso regression and handling the class imbalance issue with SMOTE, we were able to create a predictive model that identifies factors influencing user clicks effectively. The model’s performance was optimized using hyperparameter tuning techniques like HalvingRandomSearchCV and RandomizedSearchCV.

In conclusion, the combination of targeted content, optimal timing, personalized outreach, and efficient customer segmentation can significantly enhance the effectiveness of email marketing campaigns. Implementing these strategies, backed by data-driven insights, will help increase engagement and maximize click-through rates in future campaigns.


## **Model Deployment** 

I deploy my model in streamlit cloud 

![ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/534e114a-0686-4303-a6d8-b34f7acec1df)





# THANKYOU FOR READING 








