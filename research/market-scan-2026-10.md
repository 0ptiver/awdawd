# Market scan, Oct 2026: looking for LOW (not zero) saturation

Method: for each underserved audience, web-search for dedicated tools/services
and count real competitors. Scale: Crowded = 5+ dedicated products or free tools
that kill pricing; Moderate = 3-4; Thin = 0-2, mostly blogs/guides/gov pages.

Limits of this scan (be honest about these):
- Search results only. No traffic, revenue, or ad-spend data (Semrush account is
  out of API units; Meta Ad Library needs a connector sign-in).
- Reddit is not searchable from here, so there is no complaint-volume evidence.
- shieldmyshop.com, passpaw.com and getdrawnwest.com were blocked by the network
  policy, so those competitors were not inspected.
- "Thin" can mean a gap OR no demand. Only a paid ad test settles that.

## Results

| Niche | Verdict | Competitors found |
|---|---|---|
| IEP prep for parents | Crowded | IEP Advocate.ai, IEP Desk, EveryIEP (free), My IEP Hero, S.S. Education |
| Homeschool transcripts | Crowded | Gradefile, Homeschool Planet, Fast Transcripts |
| College aid appeal letters | Crowded (free) | Earnest, Going Merry, How2WinScholarships, SwiftStudent |
| Western hunting draw help | Crowded | GOHUNT, onX, HuntStand, Drawn West, BookYourHunt |
| Musician royalty audit | Crowded | Mogul, Unitesync, Chartlex, Songtrust |
| Pet international travel planner | Crowded | PawVoyage, Travel Ready Pets, PassPaw, Paws Abroad, Roll Pet, Petfly |
| Creator contract scanner | Crowded (free) | Justee, Snippet |
| Maternity/paid-leave calculators | Crowded (free) | LeaveCalc, Callie Calculator, SheCalculator, Standard |
| Travel nurse licensing | Served | Nursys e-Notify, StaffDNA, Nursa |
| Aging-parent paperwork organizer | Moderate | TendTo, Family Medical Organizer |
| Handmade cosmetics (MoCRA) | Moderate | MoCRA Kit, Stocksmith, Batchforja, Craftybase |
| Medicaid long-term-care prep for caregivers | Moderate, high risk | Fortuna Health, HeyMedicaid, Waterlily ($7M seed); human planners at flat fees; elder-law attorneys $6.5-15k |
| Plain-language letter decoder, Spanish-first | Thin | xPlainly, ClearNotice (English/IRS focus) |
| Kids' product safety (CPSIA) for handmade sellers | Thin | Mostly blogs (Craftybase, ComplianceGate); ShieldMyShop unverified |
| Dog/cat treat licensing + labels | Thin | TreatLabel (free, labels only); no state-license tool found |
| Hot sauce / acidified food compliance | Thin | Ardent Seller, FDA Registration Assistance (service) |
| Paid-leave claim filing workflow (not calculators) | Thin | gov pages only; unverified |
| Elopement legal requirements | Thin (content only) | photographer blogs; monetization unclear |

## Pattern

Low saturation shows up where (a) the audience is small or hard to size, (b)
the product needs maintained state-by-state rule data, and (c) the incumbents
are blogs and consultants, not software. A large audience plus easy to build
plus zero competition basically does not exist: pick two.

## Round 4: universal problems for a 35-65 Meta audience

The user can reach 35-65 cheaply on Meta. Universal needs are the most crowded.

| Problem | Verdict | Competitors found |
|---|---|---|
| Medical bill error review | Moderate | Bill Defense and similar contingency services, patient advocates, free scripts (Careroute). Flat-fee DIY gap |
| Property tax appeal | Crowded, already undercut | Ownwell (25-35%), Five Stone, O'Connor, AppealDesk ($49), TaxFightBack ($79) |
| Social Security claiming report | Moderate | AARP/CFPB free; MySSAgent, Maximize My Social Security, $97 advisor report |
| Class action claim finders | Saturated | Settlemate, Owed, Payout, Collect, Sparrow; payouts only $20-200 |
| Scam protection for aging parents | Moderate-crowded | Scammer Guardian, SeniorShield.AI, ElderVoice |

Pattern to copy: flat-fee, keep-100% newcomers undercut 25-40% contingency firms
in property tax. CORRECTION: I first guessed medical bills had the same gap.
A deep dive found it does not: at least 6 AI flat-fee checkers already exist
at $0-$129. See research/medical-bill-checker.md.

Meta policy: ads for financial products, employment and housing are limited to
age 18-65+ with no narrowing (special ad categories), which would remove the
35-65 advantage. Ads must not imply knowledge of a person's medical condition.
Confirm the category in Ads Manager before spending.

## Shortlist to validate with a $50-100 Meta ad test each

1. "Can I legally sell this?" checker for Instagram/Etsy makers (start with dog
   treats; add kids' products, sauces). Thin, IG-native, fear hook.
2. Spanish-first official-letter explainer. Thin on Spanish-first, largest
   audience, but ChatGPT is the substitute.
3. Medicaid long-term-care application prep for caregivers. Highest price and
   pain, moderate competition, highest liability (must not give legal advice).

## Round 5: adult children dealing with a parent's life (consumer, not local business)

| Niche | Verdict | Competitors found |
|---|---|---|
| Downsizing / clear-out inventory with AI value estimates | Crowded | SaveOr, Declutter AI, HomeZada, MovingBox |
| Siblings dividing a parent's belongings | Crowded, small | SaveOr, Partage, FairSplit, Estimonia |
| Assisted-living inspection report summaries | Crowded (free) | The Care Audit (50 states, free), a new national directory, state sites |
| Aging-in-place photo safety check | Thin, unverified | HomeSafeAI (site blocked), online OT photo-review services |
| Senior-living contract and fee decoder | Thin | No dedicated tool found. Incumbents are commission-paid (A Place for Mom, Caring.com, Seniorly, CarePatrol: 70-100% of first month's rent, up to $20k per placement). WaPo 2024 conflict-of-interest story |

Pain: hidden costs often $1,000+/month, move-in fees $1.5-5k, care-level
surcharges $500-2,500/month, 3-8% annual increases. Risks: families default to
the free commission advisor, AI contract-reading accuracy, liability, and
demand is unproven. Possible compounding asset: fee benchmarks built from
uploaded contracts.

## Round 6: deadline-driven decisions for 35-65 (ACA cliff, open enrollment)

- ACA enhanced subsidies expired 12/31/2025; the 400% FPL cliff is back; Senate
  bills to restore them failed. Over half of people who lost credits are 50-64;
  AARP/Avalere: avg +$4,600/yr for high-premium 50-64 enrollees.
- Real pain, but DEAD for a paid tool: at least 7 free calculators already exist
  (ThunderHarbor, Coast Retirement, BridgeToFI, CliffEdge, SubsidyGuard,
  QuantCalc, acacalc.com).
- Meta: ACA/individual health insurance and insurance quotes/consultations fall
  under the "Financial products and services" special ad category: age locked to
  18-65+, no narrowing. Our 35-65 targeting advantage disappears.
- Employer open enrollment: free tools from HSA banks; 86% of people stay with
  their current plan and 74% find choosing confusing, i.e. they do not pay to decide.

## Structural lesson (after six rounds)

Where 35-65 consumers have the most pain (health, insurance, money, housing) is
exactly where (a) Meta removes age targeting and (b) free AI and free calculators
already exist. Paperwork-help ideas keep failing for these two reasons, not
because of bad luck. A believable idea probably sits OUTSIDE those categories.

## Round 7: real needs for 35-65 (data first, then competitors)

| Need (data) | Verdict | Why |
|---|---|---|
| Loneliness (40% of 45+ lonely) | Dead | Timeleft ($20/mo, ~3M users, funded), Meetup (60M, free), Bumble BFF, Wyzr (40+), Stitch (50+, ~200k members). Hey! VINA went out of business Feb 2026: local network effects are a money pit |
| Travel (64% of 50+ expect to travel; 86% say top spending priority; AI deal use 8% to 16%) | Dead as flight deals | Going ($49/yr, 2M+ subscribers) and Thrifty Traveler dominate |
| Rising electric bills (+7.3% in a year) | Dead | Free comparison sites (ElectricChoice, Power to Choose); only 13 states plus DC are deregulated |
| AI that calls customer service for you | Dead for us | Pine AI: $25M Series A, ~20% of savings, $2-10 per task |
| Teens and AI chatbots (parent worry) | Dead | Bark, Qustodio, OpenAI parental controls |
| Newsletter for 50+ | Crowded | RetireHub: 13 newsletters, 440k subscribers, free and ad-supported |
| Laid-off 50+ job search (64% report age discrimination; 34.5% of long-term unemployed) | Real need, bad channel | Meta "employment" ad category locks age targeting |

Conclusion: of eight rounds, one idea (grocery-cost plans for 50+ couples) has
real need data and works with Meta targeting. Remaining unresearched needs:
sleep, pets, pain/mobility, home maintenance, hobbies.
