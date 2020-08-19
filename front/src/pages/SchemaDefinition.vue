<template>
  <div>
    <types-table @show-definitions="showDefinitions" @show-nodes="showNodesByType"/>
    <div v-if="definitionType.eid">
      <definitions-table :definition-type="definitionType" @show-nodes="showNodesByDefinition"/>
    </div>
    <div v-if="nodeTypeEid || nodeDefinitionEid">
      <nodes-relations-table :type-eid="nodeTypeEid" :definition-eid="nodeDefinitionEid"/>
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
      nodeTypeEid: "",
      nodeDefinitionEid: "",
    };
  },
  methods: {
    showDefinitions(definitionType) {
      this.definitionType = definitionType;
    },
    showNodesByType(typeEid) {
      this.nodeDefinitionEid = "";
      this.nodeTypeEid = typeEid;
    },
    showNodesByDefinition(definitionEid, typeEid) {
      this.nodeTypeEid = typeEid;
      this.nodeDefinitionEid = definitionEid;
    },    
  }
};
</script>

<style lang="scss" scoped>

</style>
