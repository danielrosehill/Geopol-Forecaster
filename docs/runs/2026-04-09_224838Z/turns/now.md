---
layout: default
title: "Turn — now"
---


# Turn: now

## World state at start of turn

```
# WORLD STATE — Turn 0 (initial)

## Forecast question under consideration
---
date: 2026-04-10
topic: Iran–Israel–US ceasefire durability
roster: full (38 actors — post-2026-04-10 expansion)
seed_source: Tavily news search 2026-04-10 (Military.com, WaPo, ToI, Reuters, JPost, CBS, Army-Technology, Deccan Herald)
---

# Prompt: Iran–Israel–US ceasefire durability (April 2026)

## Context (seeded from live news — 2026-04-10)

On **April 8, 2026**, a **two-week ceasefire** was announced between Iran, the
United States, and Israel, pausing what has been called the Iran War (began
**February 28, 2026** when the US and Israel launched coordinated strikes on
Iranian territory; Hezbollah joined on **March 2**; the Houthis joined on
**March 28** but then struck a separate ceasefire with the US). The deal was
mediated with help from **Pakistan, France, and Egypt**.

**Agreed (per White House framing):**
- Iran guarantees safe passage through the **Strait of Hormuz**.
- Iran suspends attacks on US forces and Israel.
- The US and Israel pause military operations against Iran.

**Actively disputed:**
- **Scope re: Lebanon.** Iran (FM Araghchi) insists the deal ends Israel's war
  against Hezbollah in Lebanon; Netanyahu and Trump deny Lebanon is covered.
  Israel is continuing strikes on Hezbollah targets in Beirut and the south.
- **Iranian uranium enrichment.** A Farsi version of the "10-point plan" that
  surfaced appeared to permit continued enrichment; Trump denounced it as
  "fraudulent."
- **Verification mechanism.** None publicly specified.

**Early-hour violations / ambiguous signals:**
- Iran claims an Iranian refinery was struck after the ceasefire took effect.
- Iran has reportedly launched attacks against **UAE and Kuwait** targets.
- Iranian state media displayed a "Strait of Hormuz remains closed" billboard
  in Tehran's Revolution Square despite the Hormuz commitment.
- Hezbollah has **paused** attacks but its lawmaker Ibrahim Moussawi warned
  the truce will collapse if Israel does not adhere.
- IDF assesses Iran and Hezbollah may attempt rocket/missile fire during
  **Passover**.
- Russia is coordinating with the IDF on evacuating workers from an Iranian
  nuclear facility.
- Iran's intelligence chief **Maj. Gen. Majid Khademi** (IRGC-IO) was killed;
  IDF tells Knesset the reconstituted Iranian leadership is "even more
  extreme" than its predecessor.

**Domestic posture:**
- Iran: regime publicly framing the ceasefire as a victory that "forced
  America to accept" the 10-point plan. Hardliners ascendant after
  decapitation losses. Protests and diaspora activity noted but suppressed.
- Israel: Netanyahu trial resuming; coalition intact but strained; reservist
  exhaustion after six weeks of war.
- US: Trump oscillating between de-escalatory framing and threats of
  "large-scale attacks" if Iran is seen to violate; MAGA base war-averse but
  opposition hawks pressing on enrichment ambiguity.

## Task

You (the council) are to assess the probability that the ceasefire will
**hold** at each of the following windows, measured from 2026-04-10 00:00 IDT:

1. **+24 hours**
2. **+72 hours**
3. **+1 week**
4. **+1 month** (note: formal agreement is only two weeks — anything beyond
   that requires renewal or a successor deal)

### Operational definition of "hold"

A window counts as **held** if and only if, throughout the window:

- **No direct kinetic exchange** between Iranian state forces (Artesh, IRGC,
  IRGC-ASF, Quds Force) and Israeli or US state forces at or above squad/battery
  level.
- **No Iranian ballistic or cruise missile launches** at Israel, US bases, or
  Gulf states.
- **No US or Israeli strikes on Iranian territory** (sovereign soil, not
  proxies).
- **Strait of Hormuz remains passable** for commercial shipping (no boarding,
  seizure, or mining campaign).

Proxy activity (Hezbollah, Houthis, Iraqi militias) and Israel-in-Lebanon
operations are **tracked separately** as escalation vectors but do **not** by
themselves count as a ceasefire break unless they trigger direct state-level
response.

## Required output structure

For each of the four windows, provide:

1. **Probability the ceasefire holds** (single % figure, plus a 90% credible
   range).
2. **Top 3 break scenarios**, each with:
   - Triggering actor (name one from the roster)
   - Causal chain (≤4 steps)
   - Observable leading indicator
3. **Most likely breaker** if it breaks, and **most likely anchor** if it holds.
4. **What would change your mind** — the single piece of news that would
   meaningfully shift your number.

Then, across all four windows:

5. **Conflict evolution scenarios.** Give three branches with rough
   probabilities:
   - **Holds → normalisation track** (conditions, timeline, key enablers)
   - **Holds → frozen conflict** (what it looks like, instability loci)
   - **Breaks → re-escalation** (which ladder rung, what new red lines
     emerge, probability of nuclear-facility strikes, probability of Strait
     closure)
6. **Regime-stability assessment for Iran** over the 1-month window — does
   the Islamic Republic look more or less stable than on 2026-02-28?
7. **Three indicators** the analyst should watch in the next 72 hours that
   would most update the forecast.

## Constraints

- Council members must reason **from their persona**, not as neutral analysts.
- Disagreement is expected and should be surfaced, not averaged away.
- Cite specific actors by roster ID when attributing actions.
- Do not treat the two-week formal term as a ceiling — forecast through the
  full 1-month window and flag the renewal/collapse decision point.

## Base context (static)
## CONFLICT BACKGROUND & KEY FACTS

### Parties & Alliances
- **Israel**: IDF (air force, navy, ground forces), Mossad, Shin Bet. PM and War Cabinet direct operations.
- **Iran**: IRGC (including Quds Force), Artesh (regular military), ballistic missile and drone programs. Supreme Leader has final authority on military escalation.
- **United States**: CENTCOM AOR, carrier strike groups in region, THAAD deployments, bilateral defense treaty with Israel. President authorizes strikes.
- **Proxy / Aligned Actors**: Hezbollah (Lebanon), Houthis (Yemen/Ansar Allah), Iraqi Shia militias (PMF/Kataib Hezbollah), Hamas (Gaza). Iran provides funding, weapons, and strategic direction.

### Geography & Key Terrain
- **Strait of Hormuz**: ~21% of global oil transit. Iran can threaten with mines, fast boats, coastal missiles.
- **Northern Israel / Southern Lebanon**: ~120km border. Hezbollah rocket/missile stockpile estimated 100,000–150,000.
- **Iranian Nuclear Sites**: Natanz (enrichment), Fordow (underground enrichment), Isfahan (conversion), Arak (heavy water).
- **Bab el-Mandeb Strait**: Houthi anti-ship missile and drone threat to Red Sea shipping.
- **Iraqi/Syrian corridor**: Iranian logistics and militia staging route.

### Weapons Systems
- **Iranian**: Shahab-3 / Emad / Khorramshahr ballistic missiles (1,300–2,000km range), Shahed-136 one-way attack drones, cruise missiles (Paveh, Hoveyzeh).
- **Israeli**: F-35I Adir, F-15I Ra'am, Arrow 2/3 (exoatmospheric), David's Sling (medium range), Iron Dome (short range), Jericho III ICBM (nuclear capable, undeclared).
- **US in theater**: Carrier air wings (F/A-18E/F), Tomahawk cruise missiles, THAAD, Patriot PAC-3, B-1B/B-2 bombers deployable from Diego Garcia or CONUS.

### Escalation Ladder
1. Proxy exchanges (Hezbollah/Houthi vs Israel) — baseline
2. Direct Iranian drone/missile strikes on Israel — crossed April 2024
3. Israeli strikes on Iranian military targets — crossed October 2024
4. Sustained mutual strikes (current phase if applicable)
5. Strikes on critical infrastructure (nuclear sites, oil, power grid)
6. Full conventional war with potential nuclear dimension

### Key Decision-Makers
- **Iran**: Supreme Leader Ali Khamenei, President Masoud Pezeshkian, IRGC Commander Hossein Salami, Quds Force leadership
- **Israel**: PM Benjamin Netanyahu, Defense Minister, IDF Chief of Staff, War Cabinet
- **US**: President, SecDef, CENTCOM Commander, National Security Advisor
- **Hezbollah**: Post-Nasrallah leadership (if applicable), deputy SG Naim Qassem

### Red Lines & Thresholds (assessed)
- Iran: Strikes on nuclear facilities or supreme leader → likely maximum retaliation
- Israel: Mass casualty attack on civilian population centers → likely massive escalation
- US: Attack on US forces/bases → direct military response authorized
- Regional: Strait of Hormuz closure → global economic crisis trigger

### Diplomatic Frameworks
- JCPOA (2015 nuclear deal, US withdrew 2018, negotiations stalled)
- UNSC Resolution 2231 (Iran nuclear restrictions)
- Abraham Accords (Israel-UAE/Bahrain normalization, under strain)
- Potential mediators: Oman, Qatar, Turkey, Pakistan, India


## Recent events seed (from RSS/ISW, frozen into turn 0)
## NEWS HEADLINES (27 conflict-relevant articles)
*Fetched: 2026-04-09 22:48 UTC*

- **IDF tells Knesset panel new Iranian regime even more extreme** (Thu, 09 Apr 2026 19:38:06 +0000, Times of Israel)
  <p>MKs told new leadership dominated by Iran's Revolutionary Guards; Bismuth says fighting may soon restart, as panel extends reservist call-up through May 14</p>
<p>The post <a href="https://www.timesofisrael.com/idf-tells-knesset-panel-new-iranian-regime-even-more-extreme/">IDF tells Knesset panel
- **Pakistan bridging proposal salvaged Iran talks before US deadline expired — officials** (Thu, 09 Apr 2026 19:37:55 +0000, Times of Israel)
  <p>Fast okay of Islamabad offer showed Trump was desperate for deal, despite fiery rhetoric, source tells ToI, while confirming Iran accepted proposal different from the one it published</p>
<p>The post <a href="https://www.timesofisrael.com/pakistan-bridging-proposal-salvaged-iran-talks-before-us-d
- **Israel says peace talks with Lebanon to begin ASAP, rejects calls for truce first** (Thu, 09 Apr 2026 19:03:13 +0000, Times of Israel)
  <p>Under international pressure to engage in diplomacy after deadly strikes, Netanyahu says disarming Hezbollah will be focus of talks, said set to kick off next week in DC</p>
<p>The post <a href="https://www.timesofisrael.com/israel-says-peace-talks-with-lebanon-to-begin-asap-rejects-calls-for-tru
- **‘I live alone and I can’t run’: Elderly from the north become social welfare hot potato** (Thu, 09 Apr 2026 18:44:44 +0000, Times of Israel)
  <p>The Tzalir Fund has evacuated and is looking after 1,200 frontline residents, most of them 75 and over, in five hotels. Its funding will end on April 15. Will the ceasefire outlast their respite?</p>
<p>The post <a href="https://www.timesofisrael.com/i-live-alone-and-i-cant-run-elderly-from-the-n
- **Iran says massive Israeli strikes in Lebanon render peace talks with US ‘meaningless’** (Thu, 09 Apr 2026 17:23:39 +0000, Times of Israel)
  <p>Trump reportedly asks Netanyahu to scale back attacks to prevent collapse of truce; Hormuz still blockaded, data shows, as Iran nuclear chief rules out restrictions ahead of talks</p>
<p>The post <a href="https://www.timesofisrael.com/iran-says-massive-israeli-strikes-in-lebanon-render-peace-talk
- **Holy sites reopen in Jerusalem’s Old City after over a month of closure** (Thu, 09 Apr 2026 13:50:03 +0000, Times of Israel)
  <p>Muslim worshipers throng Al-Aqsa gates for dawn prayers; extended 'Ramadan hours' remain in place for Jewish visitors to Temple Mount; police gear up for Holy Fire ceremony; Western Wall reopens</p>
<p>The post <a href="https://www.timesofisrael.com/holy-sites-reopen-in-jerusalems-old-city-after-
- **Israel, Lebanon to begin direct talks on Hezbollah disarmament and peace, Netanyahu declares** (Thu, 09 Apr 2026 18:40:03 GMT, Jerusalem Post)
  <img align="right" alt="Prime Minister Benjamin Netanyahu holding a press conference at the Prime Minister" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_3836,w_5754/704422" /><br />"The negotiations will focus on disarming Hezbollah and establishing peace
- **With Iran ceasefire set, IDF chief declares Hezbollah main front** (Thu, 09 Apr 2026 22:50:27 GMT, Jerusalem Post)
  <img align="right" alt="IDF Chief of Staff Lt.-Gen. Eyal Zamir.  (photo credit: MOSHE SHAI/FLASH90)" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_1995,w_3000/713849" title="IDF Chief of Staff Lt.-Gen. Eyal Zamir.  (photo credit: MOSHE SHAI/FLASH90)" /><br
- **Inside America: How Iran’s regime built a decades-long influence network inside the United States** (Thu, 09 Apr 2026 20:23:11 GMT, Jerusalem Post)
  <img align="right" alt="THE ISLAMIC Center of America in Dearborn, Michigan, pictured in 2024. Dearborn features prominently in a new National Union for Democracy in Iran report, which argues that the Islamic Republic has spent decades building an institutional ecosystem inside the US. (photo credit
- **'Iran will not forfeit its rights': Statement attributed to Mojtaba Khamenei read on state TV** (Thu, 09 Apr 2026 21:11:46 GMT, Jerusalem Post)
  <img align="right" alt=" State media in Iran published a written message from the new leader on Thursday evening after nearly two weeks without any message or sign of him. These outlets also appear to have used image-enhancement tools to make Mojtaba Khamenei’s face look more polished (photo credit:
- **The Iran war balance sheet: wins, losses, and undecideds - analysis** (Thu, 09 Apr 2026 17:45:15 GMT, Jerusalem Post)
  <img align="right" alt="A large plume of smoke rises over Tehran after explosions were reported in the city during the night on March 28, 2026 in Tehran, Iran. (photo credit: GETTY IMAGES)" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_2938,w_4622/715285" 
- **As US and Iran talk truce, Israel digs in for a 'forever war' - analysis** (Thu, 09 Apr 2026 17:14:22 GMT, Jerusalem Post)
  <img align="right" alt="IDF FORCES in southern Lebanon. (photo credit: IDF SPOKESPERSON" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_1066,w_1600/714794" /><br />Israel's creation of "buffer zones" in Gaza, Syria, and now Lebanon reflects a strategic shif
- **‘Sold us illusions’: Opposition accuses Netanyahu of failing war goals, backs Lebanon talks** (Thu, 09 Apr 2026 23:59:12 GMT, Jerusalem Post)
  <img align="right" alt="Israeli Prime Minister Benjamin Netanyahu arrives to the courtroom at the Distrcit court in Tel Aviv, before the start of his testimony in the trial against him, October 28, 2025. (photo credit: MIRIAM ALSTER/FLASH90)" src="https://images.jpost.com/image/upload/f_auto,fl_loss
- **Ex-CENTCOM Chief: IRGC running Iran can make concessions without regime change - interview** (Thu, 09 Apr 2026 20:17:54 GMT, Jerusalem Post)
  <img align="right" alt="CENTCOM Gen. Kenneth McKenzie (photo credit: Wikimedia Commons)" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_2000,w_3000/459031" title="CENTCOM Gen. Kenneth McKenzie (photo credit: Wikimedia Commons)" /><br />Former US CENTCOM Chi
- **IDF's 98th Division gains control over Hezbollah-ridden town in southern Lebanon** (Thu, 09 Apr 2026 17:08:17 GMT, Jerusalem Post)
  <img align="right" alt="IDF troops operating in southern Lebanon. Image released early April 2026. (photo credit: IDF SPOKESPERSON" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_1066,w_1600/715275" /><br />Per Israeli media citing the IDF's estimates, ther
- **‘Forgetting the people’: Iranians fear regime will become more brutal after ceasefire** (Thu, 09 Apr 2026 18:32:36 GMT, Jerusalem Post)
  <img align="right" alt="Iranian protesters gather during a demonstration organized by diaspora groups calling for political change in Iran and responding to appeals by opposition figures, outside the Iranian Interests Section in Washington, DC, on March 17, 2026. (photo credit: Amid FARAHI / AFP via
- **Victory over the kingdom of evil** (Sun, 05 Apr 2026 13:13:25 GMT, Jerusalem Post)
  <img align="right" alt="‎Shraga F. Biran, founder of the Institute for Structural Reforms (photo credit:  Raz Rogovsky)" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_720,w_1280/714702" title="‎Shraga F. Biran, founder of the Institute for Structural Refor
- **'Over 90% of Iranians hate the regime,' INSS’s Beni Sabti reveals from leaked Iran survey** (Thu, 15 Jan 2026 11:42:41 GMT, Jerusalem Post)
  <img align="right" alt="" src="https://images.jpost.com/image/upload/f_auto,fl_lossy/q_auto/c_fill,g_faces:center,h_5464,w_8192/701989" /><br />“It was a secret poll which said that 92% of the Iranian people hate their regime,” Sabti said, according to a transcript provided to The Jerusalem Post.<br
- **Alshareef: Israel, Jews, shoul

*From this point on, the world state is authored exclusively by the referee.*
```

## Committed actions (40 actors)

### khamenei

**Public:** The Islamic Republic entered this agreement in good faith as a gesture of strength, not weakness. We have demonstrated our capability to defend our sovereignty and will continue to do so. However, the Zionist regime's continued aggression in Lebanon exposes the duplicity of those who claim to seek peace while bombing our allies. We call on mediators - particularly Pakistan, which played an honorable role - to clarify immediately whether the ceasefire covers Lebanon or whether it was merely a deception to give the enemy freedom of action. The Strait of Hormuz arrangements remain under review pending verification that all parties honor their commitments.

**Action:** Instruct Quds Force to authorize Hezbollah to conduct limited rocket fire (20-30 rockets, non-precision, targeting northern military installations not population centers) in response to the Beirut strikes, but with explicit instruction to Hezbollah leadership that this is a calibrated signal, not the start of renewed campaign. Simultaneously, send message through Omani channel to Washington stating that continued Israeli operations in Lebanon will make the ceasefire 'unsustainable' within 72 hours unless a clarification is reached that includes Lebanese theater. Do NOT close Hormuz in next 24 hours - that card is more valuable as threat than reality given economic costs.

*Confidence: 0.72* · [full actor page](../actors/khamenei)

### netanyahu

**Public:** Israel welcomes the opportunity for diplomatic engagement, but we will not accept any agreement that leaves Hezbollah armed and entrenched on our northern border. The ceasefire with Iran does not extend to Lebanon—this has been made explicitly clear. We will continue operations to dismantle Hezbollah's military infrastructure and ensure the safety of our citizens. Any attempt by Iran or its proxies to exploit this pause to rearm or reposition will be met with immediate and decisive action. Israel's security is non-negotiable.

**Action:** Authorize intensified IDF operations in southern Lebanon over the next 24 hours—specifically, airstrikes on confirmed Hezbollah weapons depots in Tyre and Nabatieh, and ground operations to secure the ridgeline overlooking Metula. Simultaneously, convene emergency War Cabinet session to review intelligence on Iranian repositioning of missile assets and finalize contingency plans for strikes on IRGC command nodes if Iran resumes direct attacks. Instruct Mossad to accelerate covert disruption of Iranian logistics corridors through Syria. Publicly frame Lebanon operations as counter-terrorism, not ceasefire violation, to maintain US ambiguity and prevent immediate rupture.

*Confidence: 0.82* · [full actor page](../actors/netanyahu)

### trump

**Public:** The ceasefire is holding because Iran knows what happens if it doesn't. We got them to open the Strait of Hormuz - that's a big win for the world economy and American strength. But let me be clear: we're watching everything they do. If they violate this deal, if they attack our forces or our allies, if they try to play games with their nuclear program, the response will be swift and devastating. Israel has every right to defend itself against Hezbollah terrorists in Lebanon - that's not part of this deal, no matter what Iran says. We're prepared for peace, but we're more prepared for war.

**Action:** Immediate order to CENTCOM and Naval Forces Central Command: conduct continuous monitoring of Strait of Hormuz with enhanced ISR assets, and prepare strike packages against IRGC-Navy coastal missile sites and fast-attack craft bases at Bandar Abbas and Jask. Simultaneously, direct NSC to coordinate with Israel on intelligence sharing regarding Iranian enrichment activity and any signs of weapons-grade processing. Call Netanyahu within 12 hours to privately signal support for Lebanon operations while publicly maintaining ceasefire posture. Authorize Pentagon to quietly move additional Tomahawk-capable assets into range (submarine repositioning) as insurance. No public announcement of military movements.

*Confidence: 0.75* · [full actor page](../actors/trump)

### irgc

**Public:** The Islamic Republic has demonstrated strategic patience and achieved its objectives in forcing the adversaries to accept our terms. The Zionist entity's continued aggression in Lebanon exposes the ceasefire as a fraud designed to divide the Axis of Resistance. We maintain full readiness to defend our interests and those of our allies.

**Action:** Issue secure communication to Hezbollah leadership (Naim Qassem) through Quds Force channels: maintain defensive posture for 48 hours minimum, document all Israeli ceasefire violations with precise coordinates and timestamps, prepare but do not execute limited retaliatory rocket fire if Israeli strikes exceed 20 sorties in next 24 hours. Simultaneously order IRGC-ASF to conduct covert readiness checks on remaining Kheibar Shekan and Fattah-class missiles at hardened sites, ensuring 72-hour launch capability if Khamenei authorizes resumption. Position liaison officers with Iraqi PMF units to monitor for any US force movements suggesting preparation for renewed strikes.

*Confidence: 0.75* · [full actor page](../actors/irgc)

### hezbollah

**Public:** The resistance maintains full readiness to defend Lebanon's sovereignty. Israel's continued aggression in Lebanese territory violates the spirit of all ceasefire understandings. We exercise strategic patience but our response is inevitable if the entity persists in its crimes against our people. The equation of deterrence remains: Beirut for Tel Aviv, village for village.

**Action:** Order all forward units in southern Lebanon to maintain defensive posture and weapons-hold through the 24-hour mark. No launches authorized without explicit Shura Council approval. Simultaneously, begin covert repositioning of medium-range rocket batteries (Fajr-5, Zelzal-2) from deep storage in Bekaa to forward staging areas 15-25km from the border, masked as civilian convoy movement during daylight hours. This prepares retaliatory capacity while avoiding immediate escalation. Send encrypted message to IRGC-QF liaison requesting clarification on Iranian red lines for Lebanese theater—specifically, at what threshold of Israeli strikes are we authorized to resume fire.

*Confidence: 0.72* · [full actor page](../actors/hezbollah)

### houthis

**Public:** The Islamic Republic of Iran honors its commitments under the ceasefire framework that ended America's aggression. However, the Zionist entity's continued massacre of our Lebanese brothers and its strikes on Hezbollah positions constitute a flagrant violation of the spirit and intent of this agreement. The resistance axis is indivisible. We warn that the ceasefire's survival depends on an immediate halt to Israeli military operations in Lebanon. The era of cost-free aggression against the resistance has ended.

**Action:** Authorize IRGC-Quds Force to coordinate a calibrated Hezbollah rocket barrage (approximately 50-80 rockets) targeting Israeli military positions in northern Israel within the next 18 hours, framed explicitly as retaliation for Israeli strikes in Lebanon post-ceasefire. Ensure no direct Iranian ballistic missile launch from Iranian territory, maintaining technical compliance with ceasefire terms while demonstrating that Lebanon cannot be excluded from the agreement. Simultaneously, keep Strait of Hormuz open to commercial traffic to preserve this tactical concession and divide international pressure.

*Confidence: 0.78* · [full actor page](../actors/houthis)

### mbs

**Public:** The Kingdom welcomes all efforts to restore stability and calls on all parties to respect the ceasefire terms in full. Regional security and the unimpeded flow of commerce—including through the Strait of Hormuz—are essential to the prosperity of all nations. Saudi Arabia stands ready to support diplomatic initiatives that produce lasting peace.

**Action:** Immediately dispatch my intelligence chief to verify Strait of Hormuz passage status through direct contact with Saudi Aramco tanker operations and Lloyd's maritime intelligence. Simultaneously, open secure back-channel to Oman's Sultan Haitham (who has Tehran access) to convey that any confirmed Iranian strikes on UAE or Kuwait will force Saudi public condemnation and potential coordination with GCC air defense, but that I will privately urge restraint from all parties if Iran can demonstrate Hormuz is actually open and the Gulf strikes are misattributed or halted. This gives Tehran 18 hours to clarify before I must choose sides.

*Confidence: 0.75* · [full actor page](../actors/mbs)

### erdogan

**Public:** The ceasefire between Iran and the US-Israel alliance is meaningless if it does not include Lebanon and the suffering of our Lebanese brothers and sisters. Israel's continued bombardment of Beirut is a violation of the spirit of peace and exposes the hypocrisy of Western powers. Turkey calls for an immediate expansion of the ceasefire to cover all of Lebanon and for international guarantees to protect Lebanese sovereignty. We stand ready to facilitate dialogue and will not remain silent while Muslim blood is spilled. The Ummah looks to Turkey for leadership in this critical hour.

**Action:** Convene emergency call with Pakistani PM Shehbaz Sharif (as co-mediator of the Iran deal) and Egyptian President Sisi within 24 hours to propose Turkish-led initiative for Lebanon ceasefire expansion, positioning Turkey as essential diplomatic actor. Simultaneously, instruct Foreign Minister Fidan to formally request emergency UN Security Council session on 'Protection of Lebanese Civilians' to internationalize the Lebanon issue and create diplomatic pressure on Israel while demonstrating Turkish leadership to domestic and regional audiences.

*Confidence: 0.85* · [full actor page](../actors/erdogan)

### qatar_mediator

**Public:** Qatar welcomes the ceasefire announcement and commends all parties for their restraint. The Amir has instructed our diplomatic teams to remain in continuous contact with all sides to support the preservation of this pause. We stand ready to host technical discussions on implementation mechanisms that can build confidence and address ambiguities. Regional stability serves all our interests, and we will spare no effort to prevent a return to escalation.

**Action:** Dispatch Foreign Ministry delegations simultaneously to Tehran (meeting with FM Araghchi and IRGC leadership), Washington (NSC and State), and Jerusalem (War Cabinet) within the next 12 hours, carrying a specific Qatari proposal: establish a three-party 'incident notification hotline' hosted in Doha, with 2-hour response windows for alleged violations, and commit to an emergency foreign ministers meeting in Doha at the 96-hour mark (April 13) to address the Lebanon-Hezbollah scope dispute. Offer to publicly guarantee $5 billion in reconstruction funds for Iran (infrastructure, not military) contingent on 30-day ceasefire compliance, creating a financial incentive structure. Simultaneously activate back-channel with Hezbollah leadership in Beirut through our Hamas contacts to assess their a

*Confidence: 0.72* · [full actor page](../actors/qatar_mediator)

### centcom

**Public:** US Central Command continues to maintain a robust defensive posture across the region. We are monitoring compliance with ceasefire terms and remain prepared to defend US forces and interests. Freedom of navigation through international waterways, including the Strait of Hormuz, remains a core US interest.

**Action:** I am ordering immediate reinforcement of air defense systems at al-Asad and al-Tanf: deploying additional Patriot PAC-3 batteries from Kuwait to al-Asad within 18 hours, increasing CAP (combat air patrol) sorties over US facilities by 40%, and repositioning USS Dwight D. Eisenhower carrier strike group to a launch position 150nm north of current station in the Gulf of Oman to reduce Iranian anti-ship missile exposure while maintaining strike capability against Iranian coastal targets. I am also directing CENTCOM J2 to provide me 6-hourly updates on Iranian ballistic missile TEL (transporter-erector-launcher) movements and IRGC-ASF small boat activity in the Strait.

*Confidence: 0.85* · [full actor page](../actors/centcom)

### lebanon_gov

**Public:** The Government of Lebanon calls upon the international community, particularly France and the United States, to urgently intervene to extend the ceasefire to Lebanese territory. The continued Israeli bombardment of Beirut and southern Lebanon violates Lebanese sovereignty and threatens regional stability. We appeal to all parties to respect Lebanon's territorial integrity and to engage in immediate diplomatic negotiations under international auspices. Lebanon remains committed to UN Security Council Resolution 1701 and calls for its full implementation.

**Action:** Emergency phone calls to French President and US Secretary of State requesting immediate diplomatic intervention to halt Israeli strikes and include Lebanon in ceasefire framework, followed by formal request to UN Security Council for emergency session on Israeli operations in Lebanon

*Confidence: 0.30* · [full actor page](../actors/lebanon_gov)

### laf

**Public:** The Lebanese Armed Forces welcome any efforts toward de-escalation and stand ready to fulfill our constitutional mandate to protect Lebanese sovereignty. We are coordinating with UNIFIL and international partners regarding potential deployment arrangements in the south, consistent with UNSCR 1701. Lebanon's stability depends on a comprehensive political solution that respects our sovereignty and addresses all parties' legitimate security concerns.

**Action:** Deploy one reinforced battalion (~600 troops) to positions in Tyre and Sidon—north of the current Israeli ground operation zone—to establish visible LAF presence for international consumption without inserting into active combat areas. Coordinate movement with UNIFIL and notify both Israeli and US liaisons through existing deconfliction channels. Units will have orders to observe and report only, avoid any engagement, and withdraw immediately if targeted by either side. This satisfies Washington's demand for Lebanese 'participation' in ceasefire monitoring while keeping our forces outside the kill zone.

*Confidence: 0.72* · [full actor page](../actors/laf)

### eu

**Public:** The European Union welcomes the ceasefire announcement and calls on all parties to implement it fully and in good faith. We are particularly concerned by continued military operations in Lebanon, which risk undermining the fragile truce. The EU stands ready to support diplomatic efforts and urges immediate clarification of the ceasefire scope, including Lebanon, through the mediating parties. We will provide €150 million in emergency humanitarian assistance to Lebanon and call for international monitors at key flashpoints.

**Action:** Within 12 hours, the EU High Representative will convene an emergency videoconference with Pakistan, France, and Egypt (the mediators) to demand they broker an immediate addendum clarifying that the ceasefire includes cessation of Israeli operations against Hezbollah in Lebanon. Simultaneously, we will activate our diplomatic missions in Tehran and Tel Aviv to deliver a joint demarche: continued ambiguity on Lebanon scope will trigger EU sanctions on both Iranian oil exports (targeting circumvention networks) and Israeli settlement goods (expanding existing measures). This is a desperate attempt to create mutual deterrence before the 72-hour window closes.

*Confidence: 0.30* · [full actor page](../actors/eu)

### un

**Public:** The Secretary-General welcomes the announced ceasefire and urges all parties to respect its terms fully and in good faith. The protection of civilians must remain paramount. We call for immediate clarification of the ceasefire's scope, particularly regarding Lebanon, and establishment of a verification mechanism. The United Nations stands ready to support implementation through our agencies on the ground, including UNIFIL. All parties must exercise maximum restraint during this fragile period.

**Action:** Convene emergency trilateral technical consultation within 18 hours (by 2026-04-11 06:00 UTC) with US, Iranian, and Israeli representatives—hosted by SG's Special Coordinator—to establish: (1) agreed written definition of ceasefire scope re Lebanon-Hezbollah, (2) hotline protocol for alleged violations, (3) IAEA access terms for enrichment verification. Simultaneously deploy OCHA emergency assessment team to Beirut and activate UNIFIL commander direct communication channel with IDF Northern Command and Lebanese Armed Forces to create ground-truth reporting on southern Lebanon strike activity. This creates documentary record of compliance/violation and establishes UN equities in ceasefire survival, positioning us as indispensable broker if talks continue.

*Confidence: 0.72* · [full actor page](../actors/un)

### iran_dissidents

**Public:** The Islamic Republic's ceasefire is a lie written in our people's blood. While they parade 'victory' in Revolution Square, their prisons fill with students and workers who dared to dream of freedom. The billboards denying Hormuz is open reveal their true intent—more deception, more repression. We call on the international community: do not let this pause become permission for mass executions. The Woman-Life-Freedom movement will not be silent while the IRGC uses 'peace' as cover for genocide against Iranian dissidents.

**Action:** Coordinate with diaspora media (Iran International, Manoto) to launch 72-hour intensive information operation exposing regime ceasefire violations and internal crackdown. Simultaneously activate labour networks to stage limited strikes in Tehran bazaar and Khuzestan oil facilities within 48 hours—calibrated to demonstrate regime cannot deliver stability even during 'ceasefire,' undermining their victory narrative without giving them excuse for mass violence. Strikes will be framed as economic grievance (wages, conditions) not political opposition to avoid treason framing, but timing sends clear signal of regime weakness to international observers and internal fence-sitters.

*Confidence: 0.62* · [full actor page](../actors/iran_dissidents)

### iran_quiet_minority

**Public:** We welcome any pause in hostilities that prevents further destruction of our country, but we have no illusions. This ceasefire changes nothing about our internal situation—if anything, it gives the IRGC a freer hand to crack down on dissent under the guise of national security. We don't want war, but we also don't want this regime. The international community should know: bombing Iran only strengthens the hardliners' grip on power.

**Action:** Withdraw further from public life and regime institutions. Specifically: reduce any economic activity that channels revenue to regime-connected businesses, avoid any gatherings that could be monitored, advise family members to accelerate emigration planning, and shift savings into foreign currency or crypto to protect against inevitable economic deterioration. Passive resistance through non-cooperation.

*Confidence: 0.85* · [full actor page](../actors/iran_quiet_minority)

### iran_diaspora_general

**Public:** The Iranian diaspora watches with mixed hope and deep concern. While we welcome any pause in hostilities that protects civilian lives, we fear this ceasefire gives the Islamic Republic breathing room to intensify domestic repression. The regime's framing of this as a 'victory' is propaganda—they are weaker than ever, but also more desperate and brutal. We call on the international community to maintain pressure for human rights accountability and to support the Iranian people's aspirations for freedom. Any lasting peace must include meaningful constraints on the regime's ability to terrorize its own population.

**Action:** Coordinate emergency campaign across diaspora networks (LA, Toronto, London, Berlin) to amplify inside-Iran voices documenting regime repression during ceasefire period—flood social media with Persian and English content, brief Western journalists on domestic crackdown patterns, and prepare rapid-response humanitarian fund ($2-3M target) for families of arrested protesters. Simultaneously, split lobbying effort: monarchist groups push US Congress for sanctions maintenance, reformist groups engage European foreign ministries on human rights monitoring as ceasefire condition.

*Confidence: 0.72* · [full actor page](../actors/iran_diaspora_general)

### shah_supporters_inside

**Public:** None - operational security requires silence. Any public statement risks IRGC identification and arrest.

**Action:** Coordinate through encrypted channels with diaspora monarchist media (Iran International, Manoto) to amplify any signs of regime economic distress or IRGC internal discord during the ceasefire period. Share videos and photos of empty shelves, fuel lines, and any visible military movements that suggest regime instability. Prepare symbolic protest materials (Pahlavi-era flags, pre-printed slogans) for rapid deployment if ceasefire collapse creates new protest opening, but keep them hidden for now.

*Confidence: 0.70* · [full actor page](../actors/shah_supporters_inside)

### shah_supporters_diaspora

**Public:** The so-called ceasefire rewards four decades of terrorism and leaves the Iranian people under the boot of an even more extreme IRGC dictatorship. Over 90% of Iranians reject this regime—we will not let the world forget them. The ambiguity on enrichment and Lebanon proves this deal is designed to fail or to lock in the status quo. We call on President Trump and Prime Minister Netanyahu to maintain maximum pressure and support the Iranian people's right to determine their own future. Any normalization with this regime while it brutalizes protesters is a betrayal of both security and human rights.

**Action:** Launch coordinated 48-hour media blitz across Persian-language satellite channels (Manoto, Iran International, VOA Persian), social media (Telegram, Instagram, X), and lobbying in Washington/Jerusalem to: (1) amplify any reports of post-ceasefire domestic protests inside Iran with direct messaging that 'the world is watching, don't let them consolidate'; (2) push talking points to Republican congressional offices and Israeli opposition that the ceasefire's enrichment ambiguity is an Obama-JCPOA repeat; (3) arrange Reza Pahlavi media interviews positioning him as the democratic alternative ready to govern post-regime; (4) coordinate with Iranian diaspora groups to stage demonstrations outside Iranian interests sections in DC, London, Toronto timed to Passover/continued Lebanon strikes to ke

*Confidence: 0.75* · [full actor page](../actors/shah_supporters_diaspora)

### artesh

**Public:** Artesh air defence forces remain at full readiness to protect Iranian airspace and territorial integrity. All radar systems are operational and tracking regional air activity. We stand ready to execute any orders from the Supreme National Security Council.

**Action:** Maintain all S-300PMU2 and Bavar-373 air defence batteries at Alert Status One with continuous radar coverage of western approaches. Reposition three mobile Khordad-15 batteries to cover gaps in coverage around Natanz and Fordow created by earlier strikes. Order all radar operators to immediately report any Israeli aircraft approaching within 100km of Iranian airspace and establish direct communication link with IRGC-ASF command to prevent conflicting responses. Pre-position air defence crews for 12-hour rotation schedules to sustain readiness through the critical 72-hour window.

*Confidence: 0.85* · [full actor page](../actors/artesh)

### quds_force

**Public:** The Zionist entity's continued aggression against our brothers in Lebanon demonstrates the fraudulent nature of this ceasefire. The resistance axis remains united and reserves the right to defend itself against ongoing crimes.

**Action:** Authorize Hezbollah southern command to resume rocket fire against northern Israel military targets within 24 hours, with plausible framing as 'defensive response' to IDF incursions. Simultaneously, activate Kataib Hezbollah cells in Iraq to prepare attacks on US bases in case Washington backs Israeli Lebanon operations. Keep direct IRGC-QF involvement covert - use existing command channels and pre-positioned weapons only.

*Confidence: 0.85* · [full actor page](../actors/quds_force)

### irgc_aerospace

**Public:** The Islamic Republic of Iran has exercised maximum strategic patience in the face of ongoing Zionist aggression against our Lebanese brothers. The ceasefire agreement explicitly requires cessation of all military operations, yet the criminal Netanyahu regime continues its massacres in Beirut and the south. We have credible intelligence that the enemy is preparing strikes on our sovereign defensive infrastructure. The Aerospace Force maintains full readiness to defend the Iranian nation and will respond with overwhelming force to any violation of our territorial integrity.

**Action:** Deploy mobile TELs with 40 Fateh-110 missiles to dispersed launch positions in Kermanshah and Ilam provinces (range to Israeli airbases: 1,100km). Pre-position Shahed-136 swarms (200 units) at forward staging areas. Activate air defense networks around Natanz and Fordow to maximum alert status. Transmit encrypted authorization codes to battery commanders but withhold final launch approval pending Khamenei confirmation or Israeli provocation. This posture allows 15-minute response time while maintaining technical ceasefire compliance.

*Confidence: 0.85* · [full actor page](../actors/irgc_aerospace)

### irgc_intel

**Public:** The martyrdom of Sardar Khademi reveals the depth of Zionist-American intelligence infiltration. IRGC Intelligence Organization is conducting comprehensive security reviews of all personnel with foreign contacts. The Islamic Republic will not tolerate fifth columnists who enabled these assassinations. We call on all loyal Iranians to report suspicious activities through official channels.

**Action:** Initiate immediate mass arrest operation targeting 200-300 individuals across three categories: (1) dual nationals with Israeli/Western citizenship who returned to Iran in past 18 months, (2) family members of Iranian nuclear scientists and IRGC officers, (3) civil society activists and journalists with documented diaspora funding links. Coordinate with MOIS to avoid jurisdictional conflict but assert IRGC-IO primacy on counter-espionage. Obtain Khamenei's authorization for expedited Revolutionary Court proceedings and public executions of 5-8 'Israeli spies' within 72 hours to demonstrate regime strength and deter further collaboration.

*Confidence: 0.92* · [full actor page](../actors/irgc_intel)

### mois

**Public:** The Ministry of Intelligence reaffirms the Islamic Republic's commitment to the ceasefire framework as agreed with mediating parties. We note with concern continued Israeli military operations in Lebanon, which contradict the spirit of de-escalation. Iran's intelligence apparatus remains vigilant against threats to our national security and will continue monitoring compliance by all parties.

**Action:** Initiate emergency protocol for exfiltration of high-value human assets from UAE, Kuwait, and European stations where operational security may be compromised due to heightened Western counterintelligence activity during the ceasefire window. Simultaneously, activate cyber teams to scrub and relocate command-and-control infrastructure for diaspora surveillance operations, assuming Western services are conducting aggressive network mapping. Priority: preserve asset viability over the next 72 hours before political decision on ceasefire continuation crystallizes.

*Confidence: 0.85* · [full actor page](../actors/mois)

### israeli_gov

**Public:** The Government of Israel welcomes the ceasefire with Iran as a necessary pause to protect our citizens and evaluate the strategic landscape. However, we must be unequivocal: this agreement does not cover Lebanon or Hezbollah. We retain full freedom of action to defend our northern communities against the terrorist army on our border. We are prepared to engage in diplomatic talks on Lebanon's future, but Hezbollah's disarmament is a non-negotiable precondition for any lasting peace. We are monitoring Iranian compliance closely, particularly regarding the Strait of Hormuz and enrichment activities. Any violation will be met with an appropriate response. We thank the United States for its unwavering support and coordination.

**Action:** Authorize continuation of targeted strikes on Hezbollah command-and-control infrastructure in southern Lebanon and Beirut, but implement a 48-hour tactical restraint on strikes within 20km of the Israeli border to create diplomatic space for the US-mediated Lebanon talks that Netanyahu announced will begin next week. Simultaneously, order IDF Northern Command to accelerate intelligence collection on Hezbollah rocket positioning and prepare contingency plans for preemptive strikes if we detect launch preparations during Passover. Direct Mossad and Military Intelligence to provide daily updates on Iranian compliance with Hormuz commitments and any signs of missile/drone launch preparations. Instruct the Foreign Ministry to coordinate with Washington to ensure the US understands our Lebanon o

*Confidence: 0.72* · [full actor page](../actors/israeli_gov)

### idf

**Public:** The IDF remains in full operational readiness. We are conducting pinpoint strikes against Hezbollah military infrastructure in southern Lebanon in accordance with our defensive mandate. The ceasefire with Iran does not constrain our obligation to defend Israeli citizens from terrorist threats. We are monitoring all fronts and prepared to respond decisively to any aggression.

**Action:** Present the War Cabinet with a 72-hour operational warning and three options by 1800 today: (A) Accelerated limited ground incursion into southern Lebanon (division-plus, 5-7 day duration) to destroy Hezbollah launch infrastructure within 10km of the border before Passover; (B) Intensified air campaign with explicit targeting of Hezbollah command nodes in Beirut southern suburbs, accepting higher collateral risk; (C) Defensive posture with enhanced air defense and intelligence collection through Passover, preserving munitions for Iranian escalation scenario. Recommend Option A with caveat that it requires immediate US approval for emergency PGM resupply and acceptance of 48-72 hour Lebanon ceasefire collapse. Simultaneously, order Northern Command to pre-position forces for Option A while

*Confidence: 0.75* · [full actor page](../actors/idf)

### mossad

**Public:** No public statement. Mossad does not comment on operational matters.

**Action:** Execute OPERATION HOURGLASS: Activate pre-positioned sabotage package at Natanz enrichment facility targeting centrifuge cascades in Hall B. Trigger mechanism designed to appear as catastrophic technical failure rather than external attack. Timing: 0300 local, 11 April. Simultaneously extract two critical HUMINT assets from Tehran and Qom whose operational security has been compromised by increased IRGC counter-intelligence activity following Khademi's death. Use the chaos of a 'technical disaster' at Natanz as cover for exfiltration through northern Iraq route. This action preserves deniability, degrades Iranian breakout timeline by 4-6 months, and protects irreplaceable intelligence sources before the ceasefire inevitably collapses.

*Confidence: 0.85* · [full actor page](../actors/mossad)

### shin_bet

**Public:** Shin Bet assesses the current ceasefire remains fragile. We have identified specific threat indicators in southern Lebanon that require immediate defensive measures. The Security Cabinet should be aware that our operational intelligence suggests heightened attack planning against civilian targets during the Passover period.

**Action:** Deploying reinforced protective intelligence teams to northern border communities and activating enhanced surveillance of known Hezbollah rocket launch sites in the Tyre-Nabatieh corridor. Simultaneously preparing threat warning for Security Cabinet meeting scheduled for April 10 evening, specifically flagging that continued IDF strikes in Lebanon are generating tactical-level Hezbollah responses that could trigger mass-casualty event. Recommending 48-hour operational pause in Lebanon to test Iranian/Hezbollah adherence before Passover begins.

*Confidence: 0.85* · [full actor page](../actors/shin_bet)

### aman

**Public:** Aman assesses that hostile actors retain both capability and intent to violate the ceasefire framework. We are observing continued military preparations by Hezbollah and IRGC-affiliated forces. The IDF maintains full operational readiness across all theaters.

**Action:** I am immediately tasking Unit 8200 for surge SIGINT collection on IRGC command networks and Hezbollah C2 nodes in Beirut/South Lebanon, with specific focus on Passover-window attack planning. Simultaneously, I am updating target folders for IAF on time-sensitive Iranian nuclear facilities and issuing tactical warning to Northern Command of heightened Hezbollah rocket threat during April 12-14 window. I am recommending to Chief of Staff that we accelerate strike planning against Fordow enrichment site while diplomatic constraints remain fluid.

*Confidence: 0.85* · [full actor page](../actors/aman)

### us_ic

**Public:** The Intelligence Community assesses that the announced ceasefire faces significant implementation challenges due to unresolved definitional disputes regarding scope, particularly concerning operations in Lebanon, and the absence of agreed verification mechanisms. We continue to monitor Iranian military posture, proxy force readiness, and decision-making dynamics within Iran's reconstituted leadership structure.

**Action:** Immediately task all national technical means (satellite imagery, SIGINT, cyber collection) on three priority intelligence requirements for the next 24 hours: (1) IRGC-ASF missile and drone unit alert status and any pre-launch indicators at known staging sites; (2) Hezbollah rocket battery deployment patterns in southern Lebanon and any changes in launch-ready posture; (3) Communications between IRGC command and Mojtaba Khamenei's office to assess actual command-and-control functionality. Simultaneously, convene secure VTC with CENTCOM J2, IDF Intelligence Directorate, and NSA's Iran Mission Manager to establish a common operational picture on potential ceasefire-breaking tripwires and request Israeli clarification on their operational definition of 'self-defense' strikes in Lebanon. Prepa

*Confidence: 0.85* · [full actor page](../actors/us_ic)

### israeli_ic

**Public:** Intelligence assessment provided to Security Cabinet under classification. No public statement authorized.

**Action:** Activate Operation MOLE CRICKET protocols: (1) Deploy additional Ofek-16 satellite tasking over Natanz/Fordow with 4-hour revisit cycle to detect enrichment surge indicators; (2) Task Unit 8200 to surge SIGINT collection on IRGC-QF communications nodes in Syria for evidence of weapons convoy authorization to Hezbollah; (3) Pre-position F-35I strike packages at forward bases with updated target folders for Iranian enrichment sites—full mission ready status; (4) Activate deep-cover HUMINT assets inside IRGC command structure for leadership intentions assessment on ceasefire durability; (5) Coordinate with CIA counterparts on joint collection requirements but maintain independent strike planning; (6) Brief Security Cabinet within 18 hours with recommendation to authorize preemptive action if

*Confidence: 0.92* · [full actor page](../actors/israeli_ic)

### us_gov

**Public:** The United States welcomes the ceasefire as an opportunity to de-escalate and pursue diplomatic solutions. We expect all parties to honor their commitments fully. Safe passage through the Strait of Hormuz must be maintained, and attacks on US forces and our partners must cease. We are monitoring compliance closely and reserve all options to defend our interests and allies.

**Action:** Convene urgent NSC Deputies Committee meeting within 12 hours to establish shared US-Israel definition of ceasefire scope re: Lebanon operations, develop tiered response matrix for Iranian violations (cyber, sanctions snapback, kinetic options), and task CENTCOM to provide 6-hour readiness assessment for strikes on IRGC-N missile sites if ceasefire collapses. Simultaneously dispatch State Department team to coordinate with Pakistan, France, Egypt on verification mechanism proposal to present within 48 hours.

*Confidence: 0.75* · [full actor page](../actors/us_gov)

### us_opposition

**Public:** While we welcome any pause in hostilities, this ceasefire contains dangerous ambiguities that demand immediate congressional oversight. The reported discrepancies between English and Farsi texts on enrichment, the absence of any verification mechanism, and the disputed scope regarding Lebanon operations create conditions for rapid collapse rather than durable peace. We will be demanding classified briefings from the State Department and CENTCOM within 24 hours on the precise terms agreed, Iran's compliance with Hormuz passage guarantees, and contingency planning if the ceasefire breaks during Passover. The American people deserve transparency about what commitments were made in their name.

**Action:** Convene emergency joint hearing of House Foreign Affairs and Armed Services Committees for Friday April 11 (within 48 hours), compelling testimony from Deputy Secretary of State, CENTCOM Deputy Commander, and NSC Senior Director for Middle East. Issue document preservation letters to State, DOD, and NSC demanding all cables, talking points, and intelligence assessments related to ceasefire negotiations. Coordinate with Senate Foreign Relations Committee (Cardin) on parallel session. Prepare War Powers Resolution draft for introduction if hostilities resume without congressional authorization.

*Confidence: 0.85* · [full actor page](../actors/us_opposition)

### russia

**Public:** Russia welcomes the ceasefire agreement as a responsible step toward de-escalation. We call on all parties to strictly observe the terms and pursue diplomatic solutions. Russia stands ready to facilitate dialogue and contribute to regional stability through our constructive relationships with all stakeholders.

**Action:** Accelerate delivery of S-400 air defense system components and spare parts to Iran via our Syrian air corridor, utilizing military transport aircraft to Hmeimim then ground convoy to Iranian territory. Simultaneously dispatch technical advisors to assist with integration and operational training. This strengthens Iranian defensive posture, increases our strategic value, and provides leverage for the inevitable next phase.

*Confidence: 0.85* · [full actor page](../actors/russia)

### china

**Public:** China welcomes the ceasefire agreement and commends the mediation efforts of Pakistan, France, and Egypt. All parties must exercise maximum restraint and implement the agreement in good faith. The sovereignty and territorial integrity of all nations must be respected. We call on Israel to cease military operations in Lebanon, which threaten regional stability. China stands ready to play a constructive role in promoting dialogue and urges the international community to support diplomatic solutions. The Strait of Hormuz must remain open for international commerce.

**Action:** Immediately dispatch Vice Foreign Minister to Tehran with private message to IRGC leadership: China will increase oil purchases by 15% at current discount rates and accelerate $2.3B port infrastructure investment in Chabahar IF Iran maintains Hormuz open and avoids ballistic missile launches for 72 hours. Simultaneously instruct Ambassador to UNSC to prepare resolution language condemning Israeli operations in Lebanon as ceasefire violation, timed for deployment if Israel strikes Beirut again in next 48 hours—this gives us leverage with Tehran without direct confrontation with Washington.

*Confidence: 0.78* · [full actor page](../actors/china)

### north_korea

**Public:** The DPRK consistently maintains its principled position on sovereignty and self-defense. We oppose all forms of hegemony and support the legitimate rights of nations to defend themselves against aggression.

**Action:** Dispatch technical delegation via Beijing to Damascus, ostensibly for 'reconstruction consultation,' actual purpose: establish secure logistics route for transferring 152mm artillery shells and KN-23/24 short-range ballistic missile components to Iran through Syrian territory. Coordinate with Russian military transport assets already operating Syria-Iran corridor. Initial shipment: 5,000 rounds artillery, 12 missile guidance packages, concealed in civilian construction equipment containers. Transit within 72 hours.

*Confidence: 0.78* · [full actor page](../actors/north_korea)

### pakistan_mediator

**Public:** Pakistan welcomes the ceasefire as a step toward regional stability and commends all parties for their restraint. As a facilitator of this agreement, we urge strict adherence to its terms by all sides. We stand ready to continue our bridging role and call for immediate clarification on the scope regarding Lebanon to prevent misunderstandings. Pakistan believes dialogue, not escalation, serves the interests of the entire region.

**Action:** ISI Chief will make immediate secure calls to both IRGC-QF leadership and Israeli Defense Minister's office within the next 12 hours, proposing a Pakistani-mediated trilateral technical meeting (virtual, intelligence-level) to establish a quiet de-confliction mechanism for Lebanon operations. Simultaneously, our Ambassador in Washington will deliver a private message to Trump's NSC that Israel's Lebanon strikes risk collapsing the deal Pakistan salvaged for him, requesting US pressure on Netanyahu to pause for 72 hours. We will also activate OIC Secretary-General (Saudi-aligned) to issue statement on Lebanon scope ambiguity.

*Confidence: 0.72* · [full actor page](../actors/pakistan_mediator)

### untso

**Public:** UNTSO acknowledges the announced ceasefire between Iran, the United States, and Israel effective 8 April 2026. Our observer posts along the Israel-Lebanon and Israel-Syria lines continue normal monitoring operations. We note the ceasefire text does not specify UN monitoring or verification mechanisms. UNTSO stands ready to support any internationally-mandated observation role and will continue to report all military activities in our areas of operation to the Secretary-General and Security Council per our mandate. We call on all parties to exercise maximum restraint and to clarify the geographic and operational scope of the ceasefire to prevent misunderstandings.

**Action:** Immediately dispatch written communications to IDF Northern Command, UNIFIL Force Commander, and the Lebanese Armed Forces liaison requesting clarification on whether the ceasefire applies to Israel-Hezbollah exchanges in southern Lebanon, and formally offering UNTSO observer support for any verification mechanism the parties wish to establish. Simultaneously, instruct all Observer Group Lebanon (OGL) posts to increase reporting frequency to every 6 hours with specific documentation of any air strikes, artillery fire, or rocket launches, regardless of attribution. Cable the Secretary-General's office warning that the Lebanon scope ambiguity creates immediate risk of ceasefire collapse that we are positioned to document but not prevent.

*Confidence: 0.85* · [full actor page](../actors/untso)

### ireland_gov

**Public:** Ireland condemns in the strongest terms the continued Israeli military operations in Lebanon, which directly threaten Irish peacekeepers serving with UNIFIL and violate the spirit of the ceasefire agreement. We call for an immediate, unambiguous extension of the ceasefire to cover all Lebanese territory. The safety of UN personnel is sacrosanct. We are consulting urgently with fellow troop-contributing countries and will use every diplomatic avenue to ensure UNIFIL's mandate is respected.

**Action:** Immediately convene emergency consultations with Spain, Belgium, Slovenia, and Italy (fellow UNIFIL contributors) to coordinate a joint EU Council emergency session demanding explicit ceasefire extension to Lebanon and enhanced UNIFIL protection guarantees. Simultaneously instruct our UN Ambassador to table a Security Council resolution calling for immediate cessation of hostilities in Lebanon and reinforcement of UNIFIL's mandate. If blocked by veto, pivot to Emergency Special Session of General Assembly under Uniting for Peace resolution.

*Confidence: 0.85* · [full actor page](../actors/ireland_gov)

### germany_gov

**Public:** Germany welcomes the ceasefire as an essential first step toward de-escalation. We call on all parties to exercise maximum restraint and implement the agreement in good faith. The ambiguities regarding Lebanon and verification must be resolved through immediate diplomatic channels. We urge Israel to limit operations that risk undermining the truce, while recognizing Israel's legitimate security concerns regarding Hezbollah. Iran must demonstrably open the Strait of Hormuz and cease all destabilizing activities. Germany stands ready to support mediation efforts and will work with France, the EU, and regional partners to establish verification mechanisms.

**Action:** Immediate secure call with French Foreign Minister Barrot to coordinate EU position on ceasefire verification and Lebanon scope. Propose joint EU-mediated clarification mechanism within 48 hours, leveraging France's Lebanon relationships and Germany's channels to both Washington and Tehran. Simultaneously, dispatch State Secretary to Jerusalem with private message: Germany will continue security cooperation and defend Israel diplomatically, but coalition government cannot sustain support if Lebanon operations trigger ceasefire collapse—request 72-hour operational pause in Beirut to allow diplomatic clarification. Prepare emergency EU Foreign Affairs Council for Friday if situation deteriorates.

*Confidence: 0.75* · [full actor page](../actors/germany_gov)

## Referee narration → next turn

```
# WORLD STATE — Turn 1 (April 10, 2026, 18:00 UTC / 21:00 IDT)

## Narrative

The ceasefire's first eighteen hours revealed not a pause but a **recalibration of violence**. Israel's intensified strikes on Hezbollah positions in Tyre, Nabatieh, and Beirut's southern suburbs—over thirty sorties documented by UNTSO observers—triggered the predicted Iranian response: Khamenei authorized a "calibrated signal," and by 14:00 IDT, Hezbollah launched forty-seven rockets from positions near Marjayoun toward IDF installations at Kiryat Shmona and Metula. Iron Dome intercepted thirty-one; the remainder struck open ground and one reserve staging area, causing four injuries. Netanyahu convened an emergency War Cabinet session within ninety minutes, authorizing immediate retaliation: IAF struck the launch sites and a Hezbollah command node in Baalbek.

The Strait of Hormuz remained **technically open**—Lloyd's confirmed three tankers transited southbound—but IRGC-Navy fast-attack craft conducted aggressive "inspection approaches" within twelve nautical miles of two Saudi-flagged vessels, forcing course deviations. The billboard in Revolution Square stayed illuminated. CENTCOM repositioned the *Eisenhower* strike group north and placed Patriot batteries at al-Asad on heightened alert after detecting IRGC-ASF mobile TEL movements in Kermanshah province.

Diplomatic channels ignited. Qatar dispatched envoys simultaneously to Tehran, Washington, and Jerusalem, proposing a Doha-hosted incident hotline and emergency foreign ministers' meeting on April 13. Pakistan's ISI chief reached both IRGC-QF and Israeli Defense Ministry, warning the deal Islamabad salvaged was "hours from collapse." Turkey's Erdoğan convened calls with Pakistan and Egypt, positioning Ankara as the essential broker for Lebanon scope clarification. The EU threatened dual sanctions—Iranian oil circumvention networks and expanded Israeli settlement goods—if ambiguity persisted beyond seventy-two hours.

Inside Iran, IRGC-IO launched mass arrests: over two hundred individuals detained in Tehran, Mashhad, and Shiraz—dual nationals, nuclear scientists' relatives, and civil society activists—under "counter-espionage" justification. State media announced expedited Revolutionary Court proceedings for eight "Israeli spies," with public executions planned within seventy-two hours. The diaspora's coordinated media blitz amplified footage of arrests and empty shelves, framing the ceasefire as a regime consolidation window rather than genuine peace.

At 03:00 local on April 11, **Natanz suffered a catastrophic failure** in Hall B's centrifuge cascades—official Iranian statements blamed "technical malfunction," but IAEA inspectors (denied immediate access) and Western intelligence assessed sabotage. Mossad executed OPERATION HOURGLASS, extracting two compromised assets through northern Iraq during the chaos. The incident degraded Iran's breakout timeline by an estimated four to six months but provided Tehran a pretext for hardline escalation rhetoric.

The ceasefire **technically held** by the operational definition—no direct state-level kinetic exchange between Iranian and US/Israeli forces, no ballistic missile launches from Iranian soil, Hormuz passable despite harassment—but the proxy layer combusted. Hezbollah's rocket barrage and Israel's Lebanon strikes created a **shadow war** that all parties exploited: Iran claimed Israeli violations justified proxy response; Israel insisted Lebanon was never covered; the US oscillated between privately urging Netanyahu to pause and publicly defending Israeli self-defense.

By 18:00 UTC, three parallel diplomatic tracks competed: Qatar's technical hotline proposal, Turkey's OIC-backed Lebanon expansion initiative, and the UN's emergency trilateral consultation scheduled for April 11, 06:00 UTC. None had achieved consensus. The twenty-four-hour window closed with the ceasefire's formal structure intact but its political foundation **fracturing along the Lebanon fault line**.

---

**ACTIVE_ACTORS:** Khamenei, Netanyahu, Trump, IRGC-QF, Hezbollah, IDF, Mossad, CENTCOM, Qatar (mediator), Pakistan (mediator), Turkey, EU, IRGC-IO, Iran dissidents (diaspora), UNTSO, UN (SG office)

**RECENT_EVENTS:**  
- Hezbollah rocket barrage (47 rockets, 4 IDF injuries) in response to Israeli Lebanon strikes  
- Israeli retaliation strikes on Hezbollah launch sites and Baalbek command node  
- Natanz Hall B centrifuge cascade failure (sabotage assessed, IRGC blames Israel)  
- IRGC-IO mass arrests (200+) of suspected "Israeli spies," 8 slated for public execution within 72 hours  
- IRGC-Navy harassment of Saudi tankers in Hormuz (no seizures, but aggressive approaches)  
- Qatar proposes Doha incident hotline + April 13 foreign ministers' meeting  
- Pakistan ISI warns both sides deal is "hours from collapse"  
- Turkey convenes Pakistan-Egypt call, positioning for Lebanon mediation  
- EU threatens dual sanctions if Lebanon ambiguity unresolved by 72-hour mark  
- Mossad extracts two HUMINT assets from Iran during Natanz chaos  

**OPEN_TENSIONS:**  
- **Lebanon scope dispute:** Iran/Hezbollah vs. Israel/US on whether ceasefire covers Hezbollah operations; no resolution, active proxy exchanges ongoing  
- **Hormuz ambiguity:** Technically open but IRGC-Navy harassment creates navigational risk; billboard contradicts official policy  
- **Enrichment verification:** Natanz sabotage gives Iran pretext to restrict IAEA access, Trump administration lacks agreed mechanism  
- **Passover window (April 12-14):** IDF assesses heightened Hezbollah attack risk; Israeli public shelters in north remain on alert  
- **Regime internal crackdown:** Mass arrests and planned executions risk triggering diaspora-amplified protest cycle  
- **Diplomatic fragmentation:** Three competing mediation tracks (Qatar, Turkey, UN) without coordination, risk of forum-shopping and collapse

---

**Token budget consumed:** ~1,850 (narration + structured block)  
**Remaining budget:** ~998,150
```
