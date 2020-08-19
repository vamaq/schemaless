<template>
  <div>
    <types-table @show-definitions="showDefinitions" @show-nodes="showNodesByType"/>
    <div v-if="definitionType.eid">
      <definitions-table :definition-type="definitionType" @show-nodes="showNodesByDefinition"/>
    </div>
    <div v-if="nodeEid || nodeTypeEid || nodeDefinitionEid">
      <nodes-relations-table
        :node-eid="nodeEid"
        :type-eid="nodeTypeEid"
        :definition-eid="nodeDefinitionEid"
        @show-node="showNode"
      />
    </div>
  </div>
</template>

<script>
import TypesTable from '../components/TypesTable.vue'
import DefinitionsTable from '../components/DefinitionsTable';
import NodesRelationsTable from '../components/NodesRelationsTable';

export default {
  name: "schema-definition",
  components: {
    TypesTable,
    DefinitionsTable,
    NodesRelationsTable,
  },
  data() {
    return {
      definitionType: {
        eid: "",
        type: "",
      },
      nodeEid: "",
      nodeTypeEid: "",
      nodeDefinitionEid: "",
    };
  },
  methods: {
    showDefinitions(definitionType) {
      this.definitionType = definitionType;
    },
    showNode(nodeEid, typeEid) {
      this.nodeEid = nodeEid;
      this.nodeTypeEid = typeEid;
      this.nodeDefinitionEid = "";
    },
    showNodesByType(typeEid) {
      this.nodeEid = "";
      this.nodeDefinitionEid = "";
      this.nodeTypeEid = typeEid;
    },
    showNodesByDefinition(definitionEid, typeEid) {
      this.nodeEid = "";
      this.nodeTypeEid = typeEid;
      this.nodeDefinitionEid = definitionEid;
    },    
  }
};
</script>

<style lang="scss" scoped>

</style>
