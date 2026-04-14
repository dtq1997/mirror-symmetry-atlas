import { getAllPeople, getAllConnections, getAllKnownSlugs } from "@/lib/data";
import { buildPeopleGraph } from "@/lib/graph";
import PeopleNetworkClient from "./PeopleNetworkClient";

export default function PeoplePage() {
  const people = getAllPeople();
  const connections = getAllConnections();
  const knownSlugs = getAllKnownSlugs();
  const graphData = buildPeopleGraph(people, connections, knownSlugs);

  return (
    <div className="flex-1 flex flex-col">
      <PeopleNetworkClient graphData={graphData} people={people} />
    </div>
  );
}
