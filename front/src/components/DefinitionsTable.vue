<template>
  <div class="definitions">
    <div class="title">
      <p>Definitions for: {{definitionType.type}}</p>
      <div>
        <b-button size="sm" variant="success" @click="loadModal()" :disabled="latestVersion != -1">Create</b-button>
      </div>
    </div>
    <b-table
      head-variant="dark"
      small
      hover
      primary-key="eid"
      :busy="loadingTable"
      :items="definitionList"
      :fields="fields"
    >
      <template v-slot:table-busy>
        <div class="text-center text-danger my-2">
          <b-spinner class="align-middle"></b-spinner>
          <strong>Loading...</strong>
        </div>
      </template>

      <template v-slot:cell(properties)="data">
        <div v-for="(property, index) in data.item.properties" :key="index" >
           <b-badge variant="secondary">{{ property.name + " (" + property.type + ")" }}</b-badge>
        </div>
      </template>

      <template v-slot:cell(relations)="data">
        <div v-for="(relation, index) in data.item.relations" :key="index" >
          <b-badge variant="info">{{ relation.label + " (" + relation.type + ")" }}</b-badge>
          
          <div v-for="(property, index) in relation.properties" :key="index" >
            <b-badge variant="secondary" class="child">{{ property.name + " (" + property.type + ")"}}</b-badge>
          </div>
        </div>
      </template>

      <template v-slot:cell(controls)="data">
        <div class="controls">
          <b-button size="sm" variant="danger" @click="remove(data.item.eid)">Delete</b-button>
          <b-button
            size="sm"
            variant="secondary"
            @click="loadModal(data.item.eid)"
            :disabled="latestVersion != data.item.version"
          >Edit</b-button>
          <b-button size="sm" variant="dark" @click="showNodes(data.item.eid)">List Nodes</b-button>
        </div>
      </template>
    </b-table>

    <b-modal
      id="definition-modal"
      size="xl"
      class="create-modal"
      :title="tempDefinition.eid ? 'Edit': 'Create'"
      @hidden="hiddenModal"
      @ok="saveModal"
    >
      <p>{{"Type: " + definitionType.type}}</p>
      <p>{{"Version: " + (latestVersion + 1)}}</p>
      <properties-list 
        :properties="tempDefinition.properties"
        @update-properties="updateProperties"
      />
      <relations-list
        :relations="tempDefinition.relations"
        :type-list="typeList"
        @update-relations="updateRelations"
      />
    </b-modal>

  </div>
</template>

<script>
import axios from "axios";
import { BTable, BButton, BModal, BSpinner, BBadge } from "bootstrap-vue";
import { filter } from "lodash";
import { EntityTypeDefinitionURL, EntityTypeURL } from "../utils/urls"

import PropertiesList from "./PropertiesList";
import RelationsList from "./RelationsList";

export default {
  name: "definitions-table",
  components: {
    BTable,
    BButton,
    BModal,
    BSpinner,
    BBadge,
    PropertiesList,
    RelationsList,
  },
  props: {
    definitionType: {
      type: Object,
      required: true,
    },
  },
  watch: {
    definitionType() {
      this.load();
    },
  },
  data() {
    return {
      tempDefinition: {
        eid: "",
        version: "",
        properties: [],
        relations: [],
        entity_type: {
          eid: "",
          type: ""
        },        
      },
      typeList: [],
      definitionList: [],
      fields: [
        {
          key: "version",
          label: "Version",
          sortable: true
        },
        {
          key: "properties",
          label: "Properties",
          sortable: false,
          tdClass: ["text-left", "properties"],
        },
        {
          key: "relations",
          label: "Relations",
          sortable: false,
          tdClass: ["text-left", "relations"],
        },
        {
          key: "controls",
          label: "Controls"
        }
      ],
      loadingTable: false,
    };
  },
  computed: {
    latestVersion() {
      return this.definitionList.reduce((max = -1, val) => max < val.version ? val.version : max, -1);
    },
  },
  created() {
    this.load();
  },
  methods: {
    saveModal() {
      this.loadingTable = true;
      let promise;
      if (this.tempDefinition.eid) {  // The same modal is used for creation and edition.
        promise = axios // Update
          .put(`${EntityTypeDefinitionURL}${this.tempDefinition.eid}`, {
            properties: this.tempDefinition.properties,
            relations: this.tempDefinition.relations,
          });
      } else {
        promise = axios // Create
          .post(EntityTypeDefinitionURL, {
            entity_type_eid: this.definitionType.eid,
            properties: this.tempDefinition.properties,
            relations: this.tempDefinition.relations,
          });
      }
      // A new definition is always created
      promise
        .then(response => {
          this.definitionList.push(response.data);
          this.loadingTable = false;
        })
        .catch(response => console.log(response.message));
    },
    loadModal(eid) {
      if (eid) {
        axios
          .get(`${EntityTypeDefinitionURL}${eid}`)
          .then(response => {
            this.tempDefinition = response.data
            this.$root.$emit("bv::show::modal", "definition-modal");
          })
          .catch(response => console.log(response.message))
      } else {
        this.$root.$emit("bv::show::modal", "definition-modal");
      }
    },
    updateProperties(properties) {  
      this.tempDefinition.properties = properties;
    },
    updateRelations(relations) {
      this.tempDefinition.relations = relations;
    },    
    hiddenModal() {
      this.tempDefinition = {
        eid: "",
        version: "",
        properties: [],
        relations: [], 
        entity_type: {
          eid: "",
          type: ""
        },
      };
    },
    load() {
      this.loadingTable = true;
      Promise.all([
        axios
          .get(EntityTypeDefinitionURL, {
            params: {
              filters: {
                  field: "entity_type_eid",
                  operation: "eq",
                  value: this.definitionType.eid
          }}}),
        axios
          .get(EntityTypeURL)
      ])
      .then(responses => {
          this.definitionList = responses[0].data;
          this.typeList = responses[1].data;
          this.loadingTable = false;
      })
      .catch(response => console.log(response.message));
    },
    remove(eid) {
      axios
        .delete(`${EntityTypeDefinitionURL}${eid}`)
        .then(() => this.definitionList = filter(this.definitionList, e => e.eid != eid))
        .catch(response => console.log(response.message));
    },
    showNodes(eid) {
      this.$emit('show-nodes', eid, this.definitionType.eid);
    },
  },
};
</script>

<style lang="scss" scoped>
.definitions {
  display: flex;
  flex-direction: column;
}

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

.definitions::v-deep .properties {
  width: 30%;
}

.definitions::v-deep .relations {
  width: 30%;
}

.child {
  margin-left: 1rem;
}

</style>
