# Security Assessment Report
## MWR CyberSec — Internship Application Portal

**Assessor:** Nozimanga Tshabalala
**TryHackMe Username:** nozimangatshabalala58
**Date of Assessment:** 10 September 2026
**Report Version:** 1.0

---

## Executive Summary

[Provide a high-level summary of your assessment. Include: the scope of testing performed, the total number of vulnerabilities identified, the overall risk posture of the application, and your key recommendations. This section should be understandable by a non-technical reader. Aim for 1-2 paragraphs.]

---

## Methodology

[Briefly describe the tools and techniques you used during the assessment. For example: manual testing with Burp Suite, browser developer tools, curl, custom scripts, etc. Include any approach you took to systematically cover the application's functionality.]

---

## Risk Rating Definitions

All findings in this report are rated using MWR CyberSec's standard risk rating scheme:

| Rating | Definition |
|--------|------------|
| **High** | Potential for an attacker to control, alter, or delete electronic assets. Unauthorized access, data capture, defacement. |
| **Medium** | Combined with other factors, potential for asset compromise. Conditional exploitation, configuration-dependent. |
| **Low** | Likelihood or impact of exploitation is extremely low. Weak ciphers, outdated protocols, programmatic CAPTCHA bypass. |
| **Informational** | Cannot be exploited directly but not aligned with best practice. Information disclosure, version leakage. |

---

## Findings

### Finding 1: [Example]

**Risk Rating:** High

**Flag:** MWR{example_flag_if_applicable} *(enter N/A if no flag was returned)*

**Description:**
The application allows authenticated users to access resources belonging to other users by manipulating the resource identifier in the request. No server-side check verifies that the requesting user owns the resource before it is returned.

**Reproduction Steps:**
1. Authenticate as User A and capture your session token.
2. Navigate to the resource endpoint and observe the resource identifier in the request (URL parameter, path segment, or request body field).
3. Replace the resource identifier with one belonging to User B (obtained by registering a second account or through enumeration).
4. Observe that User B's data is returned without an authorization error.

**Business Impact:**
An attacker could access, modify, or exfiltrate sensitive data belonging to any user of the application. In a real-world scenario, this could lead to data breaches, privacy violations, and regulatory non-compliance.

**Screenshot References:**
- screenshot_01_normal_request.png
- screenshot_02_manipulated_request.png
- screenshot_03_unauthorized_data_returned.png

**Remediation:**
Implement server-side authorization checks on every resource access. Before returning any resource, verify that the authenticated user has permission to access the requested item. Do not rely solely on client-supplied identifiers to determine ownership.

- - -

### Finding 1: [Insecure Voucher Purchase Form]

**Risk Rating:** High 

**Flag:** MWR{5EBBAC4C3AF798E} [NB: This is the voucher code I retrieved from manipulating the purchase form]

**Description:**
After the user purchases the voucher of their choice with simulated bank card details, the balance on the user's MWR bucks does not decrease to show that they've spent their MWR bucks to buy their voucher, and when I check on http history of that specific activity on Burpsuite using the Repeater,I discovered that the voucher details after the actual purchase, like the cvv number, the voucher amount and the expiry date can be altered by the attacker so that they can purchase another voucher of their choice. The root cause of this vulnerability is that the details that are used to purchase the voucher are simulated card details, not real user details, and in that way, the web application cannot verify whether the user card details are real or not, and that puts the user's personal information at risk because it means that the attacker will now alter with their card details to also buy themselves the voucher.

**Reproduction Steps:**
1. Act as a normal user and interact with the website as burpsuite records every http activity within the site, register your account and purchase the voucher with the simulated bank card details. To be more specific I bought a 15 MWR bucks voucher with these details: Amount is 15, Cardholder name:John Tail, Cardnumber: 1526478965412589 and cvv: 123.
2. After the purchase I then went to the http history and checked out the activity with url of /api/vouchers/purchase and sent it to the repeater using ctrl+R combination.
3. Before modifying any request to ensure that I did get the voucher value I got on the web application. I then altered the user card details, more specifically the amount to 120 and altered the CVV to 368 and that is how I successfully bought another voucher from an attacker's perspective.

**Business Impact:**
Since the users' private banking details are not secured, they can be used by attackers to their own advantage, which could lead to broken trust because customers no longer trust the platform as they will be convinced that their information is not safe and this will lead to them leaving the platform, which could lead to fewer sales and financial loss for the platform. Also with regards to financial loss, the platform might end up running at a loss because attackers can now manipulate the users' banking details to buy their own vouchers at no cost, which will make the platform to lose profit and run at a loss. The web application cannot verify whether the user gave existing banking details or not, since it is a simulated voucher purchase. This could lead to escalated security risks such as fraud because the attackers might end up using this vulnerability to try other tricks on the platform to convince the users into giving out their extra personal information for their own advantage, which will affect the platform's reputation

**Screenshot References:**
- Vulnerability_01_normal_request.png  [this is where I sent a normal request to verify if every detail was there before I altered anything]
- Vulnerability_01_manipulated_request.png [this is where I altered the cvv and voucher amount of 120 before I sent another request]
- Vulnerability_01_exploitation_proof.png [this is where I got the voucher code for an unauthorized 120 voucher] 

**Remediation:**
- For the verification of banking details for the voucher purchase, the development team should introduce a Multi-Factor Authentication [MFA] platform or API that will serve as an extra layer for security purposes. Before the user purchases a voucher, it should verify with the user's banking app, ask them a personal security question or request for a biometric verification so that the transaction can be verified. This platform or API should also notify the users if there is a suspicious transaction or activity that is happening in their account so that they can report it in a timely manner to prevent the issue escalating further.
- For the insecure users' banking details in the backend, the development team should add an extra security layer in the backend that encrypts the users' personal information so that attackers can hardly read the information and make it harder for them to get access to the user's personal information, This will  enhance the users' privacy.
- For the voucher purchase to correspond with the MWR balance for integrity purposes, the development team should introduce a platform or a machine learning model that will ensures that each and every transaction that occurs in voucher purchase follows  the ACID transactions rule. A for Atomicity, which means that the voucher transaction either completes fully or not at all. C for Consistency, which means that the MWR bucks balance should remain mathematically correct before and after the user has purchased the voucher, I for Isolation, which means that multiple users can purchase the vouchers without their transactions intefering with one another. Lastly, D for Durability, which means even if the user has bought a voucher, the transaction stays recorded and the balance stays the same even if the platform crashes. 

- - -

### Finding 2: [Inconsistent Review Handling]

**Risk Rating:** Medium

**Flag:** MWR{babfe5eeb88b3013f00f2f9743e7e584}

**Description:**
When a user login to their account or registers their account, their registration and login details, like email, username and password, are exposed in the backend, which makes things easier for the attacker to gain unauthorized access to the account and block the user out of their account. The root cause of this vulnerability is that there is no extra layer of verification that the user can use to constantly verify themselves that this is their account or being notified that there is someone that is trying to gain access to their account, and this might lead to the attackers seeing this information and gaining access to the user's account and changing the user's password so that they can block the user out of their own account, which leads to them now having full control of the user's account, which could put the users at risk as it gives attackers full access to perform fraudulent acts on the platform.

**Reproduction Steps:**
1. Act as a normal user and interact with the website as Burpsuite records every http activity within the site, register and login to your account.
2. After login to the account I then went to the http history and checked out the activity with url of /api/auth/login and sent it to the repeater using ctrl+R combination to view the activity in detail and then I sent the request to the web application before modifying everything to ensure that I have logged in to the account successfully.
3. On the web application as a user, I changed the password of the user which was originally Johntail12*! and changed it to Johnnydad*! as the new password as the user.
4. Then from the attacker's perspective I then went back to Burpsuite and changed the password that the user just changed, to #Beautytrees123. Now notice that the user knows their current password as Johnnydad*!, I then went to the web application and logged in with the user's password and the login failed, but from an attacker's perspective, I typed in the attacker's password which is #Beautytrees123, which means that I managed to log the user out of their account and gained access to it as an attacker.

**Business Impact:**
Since the users' registration and login information is exposed to attackers, attackers could hijack the users' accounts and log them out of their accounts whilst they gain unauthorized access to their accounts, and this creates mistrust between the platform and the users. Since attackers could hijack the user's accounts, this could lead to identity theft because it means that attackers will use the user's accounts and use them to do fraudulent acts on the platform, which violates the users' privacy and integrity.

**Screenshot References:**
- Vulnerability_02_user_login_failed.png [This is when I changed the password from Johntail12*! to Johnnydad78*! as a user and it failed]
- Vulnerability_02_unauthorized_successful_login.png [This is when I gained access to the user account as an attacker] 
- Vulnerability_02_unauthorized_password_change.png [This is when I changed the password of a user as an attacker to gain unauthorized access to the user account]
- Vulnerability_02_password_update.png [This is when I updated the password as an attacker] 

**Remediation:**
- For the registration and the logging in the account as the user, the development team should introduce a Multi-Factor Authentication [MFA] platform or API that will serve as an extra layer for security purposes. Before the user logs in to their account, it should verify with the user's personal details, ask them for an OTP they got through their messages or emails, a personal security question or request for a biometric verification so that the account can be verified. This platform or API should also notify the users if there is a suspicious activity or someone is trying to get into their account that is happening in their account so that they can report it in a timely manner to prevent the issue escalating further.
- For the insecure users' registration and login details in the backend, the development team should add an extra security layer in the backend that encrypts the users' personal information so that the attackers hardly see it and gain access to the user's accounts.
- To prevent the users from being logged out of their accounts, the development team should add the number of attempts that are allowed to login or reset the password, so that if the user continuously attempt to login to their account but they can't and they end up being told that their account is blocked, they should contact the support team of the platform to be assisted accordingly. 

---
### Finding 3: [Inconsistent review handling]

**Risk Rating:** Medium

**Flag:** MWR{babfe5eeb88b3013f00f2f9743e7e584} 

**Description:**
A user cannot access the reviews unless they bought an art-piece. So in order to get access to the reviews, As a user I purchased an art-piece in order to submit a review about it. After submitting the review, the user can still submit other reviews but the problem is that the from the second review they submit, on the frontend it shows a duplicate of the first review and rating but when checking on the http history of writing the second review from an attacker's perspective on Burpsuite, the second review that is different from the first review exactly as the user rated it, it is there exactly as the user typed it, but it is on the request site, and the when the request is sent to the site, the response displays another duplicate review of the rating of the user, which shows that the API that is responsible for managing reviews is performing inconsistently. The root cause of this vulnerability is the poor performance of the API that is responsible for managing the reviews because the API is not handling review logic properly and is exposing unreliable behavior, as it ignores different reviews but still accepting the requests, as in it allows users to submit multiple reviews, and overwriting silently but only showing duplicates of the first review back to the client. This vulnerability matters because if it is not solved in a timely manner it can put the users and the platform's integrity at risk, allowing attackers to manipulate ratings and possibly inject misleading content.

**Reproduction Steps:**
1. Act as a normal user and interact with the website as Burpsuite records every http activity within the site, register your account and purchase an artpiece.
2. After the purchase I then went to the http history on Burpsuite from an attacker's perspective and checked out the activity url of /api/shop/images and sent it to the repeater using ctrl+R combination, and that is where I retrieved the flag value.
3. I then interacted with the website again, went to the art-pieces I bought and wrote multiple different reviews on them, only to realize that the API returned duplicates of the first review.
4. I then went back to the http history to check out the activity of the multiple different reviews I wrote and realised that on the request site the ratings and the comment are exactly as the way I wrote them on the web application when I submitted them, and when I sent the request on Burpsuite it returns the duplicate of the first comment.

**Business Impact:**
Since the API mishandles multiple reviews, attackers could exploit this vulnerability to manipulate ratings or inject misleading content, which leads to data integrity risk as reviews are supposed to reflect genuine user feedback. It also leads to loss of trust & reputation, as customers rely on reviews to make purchase decisions, and if reviews don’t display correctly, users lose confidence in the platform’s fairness and reliability. Attackers could initiate a DDoS attack and flood the review management system to slow down the platform. Even if only the first review is shown, the backend may still store duplicates or inconsistent data, which could corrupt the reviews analytics. It also causes compliance issues, as inaccurate handling of user generated content could violate consumer protection standards.

**Screenshot References:**
- Vulnerability_03_different_reviews_output.png
- Vulnerability_03_flag_value.png
- Vulnerability_03_fourth_review_request.png
- Vulnerability_03_normal_request.png
- Vulnerability_03_second_review_request.png
- Vulnerability_03_third_review_request.png

**Remediation:**
- To remediate this vulnerability, the development team should should sanitize API responses to ensure no user sensitive information is disclosed in the backend for attackers. The development team should also ensure that the API review submission logic must enforce consistent handling of multiple reviews, either by rejecting duplicate submissions or updating existing reviews. Adopting strict API response schemas, implementing proper data segregation, and conducting regular security testing will prevent information disclosure and maintain data integrity.
---
### Finding 4: [Insecure Voucher Purchase Form]

**Risk Rating:** High 

**Flag:** MWR{5EBBAC4C3AF798E} [NB: This is the voucher code I retrieved from manipulating the purchase form]

**Description:**
After the user purchases the voucher of their choice with simulated bank card details, the balance on the user's MWR bucks does not decrease to show that they've spent their MWR bucks to buy their voucher, and when I check on http history of that specific activity on Burpsuite using the Repeater,I discovered that the voucher details after the actual purchase, like the cvv number, the voucher amount and the expiry date can be altered by the attacker so that they can purchase another voucher of their choice. The root cause of this vulnerability is that the details that are used to purchase the voucher are simulated card details, not real user details, and in that way, the web application cannot verify whether the user card details are real or not, and that puts the user's personal information at risk because it means that the attacker will now alter with their card details to also buy themselves the voucher.

**Reproduction Steps:**
1. Act as a normal user and interact with the website as burpsuite records every http activity within the site, register your account and purchase the voucher with the simulated bank card details. To be more specific I bought a 15 MWR bucks voucher with these details: Amount is 15, Cardholder name:John Tail, Cardnumber: 1526478965412589 and cvv: 123.
2. After the purchase I then went to the http history and checked out the activity with url of /api/vouchers/purchase and sent it to the repeater using ctrl+R combination.
3. Before modifying any request to ensure that I did get the voucher value I got on the web application. I then altered the user card details, more specifically the amount to 120 and altered the CVV to 368 and that is how I successfully bought another voucher from an attacker's perspective.

**Business Impact:**
Since the users' private banking details are not secured, they can be used by attackers to their own advantage, which could lead to broken trust because customers no longer trust the platform as they will be convinced that their information is not safe and this will lead to them leaving the platform, which could lead to fewer sales and financial loss for the platform. Also with regards to financial loss, the platform might end up running at a loss because attackers can now manipulate the users' banking details to buy their own vouchers at no cost, which will make the platform to lose profit and run at a loss. The web application cannot verify whether the user gave existing banking details or not, since it is a simulated voucher purchase. This could lead to escalated security risks such as fraud because the attackers might end up using this vulnerability to try other tricks on the platform to convince the users into giving out their extra personal information for their own advantage, which will affect the platform's reputation

**Screenshot References:**
- Vulnerability_01_normal_request.png
- Vulnerability_01_manipulated_request.png
- Vulnerability_01_exploitation_proof.png

**Remediation:**
- To remediate this vulnerability, the development team should should sanitize API responses to ensure no sensitive values are disclosed in the backend for attackers. The development team should also ensure that the API review submission logic must enforce consistent handling of multiple reviews, either by rejecting duplicate submissions or updating existing reviews. Adopting strict API response schemas, implementing proper data segregation, and conducting regular security testing will prevent information disclosure and maintain data integrity.
 
---
### Finding 5: [Insecure Voucher Purchase Form]

**Risk Rating:** High 

**Flag:** MWR{5EBBAC4C3AF798E} [NB: This is the voucher code I retrieved from manipulating the purchase form]

**Description:**
After the user purchases the voucher of their choice with simulated bank card details, the balance on the user's MWR bucks does not decrease to show that they've spent their MWR bucks to buy their voucher, and when I check on http history of that specific activity on Burpsuite using the Repeater,I discovered that the voucher details after the actual purchase, like the cvv number, the voucher amount and the expiry date can be altered by the attacker so that they can purchase another voucher of their choice. The root cause of this vulnerability is that the details that are used to purchase the voucher are simulated card details, not real user details, and in that way, the web application cannot verify whether the user card details are real or not, and that puts the user's personal information at risk because it means that the attacker will now alter with their card details to also buy themselves the voucher.

**Reproduction Steps:**
1. Act as a normal user and interact with the website as burpsuite records every http activity within the site, register your account and purchase the voucher with the simulated bank card details. To be more specific I bought a 15 MWR bucks voucher with these details: Amount is 15, Cardholder name:John Tail, Cardnumber: 1526478965412589 and cvv: 123.
2. After the purchase I then went to the http history and checked out the activity with url of /api/vouchers/purchase and sent it to the repeater using ctrl+R combination.
3. Before modifying any request to ensure that I did get the voucher value I got on the web application. I then altered the user card details, more specifically the amount to 120 and altered the CVV to 368 and that is how I successfully bought another voucher from an attacker's perspective.

**Business Impact:**
Since the users' private banking details are not secured, they can be used by attackers to their own advantage, which could lead to broken trust because customers no longer trust the platform as they will be convinced that their information is not safe and this will lead to them leaving the platform, which could lead to fewer sales and financial loss for the platform. Also with regards to financial loss, the platform might end up running at a loss because attackers can now manipulate the users' banking details to buy their own vouchers at no cost, which will make the platform to lose profit and run at a loss. The web application cannot verify whether the user gave existing banking details or not, since it is a simulated voucher purchase. This could lead to escalated security risks such as fraud because the attackers might end up using this vulnerability to try other tricks on the platform to convince the users into giving out their extra personal information for their own advantage, which will affect the platform's reputation

**Screenshot References:**
- Vulnerability_01_normal_request.png
- Vulnerability_01_manipulated_request.png
- Vulnerability_01_exploitation_proof.png

**Remediation:**
- For the verification of banking details for the voucher purchase, the development team should introduce a Multi-Factor Authentication [MFA] platform or API that will serve as an extra layer for security purposes. Before the user purchases a voucher, it should verify with the user's banking app, ask them a personal security question or request for a biometric verification so that the transaction can be verified. This platform or API should also notify the users if there is a suspicious transaction or activity that is happening in their account so that they can report it in a timely manner to prevent the issue escalating further.
- For the insecure users' banking details in the backend, the development team should add an extra security layer in the backend that encrypts the users' personal information so that attackers can hardly read the information and make it harder for them to get access to the user's personal information, This will  enhance the users' privacy.
- For the voucher purchase to correspond with the MWR balance for integrity purposes, the development team should introduce a platform or a machine learning model that will ensures that each and every transaction that occurs in voucher purchase follows  the ACID transactions rule. A for Atomicity, which means that the voucher transaction either completes fully or not at all. C for Consistency, which means that the MWR bucks balance should remain mathematically correct before and after the user has purchased the voucher, I for Isolation, which means that multiple users can purchase the vouchers without their transactions intefering with one another. Lastly, D for Durability, which means even if the user has bought a voucher, the transaction stays recorded and the balance stays the same even if the platform crashes. 
---
### Finding 6: [Insecure Voucher Purchase Form]

**Risk Rating:** High 

**Flag:** MWR{5EBBAC4C3AF798E} [NB: This is the voucher code I retrieved from manipulating the purchase form]

**Description:**
After the user purchases the voucher of their choice with simulated bank card details, the balance on the user's MWR bucks does not decrease to show that they've spent their MWR bucks to buy their voucher, and when I check on http history of that specific activity on Burpsuite using the Repeater,I discovered that the voucher details after the actual purchase, like the cvv number, the voucher amount and the expiry date can be altered by the attacker so that they can purchase another voucher of their choice. The root cause of this vulnerability is that the details that are used to purchase the voucher are simulated card details, not real user details, and in that way, the web application cannot verify whether the user card details are real or not, and that puts the user's personal information at risk because it means that the attacker will now alter with their card details to also buy themselves the voucher.

**Reproduction Steps:**
1. Act as a normal user and interact with the website as burpsuite records every http activity within the site, register your account and purchase the voucher with the simulated bank card details. To be more specific I bought a 15 MWR bucks voucher with these details: Amount is 15, Cardholder name:John Tail, Cardnumber: 1526478965412589 and cvv: 123.
2. After the purchase I then went to the http history and checked out the activity with url of /api/vouchers/purchase and sent it to the repeater using ctrl+R combination.
3. Before modifying any request to ensure that I did get the voucher value I got on the web application. I then altered the user card details, more specifically the amount to 120 and altered the CVV to 368 and that is how I successfully bought another voucher from an attacker's perspective.

**Business Impact:**
Since the users' private banking details are not secured, they can be used by attackers to their own advantage, which could lead to broken trust because customers no longer trust the platform as they will be convinced that their information is not safe and this will lead to them leaving the platform, which could lead to fewer sales and financial loss for the platform. Also with regards to financial loss, the platform might end up running at a loss because attackers can now manipulate the users' banking details to buy their own vouchers at no cost, which will make the platform to lose profit and run at a loss. The web application cannot verify whether the user gave existing banking details or not, since it is a simulated voucher purchase. This could lead to escalated security risks such as fraud because the attackers might end up using this vulnerability to try other tricks on the platform to convince the users into giving out their extra personal information for their own advantage, which will affect the platform's reputation

**Screenshot References:**
- Vulnerability_01_normal_request.png
- Vulnerability_01_manipulated_request.png
- Vulnerability_01_exploitation_proof.png

**Remediation:**
- For the verification of banking details for the voucher purchase, the development team should introduce a Multi-Factor Authentication [MFA] platform or API that will serve as an extra layer for security purposes. Before the user purchases a voucher, it should verify with the user's banking app, ask them a personal security question or request for a biometric verification so that the transaction can be verified. This platform or API should also notify the users if there is a suspicious transaction or activity that is happening in their account so that they can report it in a timely manner to prevent the issue escalating further.
- For the insecure users' banking details in the backend, the development team should add an extra security layer in the backend that encrypts the users' personal information so that attackers can hardly read the information and make it harder for them to get access to the user's personal information, This will  enhance the users' privacy.
- For the voucher purchase to correspond with the MWR balance for integrity purposes, the development team should introduce a platform or a machine learning model that will ensures that each and every transaction that occurs in voucher purchase follows  the ACID transactions rule. A for Atomicity, which means that the voucher transaction either completes fully or not at all. C for Consistency, which means that the MWR bucks balance should remain mathematically correct before and after the user has purchased the voucher, I for Isolation, which means that multiple users can purchase the vouchers without their transactions intefering with one another. Lastly, D for Durability, which means even if the user has bought a voucher, the transaction stays recorded and the balance stays the same even if the platform crashes. 
---
## Conclusion

[Summarize your overall assessment. How many vulnerabilities were found, and at what severity levels? What is the overall security posture of the application? What are your top priority recommendations for the development team to address first?]
