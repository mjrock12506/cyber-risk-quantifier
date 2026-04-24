# Threat Model — Cyber Risk Quantifier

**Methodology:** STRIDE
**Scope:** Public web application, no user data persisted, no authentication
**Author:** Mridhul Jose

## Assets
- Application availability
- Application code integrity (GitHub repo)
- User input confidentiality (in-session only)

## Threat Inventory (STRIDE)

| Threat | Category | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| Malicious user submits pathological inputs to DoS the simulation | Denial of Service | Medium | Low | Input validation, capped ranges, simulation timeout |
| Attacker compromises GitHub repo | Tampering | Low | High | Branch protection, required PR reviews (future), 2FA on GitHub |
| Dependency supply chain attack (malicious NumPy, Streamlit package) | Tampering | Low | High | Pinned versions in `requirements.txt`, `pip-audit` monthly |
| Streamlit Cloud account takeover | Spoofing | Low | High | Strong password + 2FA on Streamlit Cloud account |
| User input leaked via logs | Info Disclosure | Low | Low | No user input logged; no analytics beyond Streamlit defaults |
| XSS via input rendering | Tampering | Low | Medium | Streamlit escapes all inputs by default; no raw HTML rendering |
| Reconstruction of org identity from input patterns | Info Disclosure | Low | Medium | No persistence; no server-side logging of inputs |

## Out of Scope
- Physical security of user's machine
- Phishing of the developer's GitHub credentials (personal security, not app security)

## Compliance Notes
- Not SOC 2 in scope (no customer data)
- Not HIPAA (no PHI)
- GDPR: no personal data collected beyond Streamlit Cloud's default analytics