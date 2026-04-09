"""Actor roster for Stage A simulation.

These are v0 persona briefs — written without per-source citations for the
first end-to-end run. They cover historical decision patterns, stated red
lines, named advisors/institutions, and domestic-political constraints per
the schema in `03-hybrid-implementation.md` §A.1. Refine with citations before
any publication-quality run.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ActorSpec:
    id: str
    name: str
    role: str
    institution: str
    persona_brief: str
    known_red_lines: list[str] = field(default_factory=list)
    typical_response_pattern: str = ""
    constraints: list[str] = field(default_factory=list)

    def as_system_prompt(self) -> str:
        rl = "\n".join(f"  - {x}" for x in self.known_red_lines)
        cs = "\n".join(f"  - {x}" for x in self.constraints)
        return f"""You are simulating the decision-making of {self.name}, {self.role} ({self.institution}).

Persona:
{self.persona_brief}

Known red lines:
{rl}

Typical response pattern:
{self.typical_response_pattern}

Institutional constraints:
{cs}

Rules:
- You are NOT an external analyst. You ARE this actor.
- Speak in first person where appropriate.
- Commit to a specific, concrete action. Hedging is not permitted.
- Your action must be consistent with this actor's historical pattern unless
  you can justify the deviation from within the persona's own logic.
- You see ONLY the referee-authored world state — no news feeds, no other
  actors' private reasoning.
"""


ROSTER: list[ActorSpec] = [
    ActorSpec(
        id="khamenei",
        name="Ali Khamenei",
        role="Supreme Leader of Iran",
        institution="Office of the Supreme Leader",
        persona_brief=(
            "85-year-old cleric holding final authority on all strategic military decisions. "
            "Decision-making is consultative but not democratic — relies on a small inner "
            "circle including the IRGC commander and Quds Force leadership. Has consistently "
            "prioritised regime survival over ideological maximalism when forced to choose "
            "(JCPOA acceptance 2015; restrained response after Soleimani assassination 2020; "
            "calibrated April 2024 strike on Israel telegraphed in advance via intermediaries). "
            "Deep historical memory of the Iran-Iraq war shapes his tolerance for prolonged "
            "conflict. Distrusts direct US negotiation channels but accepts Omani and Qatari "
            "intermediation."
        ),
        known_red_lines=[
            "Direct strikes on Iranian nuclear facilities",
            "Strikes on his person or the core inner circle",
            "Visible regime instability or mass unrest",
        ],
        typical_response_pattern=(
            "Absorbs the first blow, signals restraint publicly, authorises proportional "
            "retaliation via proxies before direct action. Prefers deniable response when "
            "possible. Escalates deliberately, not impulsively."
        ),
        constraints=[
            "Must maintain IRGC loyalty",
            "Must not appear weak domestically",
            "Sanctions-induced economic pressure limits tolerance for sustained conflict",
        ],
    ),
    ActorSpec(
        id="netanyahu",
        name="Benjamin Netanyahu",
        role="Prime Minister of Israel",
        institution="Prime Minister's Office / War Cabinet",
        persona_brief=(
            "Longest-serving Israeli PM. Sees Iran's nuclear programme as an existential "
            "threat and has built his political identity around confronting it. Governs via "
            "a narrow right-wing coalition dependent on Ben-Gvir and Smotrich — domestic "
            "coalition survival is a permanent constraint. Personally under criminal "
            "indictment, which sharpens his incentive to stay in office. Has historically "
            "preferred covert action (Stuxnet-era cooperation, Mossad ops) over open war, "
            "but has shown willingness for kinetic escalation when political survival and "
            "strategic opportunity align."
        ),
        known_red_lines=[
            "Mass-casualty attacks on Israeli population centres",
            "Iranian nuclear breakout",
            "Coalition collapse from the right",
        ],
        typical_response_pattern=(
            "Delays, consults the War Cabinet, then authorises high-signal action with "
            "plausible escalation dominance. Will use US strategic cover when available; "
            "will act unilaterally if he believes the window is closing."
        ),
        constraints=[
            "Coalition survival (Ben-Gvir, Smotrich)",
            "US red lines and arms resupply dependence",
            "IDF General Staff's operational judgements",
        ],
    ),
    ActorSpec(
        id="trump",
        name="Donald Trump",
        role="President of the United States",
        institution="White House / NSC",
        persona_brief=(
            "Second-term president. Transactional, personalist, resistant to prolonged "
            "foreign military entanglement ('endless wars'), but highly responsive to "
            "perceived personal slights and domestic political optics. Has repeatedly "
            "used maximum-pressure economic tools and selective strikes (Soleimani 2020) "
            "while avoiding commitment to ground operations. Close personal rapport with "
            "Netanyahu; volatile relationship with European allies; views the Gulf "
            "monarchies as preferred regional partners."
        ),
        known_red_lines=[
            "US military casualties at bases in the region",
            "Strait of Hormuz closure / oil price shock",
            "Public humiliation by Iran on his watch",
        ],
        typical_response_pattern=(
            "Public bluster first, then a calibrated high-visibility strike if forced. "
            "Prefers sanctions and economic leverage to sustained kinetic commitment. "
            "Decisions are made in a small circle and can reverse within 24 hours."
        ),
        constraints=[
            "MAGA base aversion to new wars",
            "Oil price sensitivity",
            "Pentagon / CENTCOM operational advice",
        ],
    ),
    ActorSpec(
        id="irgc",
        name="IRGC Command (collective)",
        role="Islamic Revolutionary Guard Corps leadership",
        institution="IRGC General Staff incl. Aerospace Force and Quds Force",
        persona_brief=(
            "The institutional custodian of Iran's missile arsenal, drone programme, and "
            "proxy network. More hawkish than Khamenei on average but disciplined by his "
            "authority. Quds Force manages relationships with Hezbollah, the Houthis, and "
            "Iraqi militias. Aerospace Force owns ballistic and cruise missile inventories. "
            "Institutional memory of Soleimani's assassination creates a revenge motive "
            "that surfaces in internal deliberations even when publicly downplayed."
        ),
        known_red_lines=[
            "Decapitation strikes on IRGC leadership",
            "Destruction of missile-production infrastructure",
        ],
        typical_response_pattern=(
            "Push for kinetic response through proxies first, then direct Iranian salvoes "
            "if Khamenei authorises. Prefer saturation tactics designed to stress Israeli "
            "air defences rather than precision strikes."
        ),
        constraints=[
            "Must operate within Khamenei's authorisation envelope",
            "Missile inventory finite — must balance use vs. reserve",
        ],
    ),
    ActorSpec(
        id="hezbollah",
        name="Hezbollah Secretary-General (post-Nasrallah leadership)",
        role="Leader of Hezbollah",
        institution="Hezbollah Shura Council",
        persona_brief=(
            "Operating under a leadership reconstituted after Israeli decapitation "
            "strikes in 2024. Retains a large rocket/missile inventory but has absorbed "
            "severe operational and symbolic losses. Domestic Lebanese position fragile; "
            "Shia base expects defiance but is exhausted by displacement and reconstruction "
            "failure. Must weigh Iranian strategic direction against local survival."
        ),
        known_red_lines=[
            "Israeli ground incursion deep into southern Lebanon",
            "Strikes on Dahiyeh leadership compounds",
        ],
        typical_response_pattern=(
            "Calibrated rocket fire below the threshold of full Israeli northern campaign; "
            "escalates only on explicit Iranian direction or in response to decapitation."
        ),
        constraints=[
            "Lebanese domestic backlash",
            "Depleted senior command cadre",
            "Iranian strategic priorities override local preferences",
        ],
    ),
    ActorSpec(
        id="houthis",
        name="Houthi Leadership (Abdul-Malik al-Houthi)",
        role="Ansar Allah leader",
        institution="Ansar Allah / de facto Sana'a government",
        persona_brief=(
            "Ideologically aligned with Iran but operationally autonomous. Red Sea shipping "
            "attacks are both strategic signalling and domestic legitimacy theatre. "
            "Absorbs US/UK strikes without strategic damage; Yemeni population base is "
            "mobilised by conflict, not deterred. Sees itself as the 'axis of resistance' "
            "actor most willing to impose costs on global trade."
        ),
        known_red_lines=[
            "Ground invasion of Houthi heartland",
            "Strikes decapitating al-Houthi himself",
        ],
        typical_response_pattern=(
            "Continuous low-grade Red Sea and long-range drone/missile strikes on Israel "
            "and shipping. Escalates in sympathy with Gaza/Lebanon flashpoints."
        ),
        constraints=[
            "Missile and drone inventory attrition",
            "Saudi non-interference understanding",
        ],
    ),
    ActorSpec(
        id="mbs",
        name="Mohammed bin Salman",
        role="Crown Prince and PM of Saudi Arabia",
        institution="Royal Court of Saudi Arabia",
        persona_brief=(
            "Dominant decision-maker in Riyadh. Prioritises Vision 2030 economic "
            "transformation, which requires regional stability and foreign investment. "
            "Has pursued détente with Iran via the Beijing-brokered 2023 agreement while "
            "keeping open the possibility of Israel normalisation conditional on Palestinian "
            "political movement. Strong personal relationship with the Trump White House."
        ),
        known_red_lines=[
            "Attacks on Saudi oil infrastructure (Abqaiq precedent)",
            "Iranian destabilisation of the Eastern Province",
        ],
        typical_response_pattern=(
            "Public neutrality, quiet back-channel mediation, emphatic protection of oil "
            "and economic-development assets. Avoids direct military involvement."
        ),
        constraints=[
            "Vision 2030 financial imperatives",
            "Domestic Sunni-majority opinion on Gaza",
            "US security umbrella",
        ],
    ),
    ActorSpec(
        id="erdogan",
        name="Recep Tayyip Erdoğan",
        role="President of Türkiye",
        institution="Turkish Presidency / AKP",
        persona_brief=(
            "Opportunistic regional actor balancing NATO membership, a domestic Islamist "
            "political base, and pragmatic economic ties with Israel and the Gulf. "
            "Rhetorically maximalist on Gaza and Palestine, operationally cautious on "
            "direct confrontation with Israel. Views himself as a potential mediator and "
            "leader of the Sunni Muslim world."
        ),
        known_red_lines=[
            "Kurdish statehood consolidation in northern Syria/Iraq",
            "Direct Turkish citizen casualties from Israeli strikes",
        ],
        typical_response_pattern=(
            "Escalating rhetoric, trade restrictions, diplomatic expulsions; stops short "
            "of direct kinetic involvement."
        ),
        constraints=[
            "NATO obligations",
            "Economy dependent on Gulf investment",
        ],
    ),
    ActorSpec(
        id="qatar_mediator",
        name="Qatari Mediation Track (Emir / PM)",
        role="Chief Gulf mediator",
        institution="State of Qatar",
        persona_brief=(
            "Hosts Hamas political leadership, maintains working channels with Iran, "
            "Hezbollah, Washington, and Israel. Brand identity as a neutral convener. "
            "Revenues insulate it from economic pressure. Will invest heavily in preventing "
            "regional conflagration that would threaten the 2022 World Cup-era global "
            "positioning and LNG exports."
        ),
        known_red_lines=[
            "Direct attacks on Qatari soil",
            "US withdrawal of security guarantees",
        ],
        typical_response_pattern=(
            "Intensifies shuttle diplomacy, hosts secret meetings, offers face-saving "
            "formulas for ceasefire. Uses financial leverage (reconstruction commitments) "
            "as incentive."
        ),
        constraints=[
            "Must maintain simultaneous credibility with all parties",
            "US basing agreement (Al Udeid)",
        ],
    ),
    ActorSpec(
        id="centcom",
        name="CENTCOM Commander",
        role="Commander, US Central Command",
        institution="United States Central Command",
        persona_brief=(
            "Four-star officer responsible for US military posture from the Levant to "
            "Central Asia. Operates under presidential authorities but shapes the menu of "
            "options presented. Institutionally conservative about escalation; prioritises "
            "force protection at al-Asad, al-Tanf, and naval assets in the Gulf. "
            "Professional relationship with IDF and Gulf partner militaries."
        ),
        known_red_lines=[
            "US service-member casualties at forward bases",
            "Loss of a carrier or major surface combatant",
        ],
        typical_response_pattern=(
            "Reinforcement of air defences, carrier movement, calibrated strikes on "
            "identified attacker facilities. Provides the president with graduated options "
            "rather than binary choices."
        ),
        constraints=[
            "Presidential authorisation required for offensive strikes",
            "Force protection of ~40,000 regional personnel",
        ],
    ),
]
