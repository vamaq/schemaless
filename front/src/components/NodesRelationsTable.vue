<template>
  <div>
    <div class="nodes">
      <div class="title">
        <p>Nodes</p>
        <div>
          <b-button size="sm" variant="success">Create</b-button>
        </div>
      </div>
      <b-table
        head-variant="dark"
        small
        hover
        primary-key="eid"
        :busy="loadingTable"
        :items="nodeList"
        :fields="nodeFields"
      >
        <template v-slot:table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>

        <template v-slot:cell(controls)="data">
          <div class="controls">
            <b-button size="sm" variant="danger" @click="remove(data.item.eid)">Delete</b-button>
            <b-button size="sm" variant="secondary" @click="loadModal(data.item.eid)">Edit</b-button>
          </div>
        </template>

        <template v-slot:row-details="data">
          <div v-for="(relation, index) in data.item.__relates_to" :key="index" class="relations">
            <div class=label>
              {{relation.label}}
            </div>
            <div class=properties>
              <div v-for="(value, key) in relation.properties" :key="key">
                {{`${key} - ${value}`}}
              </div>
            </div>            
          </div>
        </template>

      </b-table>
      <b-modal id="node-modal">
        <b-form-input placeholder="hola"></b-form-input>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BTable, BButton, BModal, BFormInput, BSpinner } from "bootstrap-vue";
import { NodeURL, LatestEntityTypeDefinitionURL } from "../utils/urls"

export default {
  name: "nodes-relations-table",
  components: {
    BTable,
    BButton,
    BModal,
    BFormInput,
    BSpinner
  },
  props: {
    typeEid: {
      type: String,
      required: true,
    },
    definitionEid: {
      type: String,
      required: true,
    },
  },
  watch: {
    typeEid() {
      this.load();
    },
    definitionEid() {
      this.load();
    },    
  },
  data() {
    return {
      nodeList: [{}],
      nodeFields: [],
      loadingTable: false,
    };
  },
  created() {
    this.load();
  },
  methods: {
    mapTableStructure(definition) {
      let nodeFields = definition.properties.map(prop => prop.name);
      nodeFields.push(
        {
          key: "controls",
          label: "Controls",
        }
      );
      return nodeFields;
    },
    mapTableData(nodes) {
      return nodes.map(node => (
        {
          ...node.properties,
          eid: node.eid,          
          __relates_to: node.relates_to,
          _showDetails: true,
        }
      ));
    },
    load() {
      this.loadingTable = true;
      let options = {
        params: {}
      };

      // Set the filters for the NodeURL endpoint.
      if (this.definitionEid) {
        options.params = {
          filters: {
            field: "definition_eid",
            operation: "eq",
            value: this.definitionEid
          }
        }
      } else if (this.typeEid) {
        options.params = {
          filters: {
            field: "entity_type.eid",
            operation: "eq",
            value: this.typeEid
          }
        }
      }

      Promise.all([
        axios.get(NodeURL, options),
        axios.get(`${LatestEntityTypeDefinitionURL}${this.typeEid}`),
      ])
      .then(responses => {
          this.nodeList = this.mapTableData(responses[0].data);
          this.nodeFields = this.mapTableStructure(responses[1].data);
          this.loadingTable = false;
        })
      .catch(response => console.log(response.message));
    },
    remove(eid) {
      console.log(`Remove: ${eid}`);
    },
    loadModal(eid) {
      console.log(`Edit: ${eid}`);
    },
  },
};
</script>

<style lang="scss" scoped>

.title {
  display: flex;
  align-items: baseline;
  p {
    font-size: 24px;
    margin-bottom: 5px;
  }
  div {
    flex: 1;
    text-align: right;
  }
}

.controls {
  button {
    margin: 0px 5px 0px 5px;
  }
}

.relations {
  display: flex;
  justify-content: flex-start;
  margin-left: 10em;
}

.properties {
  margin-left: 10em;
}

</style>
