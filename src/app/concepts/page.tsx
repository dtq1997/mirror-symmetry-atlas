import { getAllConcepts } from "@/lib/data";
import { buildConceptGraph } from "@/lib/graph";
import ConceptPageClient from "./ConceptPageClient";

export default function ConceptsPage() {
  const concepts = getAllConcepts();
  const graphData = buildConceptGraph(concepts);

  return (
    <div className="flex-1 flex flex-col">
      <ConceptPageClient graphData={graphData} concepts={concepts} />
    </div>
  );
}
