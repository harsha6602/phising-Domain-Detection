# Phishing Domain Detection

## 1. Problem Statement

The rise of phishing attacks demands robust and efficient solutions for the detection of malicious domains. This project aims to address this critical cybersecurity challenge by leveraging advanced Deep Learning techniques.

## 2. Model Description

### Overview
Our model comprises two key components: 
1. **Phishing Domain Detection Module** (Uploaded on GitHub)
2. **Finding the targeted Domain** (To be uploaded soon)

![image](https://github.com/harsha6602/phising-Domain-Detection/assets/108540874/41f6ec2f-723a-412e-a3a8-1d92de69a019)
*architecture comprising both the components of our model*
 

### 1. Phishing Domain Detection Module
This section includes the first part of our project, available on GitHub. The module employs state-of-the-art Deep Learning techniques to identify and classify potential phishing domains. Below are some key highlights:

- this approach purely depends on domain name.
- A dataset of 26,206 legitimate domain names and 26,352 phishing domain names was created.
- We collected domain  features using WHOIS library and DNS resolver.
- 20 domain related features and 44 content based features have been used to train our model.
- The ANN was created and trained on the above dataset which yielded 88% accuracy in binary classification.
- On basis of this, a webpage was created.
- extention is also made which uploaded soon.

### 2. Finding the targeted Domain
This section includes the second part where the domain which is being targeted will be identified.
- VGG16 is used for finding the similarities in the logos or pictues between the phising domain and the legit domain website.(notebook uploaded)
- the content from the webpages such as html tags, css, and all design elements will be tokenized.
- using the above tokenized data will be fed into RNN which again finds similarities between legit and phising domain.
- combining the above results the targeted website will be flaged.


### Contacts
**Note**: The repository currently includes only the first part of the project. The second component will be uploaded soon to provide a comprehensive solution.

Feel free to explore, contribute, and stay engaged as we continue to enhance our Phishing Domain Detection project! 🚀
