# BUILD PROMPT: Pet Poison Emergency Triage App (iOS first, App Store ready)

> Paste everything below this line into Claude Opus 5.5 (Claude Code recommended).
> Items marked **[HUMAN GATE]** need a real person (veterinarian, lawyer, Apple account holder) and the model must stop and ask for them instead of faking them.

---

## 0. ROLE AND MISSION

You are a principal mobile engineer, security engineer, and product designer building a production iOS app from an empty repository. You will deliver a complete, secure, accessible, App Store-ready app, not a prototype.

**The app (working title `{{APP_NAME}}`)**: an emergency triage tool for worried dog and cat owners. In the moment a pet may have eaten something dangerous, it tells the owner, in plain language, how worried to be and exactly what to do next: relax and watch, call the vet today, or call poison control / go to an emergency vet now. It is NOT a diagnosis tool and NOT a replacement for a veterinarian.

Build order of priority, always: **(1) pet safety, (2) user privacy and security, (3) App Store compliance, (4) accessibility, (5) polish and distinctiveness, (6) features.** If two goals conflict, the higher one wins. Record every significant decision as a short ADR in `/docs/adr/`.

Before writing code: read the reference links in Appendix C, verify current package versions and APIs against their live documentation (do not rely on memory), and write a plan in `/docs/PLAN.md`. Work in the milestones in section 12 and stop at every HUMAN GATE.

---

## 1. PRODUCT DEFINITION

### 1.1 Users and moment
Pet owners, mostly 18-45, one hand holding the phone, possibly at 2 a.m., stressed, with a pet that may have just eaten chocolate, gum, a pill, a plant, grapes, or an edible. Stress shrinks working memory and narrows attention, so the product must ask one simple question at a time and give one clear next action.

### 1.2 Core flow (v1)
1. **Pet** (profile or quick entry): dog or cat, weight (lb/kg), optional name.
2. **What** did they eat: search a substance list, OR scan a product barcode (human medications, xylitol products, foods).
3. **How much** and **when**: amount with unit-aware helpers (for chocolate: type + ounces; for pills: tablets x strength; for gum: pieces).
4. **Result**: a risk level and next steps, computed deterministically on-device from vetted data.
5. **Act**: one-tap call to a poison control hotline, one-tap "find emergency vets" in Apple Maps, and a shareable one-page **handoff sheet** (what, how much, pet weight, time, case number) to give to a vet or hotline.

### 1.3 Free vs paid (never paywall emergency information)
- **Always free, no account:** the complete triage flow, hotline numbers, handoff sheet, one pet profile.
- **Paid subscription (RevenueCat or StoreKit 2):** multiple pet profiles, "Pet-proof my home" checklist scanner (room-by-room hazard checklist, no photos uploaded), seasonal on-device reminders (Halloween, Easter lilies for cats, Thanksgiving/Christmas foods), pet-sitter share card, case history.
- Emergency flow must never be blocked by a paywall, an account, a login, a network failure, or an ad. No ads. No tracking.

### 1.4 Explicitly out of v1
Accounts/login, social features, chat/AI assistant, photo upload of any kind, plant identification from photos, symptom-based diagnosis, telehealth, Android, web. (Plan the architecture so Android and optional plant-photo ID can come later; see section 5.5.)

---

## 2. NON-NEGOTIABLE PRINCIPLES

1. **The safety verdict is deterministic, never generative.** No LLM produces or modifies any risk verdict, dose, or instruction. The engine is plain, tested TypeScript over reviewed data.
2. **Unknown means unsafe.** If the substance, amount, pet weight, or data is missing, unverified, or out of range, the output is the highest-caution path ("Call poison control now"), never a reassuring one. The app must never output the words "safe" or "no problem"; use "low concern at this amount" only when a reviewed threshold clearly supports it.
3. **Works fully offline.** Everything required for triage and calling a hotline is bundled in the app. Network is only for optional barcode lookups and content updates.
4. **No account, no tracking, no ads, no third-party analytics SDKs.** Target the App Store privacy label "Data Not Collected." No ATT prompt.
5. **Never hard-block emergency info.** No jailbreak lockouts, no forced updates that disable triage, no certificate-pinning failures that break core flow.
6. **Be honest.** Never claim "veterinarian approved" unless a named licensed veterinarian actually signed off (section 5.3). Never fabricate ratings, testimonials, or review text.
7. **Original content only.** Do not copy text or lists from the ASPCA, Pet Poison Helpline, Merck, or other copyrighted sources. Write original wording from cited facts and link to sources.
8. **Accessible by default** (section 7.8).

---

## 3. TECH STACK AND ARCHITECTURE

Use the newest stable versions, verified at build time (as of this prompt: Expo SDK 57 / React Native 0.86 with the New Architecture on by default). Do not use Expo Go for the final app; use development builds and EAS Build.

| Concern | Choice | Notes |
|---|---|---|
| Framework | Expo (managed + config plugins), React Native, TypeScript `strict: true` | Build and submit with EAS, no Mac required for builds |
| Routing | `expo-router` | Typed routes |
| State | `zustand` (UI state) + pure functions for the triage engine | Engine has zero React/RN imports |
| Local DB | `expo-sqlite` | Encrypt at rest (see 8.3). Verify current SQLCipher support in the Expo docs; if unavailable, field-level encryption with a key in the Keychain |
| Graphics/motion | `@shopify/react-native-skia`, `react-native-reanimated`, `react-native-gesture-handler`, `expo-haptics` | For paper texture, stamps, tag physics (section 7) |
| Camera/barcode | `expo-camera` barcode scanning | On-device only |
| Share/PDF | `expo-print`, `expo-sharing` | Handoff sheet |
| Notifications | `expo-notifications`, local only | No push server, no tokens |
| IAP | RevenueCat (`react-native-purchases`) or StoreKit 2 module | Must ship a privacy manifest; verify |
| Fonts | `expo-font`, bundled files | OFL licenses only (section 7.3) |
| Backend (minimal, optional) | Cloudflare Workers (TypeScript), stateless | Barcode lookup proxy + signed content-pack hosting; no user database |
| CI | GitHub Actions + EAS | Section 8.7 |

### 3.1 Repository layout
```
/app                 expo-router screens
/src/engine          PURE triage engine (no RN imports), 100% unit-tested
/src/data            versioned, signed content packs + schema (zod)
/src/ui              design system components (section 7)
/src/lib             storage, crypto, network, haptics wrappers
/src/features        pets, scan, result, handoff, pantry, paywall
/backend             Cloudflare Worker + tests
/docs                PLAN.md, adr/, THREAT-MODEL.md, PRIVACY-DATA-MAP.md, APP-STORE.md
/legal               privacy-policy.md, terms.md, medical-disclaimer.md (drafts)
/scripts             contrast check, content-pack signer, pre-submit checks
```

### 3.2 Architecture rules
- `src/engine` is a pure library: input (pet, substance entry, amount, time) -> output (`RiskLevel`, reasons, steps, citations, `contentVersion`). Deterministic and unit-tested.
- All content is data (JSON) validated by `zod` at load and at build. A malformed or unsigned content pack is rejected and the app falls back to the bundled pack.
- Dependency injection for storage/network so the engine and features are testable.
- Feature flags and a remote "kill banner" (a signed message pack that can show a notice, e.g., "Corrected dosage info, please update") are allowed; remote code execution of any kind is not (no OTA code that changes triage logic without a new reviewed build; use signed data packs only for content).
- Turn on `react-native` strict lint rules, `eslint-plugin-security`, and TypeScript `noUncheckedIndexedAccess`.

---

## 4. TRIAGE ENGINE SPECIFICATION

### 4.1 Risk levels (each has a word, shape, color, and action; never rely on color alone)
| Level | Word | Shape | Primary action |
|---|---|---|---|
| `LOW_CONCERN` | LOW CONCERN AT THIS AMOUNT | circle | Watch at home; list signs to watch; call vet if signs appear |
| `CALL_VET_TODAY` | CALL YOUR VET TODAY | triangle | Call your vet; poison control if unreachable |
| `EMERGENCY` | GO NOW | octagon | Call poison control now / go to emergency vet; give handoff sheet |
| `UNKNOWN` | CAN'T RULE IT OUT. CALL NOW | octagon | Treated exactly as `EMERGENCY` |

`LOW_CONCERN` may only be returned when ALL are true: substance entry exists, `reviewStatus = "dvm_approved"`, a threshold table covers the pet species and the computed dose, input is within validated ranges, and the computed dose is below the lowest-concern threshold with a safety margin defined in the data. Otherwise escalate.

### 4.2 Data model (zod-validated)
```ts
type Substance = {
  id: string; names: string[]; category: 'food'|'medication'|'plant'|'household'|'recreational'|'other';
  species: Array<'dog'|'cat'>;
  hazardSummary: string;               // original wording
  doseModel?: DoseModel;               // mg/kg style thresholds when a reviewed model exists
  alwaysEscalate?: boolean;            // e.g. lilies for cats, antifreeze
  signsToWatch: string[]; timeCriticalNote?: string;
  sources: Array<{ title: string; url: string; accessed: string }>;
  reviewStatus: 'draft'|'dvm_approved'; reviewedBy?: string; reviewedAt?: string;
};
```
Thresholds are stored as data with units and tested for unit conversion (lb<->kg, oz<->g, mg<->g, tablets x strength). Use integer/decimal-safe math and clamp/validate ranges (e.g., pet weight 0.5-120 kg; reject NaN, negative, absurd values).

### 4.3 Seed content (starting values to VERIFY against the cited sources, then submit for DVM review)
Include these as `draft` until reviewed. All numbers below came from public veterinary references located during research and MUST be re-checked against the primary source before use.

- **Chocolate (theobromine)**, dogs: mild signs ~20 mg/kg; cardiovascular signs >40 mg/kg; seizures/tremors >60 mg/kg. Theobromine content differs by chocolate type (milk, dark, baker's, cocoa powder); source exact mg/oz figures from the cited paper/reference. Source: Weingart et al., J Small Anim Pract 2021, https://onlinelibrary.wiley.com/doi/10.1111/jsap.13329
- **Xylitol**, dogs: >0.1 g/kg risk of hypoglycemia; >0.5 g/kg may cause liver injury. Many gum/candy/peanut-butter/product labels list xylitol without amounts; if the amount per piece is unknown, escalate. Source: https://www.vetfolio.com/learn/article/xylitol-toxicity-in-dogs
- **Grapes / raisins / currants**, dogs: no reliably established toxic dose; treat any ingestion as potentially serious -> `alwaysEscalate`. Source: https://www.vettimes.com/news/vets/small-animal-vets/canine-grape-toxicosis
- **Ibuprofen / naproxen (NSAIDs)**, dogs: signs reported from ~50 mg/kg; kidney injury risk rises above ~175 mg/kg; CNS signs above ~400 mg/kg; cats are far more sensitive: use a much lower, DVM-defined threshold or `alwaysEscalate`. Source: Merck Veterinary Manual, https://www.merckvetmanual.com/toxicology/toxicoses-from-human-analgesics/toxicoses-from-human-analgesics-in-animals
- **Always escalate (no home-watch path):** lilies (cats; any exposure incl. pollen/vase water), antifreeze/ethylene glycol, rodenticides, acetaminophen in cats, sago palm, button batteries, any unidentified pill, any unknown product.
- Add (researched, sourced, DVM-reviewed before release): onions/garlic/chives, macadamia nuts, raw bread dough, alcohol, caffeine, nicotine/vape liquid, cannabis/THC edibles, essential oils (e.g., tea tree), ADHD/antidepressant medications, iron and vitamin D supplements, zinc (coins), pseudoephedrine.

### 4.4 Barcode / product lookups
- Human medications: barcode -> NDC -> active ingredient and strength using openFDA NDC (https://open.fda.gov/apis/drug/ndc) and DailyMed; show the ingredient and let the user confirm the number of tablets. If lookup fails or ingredient is unmapped -> `UNKNOWN`.
- Foods: use Open Food Facts for ingredients (check for xylitol/chocolate/grapes/macadamia). **Licensing:** Open Food Facts is ODbL (attribution + share-alike). Do not bundle or redistribute its data; query the API at runtime, show clear attribution, and flag for legal review **[HUMAN GATE: confirm ODbL compliance]**. Treat results as hints; never show a "safe" verdict from an ingredient list alone.

### 4.5 Engine tests (required, in CI)
- Table-driven tests for every threshold boundary (just below, at, just above) and every unit conversion.
- Property-based tests (e.g., `fast-check`): monotonicity (more substance never lowers risk), idempotence, no "LOW_CONCERN" without reviewed data, any invalid input -> escalate.
- Golden tests comparing outputs to a human-checked reference table that a veterinarian signs off **[HUMAN GATE]**.
- A test that scans every user-facing string and fails the build if it contains "safe" as a verdict, "diagnos", "cure", "treat your pet at home" instructions to induce vomiting, or any medication dosing instruction for the owner.

---

## 5. CONTENT, DATA SOURCING AND OPTIONAL AI

### 5.1 Hotlines
Show both US hotlines with their fees, and make each a `tel:` link. Verify the numbers and fees on the official sites before release **[HUMAN GATE]**: ASPCA Animal Poison Control and Pet Poison Helpline (both charge a per-case fee, roughly $89-$95; confirm current). Also always show "Call your own veterinarian or nearest emergency clinic."

### 5.2 Emergency vet search without data collection
Use a deep link to Apple Maps with a search query for "emergency veterinarian" (no location permission, no SDK, no API key). If the user wants nearby results sorted by distance, rely on Apple Maps doing it. Do not request location permission in v1.

### 5.3 Veterinary review gate **[HUMAN GATE]**
No substance can ship as `dvm_approved` until a licensed veterinarian (ideally with toxicology expertise) reviews its data, wording, and thresholds, and the app records `reviewedBy` and `reviewedAt`. Build a CLI that exports all draft content to a reviewer-friendly document and imports their approvals. The in-app "About our content" screen lists the reviewer and date only after this is real. Until then, show "Content in review" and keep the app in TestFlight only.

### 5.4 Content packs
- Bundled signed pack in the app + optional weekly update check. Sign packs with Ed25519; embed the public key; verify signature, schema, version monotonicity, and `reviewStatus` before use; keep the previous good pack as a rollback.
- In-app "Report an error" opens a prefilled mail composer (mailto) with the content version. No data collected.

### 5.5 Optional later: plant photo ID (design for it, do not build it in v1)
If added later it must (a) require explicit opt-in consent naming the third-party AI service and what is sent (Apple guideline 5.1.2(i) requires disclosure and explicit permission before sharing personal data with third-party AI), (b) strip EXIF/location, (c) route through the backend with App Attest and rate limits (never call an AI vendor from the app, never ship API keys), (d) present only "possible matches" with a confidence caveat, and (e) never produce a "safe" result; unrecognized or low-confidence always escalates.

---

## 6. SCREENS AND FEATURES (v1)

1. **First run:** one calm screen: what the app does and does not do; a single "I understand this is not veterinary advice" acknowledgment stored locally; link to sources and privacy. Not a wall of text.
2. **Home ("The Clipboard"):** one giant primary action "SOMETHING WAS EATEN," a small row for "Call poison control" and "Find emergency vet," recent cases, pet profile chip.
3. **Intake:** stepper of paper-form fields (pet, what, how much, when). One question per screen, custom large keypad, unit toggles.
4. **Result ("The Tag"):** risk tag (section 7), numbered next steps, signs to watch, sources, "This is not veterinary advice" line.
5. **Handoff sheet:** generates a one-page PDF/image styled like a carbon-copy chart: case number, time, pet, weight, substance, amount, computed concern, app/content version. User-initiated share only; no metadata beyond what is shown.
6. **Pet-proof my home (paid):** offline room-by-room hazard checklist (kitchen, bathroom, medicine cabinet, garage, garden, holiday), user ticks items; no camera.
7. **Seasonal reminders (paid):** local notifications for Halloween, Easter (lilies/cats), Thanksgiving, Christmas; permission requested contextually, never on first launch.
8. **Settings:** units, language (English first; structure for i18n), restore purchases, manage subscription, delete all local data, privacy, terms, content version and reviewer, open-source licenses/attributions.
9. **Paywall:** only shown from paid features, never from the emergency flow (section 10.4).

---

## 7. UI / UX AND DESIGN SYSTEM: "TRIAGE TAG AND CARBON COPY"

### 7.1 Why this direction (research-backed)
- 2026 design is reacting against the AI-generated look (soft gradients, perfect symmetry, glassmorphism, the same rounded pastel cards). The strategy that works is visible human decisions: texture, imperfection, tactile surfaces, hard edges, and warm non-tech palettes.
- Crisis UX research says: one thing at a time, large touch targets, plain language, high contrast, a single dominant action, progressive disclosure (see Smashing Magazine, "Designing for Stress and Emergency").
- Real veterinary/medical triage uses color-coded tags and carbon-copy paper forms. This app borrows that visual language so the interface *is* the metaphor: every result is a physical triage tag you can hand to a vet. I did not visually audit competitor apps; **before finalizing, review the App Store screenshots of ToxiPets, the ASPCA app, and Pet Poison Helpline and document in an ADR how this design differs.**

### 7.2 Concept
- **Surfaces:** unbleached paper on a kraft clipboard with a metal clip; ruled lines; the form is typed with a typewriter face; stamps and tags are the only "decoration."
- **Result = a triage tag:** hole-punched at the top with a string, a thick color band, big status word, perforated tear-off strip at the bottom ("TEAR OFF TO SHARE"). Dragging the tear strip creates the handoff sheet.
- **Handoff = carbon-copy triplicate:** white / yellow / pink sheet motif.
- **Case numbers** increment locally in a mono face like a rubber-stamped counter.
- Interface chrome is flat and hard-edged (2 px ink rules, square or tag-cut corners). No soft drop shadows; if depth is needed use a single hard offset shadow in ink.

### 7.3 Tokens (verify all contrast with a script in `/scripts`; adjust to pass; fail the build on violations)
- **Color:** paper `#F2EBDD`, kraft `#C9B38A`, ink `#14181F`, pencil `#6B6558`, tag-red `#B8281A`, tag-amber `#E9A21B`, tag-green `#2F8F5B`, carbon-pink `#F1B8B2`, carbon-yellow `#F4E08A`. No purple, no blue-to-violet gradients, no gradients at all, no glass/blur.
- **Dark mode:** do not invert. Provide a "night shift" variant: warm dark paper `#1E1B16` with cream ink `#EDE6D6`, same hues dimmed; test contrast.
- **Typography (all SIL OFL, bundled):** headings/status words **Big Shoulders Display** (industrial signage), body **Atkinson Hyperlegible** (designed for legibility; excellent for stressed and low-vision readers), form fields/case numbers **Courier Prime**. Support Dynamic Type through AX5 with layouts that reflow, not clip.
- **Grid:** 8 pt, minimum touch target 56 pt for primary controls (>= 44 pt everywhere).

### 7.4 Components to build
`ClipboardScreen`, `PaperSheet` (Skia procedural grain, no raster textures), `FormField` (typewriter label + underline), `BigKeypad` (custom numeric pad, one-handed), `UnitToggle`, `RiskTag` (4 levels), `StampMark`, `TearStrip` (gesture), `HotlineButton` (largest control on result), `StepList`, `CarbonSheet` (handoff), `CaseCounter`, `SourcesDrawer`, `Disclaimer` (single calm line).

### 7.5 Motion and haptics
- Result: tag swings in on its string (single pendulum, ~600 ms), stamp lands with one medium haptic.
- Steps slide like paper feeding into a clipboard; no bounce on everything, no spring overload, no confetti, no Lottie.
- **Reduce Motion:** replace all motion with instant or cross-fade. Haptics on by default but respect system settings.

### 7.6 Copy voice
Short, calm, clinical-warm, never cute during an emergency. Examples: "Okay. One step at a time." / "Tell us what was eaten." / "This is above the level where vets want to see pets." Never use emoji, exclamation marks in emergency screens, or hype words. No jokes in results.

### 7.7 Banned patterns (the "does not scream AI" checklist; fail design review if present)
Purple/indigo gradients; glassmorphism/blur cards; sparkles or magic-wand icons; AI/chatbot bubbles; soft 24 px-radius pastel cards with big blurry shadows; centered hero + three feature cards; generic 3D blobs or stock illustrations; emoji as icons; Inter/system-only look with no typographic personality; perfect symmetry everywhere; loading spinners in the emergency flow (use instant local results). All icons and marks are custom vector drawings; no AI-generated art anywhere in the app, icon, or screenshots.

### 7.8 Accessibility (blocking requirements)
- VoiceOver: every element labeled; correct traits; logical focus order; the risk tag reads "Emergency. Go now." first. Test with VoiceOver, Voice Control, Switch Control.
- Dynamic Type to AX5, no truncation of safety text. Reduce Motion, Reduce Transparency, Bold Text, Increase Contrast honored.
- Contrast WCAG 2.2 AA minimum (4.5:1 text, 3:1 large/UI); use shapes + words in addition to color (color-blind safe).
- Never convey urgency by color alone. Error messages are text, not just red.
- Fill in Apple's Accessibility Nutrition Label in App Store Connect honestly.

### 7.9 Visual QA process
Screenshot every screen at three device sizes + AX5 + Reduce Motion + night shift; run the grayscale and squint tests; save to `/docs/design-qa/`; run the contrast script; write an ADR describing differentiation from competitors.

---

## 8. SECURITY REQUIREMENTS (heavy; map to OWASP MASVS v2)

Treat this as a security-first build. Create `/docs/THREAT-MODEL.md` (assets, actors, abuse cases, mitigations) before coding features. Target **MASVS L1 fully and the relevant L2 controls**, and document each control's status in `/docs/SECURITY-CHECKLIST.md`.

### 8.1 What is sensitive here
Pet case history can reveal behavior a user would rather keep private (for example a cannabis edible ingestion or a medication overdose). Treat the case history, pet profiles, and any shared sheet as private data even though they are not human health records.

### 8.2 MASVS-STORAGE
- No secrets in the bundle, `app.json`, `eas.json` (public parts only), source, or logs. Only public config in the app.
- Case history and profiles: encrypted at rest (SQLCipher if supported, else field-level AES-GCM with a random key stored in the iOS Keychain via `expo-secure-store` with `WHEN_UNLOCKED_THIS_DEVICE_ONLY`). Never AsyncStorage for anything sensitive.
- Exclude the database from iCloud/iTunes backup (`NSURLIsExcludedFromBackupKey`) or document why not.
- Obscure the app-switcher snapshot when the app backgrounds. Do not use the system clipboard automatically. Disable keyboard caching/autocorrect on sensitive fields where appropriate.
- Provide "Delete all my data" that wipes DB, keys, caches, and notifications.

### 8.3 MASVS-CRYPTO
Use platform/`expo-crypto` or a vetted library (libsodium); no custom crypto; no hard-coded keys; keys generated per install; Ed25519 for content-pack verification.

### 8.4 MASVS-AUTH
No accounts in v1, so no passwords. Optional Face ID lock for the case-history screen only (LocalAuthentication), never for the emergency flow.

### 8.5 MASVS-NETWORK
- HTTPS/TLS 1.2+ only; App Transport Security on, no `NSAllowsArbitraryLoads`.
- Certificate/public-key pinning for the first-party backend only, with at least two pins (current + backup), an expiry, and a safe fallback. **Pinning failure must never break the offline emergency flow.** Provide a remote way to rotate pins via signed content.
- No third-party calls from the app except the first-party backend and Apple/RevenueCat. Do not call openFDA/OFF/vendors directly from the app; go through the backend proxy so no user identifiers or IPs leak to them and so rules/limits can be enforced.
- Validate and size-limit all responses; use timeouts; handle failure gracefully.

### 8.6 MASVS-PLATFORM
- URL schemes: allow only `tel:` and Apple Maps links; no custom URL scheme that accepts parameters from other apps, or validate strictly if added. Universal links verified.
- No WebViews in v1 (the terms/privacy pages open in the system browser). If a WebView is ever needed, disable JS where possible and restrict origins.
- Request only the permissions used: camera (barcode), notifications (contextual). Write clear, honest usage strings. No location, no photos library, no microphone, no contacts, no tracking.
- Handle deep links, pasteboard, and share extensions defensively; sanitize before display.

### 8.7 MASVS-CODE and supply chain (npm worms are real: Shai-Hulud 2025-2026)
- Package manager with a **committed lockfile**, exact version pinning, `npm ci`/frozen lockfile in CI, and install-script protections (pnpm `onlyBuiltDependencies` or `--ignore-scripts` with an allowlist). Add a minimum-release-age or manual review delay for new package versions.
- Minimize dependencies; justify each in an ADR; avoid abandoned or single-maintainer packages for security-sensitive roles.
- CI gates: typecheck, lint (`eslint-plugin-security`), tests, `npm audit`/`osv-scanner`, secret scan (`gitleaks`), license check, SBOM generation (CycloneDX), and a native-binary scan (MobSF) on the release build.
- GitHub: branch protection, required reviews, signed commits where possible, 2FA, Dependabot security updates, secret scanning, least-privilege `GITHUB_TOKEN`, pinned third-party Actions by commit SHA, no `pull_request_target` with untrusted code.
- Expo/EAS: secrets only in EAS secrets, never in the repo; separate dev/preview/production profiles; protect the Apple/EAS credentials with a hardware-key 2FA **[HUMAN GATE]**.
- Static content safety: bundled data is validated at build time; build fails on schema errors or unreviewed substances in a release channel.

### 8.8 MASVS-RESILIENCE (proportional)
Because core safety info must stay available to everyone: no hard blocks. Implement light, **log-local-only** tamper and jailbreak signals if desired; never prevent the emergency flow. Use release builds with Hermes bytecode, strip debug code and sourcemaps from the shipped bundle, and remove console logging.

### 8.9 MASVS-PRIVACY
Collect nothing. No device identifiers, no analytics SDK, no crash reporter that sends PII (if a crash reporter is added, use a privacy-reviewed option with scrubbing and declare it accurately; default is none, use Xcode/App Store Connect crash reports and TestFlight feedback). Provide `/docs/PRIVACY-DATA-MAP.md` listing every datum, where it lives, why, retention, and deletion.

### 8.10 Backend (Cloudflare Worker) hardening
- Stateless; no user DB; no PII; no request body logging; minimal access logs; short retention.
- **Apple App Attest** verification for each request (verify attestation and assertions server-side; cache keys; counter checks) plus per-device and per-IP rate limiting and global budget caps. Return generic errors.
- Strict input validation (barcode format/length), allowlisted upstream hosts only (SSRF-safe), response caching, request size limits, CORS closed, security headers, TLS only, secrets in Worker secrets, dependency scanning.
- Signed content packs served read-only; signing key kept offline/HSM-backed, never in the repo or CI **[HUMAN GATE: key custody]**.
- Document an incident-response and **content-hotfix runbook**: how to correct a wrong threshold within hours (signed pack + kill banner + expedited review request).

### 8.11 Abuse cases to test
Tampered content pack, replayed old pack (rollback attack), malicious deep link, oversized/invalid barcode input, MITM with a trusted proxy cert, API key extraction attempts (there must be nothing to extract), brute-force on the Worker, malicious dependency update, leaked signing key, user sharing a handoff sheet with unintended data, backup extraction of the DB.

---

## 9. PRIVACY, LEGAL AND CLAIMS

- Draft in `/legal/` (plain language, accurate to the real data flows): Privacy Policy, Terms of Use/EULA (needed in the paywall), Medical/Veterinary Disclaimer. Mark clearly: drafts that need attorney review **[HUMAN GATE]**.
- **Veterinary law:** advice without a veterinarian-client-patient relationship must stay general and not diagnose, prescribe, or treat a specific animal; using an app does not create a VCPR. Use language like "information to help you decide when to contact a veterinarian; it does not diagnose or treat and does not create a veterinarian-client-patient relationship." Avoid instructing owners to give medications or induce vomiting. Have counsel review state-law exposure **[HUMAN GATE]**.
- Disclaimers appear once at first run, in Settings, in the handoff sheet footer, and as one calm line under every result, not as noisy popups.
- No health or efficacy claims in the store listing beyond what is true; no "AI-powered" claim (the engine is not AI) unless a real AI feature ships.
- Marketing/UGC rules (for later): no fake testimonials, disclose AI-generated content in ads (FTC consumer-review rule; Meta/TikTok policies).
- Run a trademark and App Store name search for `{{APP_NAME}}` before registration **[HUMAN GATE]**.

---

## 10. APP STORE READINESS (build to pass review the first time)

### 10.1 Guideline checklist (verify each against the live Guidelines, https://developer.apple.com/app-store/review/guidelines/)
- **1.4.1 Physical harm / medical:** this is the biggest risk. Apps that could give inaccurate information are scrutinized more. Provide visible links to sources for the information, remind users to consult a veterinarian before decisions, make no unverifiable accuracy claims, and describe the methodology in-app ("About our content": how thresholds are set, who reviewed, when, sources).
- **2.1 App completeness:** no placeholders, no crashes, working demo path for reviewers (no login needed), real content.
- **4.2 Minimum functionality and 4.3 Spam:** the app must be distinctive and substantial (custom engine, offline data, handoff sheet, original UI). Document differentiation in review notes.
- **5.1.1 Privacy:** privacy policy URL, clear purpose strings, only needed permissions; **5.1.1(v) account deletion** is not applicable because there are no accounts, but provide in-app "Delete all my data".
- **5.1.2(i)** Third-party AI data sharing requires disclosure and explicit permission. v1 shares no personal data with any AI. Keep it that way; if that changes, add consent first.
- **3.1.1 / 3.1.2 In-app purchase & subscriptions:** see 10.4.
- **4.8 Sign in with Apple:** not required (no third-party login).
- **Kids:** not a Kids Category app; do not target children.

### 10.2 Privacy manifest and labels
- Ship `PrivacyInfo.xcprivacy` for the app and make sure every third-party SDK includes its own manifest and signature (missing manifests cause upload errors such as ITMS-91053). Follow https://docs.expo.dev/guides/apple-privacy/ and audit "required reason" API usage (UserDefaults, file timestamps, boot time, disk space).
- Answer the App Privacy "nutrition label" accurately: target **Data Not Collected** (confirm RevenueCat/any SDK usage and declare exactly what applies; do not claim "none" if an SDK collects identifiers).
- `ITSAppUsesNonExemptEncryption`: set correctly (HTTPS and standard OS crypto are generally exempt, but verify the export-compliance questionnaire) **[HUMAN GATE: confirm answers]**.

### 10.3 App Store Connect metadata pack (`/docs/APP-STORE.md`)
Name (<=30), subtitle, keywords (100 chars), description (accurate, no medical-cure claims), promotional text, What's New, category (Lifestyle or Utilities; avoid "Medical" unless truly appropriate; decide with an ADR), age rating (answer Apple's updated age-rating questionnaire honestly, including medical/wellness information questions), support URL, marketing URL, privacy policy URL, copyright, screenshots (current required iPhone sizes, designed in the tag-and-clipboard style, no AI art), app icon (1024 px, custom vector, no transparency), accessibility nutrition label answers, and **App Review notes** (explain the emergency use case, that no account is needed, where sources/disclaimers are, how to reach each feature, and hotlines are real numbers).

### 10.4 Subscription and paywall compliance
- Show price, billing period, first-charge date, trial terms, and how to cancel on the paywall itself; functional links to Terms of Use and Privacy Policy; **Restore Purchases** button; no hidden trial toggles; no dark patterns; clear free tier.
- Never display a paywall inside the emergency flow. Use StoreKit sandbox + TestFlight to test purchase, renewal, cancel, restore, and grace states.
- Offer: monthly and annual; annual preferred.

### 10.5 Release hygiene
TestFlight internal -> external beta (with the vet reviewer and 10+ pet owners) -> submit. Provide crash-free sessions >= 99.5% in beta. Check launch time, memory, battery, and bundle size. Test on the smallest and largest supported iPhones, iPad compatibility behavior, offline, airplane mode, low power mode, and interrupted calls.

---

## 11. TESTING AND QA

- Unit + property + golden tests for the engine (section 4.5); schema tests for content; signature/rollback tests for packs.
- Component tests (React Native Testing Library) and E2E (Maestro or Detox) for: first run, full triage for each risk level, barcode failure -> UNKNOWN, offline mode, handoff sheet export, paywall, restore purchases, delete data.
- Accessibility tests: automated checks plus manual VoiceOver/Dynamic Type passes recorded in `/docs/a11y-report.md`.
- Security tests: the abuse cases in 8.11, MobSF scan of the release binary, dependency/secret scans, Worker tests (auth, rate limit, SSRF, validation).
- Performance budgets: cold start < 2 s on a mid-range device, triage result < 100 ms, JS bundle size tracked, no dropped frames in tag/stamp animations (profile with Skia).
- Add `/scripts/pre-submit.sh` that fails on: lint/type/test failures, unreviewed substances in a release build, contrast failures, banned strings ("safe" as a verdict), missing privacy manifest, debug flags, console logs, secrets, or unsigned content.

---

## 12. PROCESS AND MILESTONES

Work in small, reviewable commits with clear messages. After each milestone, update `/docs/PLAN.md` and stop for review where marked.

1. **M0 Foundation:** repo, tooling, CI, threat model, ADRs, design tokens + contrast script, content schema.
2. **M1 Engine:** pure triage engine + tests + seed data (all `draft`).
3. **M2 Core flow UI:** intake -> result -> handoff, offline, accessible, tag-and-clipboard design system.
4. **M3 Lookups + backend:** barcode flow, Worker proxy with App Attest, signed content packs, abuse tests.
5. **M4 Paid features + paywall:** pantry checklist, reminders, multi-pet, compliant paywall.
6. **M5 Security and privacy hardening:** full MASVS pass, MobSF, supply-chain gates, privacy manifest, data map, delete-data.
7. **M6 Content review:** export for the veterinarian, import approvals, `dvm_approved` gating **[HUMAN GATE]**.
8. **M7 App Store pack and TestFlight:** metadata, screenshots, review notes, legal drafts reviewed **[HUMAN GATE]**, beta.
9. **M8 Submission:** final pre-submit script, submit, then plan v1.1.

**Stop and ask me (do not guess) at:** vet review, legal review, hotline number/fee verification, ODbL compliance, Apple/EAS credentials, signing-key custody, export-compliance answers, app name/trademark, final category/age rating.

---

## 13. DELIVERABLES AND DEFINITION OF DONE

Deliver: the app repo; `/docs` (PLAN, ADRs, THREAT-MODEL, SECURITY-CHECKLIST, PRIVACY-DATA-MAP, APP-STORE, a11y-report, design-qa); `/legal` drafts; the Worker; CI; scripts; a README with exact setup, build, and submission steps; a release checklist.

**Done means:** all tests green; MASVS checklist complete with evidence; no critical/high findings in scans; contrast and a11y checks pass; every shipped substance is `dvm_approved` with a named reviewer; privacy label and manifest verified; legal drafts reviewed; TestFlight beta feedback addressed; pre-submit script passes; and every open HUMAN GATE is closed. If any item cannot be satisfied, say so plainly in `/docs/KNOWN-GAPS.md` instead of hiding it.

---

## APPENDIX A: Banned behaviors for you (the builder)
- Do not invent toxicology numbers, hotline numbers, or sources. If you cannot verify, mark `draft` and ask.
- Do not use an LLM to generate triage content at runtime.
- Do not add analytics, ads, attribution, or tracking SDKs.
- Do not store or log user data on any server.
- Do not copy copyrighted lists or text.
- Do not use AI-generated images; do not use stock illustration packs.
- Do not claim App Store approval is guaranteed; produce the best-prepared submission and list residual risks.

## APPENDIX B: Residual risks to state at the end
Apple medical-app scrutiny (1.4.1); veterinary-law exposure by state; content accuracy and liability; ODbL obligations; subscription-review rejections; competitor imitation; reviewer availability for content updates.

## APPENDIX C: Reference links (read before building)
- App Review Guidelines: https://developer.apple.com/app-store/review/guidelines/
- Apple 5.1.2(i) third-party AI data-sharing update: https://techcrunch.com/2025/11/13/apples-new-app-review-guidelines-clamp-down-on-apps-sharing-personal-data-with-third-party-ai
- Expo privacy manifests: https://docs.expo.dev/guides/apple-privacy/
- OWASP MASVS: https://mas.owasp.org/MASVS/ and MASTG: https://mas.owasp.org/MASTG/
- Designing for stress and emergency: https://www.smashingmagazine.com/2025/11/designing-for-stress-emergency/
- AVMA on telehealth and the VCPR: https://www.avma.org/resources-tools/animal-health-and-welfare/telehealth-telemedicine-veterinary-practice/telehealth-and-vcpr
- openFDA NDC API: https://open.fda.gov/apis/drug/ndc
- Open Food Facts terms (ODbL): https://world.openfoodfacts.org/terms-of-use
- npm worm guidance (Shai-Hulud): https://www.microsoft.com/en-us/security/blog/2025/12/09/shai-hulud-2-0-guidance-for-detecting-investigating-and-defending-against-the-supply-chain-attack/
- FTC consumer reviews and testimonials rule: https://www.ftc.gov/business-guidance/resources/consumer-reviews-testimonials-rule-questions-answers
- Toxicology seed sources: see section 4.3 URLs.

## APPENDIX D: Working-name ideas (all unverified; run trademark and App Store checks)
Tagged, Chart Paw, Triage Tag, Case Number, Clipboard, Poison Tag. Pick one or propose better; keep `{{APP_NAME}}` as a variable until chosen.
