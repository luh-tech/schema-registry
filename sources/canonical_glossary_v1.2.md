**CTA CANONICAL GLOSSARY**

*Version 1.2  ·  2026-05-05*

*Single source of truth for terminology used across all five CTA provisional patent applications. Aligned to ACRONYMS-CATALOG-2026-05-04 (canonical upstream).*

**Scope and Discipline**

This Glossary is the locked terminology source for the patent project. It serves two distinct categories of terms:

PATENT-OWNED terms (Section B "Data Structures and Provenance," Section D "Positioning and Sensor Hardware," Section E "Cryptographic Primitives"). The catalog explicitly excludes these from its scope. The Glossary is the upstream source for these — claim language, specification language, and prosecution rely on the definitions here.

CATALOG-DERIVED terms (Sections A, C, F, G, H, I, J, K, L). The ACRONYMS-CATALOG-2026-05-04 is the canonical upstream. Definitions in this Glossary either match the catalog verbatim or carry a clear footnote when condensed for patent context. Drift between this Glossary and the catalog is a defect.

**Every term that appears in more than one provisional MUST be defined here exactly once. Definitions in any spec must match this Glossary verbatim. If drafting reveals a definition needs to change, the change is made HERE FIRST, then propagated.**

**Status legend:**

*• LOCKED — definition fixed, used in filings as-is.*

*• PATENT-OWNED — defined here; catalog defers to this Glossary.*

*• DEPRECATED — historical term, retained for cross-reference only.*

**A. Cluster and Portfolio Identifiers**

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **SBPA** | Spatially-Bound Provenance Architecture | The unified architecture spanning physically-rooted entropy, sensor hardware, cryptographic field-level provenance, voxel data model, mesh communication, and on-chain anchoring. The umbrella under which the five provisional patent applications sit. "Spatially-Bound" carries dual meaning: binding to coordinate frames at every layer of the spatial hierarchy, and binding to spatial sources of entropy at the physical-observation layer. | *LUHTECH-IP-ARCH-2026-03-10 \+ Erik 2026-05-05 · LOCKED* |
| **CTA** | — | DEPRECATED. Former umbrella name ("Cosmological Trust Architecture") superseded 2026-05-05 by SBPA. Retained here for cross-reference to legacy documents. | *DEPRECATED — use SBPA* |
| **LuhTechnology** | — | Trade name appearing in inventor correspondence and prior public disclosures. USPTO Customer Number 199224 is registered to erik@luhtechnology.com. | *USPTO 2024-04-17 · LOCKED* |
| **LuhTech Holdings** | LTH | Construction technology venture studio. Parent entity holding nine ventures on a shared open-core platform. Future assignee for CTA patent rights post-filing. | *Catalog · LOCKED* |
| **Inventor** | — | Erik J. Luhtala. Sole inventor on all CTA filings. Files in inventor's name; assignment to LuhTech Holdings post-filing; license to Ectropy and other ventures downstream. | *Erik 2026-05-04 · LOCKED* |
| **Customer Number** | — | 199224\. Registered 2024-04-17 to erik@luhtechnology.com, role: Independent Inventor. Used on every PTO/SB/16 cover sheet. | *USPTO acceptance · LOCKED* |
| **Procopio** | — | Procopio, Cory, Hargreaves & Savitch LLP — patent counsel. Prior counsel of record on US 9,322,165 B2 (Hilja). Engaged for non-provisional conversion of CTA provisionals. | *LOCKED* |

**B. Data Structures and Provenance  \[PATENT-OWNED\]**

*Patent-owned. Catalog defers to this Glossary for definitions in this section.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **ProvenanceField** | — | First-class cryptographic data type. A record comprising at minimum: (a) a sensor measurement value; (b) a voxel identifier; (c) a UWB-validated three-dimensional position; (d) an entropy-seeded sequence position; (e) a chain hash; (f) a building signature; (g) a building identifier. The validated spatial position is a structural input to the chain hash, rendering value and position cryptographically inseparable. | *P1 v1.0 · PATENT-OWNED* |
| **RVGT** | Rolling Validated Ground Truth | Append-only, hash-chained sequence into which ProvenanceField records and DecisionEvent records are linked via prev\_hash references. The integrity primitive of the system. Tamper-evidence emerges from the chain dependency structure. | *P1 v1.0 · PATENT-OWNED* |
| **chain\_hash** | — | SHA-256 hash computed over the canonical concatenation of a record's fields including its UWB-validated position and the chain hash of the immediately preceding record. | *P1 v1.0 · PATENT-OWNED* |
| **sequence\_pos** | — | Position identifier within the RVGT chain. Drawn from physically-irreducible entropy rather than a monotonic counter, to resist adversarial pre-computation of fabricated chain branches. | *P1 v1.0 · PATENT-OWNED* |
| **prev\_hash** | — | The chain\_hash of the immediately preceding record in the same RVGT chain. Linkage primitive that makes the chain append-only. | *P1 v1.0 · PATENT-OWNED* |
| **DecisionEvent** | — | Universal canonical immutable event in @ectropy/schemas. Required fields: $id (URN), schemaVersion, domain (discriminator), timestamp, projectId, actorId, agentType, classification, authorityLevel. All fields readonly. Patent embodiments of cosmologically-seeded decision entropy operate on DecisionEvent records. | *@ectropy/schemas · LOCKED* |
| **DecisionRecord** | — | Patent-context shorthand for a DecisionEvent within an RVGT chain. Carries inputs (as ProvenanceField references), authority tier, outcome, entropy-seeded chain position, pulsar epoch reference, and chain hash. | *P3 outline · PATENT-OWNED* |
| **SuccessPattern** | — | @ectropy/schemas type. Compressed validated wisdom extracted from successful DecisionEvents. Decays over time; reinforced by repeated successful application. Stored with context\_signature. | *@ectropy/schemas · LOCKED* |
| **SdiSnapshot** | — | @ectropy/schemas type. Point-in-time capture of Solution Density Index for a project. | *@ectropy/schemas · LOCKED* |
| **Evidence** | — | @ectropy/schemas type. Universal evidence record with SHA-256 chain of custody. | *@ectropy/schemas · LOCKED* |

**C. Spatial Data Model**

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **BOX** | BIM \+ BOM \+ VOX | LuhTech canonical spatial-truth container. Three coordinated data layers: BIM (design intent from IFC), BOM (procurement / actual materials), VOX (field-verified installation status). Foundation substrate beneath every spatial decision. | *Catalog · LOCKED* |
| **BIM** | Building Information Model | Industry-standard digital 3D representation of a building with embedded geometry, materials, specifications, and element relationships. Authored in Revit, AutoCAD, or IFC native tools and exchanged as IFC. | *ISO 16739 · LOCKED* |
| **BOM** | Bill of Materials | Industry-standard list of materials procured for a project: quantities, suppliers, costs, EPDs. In BOX, BOM is the procurement layer between BIM (design intent) and VOX (field-verified installation). | *Catalog · LOCKED* |
| **VOX** | Voxel verification layer | Field-verified installation status per spatial unit (voxel). The third layer of BOX. Tracks what was actually installed where, against the BIM design intent and BOM procurement. | *Catalog · LOCKED* |
| **Voxel** | — | Discrete spatial unit (volumetric pixel) anchored to BIM geometry. LuhTech standard resolution is 0.1m³ at COARSE tier. Each voxel inherits IfcSpace zone classification and tracks state lifecycle (NOT\_STARTED, IN\_PROGRESS, INSTALLED, INSPECTED, COMPLETE). | *Catalog · LOCKED* |
| **voxel\_id** | — | Identifier of a specific voxel cell. Computed by quantizing a validated UWB position to the voxel grid and looking up the unique identifier for that cell. | *P1 v1.0 · PATENT-OWNED* |
| **COARSE tier** | — | 100 mm resolution voxel grid (0.1 m cube). PM dashboard, phase gates, zone health. Decision authority L3-L4. | *BOX-ARCHITECTURE-2026-03-26 · LOCKED* |
| **STANDARD tier** | — | 40 mm resolution voxel grid (0.04 m cube). MEP coordination, clash detection, work orders. Decision authority L5. | *BOX-ARCHITECTURE-2026-03-26 · LOCKED* |
| **FINE tier** | — | 10 mm resolution voxel grid (0.01 m cube). As-built deviation, warranty, QA sign-off. Decision authority L5-L6. | *BOX-ARCHITECTURE-2026-03-26 · LOCKED* |
| **source\_type** | — | Voxel-grid attribute distinguishing BIM (design model), SCAN (lidar as-built), and MANUAL (hand-entered) sources. The delta between BIM and SCAN grids at the same tier IS the deviation surface. | *BOX-ARCHITECTURE-2026-03-26 · LOCKED* |
| **Deviation Surface** | — | Spatial map of where as-built reality (SCAN grid) diverges from design (BIM grid) at the same resolution tier. The warranty and QA value proposition. | *BOX-ARCHITECTURE-2026-03-26 · LOCKED* |

**D. Positioning and Sensor Hardware  \[PATENT-OWNED\]**

*Patent-owned. Catalog defers to this Glossary for sensor hardware specifications.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **UWB** | Ultra-Wideband | Short-range radio positioning technology operating across wide spectral bandwidth. In CTA: deployed as fixed anchor grid plus mobile tags, providing centimeter-accurate (\~±10 cm) three-dimensional position to sensing devices. | *IEEE 802.15.4z · LOCKED* |
| **Anchor Grid** | — | Set of UWB anchor nodes deployed at known positions throughout an operational environment. Multilateration against three or more anchors yields a validated position. | *P1 v1.0 · PATENT-OWNED* |
| **Multi-Anchor Consensus** | — | Position validation requirement: agreement among at least three anchors with mutual residual error below a configurable threshold (typically 15 cm for ±10 cm target accuracy). | *P1 v1.0 · PATENT-OWNED* |
| **Position Quality Indicator** | — | Field stored within a ProvenanceField record indicating: number of anchors contributing, residual error of multilateration, geometric dilution of precision. | *P1 v1.0 · PATENT-OWNED* |
| **TWR** | Two-Way Ranging | UWB positioning mode. The mobile device exchanges timed messages with each anchor; round-trip time yields range. Used for static position fixes. | *IEEE 802.15.4z · LOCKED* |
| **TDoA** | Time-Difference-of-Arrival | UWB positioning mode. Anchors timestamp the receipt of a single mobile transmission; differences in arrival time yield position. Used for high-rate tracking. | *IEEE 802.15.4z · LOCKED* |
| **Ohjaus sensor module** | — | Sensor module specification: ESP32-S3 microcontroller \+ Qorvo DWM3000 UWB module \+ Semtech SX1262 LoRa radio. The reference embedded sensor platform for ProvenanceField generation. Marketed and sold under the Ohjaus venture (open sensor infrastructure). | *Erik 2026-05-04 · PATENT-OWNED* |
| **SSB** | Silla Structural Beacon | Building structural-monitoring hardware comprising an embedded probe (sensor in concrete) and a sensor plate (surface-mounted, doubles as UWB anchor). Owned within Siltana operations platform. | *SILTANA\_SPEC\_V3 · PATENT-OWNED* |
| **LoRa** | Long Range (radio) | Low-power wide-area wireless protocol used in CTA for offline mesh communication between buildings (SX1262 transceiver, 10-15km urban, 40km+ line-of-sight). | *Semtech · LOCKED* |

**E. Cryptographic Primitives  \[PATENT-OWNED\]**

*Patent-owned. The Tri-Pulsar Protocol and related cosmological-entropy constructions are defined here.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **SHA-256** | — | FIPS 180-4 cryptographic hash function. Used for chain\_hash construction in ProvenanceField records and DecisionRecord chains. | *NIST FIPS 180-4 · LOCKED* |
| **SHAKE-256** | — | FIPS 202 extendable-output function from the SHA-3 family. Used in the Tri-Pulsar Protocol's key derivation function. | *NIST FIPS 202 · LOCKED* |
| **Tri-Pulsar Protocol** | — | Method for deriving cryptographic identity for a fixed physical structure from observed timing residuals of three millisecond pulsars over a 24-hour observation window from the structure's celestial position. Identity key \= SHAKE-256(residuals\_1 ‖ residuals\_2 ‖ residuals\_3 ‖ celestial\_position ‖ observation\_descriptor). | *P2 outline · PATENT-OWNED* |
| **Building Identity** | — | Cryptographic identity of a fixed structure derived via the Tri-Pulsar Protocol. Independent of certificate authority. Used to sign ProvenanceField records and authenticate peer building messages over LoRa mesh. | *P2 outline · PATENT-OWNED* |
| **Pulsar Timing Residuals** | — | Differences between observed pulsar pulse times-of-arrival and predictions from a timing model. Physically irreducible entropy source caused by interstellar medium fluctuations, gravitational effects, and neutron star quantum dynamics. | *Hobbs & Manchester 2006 · LOCKED* |
| **Celestial Position** | — | Right Ascension / Declination coordinates computed from the observer's geographic coordinates and observation epoch. Component of the Tri-Pulsar key derivation function — yields position-bound identity. | *P2 outline · PATENT-OWNED* |
| **Pulsar Epoch** | — | A specific 24-hour observation window from a specific celestial position. Identifies a particular entropy seed; auditable against published pulsar timing array data (NANOGrav, EPTA, PPTA). | *P2 outline · PATENT-OWNED* |
| **NANOGrav** | — | North American Nanohertz Observatory for Gravitational Waves. Pulsar timing array collaboration; publishes timing data referenceable for Pulsar Epoch audit. | *NANOGrav consortium · LOCKED* |
| **EPTA** | European Pulsar Timing Array | European consortium publishing pulsar timing data. Reference for cross-verification of Pulsar Epoch. | *EPTA consortium · LOCKED* |
| **PPTA** | Parkes Pulsar Timing Array | Australian consortium publishing pulsar timing data. Third independent reference for Pulsar Epoch verification. | *CSIRO · LOCKED* |
| **PUF** | Physically Unclonable Function | Hardware identity primitive whose value derives from manufacturing variance of a specific device. Distinguished in P2 prior art from the Tri-Pulsar Protocol — PUFs are device-bound, Tri-Pulsar is structure-and-position bound. | *Pappu et al. 2002 · LOCKED* |

**E2. Coordinate Frame Transform Attestation  \[PATENT-OWNED\]**

*Vocabulary for the unified transform-attestation primitive that operates recursively across the spatial hierarchy from sensor-frame to planetary-frame. Patent-owned. The terms in this section establish the term-of-art definitions for purposes of §112 definiteness across all five filings.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **Coordinate Frame** | — | A named reference frame with a defined origin and orientation in three-dimensional space. Frames may be related to one another by attested coordinate frame transforms. Examples: a sensor's local frame, an anchor grid frame, a building's BIM frame, a parcel/legal frame in county GIS records, a regional aggregation frame, a continental frame, the WGS84 geodetic frame. | *P1 v1.3 · PATENT-OWNED* |
| **Coordinate Frame Transform** | Transform | A mathematical relationship between two coordinate frames comprising a translation, a rotation, and optionally a scale factor. A transform takes a position expressed in a child frame and produces the corresponding position expressed in the parent frame. Transforms compose: a transform from frame A to frame C may be obtained by composing the transform from A to B with the transform from B to C. | *P1 v1.3 · PATENT-OWNED* |
| **Transform Attestation** | — | A self-attesting record per the present invention wherein the canonical concatenation comprises a coordinate frame transform, the identifiers of the child and parent frames the transform relates, the attesting observations that established the transform, and a chain hash that binds the foregoing elements. The transform attestation record is the structural primitive of the present invention's hierarchical extension. | *P1 v1.3 · PATENT-OWNED* |
| **Attesting Observation** | — | A physical observation contributing to the establishment of a coordinate frame transform. Modalities include without limitation: Ultra-Wideband multilateration against an anchor grid, multi-constellation Global Navigation Satellite System receiver fix, surveyor instrument shoot, radio-frequency timing observation of one or more astronomical sources, photogrammetric registration, and combinations thereof. | *P1 v1.3 · PATENT-OWNED* |
| **Three-Point Minimum** | — | The mathematical minimum number of attesting observations required to establish a coordinate frame transform with three-dimensional position resolution. Three points define a plane in three-dimensional space; below three observations, depth (Z-coordinate) cannot be derived. Independent claim language recites at least three attesting observations as the minimum sufficient form. | *P1 v1.3 · PATENT-OWNED* |
| **Coplanar Redundancy** | — | A regime in which four or more attesting observations all lie on or near a single plane. Beyond the three-point minimum, additional coplanar observations provide outlier detection and residual analysis but do not add depth information. The patent provides for discarding coplanar observations beyond the three required for plane definition. | *P1 v1.3 · PATENT-OWNED* |
| **Mesh Attestation** | — | A regime in which N \> 4 attesting observations form overlapping triangles, each triangle attesting a local plane and adjacent triangles cross-validating one another. Mesh attestation provides distributed attestation that resists compromise of individual observations: removal of any single observation does not invalidate the frame, because adjacent triangles can re-derive the frame from the surviving observations. | *P1 v1.3 · PATENT-OWNED* |
| **Mesh-of-Topography** | — | A representation of a curved global surface (planetary scale) as a mesh of overlapping locally-planar attestations. Each local mesh element approximates the global curvature within an acceptable tolerance for the operational scale. The patent's hierarchical transform attestation primitive composes through mesh-of-topography representations to operate from sensor scale to planetary scale. | *P1 v1.3 · PATENT-OWNED* |
| **Inter-Sensor Transform Matrix** | — | A constellation of pairwise transform attestation records produced jointly by a plurality of N sensors within a field, comprising up to N(N-1)/2 pairwise records. Each pairwise record captures a relative position, an attesting observation modality, and a chain hash. The matrix provides distributed attestation of the field's spatial topology as an emergent property of multiple independent observations. | *P1 v1.3 · PATENT-OWNED* |
| **Genesis Commit** | — | The cryptographic introduction event that registers a sensor device into a positioning mesh. Produces a genesis record per the present invention rooted in a geolocational hash and a geoposition indication, witnessed by the contributing anchor nodes via attestation records, and optionally bound to a building identity primitive. The genesis is the chain origin from which all subsequent records inherit spatial authenticity. | *P1 v1.3 · PATENT-OWNED* |
| **Geolocational Hash** | — | A SHA-256 hash computed over a canonical concatenation comprising the sensor device's initial validated three-dimensional position upon registration into a positioning mesh, the identifiers of the contributing anchor nodes, an identifier of the operational environment, and a registration epoch timestamp. The geolocational hash anchors the genesis record's chain to a specific physical introduction event. | *P1 v1.3 · PATENT-OWNED* |
| **Geoposition Indication** | — | The verifiable record element identifying the initial validated three-dimensional position at registration. Distinct from the geolocational hash: the geoposition indication is the readable position data; the geolocational hash is the cryptographic binding. | *P1 v1.3 · PATENT-OWNED* |
| **Field Record** | — | Any data structure produced according to the present invention within a bounded operational field, including without limitation sensor measurement records, network communication records, decision records, inspection records, software pipeline records, capital movement records, and registration attestation records. The term as used in the patent covers all record types that derive their integrity from the present invention's primitive. | *P1 v1.3 · PATENT-OWNED* |
| **Operational Field** | — | A bounded physical space (jobsite, building, parcel, project, asset, vehicle, region) within which a positioning mesh is deployed and within which records produced according to the present invention are spatially attested. Operational fields may be nested (a building within a parcel within a region) and the spatial hierarchy is captured by the transform attestation between their respective coordinate frames. | *P1 v1.3 · PATENT-OWNED* |

**F. Decision Architecture**

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **EFAS** | Eigenvalue Factor Assessment System | 375-factor → 12-eigenmode decomposition that feeds the state snapshot in the dual-process decision architecture. Captures project health in independent dimensions (progress, critical path, balance, cost trajectory, quality, risk, subsystems). Subject of P4. | *Catalog DRIFT-001 RESOLVED · LOCKED* |
| **SDI** | Solution Density Index | EFAS output measuring project health. Logarithm of viable paths to project success above a quality threshold: SDI \= log₁₀(count of valid paths reaching goal region). Each unit represents a 10× change in solution density. | *EFAS · LOCKED* |
| **Eigenmode** | — | Independent dimension in the reduced-dimensionality projection of project state. Standard naming: λ₁ Progress, λ₂ Critical Path, λ₃ Resource Balance, λ₄ Cost Trajectory, λ₅ Quality Trend, λ₆ Risk Exposure, λ₇₋₁₂ Subsystem. | *EFAS · LOCKED* |
| **Transform** | — | Mathematical representation of a management action as a characteristic effect on each eigenmode. Transforms compose multiplicatively in eigenspace, enabling path analysis without step-by-step simulation. | *EFAS · LOCKED* |
| **Dual-Process** | Dual-process decision architecture | Ectropy decision architecture mirroring human cognitive arbitration. Three core components: Decision Event Schema, Success Stack Compression (Engine 1, fast pattern-match), Possibility Space (Engine 2, deliberate exploration). | *Catalog · LOCKED* |
| **Success Stack** | — | Engine 1 in dual-process. Pattern-matched proven decisions from compressed validated history. Equivalent to System 1 (fast pattern recognition) in human cognition. Patterns decay over time; reinforced by reuse. | *Catalog · LOCKED* |
| **Possibility Space** | — | Engine 2 in dual-process. Full option exploration including untested alternatives. Equivalent to System 2 (deliberate analysis). Returns viable\_options, novel\_options, exploration metadata. | *Catalog · LOCKED* |
| **Exploration Budget** | — | Parameter governing how many decision paths Engine 2 evaluates and how far from known-good patterns to diverge. Function of SDI, urgency, risk profile. | *ectropy-dual-process spec · LOCKED* |
| **USF** | Unified Service Factor | Measurement across normalized standards of a service's value. Used in BPC for fab-component routing across cost/carbon/lead-time/regional alternatives. NOT "Universal Success Framework" — that earlier expansion is deprecated. | *Catalog DRIFT-005 RESOLVED · LOCKED* |
| **Cosmologically-Seeded Decision Entropy** | — | Subject matter of P3. Method wherein the exploration sampling step of a dual-process decision engine consumes entropy derived from astrophysical timing observations (via the Tri-Pulsar Protocol), and the resulting decision record's chain ordering is anchored to the pulsar epoch. | *P3 outline · PATENT-OWNED* |

**G. Atomic Reference Strategy (ARS)**

*Classification of how each DecisionEvent field references upstream truth. Used in software-embodiment claims to characterize data flow.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **ARS** | Atomic Reference Strategy | Classification system for DecisionEvent field provenance. Four classifications: LEAD, DERIVED, EXTERNAL, FLEXIBLE. Used to make claim language precise about which fields originate from the event itself versus upstream. | *Catalog · LOCKED* |
| **LEAD** | — | ARS classification. The event is the originating source of truth for these fields. | *Catalog · LOCKED* |
| **DERIVED** | — | ARS classification. Fields computed from LEAD events. | *Catalog · LOCKED* |
| **EXTERNAL** | — | ARS classification. Fields sourced from outside the event (e.g., upstream system). | *Catalog · LOCKED* |
| **FLEXIBLE** | — | ARS classification. Fields that can be authored or derived depending on context. | *Catalog · LOCKED* |

**H. Authority Cascades**

*There are FOUR distinct authority cascades in active LuhTech docs. They share the word "cascade" but are different scales for different purposes — NOT drift. Patent claims that reference authority routing must be specific about which cascade. Ambiguous reference is a §112 enablement risk.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **Core schema cascade** | — | Universal numeric scale 0–6 on DecisionEvent.authorityLevel. Domain-specific labels are extensible via AuthorityLabelMap. Source: @ectropy/schemas. | *Catalog · LOCKED* |
| **Construction-commercial labels** | — | 0=FIELD, 1=FOREMAN, 2=SUPERINTENDENT, 3=PM, 4=ARCHITECT, 5=OWNER, 6=REGULATORY. Source: @ectropy/construction-commercial-context. | *Catalog · LOCKED* |
| **Agent permission cascade** | — | 0=anonymous, 1=field, 2=project, 3=company, 4=architect, 5=owner, 6=founder. Determines which agents call which endpoints. Source: LUHTECH\_AGENT\_CONTRACTS\_V1. | *Catalog · LOCKED* |
| **EFAS SDI tier cascade** | — | 1–7 scale (different scale entirely). 1=Agent (SEPPÄ), 2=Cluster Consensus, 3=Human Supervisor, 4=PM, 5=Program Director, 6=Executive, 7=Stakeholder Assembly. SDI-threshold-based alert routing. Source: efas-technical-specification §5.2. (This is what was labeled "Seven-Tier Authority Cascade" in prior docs.) | *Catalog · LOCKED* |
| **DLP gate authority** | — | L1=AGENT, L2=SCHEMA, L3=MCP, L4=FOUNDER (Erik). Deliverable Pipeline gate approval levels — different scale and purpose. Source: DLP-STRATEGY-2026-03-14. | *Catalog · LOCKED* |

**I. Ventures**

*Ten ventures: parent \+ nine. Each appears in the Application Embodiments section of the relevant provisionals. Locked spelling and capitalization across all filings.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **LuhTech Holdings** | LTH | Construction technology venture studio. Parent entity. Excluded from SNx feature graph — has no customer-facing product features, only portfolio operations. Future assignee for CTA patent rights. | *Catalog · LOCKED* |
| **Ectropy** | — | Flagship venture and the open-core platform on which all other LuhTech ventures are built. AI construction decision intelligence. Apache 2.0 open source; commercial managed tiers layered on top. | *Catalog · LOCKED* |
| **JobsiteControl** | JSC | Last-mile jobsite connectivity venture. Mesh network and edge computing for sites with poor connectivity. Platform works offline and syncs when connection is available. | *Catalog · LOCKED* |
| **JsCone** | — | JobsiteControl hardware product — last-mile jobsite connectivity device. Js prefix \= JobSite (LuhTech internal abbreviation standard). NOT "JtCone." | *Catalog DRIFT-006 RESOLVED · LOCKED* |
| **Qullqa** | — | Full-stack residential construction execution venture. ADU (Accessory Dwelling Unit) is the beachhead. Extends Ectropy platform to residential markets. | *Catalog · LOCKED* |
| **Viiva** | — | MEP supply chain as a service. Fabrication routing intelligence — routes fabricated components through the supply chain via USF (Unified Service Factor) routing in BPC. | *Catalog · LOCKED* |
| **Raizal** | — | Farmer-owned carbon credit cooperative. Agricultural carbon MRV and credit marketplace. Hemp-soil-forest carbon intervention bundles. | *Catalog · LOCKED* |
| **Pelto** | — | Sub-brand under Raizal. Farming domain; produces carbon-credit-generating outcomes that validate against Raizal MRV. | *Catalog · LOCKED* |
| **Hilja** | — | Intelligent acoustic surfaces venture. Inventor holds USPTO patent US 9,322,165 B2 (Dynamically Adjustable Acoustic Panel Device, System and Method). Active through 2035-07-20. | *Catalog · LOCKED* |
| **Replique** | — | Research protocol intelligence venture. Life sciences focus — validated cell-culture protocols, deviation logs, reagent lot records. DLP sandbox for proving new pipeline patterns. | *Catalog · LOCKED* |
| **Siltana** | — | Pre-formation venture for building operations ("silta" \= Finnish for bridge). Extends Ectropy from construction completion into building operations lifecycle. Owns SSB hardware and Robot Registry. | *Catalog · LOCKED* |
| **Ohjaus** | — | Pre-formation venture — open sensor infrastructure. Domain ohjaus.ai is primary. The Ohjaus sensor module (formerly "Viitata") is the reference embedded platform for ProvenanceField generation. | *Catalog \+ Erik 2026-05-04 · LOCKED* |

**J. Service Network Exchange (SNx)**

*Architectural pattern: nine domain-specific Service Exchanges that compose into a unified network for construction operations. Each provisional's Application Embodiments section may reference one or more Service Exchanges — claim language must use the canonical short or long form. Replaces retired XaaS taxonomy.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **SNx** | Service Network Exchange | Umbrella term for the architectural pattern. Names the network; each member names a domain. Informal set reference: "the Nine." | *NAMING-SVCEXCHANGE-2026-05-04 · LOCKED* |
| **GovSx (GSx)** | Governance Service Exchange | Tier: Governance. Contract intelligence — parses contract PDFs (AIA, CCDC, ConsensusDOCS) into authority cascade, payment terms, dispute resolution, lien tracking. | *NAMING-SVCEXCHANGE · LOCKED* |
| **CorSx (CSx)** | Coordination Service Exchange | Tier: Governance. Takt timing, scheduling, zone/wagon flow, resource allocation, handoffs. | *NAMING-SVCEXCHANGE · LOCKED* |
| **PaySx (PSx)** | Payment Service Exchange | Tier: Governance. SOV → billing → retainage → disbursement. Voxel-completion-triggered payments via Stripe Connect. Direct application embodiment of P1 (ProvenanceField triggering automated capital movement). | *NAMING-SVCEXCHANGE · LOCKED* |
| **HumSx (HSx)** | Human Service Exchange | Tier: Smart Resources. Workers, operators, crew marketplace. Voxel-anchored worker tracking with hourly/wagon/voxel billing. | *NAMING-SVCEXCHANGE · LOCKED* |
| **RobSx (RSx)** | Robot Service Exchange | Tier: Smart Resources. Drones, Spot, AMRs, layout bots, autonomous equipment. Per-scan or per-mission billing. Direct application embodiment of P5 (Multi-Vendor Robot Registry). | *NAMING-SVCEXCHANGE · LOCKED* |
| **AgtSx (ASx)** | Agent Service Exchange | Tier: Smart Resources. SEPPÄ AI, decision routing, protocol intelligence, cross-project analytics. Per-token or per-task billing. Application embodiment surface for P3 (Cosmological Decision Entropy) and P4 (EFAS). | *NAMING-SVCEXCHANGE · LOCKED* |
| **EqpSx (ESx)** | Equipment Service Exchange | Tier: Dumb Resources. Cranes, lifts, tools, telematics, fabrication equipment. Verification via telematics \+ checkout. | *NAMING-SVCEXCHANGE · LOCKED* |
| **MatSx (MSx)** | Material Service Exchange | Tier: Dumb Resources. Concrete, steel, lumber, MEP supply chain. Verification via BOX (BIM+BOM+VOX). Application embodiment of P1 (ProvenanceField on supply chain custody). | *NAMING-SVCEXCHANGE · LOCKED* |
| **InsSx (ISx)** | Inspection Service Exchange | Tier: Dumb Resources. QC, code compliance, safety audits, MRV. Verification via pass/fail \+ evidence. Application embodiment of P1 retention-tied claims and Raizal MRV. | *NAMING-SVCEXCHANGE · LOCKED* |

**K. Platform Architecture**

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **CIS** | Construction Intelligence Service | Portfolio-shared intelligence layer callable by any agent in any venture via the CIS MCP. Domain-neutral construction intelligence (materials, cost, labor, carbon, compliance, permit, weather, voxel). Singular per canonical doc. | *Catalog DRIFT-003 RESOLVED · LOCKED* |
| **CIS MCP** | — | Tier 2 MCP server for portfolio-shared construction intelligence. Express server, Tier 2 of three-tier architecture. | *Catalog · LOCKED* |
| **SEPPÄ** | — | Ectropy AI agent. Primary interface for decision event generation in the dual-process architecture. 24+ MCP tools. Integrates with Claude API \+ SMS/Voice channels. Finnish word; not an acronym; no expansion. ASCII fallback "SEPPA" only where ä cannot render. | *Catalog DRIFT-002 RESOLVED · LOCKED* |
| **SEPPÄ MCP** | — | Tier 2 MCP server for Ectropy/SEPPÄ-specific tools. Operates on Ectropy-private schemas. | *Catalog · LOCKED* |
| **MCP** | Model Context Protocol | Open protocol (Anthropic) for connecting AI agents to tools and data sources. Servers expose tools via stdio or SSE transport. | *Anthropic · LOCKED* |
| **Three-tier architecture** | — | CIS architecture pattern: Tier 3 agents → Tier 2 MCP servers (thin HTTP proxies) → Tier 1 FastAPI services (business logic). | *Catalog · LOCKED* |
| **@ectropy/schemas** | — | npm package. Universal decision-log base schemas. Domain-neutral. Defines DecisionEvent, SdiSnapshot, SuccessPattern, Evidence, AuthorityLabelMap, GraphMetadata. Discriminator "domain" field enables extension. | *Catalog · LOCKED* |
| **@ectropy/construction-commercial-context** | — | First domain context package extending @ectropy/schemas. Adds CONSTRUCTION\_COMMERCIAL\_DOMAIN, authority labels, and construction-specific event subtypes. | *Catalog · LOCKED* |
| **DLP** | Deliverable Pipeline | MCP-supervised, schema-validated, industry-portable execution pattern. Seven-stage lifecycle (S1–S7) with hard gates. Operational across LuhTech ventures with 212+ tests passing on the ProvenanceField contract. | *DLP-STRATEGY-2026-03-14 · LOCKED* |
| **BPC** | Building Product Catalog | LuhTech material intelligence graph. \~120 fields across 13 tables. The assembly is the hub; products, performance, cost, carbon, labor, and standards radiate from it. CIS service. | *Catalog · LOCKED* |
| **Assembly (BPC)** | — | BPC hub entity. A tested, performance-rated composition of products in ordered zones and layers. Examples: GA-WP-3, ACT-24, FLR-PCT. | *Catalog · LOCKED* |
| **A2A** | Agent-to-Agent protocol | Open agent-interop standard. LuhTechAgentCard extends A2A v0.3 with venture/data scope, authority level, and surface fields. | *Catalog · LOCKED* |
| **URN** | Uniform Resource Name | Identifier format for LuhTech entities. Pattern: urn:luhtech:{scope}:{type}:{id}. Examples: urn:luhtech:agent:ventures, urn:luhtech:ectropy:voxel-grid:GRID-XXX. | *Catalog · LOCKED* |
| **Robot Registry** | — | Subject matter of P5. Building-wide multi-vendor robot fleet system normalized via VDA 5050, positioned via UWB anchor grid, navigated via BIM-derived maps, authorized via voxel zone records, coordinated via building edge server during internet absence. Surfaces as RobSx. | *P5 (planned) · PATENT-OWNED* |
| **VDA 5050** | — | German Automotive Industry Association standard for AGV/AMR interoperability. MQTT-based message protocol. Foundation for Robot Registry multi-vendor normalization. | *VDMA · LOCKED* |
| **URO** | Universal Resource Orchestration | ROS 2 extension for construction — coordinated tracking, allocation, and billing of all jobsite resources (HumSx, RobSx, AgtSx, EqpSx, MatSx, InsSx) as nodes in a unified computational graph. | *Catalog · LOCKED* |
| **ROS 2** | Robot Operating System 2 | Open-source middleware for robotics. URO uses ROS 2 topics for high/medium/low-frequency data streams across all resource categories. | *Catalog · LOCKED* |

**L. Industry Standards Bodies and Specifications**

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **buildingSMART** | buildingSMART International | Industry body publishing IFC and operating bSDD (buildingSMART Data Dictionary). | *Catalog · LOCKED* |
| **IFC** | Industry Foundation Classes | BIM data exchange standard. ISO 16739\. Authored format for BIM files used in BOX architecture. | *ISO 16739 · LOCKED* |
| **CSI** | Construction Specifications Institute | Standards body publishing MasterFormat (spec section numbers) and co-publishing OmniClass and UniFormat. | *Catalog · LOCKED* |
| **AIA** | American Institute of Architects | Publishes the AIA contract forms (A101, A105, A133, A201, C191, etc.) — the dominant US contract template family. Parsed by GovSx. | *Catalog · LOCKED* |
| **CCDC** | Canadian Construction Documents Committee | Canadian standards body publishing CCDC contract forms — the Canadian parallel to AIA. Critical for Canadian pilot. | *Catalog · LOCKED* |
| **ICC** | International Code Council | Publishes the IBC (International Building Code) and other model codes adopted across US jurisdictions. | *Catalog · LOCKED* |
| **ASTM** | ASTM International | Standards body publishing test method standards (E119 fire, E90 sound transmission, C423 sound absorption, and many others). | *Catalog · LOCKED* |
| **ANSI** | American National Standards Institute | Standards body publishing A118.4, A118.6, and other standards referenced in BPC. | *Catalog · LOCKED* |
| **UL** | Underwriters Laboratories | Testing/certification body. Publishes the Fire Resistance Directory and Product iQ database. | *Catalog · LOCKED* |
| **MRV** | Measurement, Reporting, Verification | Carbon-markets standard process. Raizal MRV submits Verra audit records. | *Verra · LOCKED* |
| **Verra** | — | Largest voluntary carbon-market standards body. Operates VCS (Verified Carbon Standard). | *Catalog · LOCKED* |
| **ISO** | International Organization for Standardization | International standards body. Various referenced standards across LuhTech docs. | *Catalog · LOCKED* |
| **IEEE 802.15.4z** | — | UWB radio standard. Defines the physical layer for the DWM3000 module and equivalent UWB hardware used in the Ohjaus sensor module. | *IEEE · LOCKED* |
| **NIST FIPS 180-4** | — | Federal Information Processing Standard for SHA-256. Underlies chain\_hash construction. | *NIST · LOCKED* |
| **NIST FIPS 202** | — | Federal Information Processing Standard for SHA-3 / SHAKE-256. Underlies Tri-Pulsar Protocol KDF. | *NIST · LOCKED* |

**M. Patent Law Shorthand**

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **§101** | — | 35 U.S.C. § 101 — patent-eligible subject matter. Alice/Mayo abstract-idea inquiry. P1, P3, P4 require careful framing to avoid §101 rejection. | *MPEP § 2106 · LOCKED* |
| **§102(b)(1)(A)** | — | Inventor exception under AIA. Disclosures by the inventor within one year before filing do not bar patentability. Anchor publications for SBPA portfolio: @ectropy/schemas v0.3.0 (2026-04-23) and v0.4.0 (2026-04-24); bar dates 2027-04-23 and 2027-04-24 respectively. | *35 U.S.C. § 102 · LOCKED* |
| **§112** | — | 35 U.S.C. § 112 — written description, enablement, definiteness. The Build Manifest's source-tracing supports §112 enablement. | *MPEP § 2161 · LOCKED* |
| **MPEP** | Manual of Patent Examining Procedure | USPTO's procedural manual. Cite by section number. | *USPTO · LOCKED* |
| **PCT** | Patent Cooperation Treaty | International filing route. Decision point at non-provisional conversion: file PCT or direct national. | *WIPO · LOCKED* |
| **PTO/SB/16** | — | USPTO cover sheet for provisional patent application. Filed with every CTA provisional. | *USPTO · LOCKED* |
| **PTO/SB/15A** | — | USPTO micro-entity certification form. Filed once with first provisional (P1). | *USPTO · LOCKED* |
| **Customer Number** | — | 199224\. See section A. | *USPTO 2024-04-17 · LOCKED* |
| **Micro-entity** | — | USPTO fee tier. Applicant qualifies if income below threshold (\~$225K) AND fewer than four prior applications. Erik qualifies as of 2026 (no revenue, first filings). | *37 CFR 1.29 · LOCKED* |
| **Applicant** | — | Party filing the application. For CTA provisionals: Erik J. Luhtala (sole inventor, filing in own name). Distinct from "assignee" — assignment to LuhTech Holdings is post-filing. | *Erik 2026-05-04 · LOCKED* |

**N. Standard Drafting Phrases (Procopio Style)**

Recurring phrases used identically across all five provisionals to maintain consistency at non-provisional conversion.

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **"comprising"** | — | Open-ended transition phrase in independent claims. Allows additional unrecited elements. Default for independent claims. Use "consisting of" only when narrow closed-set is intended. | *MPEP § 2111.03 · LOCKED* |
| **"wherein"** | — | Phrase introducing a limiting condition that captures the inventive step. The wherein clause is where the structural-input-not-metadata distinction lives in P1 claim 1\. | *LOCKED* |
| **"according to one aspect"** | — | Procopio summary-section convention. Lead each independent-claim variant in the SUMMARY with "According to one aspect..." / "According to another aspect...". | *Hilja patent · LOCKED* |
| **"by way of example only, and not limitation"** | — | Boilerplate phrase appearing early in DETAILED DESCRIPTION. Procopio standard phrasing. | *Hilja patent · LOCKED* |
| **"those of skill will appreciate"** | — | Boilerplate phrase introducing the hardware/software interchangeability paragraph late in DETAILED DESCRIPTION. Procopio standard phrasing. | *Hilja patent · LOCKED* |

**O. Prohibited and Deprecated Terms**

*Terms appearing in older docs that must NOT appear in any provisional. The supersession is locked.*

| Term | Expansion | Definition | Source / Status |
| :---- | :---- | :---- | :---- |
| **Viitata** | — | DEPRECATED. The sensor module formerly named Viitata is now "Ohjaus sensor module." The viitata.\* domains are historical aliases. Erik 2026-05-04 locked migration across all areas including patents. | *DEPRECATED — use Ohjaus* |
| **"Ectropy Forecasting and Alert System"** | — | DEPRECATED expansion of EFAS. Use "Eigenvalue Factor Assessment System." | *DEPRECATED* |
| **"Ectropy Factor Analysis System"** | — | DEPRECATED expansion of EFAS (this was a transitional name). Use "Eigenvalue Factor Assessment System." | *DEPRECATED — superseded by Catalog DRIFT-001* |
| **"Universal Success Framework"** | — | DEPRECATED expansion of USF appearing in dual-process spec. The canonical USF is "Unified Service Factor." If patent text needs to reference the success-pattern framework, use "Success Stack" or "dual-process Engine 1" instead. | *DEPRECATED — superseded by Catalog DRIFT-005* |
| **XaaS** | — | DEPRECATED. Anything-as-a-Service umbrella retired 2026-05-04 due to structural collision with cloud-services taxonomy. Use SNx (Service Network Exchange). | *DEPRECATED* |
| **"FGP" / "Feature Generation Pipeline"** | — | DEPRECATED. Superseded by DLP (Deliverable Pipeline). The category-error "feature" rename was a structural unlock. | *DEPRECATED* |
| **JtCone** | — | DEPRECATED spelling. Canonical is "JsCone" (Js \= JobSite). | *DEPRECATED* |
| **"Seven-Tier Authority Cascade"** | — | DEPRECATED as a standalone term. Refer instead to the specific cascade — "EFAS SDI tier cascade (1–7)" if that is what is meant. See section H. | *DEPRECATED — disambiguate* |
| **OpenTimestamps** | — | Not used. CTA portfolio operates under AIA first-to-file framework; no OpenTimestamps anchoring. | *PROHIBITED* |
| **"three part wrapped container"** | — | Conversational origin term for ProvenanceField. Do NOT use in patent text. Use "ProvenanceField data structure" or "ProvenanceField record." | *DEPRECATED* |
| **"blockchain"** | — | Avoid as primary characterization. The chain integrity primitive is RVGT (an append-only hash chain), not a public blockchain. "Hash-chained" or "append-only chain" preferred. | *DRAFTING DISCIPLINE* |

