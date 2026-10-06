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

### Finding 1: [Example] Insecure Direct Object Reference

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
[After the user purchases the voucher of their choice with simulated bank card details, the balance on the user's MWR bucks does not decrease to show that they've spent their MWR bucks to buy their voucher, and when I check on http history of that specific activity on Burpsuite using the Repeater,I discovered that the voucher details after the actual purchase, like the cvv number, the voucher amount and the expiry date can be altered by the attacker so that they can purchase another voucher of their choice. The root cause of this vulnerability is that the details that are used to purchase the voucher are simulated card details, not real user details, and in that way, the web application cannot verify whether the user card details are real or not, and that puts the user's personal information at risk because it means that the attacker will now alter with their card details to also buy themselves the voucher.]

**Reproduction Steps:**
1. [Act as a normal user and interact with the website as burpsuite records every http activity within the site, and purchase the voucher with the simulated bank card details. To be more specific I bought a 15 MWR bucks voucher with these details: Amount is 15, Cardholder name:John Tail, Cardnumber: 1526478965412589 and cvv: 123. ]
2. [After the purchase I then went to the http history and checked out the activity with url of /api/vouchers/purchase and sent it to the repeater using ctrl+R combination.]
3. [Before modifying any request to ensure that I did get the voucher value I got on the web application. I then altered the user card deatils, more specifically the amount to 120 and altered the CVV to 368 and that is how I successfully bought another voucher from an attacker's perspective.]

**Business Impact:**
[What is the real-world impact if this vulnerability were exploited? Consider data confidentiality, integrity, availability, and regulatory or compliance implications.]

**Screenshot References:**
- [List screenshot filenames that support this finding]

**Remediation:**
[How should the development team fix this? Be specific and actionable.]

- - -

*Repeat the above template for each vulnerability found. Remember: document ALL findings, not just those that returned a flag.*

---

## Conclusion

[Summarize your overall assessment. How many vulnerabilities were found, and at what severity levels? What is the overall security posture of the application? What are your top priority recommendations for the development team to address first?]
