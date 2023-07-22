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
    </div>
    <div class="theatre-circle-container">
      <div class="theatre-circle" @click="openAddShowModal">
        <div class="theatre-plus-container">
          <div class="theatre-horizontal-plus"></div>
          <div class="theatre-vertical-plus"></div>
        </div>
      </div>
    </div>
    <b-modal id="add-show-circle-modal" v-model="showAddShowModal" size="lg" variant="primary" no-close-on-backdrop>
      <template #modal-header>
        <h3 class="mb-0">Add Show</h3>
      </template>
      <template #default>
        <div class="form-group">
          <div id="admin-show-theatre-error-message" v-if="(errorMessages.length > 0 || serverErrorMessages.length > 0) && isAddSubmitButtonClicked" class="theatre-error-message">
              <ul>
                  <template v-if="errorMessages.length > 0">
                    <li v-for="errorMessage in errorMessages" :key="errorMessage">{{ errorMessage }}</li>
                  </template>
                  <template v-else-if="serverErrorMessages.length > 0">
                    <li v-for="serverErrorMessage in serverErrorMessages" :key="serverErrorMessage">{{ serverErrorMessage }}</li>
                  </template>
              </ul>
          </div>
          <label for="place">Name:</label>
          <input type="text" id="place" class="form-control" v-model="addShowData.name" />
        </div>
        <div class="form-group">
          <label for="capacity">Price:</label>
          <input type="number" id="capacity" class="form-control" v-model="addShowData.price" />
        </div>
        <div class="form-group">
          <label for="date">Date:</label>
          <input type="date" id="date" class="form-control" v-model="addShowData.date" />
        </div>
        <div class="form-group">
          <label for="startTime">Start Time:</label>
          <input type="time" id="startTime" class="form-control" v-model="addShowData.startTime" />
        </div>
        <div class="form-group">
          <label for="endTime">End Time:</label>
          <input type="time" id="endTime" class="form-control" v-model="addShowData.endTime" />
        </div>
        <div class="form-group">
          <label for="tags">Tags:</label>
          <select id="tags" class="form-control" v-model="addShowData.tags" multiple>
            <option value="drama">Drama</option>
            <option value="thriller">Thriller</option>
            <option value="action">Action</option>
            <option value="romance">Romance</option>
            <option value="comedy">Comedy</option>
            <option value="fiction">Fiction</option>
            <option value="sports">Sports</option>
            <option value="horror">Horror</option>
            <!-- Add more options as needed -->
          </select>
        </div>
      </template>
      <template #modal-footer>
        <b-btn class="primary" @click="submitAddShowForm(theatre)">Submit</b-btn>
        <b-btn @click="closeAddShowModal">Close</b-btn>
      </template>
    </b-modal>
    <Notification v-if="$store.state.notification" :variant="$store.state.notification.variant" 
        :message="$store.state.notification.message" @clear-notification="clearNotification"/> 
  </div>
</template>

<script>
import Notification from './Notification.vue'

export default {
  name: 'AdminShow',
  props: {
    theatre: {
      type: Object,
      required: true
    }
  },
  components: {
    Notification
  },
  data() {
    return {
      showEditShowModal: false,
      showAddShowModal: false,
      addShowData: {
        id: null,
        name: "",
        price: null,
        rating: 0,
        date: null, 
        startTime: null, 
        endTime: null,
        tags: [],
      },
      errorMessages: [],
      serverErrorMessages: [],
      isAddSubmitButtonClicked: false
    }
  },
  methods: {
    clearNotification() {
      this.$store.commit('clearNotification');
    },
    openAddShowModal() {
      this.showAddShowModal = true;
    },
    closeAddShowModal() {
      this.showAddShowModal = false;
      this.addShowData = {
        id: null,
        name: "",
        price: null,
        rating: 0,
        tags: []
      }

    },
    validateEachEntity(entityToValidate, message) {
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (entityToValidate == null || entityToValidate == '') {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }
      }
      else {
        if (entityToValidate == null || entityToValidate == '') {
          this.errorMessages.push(message);
        }
      }
    },
    addShowValidation() {
      let message = 'Name cannot be empty'
      this.validateEachEntity(this.addShowData.name, message);

      message = 'Place cannot be empty';
      this.validateEachEntity(this.addShowData.price, message);

      message = 'Date cannot be empty';
      this.validateEachEntity(this.addShowData.date, message);

      const currentDate = new Date();
      const selectedDate = new Date(this.addShowData.date);
      message = 'Selected date cannot be in the past';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (this.addShowData.date != null && selectedDate.getDate() < currentDate.getDate()) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }
      }
      else {
        if (this.addShowData.date != null && selectedDate.getDate() < currentDate.getDate()) {
          this.errorMessages.push(message);
        }
      }


      // Start time and End time validation
      message = 'Start time cannot be empty';
      this.validateEachEntity(this.addShowData.startTime, message);

      message = 'End time cannot be empty';
      this.validateEachEntity(this.addShowData.endTime, message);

      const selectedStartTime = new Date();
      if (this.addShowData.startTime != null) {
        selectedStartTime.setHours(Number(this.addShowData.startTime.slice(0, 2)));
        selectedStartTime.setMinutes(Number(this.addShowData.startTime.slice(3)));
      }

      const selectedEndTime = new Date();
      if (this.addShowData.endTime != null) {
        selectedEndTime.setHours(Number(this.addShowData.endTime.slice(0, 2)));
        selectedEndTime.setMinutes(Number(this.addShowData.endTime.slice(3)));
      }

      message = 'Start time cannot be before or equal to the current time';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (this.addShowData.startTime != null && selectedStartTime <= currentTime) {
            this.errorMessages.splice(indexOFMessage, 0, message);
          }
        }
      }
      else {
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (this.addShowData.startTime != null && selectedStartTime <= currentTime) {
            this.errorMessages.push(message);
          }
        }
      }

      message = 'End time cannot be before or equal to the current time';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (this.addShowData.endTime != null && selectedStartTime <= currentTime) {
            this.errorMessages.splice(indexOFMessage, 0, message);
          }
        }
      }
      else {
        if (selectedDate.getDate() === currentDate.getDate() && selectedDate.getFullYear() === currentDate.getFullYear() && selectedDate.getMonth() === currentDate.getMonth()) {
          const currentTime = new Date();
          if (this.addShowData.endTime != null && selectedEndTime <= currentTime) {
            this.errorMessages.push(message);
          }
        }
      }

      message = 'End time should be greater than start time';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (this.addShowData.endTime != null && this.addShowData.startTime != null && selectedEndTime <= selectedStartTime) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }

      }
      else {
        if (this.addShowData.endTime != null && this.addShowData.startTime != null && selectedEndTime <= selectedStartTime) {
          this.errorMessages.push(message);

        }
      }

      // Tags validation
      message = 'No tags selected';
      if (this.errorMessages.includes(message)) {
        let indexOFMessage = this.errorMessages.indexOf(message);
        this.errorMessages = this.errorMessages.filter((errorMessage) => errorMessage !== message);
        if (this.addShowData.tags.length === 0) {
          this.errorMessages.splice(indexOFMessage, 0, message);
        }

      }
      else {
        if (this.addShowData.tags.length === 0) {
          this.errorMessages.push(message);

        }
      }
    },
    async submitAddShowForm(theatre) {
      this.isAddSubmitButtonClicked = true;
      this.addShowValidation();
      if (this.errorMessages.length > 0) {
        return;
      }
      
      const user_id = parseInt(localStorage.getItem('userId')); 
      const tagsString = this.addShowData.tags.join(",");
      const response = await fetch(`http://127.0.0.1:5000/user/${user_id}/theatre/${theatre.id}/show_api`, {
        method: "POST",
        headers: {
          Authorization: 'Bearer ' + localStorage.getItem('access_token'),
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          input_name: this.addShowData.name,
          input_price: this.addShowData.price,
          input_date: this.addShowData.date,
          input_startTime: this.addShowData.startTime,
          input_endTime: this.addShowData.endTime,
          input_tags: tagsString
        })
      }).then(async result => {
        const data = await result.json();
        if (result.ok) {
          this.$store.commit('setNotification', { variant: 'success', message: data.message });
        }
        else {
          this.$store.commit('setNotification', { variant: 'error', message: 'Something went wrong. Try again!!!' });
        }
        this.closeAddShowModal();
      })
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

#admin-show-theatre-error-message {
  width: 750px;
  margin-top: -15px;
  border-color: black; 
  border: 2px solid black;
}

#admin-show-theatre-error-message ul {
  color: white;
  background-color: lightcoral;
  padding: 10px;
  margin: 0;
  list-style-type: none;
}



</style>