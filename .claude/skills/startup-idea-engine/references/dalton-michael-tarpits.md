# Reference: Dalton & Michael Tarpit Ideas Catalog

**Source:** [Dalton & Michael - Where do great startup ideas come from?](https://www.ycombinator.com/library/DU-dalton-michael-where-do-great-startup-ideas-come-from) and the YC podcast series, particularly "Avoid These Tempting Startup Ideas."

**What is a tarpit idea?** A pattern that first-time founders cluster on. The idea sounds attractive on first inspection. A generation of failed attempts has established that it does not work for *structural* reasons - not for execution reasons. The next founder to try this idea fails for the same reasons.

**The fatal property of tarpit ideas:** They are easy to talk about, easy to imagine succeeding, easy to get friends excited about. They look like opportunities. They are not.

This file catalogs the documented tarpit shapes plus founder-specific tarpit history. It is loaded by `sub-skills/02-framework-tests.md` (Test 6) and `sub-skills/04-adversarial-review.md` (Tarpit Auditor critic).

---

## Canonical Tarpit Patterns

### TP-01 - "Better X" where X is a category leader

**Examples:** Better email client. Better project management. Better calendar. Better CRM. Better Slack. Better Notion.

**Why it's a tarpit:** Switching costs in entrenched horizontal categories are huge. Users tolerate awful incumbents because the cost of switching across a team is enormous. "10x better" is rarely 10x enough to overcome network effects + integration debt.

**Escape conditions:** A wedge that doesn't require horizontal switching - vertical specialization, AI-native rebuild that creates a new category, or a structural change in the underlying technology that makes the incumbent's architecture obsolete.

### TP-02 - "Marketplace for X" with no captive side

**Examples:** Marketplace for handymen. Marketplace for tutors. Marketplace for designers.

**Why it's a tarpit:** Two-sided liquidity is famously hard. If neither side is captive (i.e., neither side has lock-in to the marketplace), the marketplace gets disintermediated the moment value is delivered. Users discover each other and transact off-platform. The vast majority of marketplaces fail this test.

**Escape conditions:** One side structurally captive (e.g., regulated supply, scarce supply, network-effect supply). Embedded payments + escrow that make off-platform transactions painful. Or a different business model entirely (subscription, lead-fee with single-side captive).

### TP-03 - "Social network for X profession"

**Examples:** Social network for doctors. Social network for lawyers. Social network for engineers (besides the existing entrenched ones).

**Why it's a tarpit:** Professional social networks have powerful winner-take-all dynamics. LinkedIn is the entrenched winner for most professions in 2026. Existing players (Doximity for doctors, Lex for lawyers, etc.) occupy the niches. Network effects compound; new entrants face cold-start problems with no clear differentiator.

**Escape conditions:** A wedge that isn't actually social-networking (e.g., professional tooling that has incidental social features). Or a profession in genuine acute crisis where existing networks are structurally inadequate (T11's cooperative substrate for AI-displaced professionals partially fits this exception).

### TP-04 - "AI-powered X" where X is generic vertical software

**Examples:** AI-powered scheduling. AI-powered CRM. AI-powered project management. AI-powered SMB operations.

**Why it's a tarpit:** AI is a capability layer; "AI-powered X" without a specific structural insight is a feature pretending to be a category. Incumbents are shipping AI features; new entrants compete on AI capability against companies with 10x the data and distribution.

**Escape conditions:** A specific structural insight that the AI capability enables (e.g., "Computer Use makes cross-platform agentic operations affordable for SMB for the first time"). Vertical depth + agent-native architecture that incumbents can't retrofit.

### TP-05 - Attention-economy / engagement-maximization tooling

**Examples:** Anything optimized for time-on-app. Newsletter / content platforms with feed mechanics. Notification-driven anything.

**Why it's a tarpit:** The category is structurally overcrowded. The economics are advertising-shaped (low margin per user) requiring massive scale. The principle violation (Cognitive Sovereignty) is severe.

**Escape conditions:** None for principle-aligned founders. Categorically foreclosed by the operator's Principle 4.

### TP-06 - "Tools for creators" without distribution edge

**Examples:** Yet-another newsletter platform. Yet-another podcast hosting. Yet-another video editing AI.

**Why it's a tarpit:** Creator tooling is an extremely competitive category with low switching costs and high creator-side churn. Most creators consolidate to 1-2 platforms with the best distribution; tools without distribution advantages can't acquire users.

**Escape conditions:** Distribution-bundled tools (Substack, Beehiiv pattern). Or genuinely novel modality (AI video at the moment Runway / Sora / Pika defined the category).

### TP-07 - "Consumer crypto" without payments use case

**Examples:** NFT-driven anything that isn't a real payment. Web3 social. Tokenized X.

**Why it's a tarpit:** Multiple cycles of failed consumer crypto experiments. Without a real payments use case (stablecoins, cross-border, etc.), the category structurally lacks pull.

**Escape conditions:** Stablecoin / payments-anchored use cases. Skip otherwise.

### TP-08 - "X for nonprofits" / "X for restaurants" / "X for SMB" with no structural reason

**Examples:** AI for nonprofits. CRM for restaurants. Software for SMB owners.

**Why it's a tarpit:** Hard-to-sell-to verticals are hard-to-sell-to for structural reasons (low budget, no procurement, founder-led tiny IT, tight margins). Choosing them as wedges multiplies sales-cycle pain. Many founders pick these because they sound noble or because they're "underserved" - but underserved often means unbuyable.

**Escape conditions:** A structural reason this vertical can suddenly buy (e.g., PE consolidation creating budget at the platform level; a regulatory forcing function; a wave that creates urgency the vertical didn't have before).

### TP-09 - "Email assistant" / "AI scheduling assistant" / generic AI agent for personal productivity

**Examples:** Yet-another AI inbox. Yet-another AI calendar. Yet-another AI executive assistant.

**Why it's a tarpit:** Massive cohort of failed attempts (Astro, Mailbox, Sunrise, x.ai, Clara Labs, several rounds since). Personal productivity AI has graveyards. Big-tech is also building this natively.

**Escape conditions:** Vertical-specific (e.g., "AI inbox for litigators" with deep workflow integration) - even then, demonstrate structural reason this generation of attempts succeeds where the prior generations failed.

### TP-10 - "Vertical AI receptionist / chatbot" without distribution edge

**Examples:** AI receptionist for HVAC. AI booking agent for med-spa. AI customer-service for restaurants.

**Why it's a tarpit (in 2026):** Massive cohort of well-funded entrants in 2024-2026 (Goodcall, Numa, Slang, Bland, Vapi, Ada, dozens more). Voice/chat AI agent is commoditizing fast. Distribution is the moat, not the agent.

**Escape conditions:** Underlying knowledge-graph / data-grounding layer that makes agents *honest* (the prerequisite layer most current entrants skip). Or vertical-specific deployment with deep workflow integration that creates lock-in beyond the agent itself.

---

## the operator-Specific Tarpit History (the workspace Q1 2026)

These shapes have *already failed* in the operator's hands. Treat any candidate that re-runs these shapes as tarpit-shaped repetition unless a structural difference is named.

### TPS-01 - Cold outbound to SMB owners (any pitch)

**The Q1 data:** 12 meetings booked, 3 real ICP demos, 1 conversion (Reeis, since churned). 0/15 HCP discovery conversations attempted. 0/15 law firm conversations attempted. Loom videos without personalized messages: 0 replies.

**Why it's a tarpit:** SMB owners are not in budget-aware buying motion for software they didn't know they needed. They buy from referrals, vendors they already work with, and at moments of acute crisis. Cold outbound to a marketing-director or owner persona, with any pitch shape, has not converted at velocity for the operator.

**Escape conditions:** Owner-to-owner referral motion (requires existing community the operator doesn't yet have); vendor-bundled distribution (requires partnership the operator doesn't yet have); buyer-moment-triggered outreach (acute pain, fresh hire, post-acquisition, not generic).

### TPS-02 - "Your funnel is leaking" / conversion-optimization-for-trades pitch

**The Q1 data:** Reeis converted on this pitch and churned. Beantown is on free tier with no engagement. Mother dormant. The 13x conversion lift was real but did not produce a sustainable retention model.

**Why it's a tarpit (for the operator):** The pitch is too plausible (Test 7 - plausibility trap). Trades owners hear it from every agency and every vendor. The proof point (13x lift) is real but the buyer's procurement reality (price sensitivity, slow cycle, low-budget marketing function) does not support the implied price-to-value math.

**Escape conditions:** Reframing from "we improve your conversion" to a different value layer entirely (operational / financial / regulatory). Or selling to a different buyer (PE rollup ops VP, not single-shop owner).

### TPS-03 - Trades-agency referral channel (white-label / resale)

**The Q1 data:** 7-8 agencies expressed interest, 0 conversions to active referral. Confirmed long cycle (months to quarters) regardless of pitch shape.

**Why it's a tarpit:** Agencies that haven't built proprietary tooling don't suddenly become product distributors. Their incentive is billable hours, not platform partnership. Profit-share-on-referral is the structurally weakest deal shape because it provides no reason for the agency to push.

**Escape conditions:** Foundational-partner deal with up-front commitment ($X + N-client minimum) that filters serious agencies on day one. OR selling INTO the agency for their own ops (not for resale to clients) - which is a different sale, different buyer.

### TPS-04 - Selling against the incumbent vendor's owned territory

**The Q1 data:** the workspace scheduler is structurally adjacent to the incumbent vendor's built-in scheduler. the incumbent vendor announced "CRM: Residential automates follow-ups" generally available summer 2026 - direct competitive collision.

**Why it's a tarpit:** the incumbent vendor owns the customer relationship, the data, the routing, and the buying process. Selling a competitive feature to their customers triggers their roadmap response.

**Escape conditions:** Architecture decisions that make the workspace a non-competitor and/or platform-portable (read/write split, customer-owned portable spec, multi-platform from Day 90). Or specifically picking a domain the incumbent vendor won't ship in 12 months (e.g., cross-vertical operations substrate that bridges ST and HCP and Jobber - ST won't build this).

---

## How This Catalog Is Used

- **Test 6 (Tarpit Check):** Every candidate is matched against TP-01 through TP-10 (canonical) and TPS-01 through TPS-04 (the operator-specific). FAIL if a clean match exists with no structural difference.
- **Critic 4 (Tarpit Auditor):** Reads this file and assesses each candidate. Cites the specific TP/TPS code in the verdict.
- **Maintenance:** When a new tarpit pattern is observed in production (a new shape that fails for structural reasons), append it as TP-XX (canonical) or TPS-XX (the operator-specific) with date and observed-failure context.

---

## A Note on the Tarpit Mindset

A candidate is not automatically tarpit-shaped just because incumbents exist. PG explicitly says crowded markets are a positive signal - they confirm demand. The tarpit test is more specific:

> A tarpit idea is one where (a) many founders before you tried it, (b) most of them failed, (c) the failures were for structural reasons (not execution), and (d) your version does not have a documented structural difference.

If the candidate has a structural difference - *and that difference is documented in the Raw Idea doc, with reasoning* - it can survive the tarpit test even within an established tarpit shape. The structural difference must be specific. "We're better" is not structural. "Our distribution channel is owner-to-owner referral, which existing players don't have" is structural.
