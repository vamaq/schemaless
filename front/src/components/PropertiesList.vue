<template>
  <div class="property-list">
    <label for="property-list-box" v-if="labels">Properties</label>
    <div id="property-list-box" class="property-list-box">
      <div v-for="(prop, index) in localProps" :key="index" class="property">
        <div>
          <div v-if="editPropIndex != index" @click="startEditProp(index)">
            {{prop.name}}
          </div>
          <input
            type="text"
            v-else
            v-model="editProp"
            class="edit-prop"
            @keydown="propEditkey"
            
          />
        </div>

        <div>
          <div v-if="editPropTypeIndex != index" @click="startEditPropType(index)">
            {{"("+ prop.type + ")"}}
          </div>
          <select 
            v-else
            class="edit-prop-type"
            v-model="editPropType"
            @change="saveEditPropType"
          >
            <option v-for="(type, index) in typesList" :value="type" :key="index">
            {{ type }}
            </option>
          </select>
        </div>

        <button class="prop-remove" @click="deleteProp(index)"/>
      </div>
      
      <input
        type="text"
        class="text-box"
        placeholder="Add a property by name and hit enter..."
        v-model="tempProp" 
        @keydown="propCreateKey" 
      />
    
    </div>
    <small v-if="labels">
      Press <kbd>Backspace</kbd> to remove the last tag entered. Click on property or type to edit.
    </small>
  </div>
</template>

<script>

import { cloneDeep } from 'lodash';

const KEY_BACK_SPACE = 8;
const KEY_RETURN = 13;
const KEY_ENTER = 14;

export default {
  name: "properties-list",
  props: {
    properties: {
      type: Array,
      default: () => [],
    },
    labels: {
      type: Boolean,
      default: true,
    }
  },
  watch: {
    properties () {
      this.localProps = cloneDeep(this.properties);
    },
  },
  data () {
    return {
      localProps: [],
      tempProp: "",
      //
      editProp: "",
      editPropIndex: -1,
      //
      editPropType: "",
      editPropTypeIndex: -1,
      typesList: ["string", "boolean", "integer", "float", "date"]
    }
  },
  created () {
    this.localProps = cloneDeep(this.properties);
  },
  methods: {
    propCreateKey (e) {
      if (e.keyCode == KEY_BACK_SPACE && this.tempProp == "") {
        this.deleteProp();
      }
      else if (e.keyCode == KEY_ENTER || e.keyCode == KEY_RETURN) {
        this.localProps.push({ name: this.tempProp, type: "string" });
        this.$emit('update-properties', this.localProps);
        this.tempProp = "";
      }
    },
    startEditProp (index) {
      this.editPropIndex = index;
      this.editProp = this.localProps[index].name;
    },
    propEditkey (e) {
      if (e.keyCode == KEY_ENTER || e.keyCode == KEY_RETURN) {
        this.saveEditProp();
      }
    },
    saveEditProp () {
      this.localProps[this.editPropIndex].name = this.editProp;
      this.$emit('update-properties', this.localProps);
      this.editPropIndex = -1;
    },
    startEditPropType (index) {
      this.editPropTypeIndex = index;
      this.editPropType = this.localProps[index].type;
    },
    saveEditPropType () {
      this.localProps[this.editPropTypeIndex].type = this.editPropType;
      this.$emit('update-properties', this.localProps);
      this.editPropTypeIndex = -1;
    },
    deleteProp (index=-1) {
      if (index > -1) {
        this.localProps.splice(index, 1);
      } else {
        this.localProps.pop()
      }
      this.$emit('update-properties', this.localProps);
    },
  }
}
</script>

<style lang="scss" scoped>

.property-list {
  flex-grow: 1;
  margin: 0.5rem 0 0.5rem 0;
}

.property-list-box {
  display: flex;
  flex-grow: 1;
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

.property {
  display: flex;
  align-items: center;
  color: #fff;
  background-color: #6c757d;
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

.prop-remove {
  padding: 0;
  background-color: transparent;
  border: 0;
}

.prop-remove::before {
    content: "x";
    padding: 0.25em;
    color: #fff;
    font-weight: 700;
}

.edit-prop:focus {
  outline: none !important;
}

.edit-prop-type:focus {
  outline: none !important;
}

</style>