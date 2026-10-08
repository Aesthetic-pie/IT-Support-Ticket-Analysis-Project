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
### Finding 4: [Absence of privacy policy, terms of service and customer support contact details]

**Risk Rating:** Informational

**Flag:** N/A

**Description:**
It is mandatory that each and every web application that asks the user for their personal information when they use the website to have a privacy policy. A privacy policy it's a legal statement that describes how a website collect, uses, and protects the personal information of its users. It details what data is gathered, like names or email addresses, and how that information is stored and shared. This policy is important because users deserve to know how their personal information is used and protected. Terms of service are the rules and guidelines that users must agree to in order to use a website or a service. It outlines what is permitted, such as acceptable behavior, and what is prohibited, like copyright infringement, as well as consequences for violating the rules. This document is important because it allows the platform to legally terminate accounts that engage in malicious activity, giving them ground to ban users who try to exploit or attack the website. The users also deserve to contact the customer support side of the company in case they need assistance, report something or enquire if they have question so that they can get clarity. The root cause of these vulnerabilities is the oversight during the development phase or a lack of legal awareness by the developers, as sometimes teams rush to launch a site and prioritize features over compliance and transparency, and that could make the site to be untrustworthy to the users and attackers could take advantage of that.

**Reproduction Steps:**
1. You interact with the website as normal and click through the website features and there is no privacy policy, terms of service and customer support contact details anywhere on the website.

**Business Impact:**
The absence of terms of service and privacy policy poses a significant legal, financial and reputational risk on the web application. The web application could face regulatory fines for data privacy violations and be sued by the users. It could also reduce user trust because the absence of these documents exposes the organization to regulatory risk (e.g., under data protection laws such as POPIA/GDPR) and they are violating the user privacy rights, hence putting the reputation of the web application on the line. The absence of terms of services pose a significant threat on the web application because now this gives attackers privilege to use the customers information however they like and the exploit the web application to use it for fraudulent activities, which will make the web application lose sales and run at a loss. The absence of customer support contact details weakens the trust between users and the platform because it means that now when they encounter problems they will struggle to get assistance on time, or if they noticed suspicious activity in their account and they can't find contact details for assistance, it could lead to the problem escalating.

**Screenshot References:**
- Vulnerability_04_general_website.png

**Remediation:**
- To remediate this vulnerability, the development team should draft and implement a clear Privacy Policy and Terms of Service, accessible from when the user registers their account and checkout art pieces, outlining data handling practices. They should place clear and accessible link to both documents in the main navigation or footer across all pages of the web application. They should also establish a maintenance schedule for both of these documents so that they continuously review and update the policies whenever they deploy new features, change data collection practices or as data protection regulations evolve. The development team should also include the customer support contact details to enhance the trust between the platform and the users, as it also facilitates security and bug reporting because clear contact channels give users and external parties a direct line to report security vulnerabilities, bugs, or fraudulent activity before they are publicly disclosed or exploited.
 
---
### Finding 5: [Missing Referrer Policy Header]

**Risk Rating:** Informational

**Flag:** N/A

**Description:**
The web application does not provide a Referrer-Policy security setting in its HTTP responses. This setting controls how much information about the web application a user is visiting is shared with another website when the user follows a link or is redirected elsewhere. For example if a user buys a voucher and they now have to click a link to verify the transaction, the web application does not control how much information is shared between the web application the user is purchasing from and the web application the user is verifying from. Because this policy is missing, the browser may share the address of the page the user was visiting with the external website. Depending on the URL, this vulnerability could expose information about their browsing activity to external websites and potentially leaking sensitive information. While the missing header does not directly allow an attacker to take over an account or steal payment information, it can result in unnecessary information being disclosed outside of the application. The root cause of this vulnerability is that the web application server has not been configured properly to send an appropriate Referrer-Policy HTTP response header to control the amount of information that is shared between two sites. The application therefore relies on the browser's default behavior when deciding what referrer information should be shared with other websites. This means the application is not explicitly controlling the amount of information that may leave the web application when users navigate to external resources or websites. Users may reasonably expect their activity on the web application to remain within the application. If information about the pages they visit is unnecessarily passed to another website through an API, this creates an avoidable information disclosure risk. For example, if a user is viewing a particular artwork they wanna purchase and then follows an external link, information about the page they came from may be exposed to third party web applications.

**Reproduction Steps:**
1. Make sure that nikto is intalled on your kali linux then type a command in the Kali Linux to allow Nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up.

**Business Impact:**
Because the application does not control what referrer information is shared, most parts of the web page address that a user is visiting may be sent to another website when the user follows an external link, and this could potentially reveal information about a user's activity on the application to third-party websites. Although this vulnerability does not directly give an attacker access to user accounts or payment information, it creates an unnecessary risk of information being exposed outside the application because chances are the third party web application may also be vulnerable to attackers, which puts the user and the web application's information at risk of being exploited.

**Screenshot References:**
- Nikto_Vulnerability_Scanning_Output.png

**Remediation:**
- The development team should make the web application to be configured to tell users' web browsers how much information they are allowed to share with third party applications when leaving the website. A recommended setting is: [Referrer-Policy: strict-origin-when-cross-origin]. This setting limits the amount of information sent to other websites while still allowing normal website functionality to work. A stricter policy can also be used if the application does not require referrer information to be shared. The referrer policy header should be added to the application's server responses so that it is consistently applied across the website.
  
---
### Finding 6: [Missing Content-Security-Policy (CSP) Header]

**Risk Rating:** Low

**Flag:** N/A

**Description:**
The application does not have a Content-Security-Policy (CSP) header configured. A CSP is a security control that tells a user's web browser which websites and sources it is allowed to load content from, such as scripts, images, stylesheets, and other resources. Without this policy, the browser has fewer restrictions on what content can be loaded and executed within the web application. This means that if another vulnerability, such as a Cross-Site Scripting (XSS) vulnerability, were present in the application, there would be fewer browser-level protections to prevent malicious code from running. This is important because users may provide personal information or interact with pages containing account and transaction-related functionality. A CSP provides an additional layer of protection that can help reduce the impact of other security weaknesses. The root cause is that the web application has not been configured to send a Content-Security-Policy header in its responses. As a result, the user's browser is not given specific instructions about which sources the web application considers trusted. The web application therefore misses an opportunity to add an additional layer of protection against malicious or unexpected content being loaded or executed into the platform. It removes an important security layer that could help protect users if another vulnerability is discovered in the application, especially increasing the potential impact of attacks against users and exposing their browsing sessions and information.

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up.

**Business Impact:**
The main business impact is an increased level of risk of another web security vulnerability is present in the web application. Without a CSP, a successful attack such as XSS could potentially have a greater impact because the browser has fewer restrictions on what malicious content can do. Depending on the circumstances, this could allow an attacker to interfere with what a user sees, perform actions on their behalf, or attempt to access information available through the user's browser session. Although the missing CSP does not directly expose user information or provide an attacker with access to accounts, it removes an additional security control that could help limit the damage caused by other vulnerabilities.

**Screenshot References:**
- Nikto_Vulnerability_Scanning_Output.png

**Remediation:**
- The development team should implement a Content-Security-Policy that only allows the website to load content from trusted sources. A starting point could be: [Content-Security-Policy: default-src 'self']. This tells the browser to only load resources from the application's own trusted source by default. However, the policy should be tested and adjusted to match the web application's legitimate requirements. For example, if the Imgurr uses trusted external services for images, payment processing, fonts, or other functionality, those services may need to be explicitly allowed. Implementing a properly configured CSP will provide an additional layer of protection against malicious content and help reduce the potential impact of future web vulnerabilities.
---

### Finding 7: [Missing Permissions-Policy Header]

**Risk Rating:** Informational

**Flag:** N/A

**Description:**
The application does not include the X-Content-Type-Options security header in its responses. This header tells a user's web browser to trust the type of file that the web application says it is sending, rather than trying to guess the file type itself. For example, if the application says that a file is an image, the browser should treat it as an image instead of trying to interpret the file as another type of content, such as a webpage or script. Without this protection, the browser may sometimes try to determine a file's type on its own. This can become a security concern if the application allows users to upload files and an attacker is able to upload a file containing malicious content. The root cause is that the application has not been configured to send the X-Content-Type-Options header with its responses, as there is nowhere on the application where the user can upload their art piece to sell them cos it is waiting for an admin's approval. The application therefore does not explicitly tell the user's browser to strictly follow the file type provided by the server. This leaves the browser with the ability to attempt to determine the file type itself. If another vulnerability exists in the application's file-upload functionality, an attacker could potentially upload a file that the browser interprets differently from what the application intended. In certain circumstances, this could allow malicious content to be displayed or executed in a user's browser. 

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up.

**Business Impact:**
The main business impact is that users may have less protection when interacting with files provided by the application. If an attacker were able to combine this weakness with another vulnerability, such as an insecure file-upload function, a specially crafted file could potentially be interpreted by a user's browser as something other than what the application intended. Depending on the circumstances, this could result in malicious content being displayed to users or potentially allow an attacker to perform actions within a user's browser session. The missing header alone does not demonstrate that this attack is possible, but it removes a security control that could help prevent or reduce the impact of such attacks. 

**Screenshot References:**
- Nikto_Vulnerability_Scanning_Output.png

**Remediation:**
- The application should add the following security header to its responses: [X-Content-Type-Options: nosniff]. This tells the browser to not try to guess what type of file this is. Use the file type provided by the web application. The header should be applied consistently to the application's responses, particularly where files or user-uploaded content are involved. The application's file-upload functionality should also continue to validate uploaded files properly, including checking the file type, file contents, and permitted file extensions. This provides multiple layers of protection rather than relying on the security header alone.

---

### Finding 8: [Missing X-Content-Type-Options Header]

**Risk Rating:** Informational

**Flag:** N/A

**Description:**
The application does not include the X-Content-Type-Options security header in its responses. This header provides instructions to a user's web browser about how it should handle files received from the application. Normally, when a website sends a file, it also tells the browser what type of file it is. For example, an image may be identified as an image. The X-Content-Type-Options: nosniff setting tells the browser to trust this information rather than trying to work out the file type itself. The web application currently does not provide this instruction. As a result, the browser may attempt to determine the type of a file on its own in certain situations. This becomes more important for an art marketplace because the application may handle images and other files uploaded or provided to users. If an attacker were able to combine this weakness with another vulnerability, such as an insecure file-upload function, the browser could potentially interpret a specially crafted file as something more dangerous than the application intended. The root cause is that the application has not been configured to send the X-Content-Type-Options header with its responses. Because the header is missing, the web application does not explicitly instruct browsers to stop trying to determine the type of files themselves. The missing header does not, by itself, allow an attacker to upload malicious files or execute code. However, it removes an additional security layer that could help protect users from certain types of attacks. If another weakness exists in the application's file-upload or file-handling functionality, an attacker could potentially create a file that is intended to be treated as an image or another harmless file but is instead interpreted by the browser as executable web content. For Imgurr, where users may view or interact with uploaded artwork and other files, having the browser strictly follow the application's stated file types helps reduce this risk.

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up. 

**Business Impact:**
If this weakness were combined with another vulnerability, such as an insecure file-upload mechanism, an attacker could potentially cause a malicious file to be interpreted as executable web content. Depending on the circumstances, this could potentially allow malicious content to be displayed to customers or contribute to attacks such as Cross-Site Scripting (XSS). A successful attack of this nature could affect the confidentiality of information available through a user's browser, potentially expose customer activity, or allow actions to be performed within the user's session. There could also be an integrity impact if an attacker were able to use the resulting attack to alter what users see or interact with on the website. For an online art marketplace, this could potentially affect the presentation of artwork, customer-facing pages, or other website content. The finding does not currently demonstrate that these attacks are possible, so these impacts should be considered potential consequences if another vulnerability can be combined with the missing header. There is no direct evidence from this finding alone of data loss, service disruption, or a specific regulatory violation. However, reducing unnecessary security weaknesses helps protect customer information and supports good security practices.

**Screenshot References:**
- Nikto_Vulnerability_Scanning_Output.png

**Remediation:**
- The development team should configure the application's web server to include the following HTTP response header: [X-Content-Type-Options: nosniff]. This should be applied consistently to the application's HTTP responses, particularly responses that provide files or user-uploaded content. In simple terms, this tells the browser to use the file type provided by the application and do not try to guess what the file is. The development team should also review the application's file-upload functionality and ensure that it only allows file types that are required by the application, checks both the file extension and the actual contents of uploaded files, prevents uploaded files from being treated as executable web content, stores uploaded files in a location where they cannot be executed as website code, returns the correct Content-Type for files being served to users. After implementing the header, the team should test the application's normal file-upload and file-viewing functionality to make sure legitimate artwork and other files continue to work correctly. Implementing X-Content-Type-Options: nosniff together with proper file-upload validation provides multiple layers of protection rather than relying on a single security control.

---

### Finding 9: [Missing Strict-Transport-Security (HSTS) Header]

**Risk Rating:** Informational

**Flag:** N/A

**Description:**
The web application does not include the Strict-Transport-Security (HSTS) security header in its responses. HSTS is a security setting that tells a user's web browser to use a secure HTTPS connection when communicating with this website. HTTPS protects information while it travels between the user's browser and the website. This is particularly important for this web application because users may provide information such as login credentials, personal details, and potentially payment-related information. Without HSTS, a browser is not given instructions to automatically enforce HTTPS for future connections to the website. If the application is available over both HTTP and HTTPS in a production environment, an attacker positioned between the user and the website could potentially attempt to force the user onto the less secure HTTP connection. This assessment target is currently served over HTTP, so HSTS cannot provide protection for the existing HTTP connection. The missing header is therefore primarily a security hardening issue that should be addressed before deploying the application in a production environment using HTTPS. The root cause is that the application has not been configured to enforce HTTPS through the Strict-Transport-Security response header. In addition, the web application currently uses HTTP rather than HTTPS. This means that information exchanged between the user's browser and the application is not protected by HTTPS encryption. Without HTTPS and HSTS, if a customer logs into the art marketplace, sensitive information such as their username and password could be at risk if an attacker were able to intercept or manipulate an insecure connection.

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up. 

**Business Impact:**
If the application were deployed in production without HTTPS and appropriate HSTS protection, an attacker who is able to intercept a user's network connection could potentially attempt to downgrade the user's connection from HTTPS to HTTP. A successful downgrade or interception attack could expose information being transmitted between the customer and the application. Depending on what information is being transmitted, this could include login credentials, session information, personal details, or other sensitive customer data. This could affect confidentiality, meaning sensitive information could potentially be viewed by an attacker while it is being transmitted, integrity, which means that an attacker will be able to intercept an insecure connection and could potentially modify information being exchanged between the user and the web application, user trust, meaning exposure of customer information could damage the reputation of the art marketplace, and compliance, meaning if personal or payment-related information were exposed, the incident could potentially create privacy or regulatory concerns depending on the information involved and the applicable laws.

**Screenshot References:**
- Nikto_Vulnerability_Scanning_Output.png 

**Remediation:**
- Before deploying the application to production, the development team should enable HTTPS across the entire website to obtain and correctly configure a trusted TLS certificate for the application's domain, redirect HTTP traffic to HTTPS so that requests made using http:// should automatically be redirected to the secure https:// version of the website, and add the HSTS header to HTTPS responses [Strict-Transport-Security: max-age=31536000; includeSubDomains]. This tells the browser to use HTTPS for the domain for one year and to also apply the rule to its subdomains. They should also ensure the configuration is tested before deployment. The development team should verify that all pages, images, APIs, login functions, and other application features work correctly over HTTPS and that there are no remaining insecure HTTP resources. This will help protect customer information from being intercepted or modified while it travels between the customer's device and the art marketplace.

---

### Finding 10: [Outdated nginx Version (1.24.0)]

**Risk Rating:** Low

**Flag:** N/A

**Description:**
The web application is running an outdated version of nginx, identified as nginx 1.24.0. nginx is software that helps the website receive and process requests from users' browsers and deliver the website's content back to them. It is therefore an important part of the application's security. The version currently being used is behind newer available releases. Running an older version means the application may not contain security improvements and fixes that have been introduced in later versions. Older software can also become a security concern because security weaknesses discovered in previous versions may be publicly documented, allowing attackers to research the software version and determine whether known vulnerabilities could apply. The root cause is that the server has not been kept up to date with current nginx releases and security patches. The web application is therefore running an older version of an important server component instead of a supported and appropriately patched version. This is primarily a server maintenance and patch-management issue, rather than a vulnerability within the artwork marketplace's business functionality itself. Using outdated software increases the application's exposure to security risks that may already be known publicly. An attacker does not necessarily need to discover a completely new weakness. If a security vulnerability has previously been identified in the version of nginx being used, an attacker could research that version and attempt to determine whether the application is affected. The version number being exposed also gives an attacker useful information about the technology running the website, which can make it easier to research potential attacks. The presence of an outdated version does not, by itself, prove that the application can be compromised. The actual risk depends on which security vulnerabilities affect the installed version, whether security patches have been backported, and how nginx is configured.

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up.

**Business Impact:**
If the outdated nginx version contains a vulnerability that can be exploited against this application, the consequences could range from information disclosure to more serious attacks against the website. Depending on the vulnerability and how the server is configured, a successful attack could potentially expose confidential information, such as customer or application data, Alter website content, potentially affecting artwork listings or other information displayed to customers, Disrupt the website, preventing customers from browsing or purchasing artwork and provide attackers with a foothold from which they could attempt further attacks against the application. For Imgurr, a successful server-level attack could therefore affect customer trust, business operations, and the availability and integrity of the website. There may also be privacy or regulatory consequences if a successful attack resulted in the exposure of personal customer information. The exact compliance impact would depend on what information was exposed and the laws and regulations applicable to the business.

**Screenshot References:**
- Nikto_Vulnerability_Scanning_Output.png 

**Remediation:**
- The development or infrastructure team should upgrade nginx from version 1.24.0 to a current, supported release that contains the latest security fixes.
Review the nginx security advisories and CVEs relevant to the currently installed version to determine whether any known vulnerabilities require immediate attention, test the upgraded version in a non-production environment first to ensure that the website, artwork functionality, uploads, authentication, and other application features continue to work correctly. deploy the updated version to the production environment once testing has been completed. establish a regular patch-management process so that nginx and other server software are regularly checked for security updates rather than being updated only after a vulnerability is discovered, remove unnecessary version disclosure where possible, so that the exact nginx version is not unnecessarily revealed to external users. This reduces the likelihood that attackers can exploit publicly known weaknesses in an outdated version of nginx.

---

### Finding 11: [Server Leaks Inodes via ETags]

**Risk Rating:** Informational

**Flag:** N/A

**Description:**
The application is exposing an internal server detail through its ETag response header. An ETag is normally used by a website to help a browser determine whether a file has changed since the browser last downloaded it. This helps the website load faster because the browser does not always need to download the same file again. In this case, the server's ETag value contains an inode number. An inode is an internal identifier that the server's operating system uses to keep track of files. Users normally do not need to see this information, as it is part of how the server manages its files internally. For example, the application returned an ETag containing values similar to [0x6a9fad21 0x19c]. This indicates that information about how files are stored internally on the server is being exposed to users. The disclosure does not immediately allow an attacker to access the files themselves. However, it provides information about the underlying server's file system that would normally remain internal. The root cause is the server's configuration for generating ETag values. The web server is generating ETags using information associated with the files on the server, including their internal inode information, instead of using a value that does not reveal details about the underlying file system. As a result, information about the server's internal file structure is included in responses sent to users. The information exposed by the ETag is not normally useful to an ordinary customer browsing the art marketplace. However, it can be useful to someone performing detailed reconnaissance against the application. Think of it like accidentally showing a visitor a small part of the filing system behind the shop. The visitor cannot necessarily open the filing cabinet, but they have learned something about how the shop stores its records. On its own, this does not allow an attacker to log in, steal artwork, modify customer information, or take control of the server. However, attackers often collect small pieces of information like this and combine them with other weaknesses to build a better understanding of their target.

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up.

**Business Impact:**
The direct business impact of this finding is an unnecessary disclosure of information about the server's internal file system. If combined with another vulnerability, this information could potentially help an attacker better understand the application's underlying environment and plan further attacks. The potential impact could therefore include confidentiality, meaning no direct exposure of customer information has been demonstrated, but the additional server information could assist attacks that target sensitive data, integrity, meaning this finding alone does not allow an attacker to modify artwork, customer information, or other application data, availability, meaning this vulnerability alone does not provide a way to disrupt or take down the website, and security reconnaissance, meaning an attacker gains additional information about how the application is hosted and how files are managed internally.

**Screenshot References:**
- Nikto_Vulnerability_Scanning OutPut.png

**Remediation:**
- The development or infrastructure team should change the server configuration so that ETag values do not expose internal file-system information such as inode numbers. Where ETags are required, the team should configure the web server to use a method that does not disclose internal server details. If ETags are not required by the application, they can be disabled in nginx using [etag off]. The team should then verify that the application continues to load artwork, images, and other resources correctly and that browser caching continues to work as expected. The server should also be retested after the change to confirm that the inode information is no longer being returned in the ETag header.

---

### Finding 12: [Missing X-Frame-Options Header (Clickjacking Risk)]

**Risk Rating:** Low

**Flag:** N/A

**Description:**
The application does not include an X-Frame-Options security header. This header tells a user's browser whether a page from the application is allowed to be displayed inside another website. Without this protection, an attacker-controlled website may be able to display the application's pages inside an invisible or disguised frame. The attacker can then place their own content on top of the hidden application page to make it appear as though the victim is clicking something harmless. For example, a victim may believe they are clicking a button on a page offering a prize or viewing content, while they are actually clicking a button on the art marketplace underneath the attacker's page. This type of attack is known as clickjacking because the attacker tricks the victim into clicking something different from what they believe they are clicking. For an application that allows users to purchase artwork, spend MWR Bucks, submit reviews, or perform other account-related actions, this could potentially cause users to unintentionally perform actions on their accounts. The root cause is that the application has not been configured to prevent its pages from being displayed inside frames on other websites. The application does not provide an X-Frame-Options header, nor does it appear to have an equivalent browser policy that restricts which websites are allowed to embed its pages. As a result, the user's browser does not have clear instructions telling it to prevent the application from being loaded inside an attacker's webpage. The vulnerability creates an opportunity for an attacker to disguise actions performed on the application. A successful attack would generally require the victim to already be logged into the art marketplace, visit an attacker-controlled webpage, and interact with the attacker's webpage without realising that the application's page is hidden underneath it. If the victim clicks in the right location, the click could potentially be registered by the hidden application instead of the content the victim believes they are interacting with. This means that the vulnerability does not automatically give an attacker access to an account. Instead, it can be used to trick an already-authenticated user into performing actions they did not intend to perform.

**Reproduction Steps:**
1. Make sure that nikto is installed on your kali linux then type a command in the Kali Linux to allow nikto to scan website for any vulnerabilities using this command: nikto -h http://10.113.170.161, and that is where this vulnerability showed up.

**Business Impact:**
If successfully exploited, clickjacking could cause a logged-in customer to unintentionally perform actions on their account. Depending on which functions can be triggered through the affected pages, this could potentially include actions such as making a purchase, spending MWR Bucks, submitting content, changing account information, or performing other actions available to the user. The potential impact includes confidentiality meaning this finding alone does not directly expose customer information to the attacker, integrity, meaning an attacker could potentially cause a user to make unwanted changes or perform unintended actions while logged in. Financial impact, meaning if purchasing or voucher-related functionality can be triggered through the attack, a user could potentially spend money or account credits without intending to. user trust, meaning unauthorised actions performed through a customer's account could result in complaints and loss of confidence in the application. availability, meaning this finding does not directly allow an attacker to take the website offline or disrupt its availability. The attack does require user interaction and specific circumstances, particularly convincing a logged-in user to visit an attacker-controlled webpage. Therefore, the likelihood of successful exploitation is relatively limited, supporting a low severity rating.

**Screenshot References:**
- Nikto_Vulnerability_Scanning OutPut.png

**Remediation:**
- The development team should prevent sensitive application pages from being loaded inside frames controlled by other websites. The recommended protection is to add [X-Frame-Options: DENY]. This tells the browser to not allow this page to be displayed inside a frame on another website. If the application legitimately needs to display certain pages inside frames on the same website, the team could instead use [X-Frame-Options: SAMEORIGIN]. For modern browsers, the preferred and more flexible approach is to also use the Content Security Policy frame-ancestors directive [Content-Security-Policy: frame-ancestors 'none']. This provides stronger and more flexible control over which websites are allowed to embed the application's pages. The development team should apply the protection to sensitive pages, particularly pages that allow users to make purchases, spend account credits, modify account information, submit content, or perform other important actions. After implementing the protection, the team should test the affected pages to confirm that they cannot be embedded by an unauthorized external website while legitimate application functionality continues to work correctly.

---
## Conclusion

[Summarize your overall assessment. How many vulnerabilities were found, and at what severity levels? What is the overall security posture of the application? What are your top priority recommendations for the development team to address first?]
