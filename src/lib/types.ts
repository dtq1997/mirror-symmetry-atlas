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
  google_scholar?: string;
  mathscinet?: string;
  arxiv_author?: string;
}

export interface SourceRef {
  label: string;
  url: string;
}

export interface Publication {
  id: string; // arXiv ID e.g. "2511.10082"
  title: string;
  year: number;
  coauthors: string[]; // person slugs
  doi?: string;
  journal?: string;
}

export interface Person {
  slug: string;
  name: MultiLangName;
  born?: number;
  died?: number | null;
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
  name: MultiLangName;
  aliases?: string[];
  category: ConceptCategory;
  difficulty: Difficulty;
  discipline: Discipline;
  year_introduced?: number;
  introduced_by: string[];
  definition?: string;
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
  | "friendship"
  | "institutional"
  | "co-student"
  | "grant";

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

export interface Institution {
  slug: string;
  name: MultiLangName;
  type: "university" | "research-institute" | "center";
  country: string;
  city: string;
  location?: { lat: number; lng: number };
  founded?: number;
  url?: string;
  relevance: "high" | "medium" | "low";
  research_groups: ResearchGroup[];
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
  status: "open" | "partially-solved" | "solved" | "abandoned";
  importance: "millennium" | "major" | "significant" | "niche";
  year_proposed?: number;
  proposed_by: string[];
  description?: string;
  prerequisites: string[];
  related_problems: string[];
  key_people: string[];
  progress: ProblemProgress[];
  current_approaches?: string[];
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
  type: ConnectionType;
  weight: number;
  color: string;
  dash?: number[];
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
