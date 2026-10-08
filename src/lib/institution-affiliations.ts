import type { AppointmentCheck, CareerEntry, Institution, Person } from "./types";

export interface RecordedAffiliation {
  person: string;
  career: CareerEntry[];
  groupClaims: Array<{ group: string; recordedAs: "current" | "past" }>;
  appointmentChecks: AppointmentCheck[];
}

/** Exact institution/person references only. A last row, "present", a visit,
 * or an undated group list never establishes a current appointment. */
export function recordedAffiliations(institution: Institution, people: Person[]): RecordedAffiliation[] {
  const records = new Map<string, RecordedAffiliation>();
  const entry = (person: string) => {
    let record = records.get(person);
    if (!record) {
      record = { person, career: [], groupClaims: [], appointmentChecks: [] };
      records.set(person, record);
    }
    return record;
  };
  for (const person of people) {
    const career = (person.career_timeline ?? []).filter((e) =>
      e.institution === institution.slug && ["education", "position", "visit"].includes(e.type));
    if (career.length) entry(person.slug).career = career.map((e) => ({ ...e }));
  }
  for (const group of institution.research_groups ?? []) {
    for (const [recordedAs, members] of [
      ["current", group.current_members], ["past", group.past_members],
    ] as const) {
      for (const person of new Set(members ?? [])) {
        entry(person).groupClaims.push({ group: group.name, recordedAs });
      }
    }
  }
  for (const check of institution.appointment_checks ?? []) {
    entry(check.person).appointmentChecks.push({ ...check, source: { ...check.source } });
  }
  return [...records.values()].sort((a, b) => a.person.localeCompare(b.person));
}
