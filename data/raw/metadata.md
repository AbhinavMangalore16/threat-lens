# Description:
This dataset contains 48 features extracted from 5000 phishing webpages and 5000 legitimate webpages, which were downloaded from January to May 2015 and from May to June 2017. An improved feature extraction technique is employed by leveraging the browser automation framework (i.e., Selenium WebDriver), which is more precise and robust compared to parsing approach based on regular expressions. This dataset is WEKA-ready.

Phishing webpage source: PhishTank, OpenPhish
Legitimate webpage source: Alexa, Common Crawl

Anti-phishing researchers and experts may find this dataset useful for phishing features analysis, conducting rapid proof of concept experiments or benchmarking phishing classification models.


# Steps to reproduce:
The complete HTML documents and the related resources (e.g., images, CSS, JavaScript) are downloaded using the GNU Wget tool and Python script. This is to ensure proper off-line rendering in the browser. To automate the feature extraction, Selenium WebDriver and Python scripts were utilised to direct the browser to load the webpage, render the webpage content, extract the feature value, and save it to text files. The text files were later processed into a single Weka’s Attribute-Relation File Format (ARFF) file.

# Institution who sourced the data:
Universiti Malaysia Sarawak Faculty of Computer Science and Information Technology