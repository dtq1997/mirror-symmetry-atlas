import { getAllPeople, getAllConnections } from "@/lib/data";
import { buildAckGraph } from "@/lib/graph";
import AckNetworkClient from "./AckNetworkClient";

export default function AcknowledgementsPage() {
  const people = getAllPeople();
  const connections = getAllConnections();
  const graphData = buildAckGraph(people, connections);

  return (
    <div className="flex-1 flex flex-col">
      <AckNetworkClient graphData={graphData} peopleCount={people.length} />
    </div>
  );
}
