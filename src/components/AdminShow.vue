<template>
  <div>
    <div class="shows-box">
      <div v-for="show in theatre.shows" :key="show.id" class="show-item">
        <div class="show-actions">
          Actions dropdown for each show
          <b-dropdown variant="secondary" class="mr-2">
            <template #button-content>
              Actions
            </template>
            <b-dropdown-item>Edit Show</b-dropdown-item>
            <b-dropdown-item>Delete Show</b-dropdown-item>
          </b-dropdown>
        </div>
        <div class="show-details">
          Show details
        </div>
      </div>
      <div class="theatre-circle-container">
        <div class="theatre-circle" @click="openModal">
          <div class="theatre-plus-container">
            <div class="theatre-horizontal-plus"></div>
            <div class="theatre-vertical-plus"></div>
          </div>
        </div>
      </div>
    </div> 
  </div>
</template>

<script>

export default {
  name: 'AdminShow',
  props: {
    theatre: {
      type: Object,
      required: true
    }
  }
}

</script>

<style scoped>
.theatre-circle-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40%;
}

.theatre-circle, .show-circle {
  position: relative;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: rgb(44, 108, 128);
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}

.theatre-plus-container, .show-plus-container {
  position: relative;
  width: 60%;
  height: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.theatre-horizontal-plus,
.theatre-vertical-plus {
  position: absolute;
  background-color: #FFFFFF;
}

.theatre-horizontal-plus {
  width: 50%;
  height: 2px;
  top: 50%;
  transform: translateY(-50%);
}

.theatre-vertical-plus {
  width: 2px;
  height: 50%;
  left: 50%;
  transform: translateX(-50%);
}

/* .show-plus-container {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 25px;
  height: 25px;
  background-color: #e6e6e6;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
}

.show-horizontal-plus,
.show-vertical-plus {
  position: absolute;
  background-color: #d41818;
}

.show-horizontal-plus {
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
}

.show-vertical-plus {
  left: 50%;
  top: 0;
  bottom: 0;
  width: 2px;
} */

</style>