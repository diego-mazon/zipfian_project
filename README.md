
# Keeping students engage with online courses

Online courses have given rise to a revolution in education. There is a large number of reasons for their success, namely, they are inexpensive (being most of them free), students do not have to follow a rigid schedule, the are taught by experts on the field, etc. But what makes them different from conventional courses, and unique, is the huge number of students who attend these courses: every internet user from all around the world is a potential student. In particular, for the dataset I have been using for this analysis, the average number of students per course was grater than 20,000. 

On the other hand, less than  5% of the total number of students received a certificate (equivalently, passed the course). And only 20% of the total got grades higher than zero. However, these percentages are not as relevant as they are for conventional courses: first, the number of students, rather than the fraction, who got a certificate is still large, and second — and more importantly — there were many students who watched a large number of videos or wrote several posts in the forums, but did not get good grades, probably because they were not interested in getting a certificate. 

Nevertheless, most students left the course during the first or the second week after they registered. In order to prevent students from giving up and identify different lifetime behaviors depending on features of the student, it would be interesting to estimate the probability that a given student or group of students (for example, students with certain highest degree of education) leaves the course after a given number of days. This way, we could identify those users who are more likely to keep engaged longer or offer an incentive to those who are probably going to leave the course within the next days.

The statistical method for this kind of study is called Survival Analysis. Its main object is the survival function, which tells us the probability that a student keeps engaged for a given time interval. 

For this project I decided to learn Survival Analysis because I realized that it is a powerful statistical tool with applications in many areas. In particular, it predicts client company engagement, which can be used to determine the best marketing approaches. It may also be extremely useful to develop strategies to maintain client engagement. 

Instead of using the total number of days between enrollment and the last day the student logged in, I use the number of days the student was actively interacting with the course. The reason is that the latter is more correlated to the number of videos the user watched, the number of chapter they explored, and the grade the student obtained.  In addition, among all features (explanatory variables) included in the dataset, I only used those who can be known before the course is closed, namely, the student’s gender, age, highest degree of education, and country from where the student follows the course. 

#### Interesting results from the exploratory analysis and the time-dependent regression

- Users with less than secondary education kept engaged longer than those with secondary education and with Bachelor’s degree and the same as those with a Mater’s or PhD degree.

- Students following the course from a few countries, especially Spain (but also Greece), kept significantly more days interacting with their course, regardless of their age, gender, or degree of education. They also obtained higher grades. Given the high unemployment rate in Spain (and Greece), it would be interesting to study how this variable (unemployment rate) correlates to grades and engagement.
  

#### Machine learning algorithms

- Random Forest and Logistic Regression to determine the correlations among features (gender, country, age, and highest degree of education), number of days the user was actively interacting with the course, grades they obtained, and whether or not they got a certificate.

- Aalen’s Additive model: Time-dependent linear regression (one linear regression for each day). Dependent variable: Hazard rate. Explanatory variables: Highest degree of education, age, country, gender. Parameter: number of days the student was actively interacting with the course.

#### Coding

Aside from cleaning, visualizing, and doing exploratory data analysis, I coded the function (kfoldcv within kfoldcv.py) to k-fold-cross-validate the survival function. This function, unlike the original k_fold_cross_validation within the lifelines library,  compares (for every day) the predicted probability that a student keeps engaged with the observed fraction of students with the same features that remained engaged. It returns the relative average difference between the predicted probability and the observed fraction. 

##### Language and libraries: 

Python (scikit-learn, Pandas, NumPy, [Lifelines], pickle, matplotlib)


[Lifelines]:https://github.com/CamDavidsonPilon/lifelines

