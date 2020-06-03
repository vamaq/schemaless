<template>
  <div id="app">
    <schema-definition />
  </div>
</template>

<script>

import SchemaDefinition from './pages/SchemaDefinition.vue'

export default {
  name: 'App',
  components: {
    SchemaDefinition
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin: 60px;
  
}
</style>
