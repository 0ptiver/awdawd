# LEAN BUILD PROMPT: Pet Poison Triage App v1 (iOS, TestFlight -> App Store)

> Paste everything below the divider into Claude Opus 5.5 (Claude Code). The full 5,600-word version is in `pet-toxin-app-build-prompt.md` for later; this one is the minimum that is still secure, App Store ready, and safe.

---

## MISSION
Build a small, polished iOS app (working title `{{APP_NAME}}`) that helps a worried dog or cat owner decide what to do after a pet may have eaten something dangerous: relax and watch, call the vet today, or call poison control now. It is information only, not a diagnosis or a vet.

Priority order: **pet safety > privacy/security > App Store compliance > polish.** Keep v1 small. Do not add features I did not ask for.

## HARD RULES (these are the few things we do NOT cut)
1. **No AI makes the verdict.** The risk result comes from plain, tested TypeScript over a small JSON table. No LLM at build-time-generated-runtime or run-time.
2. **Unknown means escalate.** If the substance, amount, weight, or species is missing, unrecognized, or out of range, the result is "CAN'T RULE IT OUT. CALL NOW." The app never says "safe." Use "LOW CONCERN AT THIS AMOUNT" only when a cited threshold exists for that species AND the dose is under 25% of the lowest published mild-sign threshold. Cats and any substance without a threshold are never "low concern."
3. **Always show the next action:** a one-tap `tel:` link for ASPCA Animal Poison Control and Pet Poison Helpline (verify numbers and the roughly $89-95 fees on their official sites; do not guess), plus "Call your own vet" and a link that opens Apple Maps searching "emergency veterinarian."
4. **Show sources and a calm disclaimer.** Every result links to its sources and carries one line: "Information only. Not veterinary advice. It does not replace your vet." (Apple guideline 1.4.1 requires sources and consult-a-professional language for medical-type apps.)
5. **Zero data collection.** No accounts, no analytics, no ads, no tracking SDKs, no network calls, no permissions. Everything runs offline.

## STACK
Expo (current stable SDK; verify versions in the live docs, not from memory), React Native, TypeScript strict, `expo-router`, `zustand`, `react-native-reanimated`, `@shopify/react-native-skia`, `expo-haptics`, `expo-font`. Build/submit with EAS. Engine lives in `/src/engine` with zero React imports. No backend. No database (store pet name/weight and recent cases in memory + a tiny local store via `expo-secure-store` or `expo-sqlite`; no cloud).

## V1 SCOPE (only this)
1. **First run:** one short screen: what the app does/doesn't do; one acknowledgment; links to sources and privacy.
2. **Home:** one huge button "SOMETHING WAS EATEN," plus small "Call poison control" and "Find emergency vet."
3. **Intake (one question per screen, big custom keypad):** dog or cat -> weight (lb/kg) -> what (searchable list) -> how much (unit-aware helpers: chocolate by type + ounces; pills by count x strength; gum by pieces) -> when.
4. **Result tag:** risk level, numbered next steps, signs to watch, sources, disclaimer line.
5. **Handoff sheet:** a one-page PDF/image (case number, time, pet, weight, substance, amount, concern level) the user can share with a vet. User-initiated only.
6. **Settings:** units, "Delete all my data," privacy, sources, open-source notices.
Out of scope for v1: barcode scanning, photos, accounts, subscriptions/paywall, notifications, multi-pet, backend, AI of any kind.

## CONTENT (small and conservative)
Create `/src/data/substances.json` validated by `zod`. Each entry: id, names, species, original-wording summary, threshold model (if any), `alwaysEscalate`, signs to watch, sources (title, URL, date accessed). Do not copy text or lists from the ASPCA, Pet Poison Helpline, or Merck; write original wording from cited facts.

Seed values (re-check each against the cited source before use; mark entries `draft` in the UI footer until a vet has read them):
- **Chocolate, dogs (theobromine):** mild signs ~20 mg/kg; heart effects >40 mg/kg; seizures >60 mg/kg. Theobromine per ounce varies by chocolate type: take the figures from the cited paper. Source: https://onlinelibrary.wiley.com/doi/10.1111/jsap.13329
- **Xylitol, dogs:** >0.1 g/kg low blood sugar risk; >0.5 g/kg liver injury risk. If xylitol per piece is unknown, escalate. Source: https://www.vetfolio.com/learn/article/xylitol-toxicity-in-dogs
- **Grapes/raisins, dogs:** no reliable safe dose; always escalate. Source: https://www.vettimes.com/news/vets/small-animal-vets/canine-grape-toxicosis
- **Ibuprofen/naproxen, dogs:** signs from ~50 mg/kg; kidney risk >~175 mg/kg; CNS signs >~400 mg/kg. Cats: always escalate. Source: https://www.merckvetmanual.com/toxicology/toxicoses-from-human-analgesics/toxicoses-from-human-analgesics-in-animals
- **Always escalate (no watch-at-home path):** lilies (cats), antifreeze, rodenticides, acetaminophen (cats), sago palm, button batteries, any unidentified pill or product.
- Add 8-10 more common ones only if you can cite a reliable source; otherwise mark `alwaysEscalate`.

Never instruct owners to give medication or induce vomiting. Do not give dosing instructions.

## DESIGN: "TRIAGE TAG AND CARBON COPY" (distinctive, not AI-looking)
- **Idea:** every result is a physical veterinary triage tag (hole-punched, string, thick color band, big status word, perforated tear-off strip "TEAR OFF TO SHARE" that produces the handoff sheet). Home screen looks like a clipboard with paper and a metal clip. Handoff looks like a carbon-copy chart.
- **Tokens:** paper `#F2EBDD`, kraft `#C9B38A`, ink `#14181F`, pencil `#6B6558`, tag red `#B8281A`, amber `#E9A21B`, green `#2F8F5B`, carbon pink `#F1B8B2`, carbon yellow `#F4E08A`. Hard 2 px ink edges, single hard offset shadow at most. Run a contrast script and fix any pair below WCAG AA (4.5:1 text, 3:1 large/UI).
- **Fonts (open license, bundled):** Big Shoulders Display (status words), Atkinson Hyperlegible (body), Courier Prime (form fields and case numbers).
- **Never rely on color alone:** each level has a word and a shape (circle = low concern, triangle = call vet today, octagon = go now).
- **Motion:** tag swings in once on its string, stamp lands with one medium haptic. No bounce everywhere, no confetti, no spinners. Reduce Motion = instant/cross-fade.
- **Draw it in code:** paper grain via Skia noise, stamps and icons as custom vectors. No AI-generated images, no stock illustrations, no emoji.
- **Banned (the "AI look"):** purple/indigo gradients, glass/blur cards, sparkles/magic-wand icons, chatbot bubbles, soft pastel 24 px cards with blurry shadows, centered hero + 3 feature cards, 3D blobs.
- **Copy voice:** short, calm, clinical-warm. "Okay. One step at a time." No jokes or exclamation marks in results.
- **Accessibility:** VoiceOver labels on everything, Dynamic Type through AX5 with no clipped safety text, large 56 pt primary targets, works one-handed.
- Before finalizing, look at the App Store screenshots of ToxiPets, the ASPCA app, and Pet Poison Helpline, and write 5 lines in `/docs/design-notes.md` about how this differs.

## SECURITY (secure by being small)
Because there is no backend, no account, no network, and no secrets, most attacks have nothing to hit. Still do these:
- No secrets, keys, or tokens anywhere in the repo or app bundle.
- Only the permissions actually used (none in v1). No `NSAllowsArbitraryLoads`.
- Only open `tel:` and Apple Maps links; sanitize anything displayed.
- Pet/case data stays on-device; obscure the app-switcher snapshot; "Delete all my data" really deletes.
- Dependencies: few, committed lockfile, exact versions, frozen installs in CI (`npm ci`), install scripts disabled except an allowlist, `npm audit` and `gitleaks` in CI, Dependabot on, no unpinned third-party GitHub Actions.
- Release build only: strip debug code, console logs, and source maps. Enable GitHub 2FA and protect the Apple/EAS accounts with it.
- Write a half-page `/docs/SECURITY.md` listing what the app collects (nothing), what it stores locally, and the controls above.

## APP STORE READINESS (do these, they prevent most rejections)
- **1.4.1 (medical/physical harm):** sources linked in-app, consult-a-vet language, a short "How we set these thresholds" screen, no accuracy claims you cannot back up.
- **4.2/4.3 (minimum functionality/spam):** the custom engine, offline data, handoff sheet, and original UI are the differentiators; mention them in review notes.
- **Privacy:** privacy policy page (a simple static page; draft it plainly: no data collected), correct App Privacy label ("Data Not Collected"), `PrivacyInfo.xcprivacy` present (follow https://docs.expo.dev/guides/apple-privacy/), no tracking so no ATT prompt.
- **Export compliance:** answer `ITSAppUsesNonExemptEncryption` correctly (v1 has no networking; confirm in the questionnaire).
- **Metadata:** name, subtitle, keywords, honest description (no cure/diagnosis claims, no "AI-powered" claim), category, age rating via Apple's current questionnaire, support URL, screenshots in the tag-and-clipboard style, 1024 px custom icon.
- **Review notes:** explain the emergency use case, that no login is needed, where sources/disclaimers live, and that hotline numbers are real.
- Ship to TestFlight first; fix crashes; then submit.

## TESTING (keep it focused)
- Unit tests for the engine: every threshold boundary (below/at/above), every unit conversion, invalid input -> escalate, cats -> never low concern.
- A test that fails the build if any user-facing string uses "safe" as a verdict, says "diagnos", or tells owners to give meds or induce vomiting.
- Table-driven test that `LOW_CONCERN` is unreachable without a cited threshold and a dose under 25% of the lowest mild-sign threshold.
- One end-to-end happy path per risk level (Maestro or Detox), VoiceOver and Dynamic Type spot checks, offline/airplane-mode check.
- `scripts/pre-submit` that fails on lint/type/test errors, contrast violations, banned strings, secrets, console logs, and missing privacy manifest.

## PROCESS
1. **M1:** repo, tooling, CI, tokens + contrast script, content schema + seed data, engine + tests.
2. **M2:** full intake -> result -> handoff UI in the design system, accessible, offline.
3. **M3:** security/privacy pass, App Store pack, TestFlight build.
Make small commits. Record any significant decision in a one-paragraph note in `/docs/decisions.md`. If you cannot verify a number, URL, or hotline, mark it `draft` and tell me instead of guessing.

## BUILDER RULES
Do not add analytics, ads, accounts, a backend, subscriptions, barcode scanning, or any AI feature. Do not invent toxicology numbers or sources. Do not copy copyrighted lists. Do not use AI-generated art. Do not claim App Store approval is guaranteed; list the remaining risks at the end.
