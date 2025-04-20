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




