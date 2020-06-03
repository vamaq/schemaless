<template>
  <div>
    <types-table @show-definitions="showDefinitions"/>
    <div v-if="definitionType.eid">
      <definitions-table :definition-type="definitionType"/>
    </div>
  </div>
</template>

<script>
import TypesTable from '../components/TypesTable.vue'
import DefinitionsTable from '../components/DefinitionsTable';

export default {
  name: "schema-definition",
  components: {
    TypesTable,
    DefinitionsTable,
  },
  data() {
    return {
      definitionType: {
        eid: "",
        type: ""
      },      
    };
  },
  methods: {
    showDefinitions(definitionType) {
      this.definitionType = definitionType;
    },    
  }
};
</script>

<style lang="scss" scoped>

</style>
