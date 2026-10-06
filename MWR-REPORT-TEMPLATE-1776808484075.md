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

### Finding 2: [Insecure User login and account registration details]

**Risk Rating:** High 

**Flag:** N/A

**Description:**
When a user login to their account or registers their account, their registration and login details, like email, username and password, are exposed in the backend, which makes things easier for the attacker to gain unauthorized access to the account and block the user out of their account. The root cause of this vulnerability is that there is no extra layer of verification that the user can use to constantly verify themselves that this is their account or being notified that there is someone that is trying to gain access to their account, and this might lead to the attackers seeing this information and gaining access to the user's account and changing the user's password so that they can block the user out of their own account, which leads to them now having full control of the user's account, which could put the users at risk as it gives attackers full access to perform fraudulent acts on the platform.

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
### Finding 3: [Insecure Voucher Purchase Form]

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
- For the verification of banking details for the voucher purchase, the development team should introduce a Multi-Factor Authentication [MFA] platform or API that will serve as an extra layer for security purposes. Before the user purchases a voucher, it should verify with the user's banking app, ask them a personal security question or request for a biometric verification so that the transaction can be verified. This platform or API should also notify the users if there is a suspicious transaction or activity that is happening in their account so that they can report it in a timely manner to prevent the issue escalating further.
- For the insecure users' banking details in the backend, the development team should add an extra security layer in the backend that encrypts the users' personal information so that attackers can hardly read the information and make it harder for them to get access to the user's personal information, This will  enhance the users' privacy.
- For the voucher purchase to correspond with the MWR balance for integrity purposes, the development team should introduce a platform or a machine learning model that will ensures that each and every transaction that occurs in voucher purchase follows  the ACID transactions rule. A for Atomicity, which means that the voucher transaction either completes fully or not at all. C for Consistency, which means that the MWR bucks balance should remain mathematically correct before and after the user has purchased the voucher, I for Isolation, which means that multiple users can purchase the vouchers without their transactions intefering with one another. Lastly, D for Durability, which means even if the user has bought a voucher, the transaction stays recorded and the balance stays the same even if the platform crashes. 
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
