<template>
  <div class="relation-list" @mouseleave="hideProperties">
    <label for="relation-list-box">Relations</label>
    <div id="relation-list-box" class="relation-list-box">

      <div
        v-for="(relation, index) in localRelations" 
        :key="index"
        class="relations"
        @mouseover="showProperties(index)"
      >
        <div>
          <div v-if="editRelationLabelIndex != index" @click="startEditRelation(index)">
            {{relation.label}}
          </div>
          <input
            type="text"
            v-else
            v-model="editRelationLabel"
            class="edit-relation-label"
            @keydown="editRelationKeyDown"
            @blur="saveEditRelation"
          />
        </div>

        <div>
          <div v-if="editRelEntityTypeIndex != index" @click="starteditRelationLabel(index)">
            {{"("+ relation.type + ")"}}
          </div>
          <select
            v-else
            class="edit-relation-type"
            v-model="editRelEntityType"
            @change="saveeditRelationLabel"
          >
            <option v-for="(type, index) in typeList" :value="type.type" :key="index.eid">
            {{ type.type }}
            </option>
          </select>
        </div>

        <button class="tag-button rel-remove" @click="deleteRelation(index)"/>
      </div>
      
      <input
        type="text"
        class="text-box"
        placeholder="Add a relation by name..."
        v-model="tmpRelationLabel" 
        @keydown="createRelationKeyDown" 
      />
      
    </div>

    <small v-if="focusOnRelationIndex == -1">
      Press <kbd>Backspace</kbd> to remove the last tag entered. Click on relation or type to edit.
    </small>
    <div v-else class="relation-properties">
      <p>{{localRelations[focusOnRelationIndex].label + "(" + localRelations[focusOnRelationIndex].type + ") properties:"}}</p>
      <properties-list
        :properties="localRelations[focusOnRelationIndex].properties"
        :labels="false"
        @update-properties="updateProperties"
      />
    </div>

  </div>
</template>

<script>
import { cloneDeep } from 'lodash';
import PropertiesList from "./PropertiesList";

const KEY_BACK_SPACE = 8;
const KEY_RETURN = 13;
const KEY_ENTER = 14;

export default {
  name: "relations-list",
  components: {
    PropertiesList,
  },
  props: {
    relations: {
      type: Array,
      default: () => [],
    },
    typeList: {
      type: Array,
      default: () => [],
    }
  },
  watch: {
    relations () {
      this.localRelations = cloneDeep(this.relations);
    },
  },
  data () {
    return {
      localRelations: [],
      tmpRelationLabel: "",
      //
      editRelationLabel: "",
      editRelationLabelIndex: -1,
      //
      editRelEntityType: "",
      editRelEntityTypeIndex: -1,
      // The possition of the relation being focused.
      focusOnRelationIndex: -1,
    }
  },
  created () {
    this.localRelations = cloneDeep(this.relations);
  },
  methods: {
    createRelationKeyDown (e) {
      if (e.keyCode == KEY_BACK_SPACE && this.tmpRelationLabel == "") {
        this.deleteRelation();
      }
      else if (e.keyCode == KEY_ENTER || e.keyCode == KEY_RETURN) {
        this.localRelations.push({ label: this.tmpRelationLabel, type: this.typeList[0].type });
        this.$emit('update-relations', this.localRelations);
        this.tmpRelationLabel = "";
      }
    },
    startEditRelation (index) {
      this.editRelationLabelIndex = index;
      this.editRelationLabel = this.localRelations[index].label;
    },
    editRelationKeyDown (e) {
      if (e.keyCode == KEY_ENTER || e.keyCode == KEY_RETURN) {
        this.saveEditRelation();
      }
    },
    saveEditRelation () {
      this.localRelations[this.editRelationLabelIndex].label = this.editRelationLabel;
      this.$emit('update-relations', this.localRelations);
      this.editRelationLabelIndex = -1;
    },
    starteditRelationLabel (index) {
      this.editRelEntityTypeIndex = index;
      this.editRelEntityType = this.localRelations[index].type;
    },
    saveeditRelationLabel () {
      this.localRelations[this.editRelEntityTypeIndex].type = this.editRelEntityType;
      this.$emit('update-relations', this.localRelations);
      this.editRelEntityTypeIndex = -1;   
    },
    deleteRelation (index=-1) {
      this.hideProperties();
      if (index > -1) {
        this.localRelations.splice(index, 1);
      } else {
        this.localRelations.pop()
      }
      this.$emit('update-relations', this.localRelations);
    },
    showProperties(index) {
      this.focusOnRelationIndex = index;
    },
    hideProperties () {
      this.focusOnRelationIndex = -1;
    },
    updateProperties(properties) {  
      this.localRelations[this.focusOnRelationIndex].properties = properties;
      this.$emit('update-relations', this.localRelations);
    },    
  }
}
</script>

<style lang="scss" scoped>

.relation-list {
  margin: 0.5rem 0 0.5rem 0;
}

.relation-list-box {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
}

.text-box {
  border: none;
  width: 100%;
  padding: 0.375rem 0.75rem;
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.5;
  color: #495057;
}

.text-box:focus {
  outline: none !important;
}

.relations {
  display: flex;
  align-items: center;
  color: #fff;
  background-color: #17a2b8;
  padding: 0.25em 0.4em;
  margin: 0.25em;
  font-size: 75%;
  font-weight: 700;
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  vertical-align: baseline;
  border-radius: 0.25rem;  
}

.tag-button {
  padding: 0;
  background-color: transparent;
  border: 0;
}

.tag-button::before {
    content: "x";
    padding: 0.25em;
    color: #fff;
    font-weight: 700;
}

.edit-relation-label:focus {
  outline: none !important;
}

.edit-relation-type:focus {
  outline: none !important;
}

.relation-properties {
  display: flex;
  align-items: center;

  p {
    margin: 0 0.5rem 0 0;
    padding: 0px;

  }
}

</style>