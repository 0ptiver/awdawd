# Pet toxin app deep dive (Oct 2026)

## Demand and urgency
- ASPCA Poison Control: 451,000+ calls in 2024 (+4%); about 51,000 chocolate calls
  in 2025 (about 5 chocolate cases per hour); human OTC medications are the #1
  category (16.5%); grapes/raisins and xylitol are common. Cat/lily calls spiked
  50% around Easter 2025. Pet Poison Helpline's busiest months are Nov-Dec.
- Hotlines charge per case: $95 (ASPCA), $89 (Pet Poison Helpline). People pay
  real money for fast decisions in this moment.

## Competition: many apps, weak traction
- ToxiPets: 3.5 stars from 15 iOS ratings, 3.7 from 44 on Google Play; $1.99
  weekly / $4.99 monthly / $14.99 yearly / $59.99 lifetime; 700k+ items, 37k
  plants; complaints: scan failures, AI images, "work in progress".
- Free authoritative rivals: ASPCA Poison Control app (free; chocolate and
  rodenticide calculators), Pet Poison Helpline web calculator (free). $1.99
  apps: Pet Poison Help, Chocolate Toxicity Calculator.
- Paid pet apps can work: Woofz (dog training) hit $20M ARR bootstrapped,
  21M downloads; pet UGC creators charge about $150-250 per video.

## Risks
- Plant-ID app accuracy 53-96%; PlantSnap identified 1 of 17 toxic plants. A false
  "safe" can kill a pet. Be conservative: unknown = unsafe; prefer barcode and
  ingredient OCR over visual ID; always show a one-tap call to poison control.
- Paywalling emergency information is an ethics and PR risk.
- Apple may review medical-style apps more strictly (not verified).

## Candidate wedge
Emergency triage, not just a scanner: what / how much / pet weight / time ->
risk level and next step (home, vet, poison control) across the top ~20 toxins,
including human medications and xylitol products via barcode. Generate a one-page
handoff for the vet or hotline. Free emergency basics (trust, virality); paid for
prevention: household scan, multi-pet profiles, seasonal alerts (Easter lilies,
Halloween, Nov-Dec holidays), pet-sitter sharing.

## Test now
Halloween is about 4 weeks away and Nov-Dec is the peak. Run organic demo-style
videos ("Halloween candy that can hurt your dog") to a free early-access page.

## STATUS: DROPPED (founder decision)
We will not engage a lawyer or veterinarian, and a safety-advice app needs both
(veterinary-law exposure by state, Apple 1.4.1 medical-app scrutiny, content
liability). Build prompts remain in /prompts for reference only
(pet-toxin-app-build-prompt.md, pet-toxin-app-lean-prompt.md). Do not build.
