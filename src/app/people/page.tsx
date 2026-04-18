import {
  getAllPeople,
  getAllConnections,
  getAllKnownSlugs,
  getAllInstitutions,
} from "@/lib/data";
import { buildPeopleGraph } from "@/lib/graph";
import PeopleNetworkClient from "./PeopleNetworkClient";

export default function PeoplePage() {
  const people = getAllPeople();
  const connections = getAllConnections();
  const knownSlugs = getAllKnownSlugs();
  const institutions = getAllInstitutions();
  const graphData = buildPeopleGraph(people, connections, knownSlugs);

  const institutionNames: Record<string, string> = {};
  for (const inst of institutions) {
    institutionNames[inst.slug] = inst.name.zh || inst.name.en;
  }

  return (
    <div className="flex-1 flex flex-col">
      <PeopleNetworkClient
        graphData={graphData}
        people={people}
        institutionNames={institutionNames}
      />
    </div>
  );
}
