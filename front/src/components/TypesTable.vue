<template>
  <div>
    <div class="types">
      <div class="title">
        <p>Types</p>
        <div>
          <b-button size="sm" variant="success" @click="loadModal()">Create</b-button>
        </div>
      </div>
      <b-table
        head-variant="dark"
        small
        hover
        primary-key="eid"
        :busy="loadingTable"
        :items="typeList"
        :fields="fields"
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
            <b-button size="sm" variant="info" @click="showDefinitions(data.item)">Definitions</b-button>
            <b-button size="sm" variant="dark" @click="showNodes(data.item.eid)">List Nodes</b-button>
          </div>
        </template>
      </b-table>
      <b-modal
        id="type-modal"
        :title="tempType.eid ? 'Edit': 'Create'"
        @hidden="hiddenModal"
        @ok="saveModal"
      >
        <b-form-input v-model="tempType.type" placeholder="Type"></b-form-input>
      </b-modal>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { BTable, BButton, BModal, BFormInput, BSpinner } from "bootstrap-vue";
import { filter } from "lodash";
import { EntityTypeURL } from "../utils/urls"

export default {
  name: "types-table",
  components: {
    BTable,
    BButton,
    BModal,
    BFormInput,
    BSpinner
  },
  data() {
    return {
      nodeTypeEid: '',
      tempType: {
        eid: "",
        type: "",
      },
      typeList: [],
      fields: [
        {
          key: "type",
          label: "Type Label",
          sortable: true,
          tdClass: ["text-left"],
        },
        {
          key: "controls",
          label: "Controls",
        }
      ],
      loadingTable: false,
    };
  },
  created() {
    this.load();
  },
  methods: {
    saveModal() {
      this.loadingTable = true;
      if (this.tempType.eid) {
        axios
          .put(`${EntityTypeURL}${this.tempType.eid}`, {type: this.tempType.type})
          .then(response => {
            this.typeList = this.typeList.map(type => type.eid == response.data.eid ? response.data : type);
            this.loadingTable = false;
          })
          .catch(response => console.log(response.message));
      } else {
        axios
          .post(EntityTypeURL, { type: this.tempType.type })
          .then(response => {           
            this.typeList.push(response.data);
            this.loadingTable = false;
          })
          .catch(response => console.log(response.message));
      }
    },
    loadModal(eid) {
      if (eid) {
        axios
          .get(`${EntityTypeURL}${eid}`)
          .then(response => {
            this.tempType = response.data;
            this.$root.$emit("bv::show::modal", "type-modal");
          })
          .catch(response => console.log(response.message))
      } else {
        this.$root.$emit("bv::show::modal", "type-modal");
      }      
    },
    hiddenModal() {
      this.tempType = { eid: "", type: "" };
    },
    load() {
      this.loadingTable = true;
      axios
        .get(EntityTypeURL)
        .then(response => {
          this.typeList = response.data;
          this.loadingTable = false;
        })
        .catch(response => console.log(response.message));
    },
    remove(eid) {
      axios
        .delete(`${EntityTypeURL}${eid}`)
        .then(() => {this.typeList = filter(this.typeList, e => e.eid != eid);})
        .catch(response => console.log(response.message));
    },
    showDefinitions(definitionType) {
      this.$emit('show-definitions', definitionType);
    },
    showNodes(eid) {
      console.log(`list nodes for eid ${eid}`);
    }
  }
};
</script>

<style lang="scss" scoped>
.types {
  display: flex;
  flex-direction: column;
  width: 600px;
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
</style>
