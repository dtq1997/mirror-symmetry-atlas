// ===== Shared Types =====

export interface MultiLangName {
  en: string;
  zh?: string;
  local?: string;
}

// ===== Person =====

export type CareerType = "education" | "position" | "visit" | "award" | "event";

export interface CareerEntry {
  period: string;
  type: CareerType;
  institution?: string;
  role?: string;
  advisor?: string;
  title?: string;
  notes?: string;
}

export interface Collaborator {
  person: string;
  since?: number;
  met_context?: string;
  topic?: string;
  papers_count?: number;
}

export interface Activity {
  total_papers?: number;
  t1_papers?: number;
  t2_papers?: number;
  t3_papers?: number;
  t4_papers?: number;
  /** Legacy key: records with publication clues; not verified publication status. */
  published_count?: number;
  /** Legacy key: records lacking publication clues; not necessarily unpublished. */
  preprint_only_count?: number;
  h_index?: number;
  mathscinet_citations?: number;
  google_scholar_citations?: number;
  active_period?: string;
  peak_period?: string;
  phd_students?: number;
  academic_descendants?: number;
  last_arxiv_paper?: string;
}

export interface ExternalIds {
  orcid?: string;
  openalex?: string;
  mathgenealogy?: string;
  zbmath?: string;
  inspire?: string;
}

export interface PersonLinks {
  homepage?: string;
  faculty_page?: string;
  cv?: string;
  google_scholar?: string;
  mathscinet?: string;
  arxiv_author?: string;
  zbmath?: string;
  researchgate?: string;
  github?: string;
  youtube?: string;
  email?: string;
}

export interface SourceRef {
  label: string;
  url: string;
  notes?: string;
  last_verified?: string;
}

export type DatePrecision = "year" | "month" | "day" | "circa" | "unknown";

export interface LifeDateFact {
  /** ISO-like date string when known: YYYY, YYYY-MM, or YYYY-MM-DD. */
  date?: string;
  precision?: DatePrecision;
  place?: string;
  notes?: string;
  sources?: SourceRef[];
}

export type OnlineTraceType =
  | "homepage"
  | "faculty"
  | "cv"
  | "google_scholar"
  | "orcid"
  | "mathgenealogy"
  | "zbmath"
  | "mathscinet"
  | "arxiv"
  | "openalex"
  | "video"
  | "interview"
  | "lecture_notes"
  | "slides"
  | "news"
  | "blog"
  | "github"
  | "wayback"
  | "other";

export interface OnlineTrace {
  type: OnlineTraceType;
  label?: string;
  url: string;
  archived_url?: string;
  last_verified?: string;
  notes?: string;
}

export interface Publication {
  /** Primary identifier. Prefer arXiv ID; if no arXiv preprint exists, use
   *  the DOI as the id (prefixed with "doi:"), or an OpenAlex work id. */
  id: string;
  title: string;
  year: number;
  coauthors: string[]; // person slugs (or raw names if not yet stubbed)
  doi?: string;
  journal?: string;
  /** arXiv primary category (math.AG, math-ph, hep-th, ...) when available */
  primary_category?: string;
  /** Which data source(s) reported this paper. Helps users see provenance. */
  sources?: ("arxiv" | "openalex" | "crossref" | "manual")[];
  /** OpenAlex work id (e.g. "W2964093293") when known */
  openalex_id?: string;
  /** True if this paper exists in our records but never appeared on arXiv. */
  no_arxiv?: boolean;
}

export interface Person {
  slug: string;
  name: MultiLangName;
  /** Legacy coarse field; prefer `birth` for new precise/sourceable data. */
  born?: number | string | null;
  /** Legacy coarse field; prefer `death` for new precise/sourceable data. */
  died?: number | string | null;
  birth?: LifeDateFact;
  death?: LifeDateFact;
  nationality?: string;
  gender?: string;
  photo_url?: string | null;
  career_timeline: CareerEntry[];
  research_areas: string[];
  advisor?: string;
  students: string[];
  key_collaborators: Collaborator[];
  activity: Activity;
  external_ids: ExternalIds;
  links: PersonLinks;
  online_traces?: OnlineTrace[];
  known_emails?: string[];
  known_affiliations?: string[];
  publications?: Publication[];
  personal_notes?: string;
  sources?: SourceRef[];
  tags: string[];
}

// ===== Concept =====

export type ConceptCategory =
  | "algebraic-structure"
  | "geometric-structure"
  | "equation"
  | "conjecture"
  | "technique";
export type Difficulty =
  | "introductory"
  | "intermediate"
  | "advanced"
  | "research-frontier";
export type Discipline = "math" | "physics" | "both";

export interface ConceptContribution {
  person: string;
  role: "founder" | "major" | "promoter" | "applier";
  description?: string;
}

export interface Concept {
  slug: string;
  /** Explicit alias entry; never inferred from similar names. */
  alias_of?: string;
  name: MultiLangName;
  aliases?: string[];
  category: ConceptCategory;
  difficulty: Difficulty;
  discipline: Discipline;
  year_introduced?: number;
  introduced_by: string[];
  definition?: string;
  history_note?: string;
  review_note?: string;
  sources?: SourceRef[];
  dual_to?: string | null;
  notation_variants?: string | null;
  prerequisites: string[];
  leads_to: string[];
  related: string[];
  key_people: string[];
  key_papers: string[];
  contributions?: ConceptContribution[];
}

// ===== Paper =====

export type PaperType =
  | "published"
  | "preprint"
  | "lecture_notes"
  | "unpublished_manuscript";
export type Importance = "seminal" | "major" | "notable" | "regular";

export interface SemanticRelation {
  target: string;
  type: "cites" | "generalizes" | "corrects" | "alternative-proof" | "surveys";
  description?: string;
}

export interface Paper {
  arxiv_id?: string;
  doi?: string;
  title: string;
  authors: string[];
  authors_raw: string[];
  year: number;
  journal?: string;
  type: PaperType;
  discipline?: Discipline;
  categories?: string[];
  primary_category?: string;
  concepts?: string[];
  importance?: Importance;
  citations_count?: number;
  cited_by?: string[];
  semantic_relations?: SemanticRelation[];
  notes?: string;
  abstract?: string;
  relevance_score?: number;
  matched_people?: string[];
  matched_concepts?: string[];
  reviewed?: boolean;
  source?: "manual" | "openalex" | "semantic-scholar" | "arxiv-fetch";
  source_url?: string;
  last_verified?: string;
}

// ===== Timeline =====

export type Era = "prehistory" | "classical" | "modern" | "contemporary";
export type EventImportance = "milestone" | "major" | "notable";

export interface TimelineEvent {
  slug: string;
  date: string;
  precision: "year" | "month" | "day";
  title: MultiLangName;
  description?: string;
  people: string[];
  concepts: string[];
  papers: string[];
  era: Era;
  importance: EventImportance;
  /** What the date refers to: lecture, first submission, publication or announcement. */
  date_note?: string;
  review_note?: string;
  reviewed_on?: string;
  sources?: SourceRef[];
}

// ===== Conference =====

export interface ConferenceSeries {
  slug: string;
  name: MultiLangName;
  organizers: string[];
  institution?: string;
  frequency: "annual" | "biennial" | "irregular";
  typical_month?: number;
  location?: string;
  url?: string;
  relevance: "high" | "medium" | "low";
  region: "china" | "asia" | "europe" | "americas" | "global";
  topics: string[];
  notes?: string;
}

export interface ConferenceEvent {
  slug: string;
  series?: string;
  name: MultiLangName;
  date_start: string;
  date_end?: string;
  location?: string;
  institution?: string;
  organizers: string[];
  invited_speakers: string[];
  attendees?: string[];
  topics: string[];
  url?: string;
  source?: string;
  notes?: string;
}

// ===== Connection =====

export type ConnectionType =
  | "advisor-student"
  | "postdoc-mentor"
  | "postdoc-group"
  | "coauthor"
  | "institutional"
  | "co-student"
  | "grant"
  | "acknowledgement";

export interface Connection {
  source: string;
  target: string;
  type: ConnectionType;
  year?: number;
  weight?: number;
  period?: string;
  institution?: string;
  notes?: string;
  derived?: boolean;
  papers?: string[];  // for acknowledgement edges: list of arxiv ids
  review_status?: "accepted"; // acknowledgement identity and subject reviewed per paper
  /** Legacy bucket names: with/without publication clues, not publication verdicts. */
  coauthored_papers?: {
    published: { id: string; title: string; year: number; doi?: string; journal?: string }[];
    preprint: { id: string; title: string; year: number; primary_category?: string }[];
  };
}

// Single-ack: shown in detail sidebar rather than network
export interface AckMention {
  source: string;  // the person who acknowledged
  target: string;  // the person being acknowledged
  papers: string[];
}

// ===== Institution =====

export interface ResearchGroup {
  name: string;
  topics: string[];
  current_members: string[];
  past_members: string[];
}

export interface InstitutionEvent {
  year: number;
  description: string;
}

/** A dated reading of an identified person's appointment in a primary source.
 * Does not certify continued employment after the observation date. */
export interface AppointmentCheck {
  person: string;
  role: string;
  checked_on: string;
  source: SourceRef;
}

export interface Institution {
  slug: string;
  alias_of?: string;
  name: MultiLangName;
  type: "university" | "research-institute" | "center";
  country: string;
  city: string;
  location?: { lat: number; lng: number };
  founded?: number;
  url?: string;
  relevance: "high" | "medium" | "low";
  research_groups: ResearchGroup[];
  appointment_checks?: AppointmentCheck[];
  sources?: SourceRef[];
  events?: InstitutionEvent[];
  notes?: string;
}

// ===== Open Problem =====

export interface ProblemProgress {
  date: string;
  description: string;
  papers: string[];
}

export interface OpenProblem {
  slug: string;
  name: MultiLangName;
  status: "open" | "partially-solved" | "solved" | "abandoned" | "needs-review";
  importance: "millennium" | "major" | "significant" | "niche";
  year_proposed?: number;
  proposed_by: string[];
  description?: string;
  prerequisites: string[];
  related_problems: string[];
  key_people: string[];
  progress: ProblemProgress[];
  current_approaches?: string[];
  status_note?: string;
  reviewed_on?: string;
  review_note?: string;
  sources?: SourceRef[];
  notes?: string;
}

// ===== Seminar =====

export interface Seminar {
  slug: string;
  name: MultiLangName;
  institution: string;
  organizers: string[];
  frequency: "weekly" | "biweekly" | "monthly" | "irregular";
  typical_day?: string;
  typical_time?: string;
  location?: string;
  url?: string;
  topics: string[];
  active: boolean;
  notes?: string;
}

// ===== Graph =====

export type EntityType = "person" | "concept" | "paper" | "institution";
export type ConceptRelationType = "prerequisite" | "leads-to" | "related";

export interface GraphNode {
  id: string;
  label: string;
  type: EntityType;
  radius: number;
  color: string;
  opacity: number;
  isGhost: boolean;
  data?: Person | Concept | Paper | Institution;
  x?: number;
  y?: number;
  fx?: number;
  fy?: number;
}

export interface GraphLink {
  source: string;
  target: string;
  type: ConnectionType | ConceptRelationType;
  weight: number;
  color: string;
  dash?: number[];
  curve?: number;
  opacity: number;
  label?: string;
  data?: Connection;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
}

// ===== Data Store (all loaded data) =====

export interface DataStore {
  people: Map<string, Person>;
  concepts: Map<string, Concept>;
  papers: Paper[];
  timeline: TimelineEvent[];
  conferences: { series: ConferenceSeries[]; events: ConferenceEvent[] };
  connections: Connection[];
  institutions: Map<string, Institution>;
  problems: Map<string, OpenProblem>;
  seminars: Seminar[];
}
