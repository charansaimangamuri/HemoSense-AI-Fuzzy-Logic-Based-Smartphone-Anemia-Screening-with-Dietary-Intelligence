# HemoSense AI — 10-Hour Review Guide

Crash plan built from the actual repo, with a memorization sheet and a question bank. Follow it in order — do not jump around.

---

# PART 1 — The 10-hour timetable

| Time | What to do | Files / actions |
|---|---|---|
| **0:00–0:45** | Learn the *identity* of the project. Read the two "source of truth" docs. Write one sentence: "HemoSense is a Flutter Android app that screens anemia from a photo of the inner eyelid using a fuzzy ANFIS model on a Python server, then suggests an iron-rich diet." | `docs/APP_END_TO_END.md` (all 247 lines), `docs/PROJECT_CONTEXT.md` §1–3 |
| **0:45–1:15** | Memorize the end-to-end flow (Part 2 master sheet). Draw the 12-step user journey on paper from memory. | `docs/APP_END_TO_END.md:12` |
| **1:15–2:30** | **Image pipeline.** Read `segment.py` then `features.py`. Learn every rejection code and threshold, GrabCut + Otsu + crescent prior, and the 4 feature formulas. Run one demo: load a demo photo, call `segment_conjunctiva`, print features. | `hemosense/segment.py`, `hemosense/features.py`, `research/tmp/demo_photos/` |
| **2:30–3:45** | **The model.** Read `anfis.py` line by line. Derive: 3 inputs × 3 Gaussian terms → 27 rules; 9 centres + 9 widths + 27 consequents = **45 params**; firing → normalized weight → weighted sum → Platt sigmoid. Skim `mamdani.py` as baseline. | `hemosense/anfis.py`, `hemosense/mamdani.py` |
| **3:45–4:30** | **Validation & numbers.** Memorize the results table and protocol (patient-level 5-fold, leakage fixes, 0.879 AUC, 0.77/0.82 operating point). | `research/results/summary.md`, `paper/WRITING_KIT.md:99-118` |
| **4:30–5:45** | **Backend.** Read `main.py` endpoints, `pipeline.py:143` (one-photo path), `clinical.py:50` (aggregation), `schemas.py`. Then run the server and hit `/health`, `/symptoms`, `/diet/foods`. | `api/*.py`; commands below |
| **5:45–6:30** | **Diet + RAG + LLM.** Learn the absorption formula, USDA traceability, BM25 chunks, AI-proposes/server-validates pattern, and the fallback. | `hemosense/diet.py`, `hemosense/rag.py`, `api/llm.py`, `diet_config.json` |
| **6:30–8:00** | **Flutter app.** Read `main.dart`, `providers.dart`, `api_client.dart`, `local_store.dart`, then the screens in journey order (splash → camera → review → result → why → diet → history). | `app/lib/` |
| **8:00–8:30** | **Deployment.** URL, AWS pieces, Docker Compose, Caddy, safety/privacy rules. | `deploy/`, `Dockerfile`, `docs/APP_END_TO_END.md:214` |
| **8:30–9:30** | **Drill Part 3 out loud.** Answer every question without looking; mark the ones you miss. Re-read only those. | Part 3 below |
| **9:30–10:00** | **Final pass:** master sheet (Part 2), weak questions, run `pytest` once more, sleep. | — |

Commands to run during the practical blocks (from repo root):

```powershell
.venv\Scripts\python -m pytest tests -q
.venv\Scripts\python -m uvicorn api.main:app --port 8000
# in another terminal:
curl http://localhost:8000/health
curl http://localhost:8000/symptoms
curl http://localhost:8000/diet/foods
```

```powershell
# inside the Flutter app folder:
cd app; flutter analyze; flutter test
```

---

# PART 2 — Master sheet (memorize this)

**One-line project:** smartphone camera photo of the lower eyelid → user draws box → quality gate → GrabCut segmentation → 4 colour features → 2 ANFIS models → grade + confidence + explanation → personalised diet plan. No Hb value is ever estimated or shown.

**Stack:** Flutter 3.47 / Dart 3.13 / Riverpod 3 / Dio / Hive / camera / fl_chart → HTTPS multipart → FastAPI + Pydantic + uvicorn → numpy / OpenCV / Pillow → ANFIS in `models/anfis.json` → USDA food table + BM25 RAG + OpenRouter LLM (falls back to rules) → AWS EC2 t3.small ap-south-1 + Caddy + Docker Compose. React/Next.js `frontend/` is a demo only; `app/` is the deliverable.

**Pipeline (12 steps):** splash/consent → profile → tutorial → guide+symptoms → camera (torch, 0.8 s settle, 3 frames 0.35 s apart, 10–15 cm) → review (one draggable box, "Analyse" disabled until placed) → `POST /screen/batch` → rejection gates → segment → features → ANFIS → aggregate → result/why/diet/history.

**Rejections (422 with code):** `too_far` (<40 px box), `too_dark` (brightness <0.15), `overexposed` (>25% clipped), `blurry` (Laplacian var <12 at 320 px), `no_conjunctiva` (<max(150 px, 2% of box)), `not_crescent` (elongation <2.7 or solidity >0.85 or w/h <1.1), `no_eye` (no sclera above box), `bad_image`.

**Features:** `EI = 100(log10 R̄ − log10 Ḡ)`; mean CIELAB `a*`; `HHR` = share of pixels with hue ±15° of red and S>0.30; mean HSV saturation. Model inputs = **a, hhr, ei** (selected by greedy forward selection inside training folds).

**Model:** two zero-order Sugeno ANFIS ("anemic" and "moderate-or-severe"); 3 Gaussian terms Low/Medium/High; 27 rules (21 active deployed); 45 params; centres initialised from anemic/non-anemic medians; consequents by ridge least squares; Adam on BCE + L2; early stopping; rule pruning; Platt calibration; decision p ≥ 0.5.

**Grades:** Normal / Mild / Moderate-to-Severe. Aggregation: median probability over accepted photos, agreement = share of matching votes; <0.7 agreement → "Inconclusive" and confidence forced to Low. Confidence comes from cross-validated certainty bins (`models/confidence.json`).

**Endpoints:** `GET /health`, `/symptoms`, `/diet/foods`, `/diet/usage`; `POST /screen`, `/screen/batch`, `/screen/roi`, `/diet/recommendations`, `/diet/plan`. Boxes are 0–1 fractions of the EXIF-rotated photo. Photos are processed in memory, never saved. `predicted_hb_gdl` is always `None`.

**Numbers to quote:** 218 listed / **215 usable** (94 India, 121 Italy; 90 anemic, 53 mod-sev); ANFIS live AUC **0.879 [0.829–0.922]**; app rule sensitivity **0.767**, specificity **0.816**; LogReg 0.897 (DeLong p=0.079), Mamdani 0.888, RF 0.879, CNN 0.876; segmentation Dice **0.82**; 3-grade accuracy 0.688; within-India AUC 0.649; 45 Python tests.

**Diet:** 46 USDA SR Legacy foods with FDC ids; absorbable = heme×0.25 + non-heme×0.10×E×I (E=×2 if VitC ≥25 mg or meat; I=×0.7 if Ca ≥300 mg, ×0.8 phytate, ×0.6 tea/coffee); RDA 18 mg women 19–50, 8 mg men, 27 mg pregnant; liver excluded in pregnancy; AI proposes dish names/times/costs, server rejects unallowed foods and recomputes all nutrients; fallback = rule-based plan (OpenRouter key currently 401).

**Deployment:** `https://3-111-237-63.sslip.io` (fallback `http://3.111.237.63`), EC2 t3.small Mumbai, Caddy TLS, `docker compose` (api + caddy), CloudWatch auto-recover, SSH only from deployer IP, ~$0.025/hr, `bash deploy/aws_deploy.sh`.

**Safety/privacy:** no login, history/profile/consent on phone only, "Screening only, not a diagnosis" on every screen, "See a doctor" banner for moderate/severe or red-flag symptoms (chest pain, fainting, breathlessness at rest).

**Limitations to admit:** one dataset (215 adults), no prospective phone study, no colour reference card, manual box (U-Net is future work), USDA/NIH values not yet ICMR-verified, within-India AUC ~0.65.

---

# PART 3 — Question bank (answer each out loud)

## Big picture

1. What does the project do? → Screening, from eyelid photo, fuzzy model, diet plan; no Hb, no diagnosis.
2. Why the conjunctiva? → Pallor is a clinical sign; its colour can be quantified from a photo; non-invasive.
3. What are the three app grades? → Normal / Mild / Moderate-to-Severe (WHO 4 grades collapsed).
4. What are the deliverables? → Flutter Android app, FastAPI server, shared `hemosense/` core, research paper, AWS deployment.
5. Why no Hb value? → Model is trained for classification, not regression; showing a number would be false precision.
6. Why fuzzy logic? → Pallor is a gradual, linguistic concept; ANFIS gives 45 interpretable parameters and per-decision rules.

## Data & validation

7. Dataset and size? → Eyes-defy-anemia (IEEE DataPort), 218 listed, 215 usable adults from India/Italy.
8. Three data bugs fixed? → image-level split leak, Italian decimal commas dropping 15 patients, three mask encodings.
9. Split strategy? → one sample per participant, StratifiedKFold(5, shuffle, seed 42) on region×anemia, identical folds for all models.
10. Where do thresholds come from? → inner 5-fold out-of-fold predictions on the training fold only; never from test data.
11. Main result? → live AUC 0.879 [0.829–0.922]; app rule sensitivity 0.767, specificity 0.816.
12. Is ANFIS significantly worse than LogReg/CNN? → No: DeLong p=0.079 (LogReg) and p=0.618 (CNN) — statistically level.
13. What was the protocol revision? → top-3 by univariate AUC (0.828, redundant features) replaced by greedy forward selection (0.879); disclosed as ablation.
14. Why report cross-region results? → to expose generalisation failure: India→Italy 0.909, Italy→India 0.687, within-India 0.649.
15. Confidence numbers mean? → certainty = max(p,1−p); e.g. at 0.8–0.9, 61 of 72 cross-validated patients were classified correctly.

## Image pipeline

16. Why the EXIF step? → the user draws the box on the phone's displayed (rotated) photo; pixels must be rotated the same way.
17. What does the box represent? → 0–1 fractions [x,y,w,h] over the pulled-down lower eyelid; one box shared by the burst frames.
18. Quality gate thresholds? → brightness <0.15, clipped >25%, Laplacian variance <12 at 320 px, box shorter side <40 px.
19. How does GrabCut run? → on a crop with 15% margin, downscaled to ≤360 px, 4 iterations, seeded by the box rectangle.
20. What is the Otsu step? → split smoothed CIELAB a* of candidates into two classes only if their means differ by >8 a* units; floor a*≥8 so pale eyelids survive.
21. Why the crescent prior? → real eyelids are elongated half-moons (elongation ≥2.9, solidity ≤0.80, w/h ≥1.24 on 215 photos); shirt/nose patches are compact blobs. Thresholds set just outside that range.
22. Why the "no_eye" check? → a pulled-down eyelid always has white sclera just above it; other red objects don't.
23. What is Dice 0.82? → overlap of live segmentation with expert masks on 215 photos with simulated user boxes.
24. Why was the safety layer added *after* evaluation? → live tests showed boxes on shirt/nose being analysed; gates were added without retraining, then a sensitivity rerun showed AUC unchanged.

## Fuzzy / ANFIS

25. ANFIS architecture? → 3 features, 3 Gaussian MFs each, 27 rules, zero-order Sugeno, 45 parameters, Platt output.
26. How are the 45 params counted? → 9 centres + 9 widths + 27 rule consequents.
27. Write the inference equation → w_r = Π μ_k,j; w̄_r = w_r/Σw; z = Σ w̄_r θ_r; p = sigmoid(a·z + b).
28. How are centres initialised? → Low = median of anemic group, High = median of non-anemic, Medium = midpoint.
29. How are consequents initialised? → ridge least squares on normalised firing strengths (Jang hybrid idea).
30. Training details? → Adam lr 0.01, binary cross-entropy + L2 0.01, early stopping patience 60/max 800 epochs, rules with mean firing <0.005 pruned.
31. Why is it explainable? → `explain()` returns the top-3 firing rules in IF–THEN form with firing weight and risk; `memberships()` returns Low/Medium/High values per feature.
32. Mamdani vs ANFIS? → Mamdani uses hand-written EI×a* rules with HHR shift, min–max inference, centroid defuzzification; ANFIS learns its parameters from data.
33. Why two models? → one detects anemic vs not; the second separates moderate-or-severe from mild to produce the 3 grades.

## Backend & app

34. Endpoints? → (list the 9 from the master sheet).
35. Walk through `/screen/batch` → validate 1–10 images + JSON boxes → per-photo screen → collect errors → if too few valid, 422 with first rejection code → aggregate → symptoms + diet plan + disclaimer.
36. What does `_read_upload` enforce? → content type, non-empty, ≤10 MB (413/415/400).
37. How is agreement computed? → max(anemic votes, n−anemic votes)/n; <0.7 ⇒ inconclusive + Low confidence.
38. What does the app store locally? → consent, profile, settings, history in Hive boxes (`hs_settings`, `hs_profile`, `hs_history`); backend URL in settings with `/health` test.
39. How does Riverpod fit? → `ProviderScope` in `main.dart`; Notifier-style providers hold state; Dio client posts multipart; Hive persists data; no codegen.
40. Why is the box editor important? → it prevents the silent failure mode of analysing skin/nose; Analyse stays disabled until the box is placed.
41. What happens on upload failure? → error screen shows the server's specific code/message (too dark, blurry, etc.), never a guessed result.
42. Why is the React `frontend/` not the deliverable? → it's a demo UI; the Flutter `app/` is the submitted Android app.

## Diet, RAG, LLM

43. Where do food numbers come from? → USDA FoodData Central SR Legacy, 46 foods, each with FDC id; tests trace every nutrient to its CSV row.
44. Absorbable iron formula? → heme×0.25 + non-heme×0.10×E×I; E=2 with ≥25 mg vitamin C or meat; I=0.7 with Ca≥300 mg, 0.8 phytate without enhancer, 0.6 tea/coffee.
45. How is the plan assembled? → per meal slot, pick allowed food adding most absorbable iron, add servings until RDA; tea/coffee/dairy excluded from iron meals; vitamin C source per meal.
46. How does the AI planner stay safe? → AI proposes meals/dish names/costs using only the verified food list; server rejects foreign or disliked foods and recomputes every nutrient from USDA data.
47. What happens when AI is unavailable? → rule-based plan with warning "Data-driven plan (AI unavailable)" — currently the case because the OpenRouter key returns 401.
48. What is RAG used for here? → BM25 retrieval over WHO/Indian anaemia-guidance PDFs (900-char chunks, 150 overlap), zero external calls, query built from severity + user context.

## Deployment, safety, critical thinking

49. Deployment URL and stack? → sslip.io HTTPS, EC2 t3.small Mumbai, Caddy + FastAPI in Docker Compose, auto-recover alarm.
50. Why no TensorFlow at serving time? → the deployed model is a small numpy ANFIS in JSON; keeps the container light and startup fast.
51. Privacy design? → no login, photos in memory only, profile/history/consent on device.
52. Red-flag symptoms? → chest pain, fainting, breathlessness at rest → urgent banner regardless of photo result.
53. Biggest limitation? → single small dataset, adults only; within-India AUC ~0.65; no prospective phone validation.
54. If you had another month, what would you do? → U-Net auto-segmentation, colour reference card, CP-AnemiC children dataset, prospective phone study, ICMR-verified nutrition tables.

---

**Study technique that works in 10 hours:** for every question, answer in 2–3 sentences, then point to the file and line where the answer lives. If you can do that for all 54, you can defend the project. Prioritize questions 7–12, 16–23, 25–32, 34–40 — those are where most questions come from.
