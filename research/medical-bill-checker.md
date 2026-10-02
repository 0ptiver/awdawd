# Deep dive: flat-fee medical bill checker (Oct 2026)

Verdict: DO NOT build a generic flat-fee checker. The "flat-fee gap" I claimed
earlier does not exist. The market is saturated and the price is near zero.

## Competitors (flat-fee / AI checkers, price)

- OverBilled: AI audit, dispute letter $29 if errors found
- Bill Bodyguard: free scan, $9 dispute pack
- IsMyBillWrong: free scan, audit from $49 flat
- mediloop: flat $69 / $129 / $499
- MedBillAI (uses Claude, confidence levels), Health Resolve, Bursify (sends
  appeals by fax/certified mail), LowerMedicalBills, MyMedBill
- Hospital Bill Checker: open source, free

Contingency / service:
- Goodbill: 20%, $1,000 cap, unpaid hospital bills not in collections, screens
  for charity care; BBB accredited
- CareRoute (Bill Defense): 25% (18% subscribers), $1,000 cap
- Resolve Medical Bills: 10-25% plus $249-499 deposit
- Independent advocates: $100-500/hour or $200-1,000 flat

Free: Dollar For (nonprofit; ~$93M debt eliminated since 2021; 42% of tracked
applications approved), Patient Advocate Foundation, SHIP counselors, many
free scripts and guides.

Not inspected (blocked by network policy): ismybillwrong.com, mediloop.ai,
overbilled.org. No independent accuracy tests of any AI checker were found.

## What a checker can and cannot verify

From the bill alone: duplicates, unbundling (CMS NCCI edit tables, free,
quarterly), excess units (Medically Unlikely Edits, free), math errors,
bill vs EOB mismatch, charges insurer denied but patient billed, no-surprise
balance billing, price outliers.
Needs the medical chart: upcoding, services not rendered.
Biggest dollars are usually NOT coding errors: charity care (50-100%
forgiven), self-pay/prompt-pay discounts (30-60%), negotiation (~30%).
(Share-of-savings breakdown not found in sources: this is inference.)

Error-rate claim: "80% of bills have errors" comes from billing advocates who
sell the service (Medical Billing Advocates of America). Independent
estimates: AMA 7.1% of paid claims (2013), NerdWallet 49% of Medicare claims
(2014), U. Minnesota 30-40%. Do not use 80% in ads.

## Data and build constraints

- CMS NCCI edits, MUEs, Medicare Physician Fee Schedule: free and public.
- CPT codes and descriptors are copyrighted by the AMA; commercial use
  needs a license (developer program is royalty-free only while building).
  HCPCS Level II and ICD-10 are public.
- Hospital price transparency data is messy: 49.4% compliance by one measure,
  21.1% fully compliant by another; only ~18% post real dollar prices broadly.
- RAND: private insurers paid ~254% of Medicare for hospital services in 2022.
- LLMs alone are poor medical coders (NEJM AI benchmark). Specialized models
  F1 about 0.54-0.74. A multi-pass system reached ~94% PPV on principal
  diagnoses in one study. False positives are the main product risk.

## Legal and privacy

- HIPAA does not apply to direct-to-consumer tools, but the FTC Health Breach
  Notification Rule and state laws (Washington My Health My Data Act, no size
  threshold) do. Uploaded bills are sensitive health data.
- Advocates need no license, but drafting legal documents or negotiating legal
  rights for pay can be unauthorized practice of law in some states. Safer:
  informational tool, user sends their own letter. Acting for the patient
  needs written authorization.
- Patients have a federal right to an itemized bill (and UB-04 via HIPAA
  access), free, within 30 days.

## Meta ads

- Debt relief / credit repair are prohibited commercial practices; financial
  products fall under a special ad category with no age narrowing (loses the
  35-65 targeting). "Are you struggling with medical debt?" is rejected
  (personal attributes policy). Needs checking in Ads Manager.
- 2026 benchmarks: health ~$28 CPA, finance/insurance ~$55 CPA. With competitors
  charging $9-$49, a $29-49 product is roughly break-even on ads before
  refunds, support and AI costs.

## Demand is real, supply is saturated

KFF: 41% of adults have health care debt; a third of insured adults got an
unexpected bill in two years; ages 50-64 most likely to carry medical debt.

## Options if we still want to be in this space

1. Skip it (recommended unless a distinct wedge appears).
2. Charity care application prep only (biggest dollars; competes with Dollar
   For free and content sites).
3. Refer users to existing services instead of building (needs affiliate terms
   checked; Meta restrictions still apply).
