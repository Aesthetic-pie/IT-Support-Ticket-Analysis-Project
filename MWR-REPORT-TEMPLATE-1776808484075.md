# Security Assessment Report
## MWR CyberSec — Internship Application Portal

**Assessor:** [Your Name]
**TryHackMe Username:** [Your THM Username]
**Date of Assessment:** [Date]
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

### Finding 2: [Title]

**Risk Rating:** [High / Medium / Low / Informational]

**Flag:** [MWR{...} or N/A]

**Description:**
[What is the vulnerability? What is the root cause? Describe what the application does incorrectly and why it matters.]

**Reproduction Steps:**
1. [Step-by-step instructions to reproduce the finding]
2. [Be specific — include endpoints, parameters, and any values used]
3. [Another assessor should be able to reproduce this from your steps alone]

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
